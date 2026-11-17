# Arquitetura

Como o código está organizado. A descrição completa, com todas as funções, está na documentação gerada pelo Sphinx (pasta `docs` do repositório).

## Camadas

O código está separado por responsabilidades. Cada camada só conhece as que estão abaixo dela.

```
__main__        arranca a aplicação
   |
cli             mostra menus, lê respostas, apresenta resultados
   |
servicos        regras de negócio: decide o que é permitido
   |
repositorios    lê e escreve na base de dados (único sítio com SQL)
   |
bd              abre a ligação e cria as tabelas
   |
SQLite          ficheiro dados/app.db
```

| Camada | Pasta | Regra |
|---|---|---|
| Menus | `gestor_campanhas/cli/` | Só pergunta e mostra. Não decide nada |
| Serviços | `gestor_campanhas/servicos/` | Tem as regras. Não lê do teclado nem escreve no ecrã |
| Repositórios | `gestor_campanhas/repositorios/` | Único sítio com SQL. Um módulo por tabela |
| Base de dados | `gestor_campanhas/bd.py` | Abre a ligação e cria as tabelas |

Esta separação é o que permite testar as regras diretamente, sem simular o teclado, e com uma base de dados em memória.

## Erros

Quando uma regra não é cumprida, o serviço lança um erro próprio (`ErroAutenticacao`, `ErroValidacao`). O menu apanha-o e mostra a mensagem. O programa não para.

## Exemplo: adicionar um cliente

1. O menu (`cli/gestao.py`) pede os dados no ecrã.
2. O serviço (`servicos/gestao.py`) valida-os, confirma que o email ainda não tem conta e gera a password inicial.
3. O repositório (`repositorios/utilizadores.py`) guarda a conta, com o hash da password.
4. O serviço de emails (`servicos/correio.py`) envia as credenciais.

Se um dado não for válido, o serviço lança `ErroValidacao` antes de guardar seja o que for, e o menu mostra a mensagem.

Os mesmos ecrãs e as mesmas funções servem para clientes e para marketeers: o perfil é passado como argumento.

## Exemplo: aprovar um pedido de campanha

1. O menu (`cli/pedidos.py`) pede o número do pedido e mostra-o. O serviço passa-o de pendente para em análise.
2. O menu pede o nome da campanha, o budget inicial e o marketeer responsável.
3. O serviço (`servicos/pedidos.py`) confirma que o pedido ainda está por decidir e valida os dados.
4. O repositório das campanhas cria a campanha, e o dos pedidos marca o pedido como aprovado, com o número da campanha.
5. O serviço de emails avisa o cliente e o marketeer.

Se algum dado não for válido, o erro é lançado antes de a campanha ser criada, e o pedido continua em análise.

## Campanhas e pedidos

Uma campanha tem sempre um cliente e um marketeer responsável. O estado de uma campanha (por começar, em curso, terminada) não é guardado: é calculado a partir das datas sempre que é mostrado.

Cada perfil só chega às campanhas que lhe dizem respeito. As funções `obter_do_marketeer` e `obter_do_cliente` devolvem uma campanha só se for de quem a pede, com a mesma mensagem de erro quando a campanha não existe e quando é de outra pessoa.

Um pedido de campanha passa por estes estados:

```text
Pendente --> Em análise --> Aprovado   (é criada a campanha)
   |              |
   |              +-------> Rejeitado  (com um motivo)
   +--> Cancelado (pelo cliente, só enquanto está pendente)
```

## Criativos

Um criativo pertence a uma campanha e não tem marketeer nem cliente próprios: chega-se a eles através da campanha. Por isso, as funções `obter_do_marketeer` e `obter_do_cliente` dos criativos leem o criativo e confirmam que a campanha dele é de quem o pede.

As passagens de estado estão todas num dicionário, `PROXIMOS_ESTADOS`, em `servicos/criativos.py`: para cada estado, os estados para onde o marketeer o pode mudar. O menu só mostra essas escolhas. Aprovar e rejeitar ficam fora do dicionário, porque são decisões do cliente, com funções próprias.

```text
Em preparação --> Em revisão --> Aprovado --> Publicado
                       |
                       +-------> Rejeitado --> Em preparação ou Em revisão
```

A despesa de uma campanha (a soma do custo dos criativos) não é guardada: é calculada sempre que é mostrada, com uma consulta `SUM ... GROUP BY` que soma todas as campanhas de uma vez. Assim, nunca fica desatualizada quando um criativo muda de custo ou é eliminado.

## Ficheiros

Os ficheiros dos criativos ficam fora da base de dados, na pasta `dados/ficheiros/<número do criativo>/`. A base de dados guarda só o nome do ficheiro. O módulo `servicos/ficheiros.py` trata de copiar, descrever (tipo e tamanho), abrir e descarregar ficheiros, e não sabe nada de criativos: recebe só caminhos e números.

Os testes usam sempre uma pasta de dados temporária (a fixture `dados_temporarios`, em `tests/conftest.py`), para nunca mexerem nos ficheiros verdadeiros.

## Dinheiro

Os valores em euros (o budget de uma campanha, o orçamento de um pedido e o custo de um criativo) são guardados em cêntimos, como números inteiros, para as contas darem sempre certo. O módulo `dinheiro.py` converte o que o utilizador escreve em cêntimos e os cêntimos no texto que é mostrado (`1 500,50 €`, ou `-200,00 €` quando o valor é negativo).

## Validação dos dados

As regras do nome, do email, do telefone, do NIF e das datas estão num só módulo, `servicos/validacao.py`. São as mesmas quando é o próprio a alterar os seus dados e quando é o Administrador a criar ou a editar uma conta.

## Contas desativadas

Remover um cliente ou um marketeer não apaga a linha da tabela `utilizadores`: põe a coluna `ativo` a zero. Assim, as sessões já registadas e as campanhas continuam ligadas a uma conta que existe. Uma conta desativada não pode entrar nem recuperar a password, e pode ser reativada.

Um marketeer só pode ser desativado quando já não for responsável por campanhas por terminar.

## Tabelas

| Tabela | Conteúdo |
|---|---|
| `utilizadores` | Uma linha por conta: nome, email (único), hash da password, perfil, se está ativa, telefone, empresa e NIF |
| `sessoes` | Uma linha por entrada na aplicação: utilizador, hora de entrada, hora de saída e motivo da saída |
| `campanhas` | Uma linha por campanha: nome, objetivo, cliente, marketeer responsável, budget em cêntimos e datas de início e de fim |
| `criativos` | Uma linha por criativo: campanha, nome, descrição, custo em cêntimos, prazo, público-alvo, plataforma, estado, motivo da rejeição e nome do ficheiro |
| `pedidos_campanha` | Uma linha por pedido de nova campanha: cliente, objetivo, orçamento em cêntimos, prazo, plataformas, estado, motivo da rejeição e campanha a que deu origem |
| `recuperacoes` | Códigos de recuperação da password: utilizador, hash do código, validade e se já foi usado |
| `configuracoes` | Definições que podem ser alteradas, como pares chave/valor |

## Passwords

A aplicação nunca guarda passwords. Guarda um hash calculado com PBKDF2 (SHA-256) e um *salt* aleatório por conta. Para confirmar uma password, repete a conta e compara os resultados.

## Sessões e inatividade

Cada entrada fica registada na tabela `sessoes`. Uma aplicação de linha de comandos fica parada à espera do teclado, por isso a inatividade é verificada quando o utilizador responde a um menu: se passaram mais de 15 minutos, a sessão é dada como terminada à hora em que o limite foi atingido.

## Emails

Não são enviados emails verdadeiros. O módulo `servicos/correio.py` escreve cada mensagem num ficheiro de texto da pasta `dados/caixa_saida`. Para enviar a sério, só esse módulo teria de mudar.

## Testes

Os testes usam o pytest e estão na pasta `tests`. Cada teste recebe uma base de dados em memória nova, e o relógio da aplicação pode ser substituído para simular a passagem do tempo. O GitHub Actions corre os testes em cada pull request.
