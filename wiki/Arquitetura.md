# Arquitetura

Como o código está organizado, na versão 1.0.0. A descrição completa, com todas as funções, está na documentação gerada pelo Sphinx (pasta `docs` do repositório). As tabelas e as relações entre elas estão em [Modelo de dados](Modelo-de-dados), e os testes em [Testes](Testes).

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

## Budget

Um pedido de alteração de budget usa os mesmos estados de um pedido de campanha, mas quem o faz avançar é diferente:

```text
Pendente --(parecer do marketeer)--> Em análise --(o Administrador aprova)--> Aprovado   (o budget muda)
   |                                     |
   |                                     +--------(o Administrador rejeita)--> Rejeitado  (com um motivo)
   +--> Cancelado (pelo cliente, só enquanto está pendente)
```

O pedido não guarda o cliente nem o marketeer: chega-se a eles pela campanha. Assim, se a campanha mudar de marketeer, os pedidos passam a aparecer ao marketeer novo. O pedido guarda o budget que a campanha tinha quando foi feito, para se poder comparar com o valor pedido mesmo depois de o budget mudar.

O budget de uma campanha está na tabela `campanhas`; o histórico, na tabela `alteracoes_budget`. Para nunca ficarem desencontrados, todas as alterações passam por uma só função, `alterar_budget`, em `servicos/campanhas.py`, que muda o budget e regista a alteração ao mesmo tempo. Usam-na a opção "Definir budget" do Administrador e a aprovação de um pedido de alteração de budget. O histórico só cresce: as linhas nunca são alteradas.

O resumo global do budget não tem tabela própria: é calculado sempre que é mostrado, a partir das campanhas e da despesa de cada uma, como a despesa. A regra "acima do budget" está numa só função, `acima_do_budget`, em `servicos/budget.py`: uma campanha sem budget nunca está acima do budget.

## Comentários

Os comentários do cliente e as respostas do marketeer ficam na mesma tabela, `comentarios`. Uma resposta é um comentário com a coluna `resposta_a` preenchida, com o número do comentário a que responde. Assim, uma só consulta traz a conversa toda de um criativo, pela ordem em que foi escrita, e a função `conversa`, em `servicos/comentarios.py`, arruma-a em pares (comentário, respostas). Não se responde a uma resposta, por isso a conversa tem só dois níveis.

## Notificações

Todas as notificações passam por uma só função, `notificar`, em `servicos/notificacoes.py`: guarda a notificação na tabela `notificacoes` e envia o mesmo texto por email. Quem decide quem é notificado são as regras de cada assunto, no fim de cada operação que corre bem (`servicos/campanhas.py`, `budget.py`, `criativos.py` e `comentarios.py`). Como a notificação é a última coisa a acontecer, uma operação recusada não notifica ninguém.

Cada notificação guarda o tipo do item (`campanha`, `pedido_budget` ou `criativo`) e o número dele. Esse número não é uma chave estrangeira, porque aponta para tabelas diferentes conforme o tipo. Ao abrir a notificação, o item é procurado com as mesmas funções dos menus (por exemplo `obter_do_cliente`), por isso ninguém vê, por uma notificação antiga, um item a que já não tem acesso.

## Painel de marketeers

Os indicadores do painel (criativos ativos, em atraso e concluídos) não são guardados: são calculados sempre que o painel é mostrado, em `servicos/painel.py`. Os estados que contam em cada grupo estão nas constantes `ATIVOS` e `CONCLUIDOS`.

A tabela `criativos` não guarda a data da última alteração, e o `CREATE TABLE IF NOT EXISTS` não acrescenta colunas a uma tabela que já existe. Por isso a atividade dos marketeers tem uma tabela própria, `atividades`, onde ficam registadas as alterações aos criativos e as respostas a comentários. Para os criativos que já existiam, conta a data de criação. O número de dias sem atividade (7, de início) fica na tabela `configuracoes`, como o limite de inatividade das sessões.

## Relatório

O relatório do cliente é montado em `servicos/relatorios.py`, com as mesmas funções que mostram as campanhas e a despesa no ecrã, e gravado com o módulo `csv` da biblioteca padrão. O formato pensa no Excel em português: colunas separadas por `;` (a vírgula é a das casas decimais), euros sem `€` e sem o espaço dos milhares, e o ficheiro em UTF-8 com a marca inicial, sem a qual o Excel troca os acentos. O nome do ficheiro é escolhido pela mesma função que escolhe o nome de um ficheiro descarregado, `caminho_livre`, por isso nenhum ficheiro é apagado.

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
| `pedidos_budget` | Uma linha por pedido de alteração de budget: campanha, budget de partida e budget pedido em cêntimos, motivo, estado, parecer do marketeer e justificação, motivo da rejeição e data da decisão |
| `alteracoes_budget` | O histórico do budget: uma linha por alteração, com a campanha, o budget anterior e o novo, o motivo, a data e o pedido que lhe deu origem, se houver |
| `comentarios` | Uma linha por comentário ou resposta: criativo, autor, texto, data e, numa resposta, o comentário a que responde |
| `notificacoes` | Uma linha por notificação: quem a recebe, o texto, o tipo e o número do item, se já foi lida e a data |
| `atividades` | A atividade dos marketeers: uma linha por alteração, com o marketeer, a descrição e a data |
| `recuperacoes` | Códigos de recuperação da password: utilizador, hash do código, validade e se já foi usado |
| `configuracoes` | Definições que podem ser alteradas, como pares chave/valor |

Uma campanha com criativos não pode ser apagada. Os pedidos de alteração de budget e o histórico do budget não impedem: têm `ON DELETE CASCADE`, e são apagados com a campanha. Os comentários de um criativo também têm `ON DELETE CASCADE`, e são apagados com o criativo.

As relações entre as tabelas, os estados e a forma como cada valor é guardado estão em [Modelo de dados](Modelo-de-dados).

## Passwords

A aplicação nunca guarda passwords. Guarda um hash calculado com PBKDF2 (SHA-256) e um *salt* aleatório por conta. Para confirmar uma password, repete a conta e compara os resultados.

## Sessões e inatividade

Cada entrada fica registada na tabela `sessoes`. Uma aplicação de linha de comandos fica parada à espera do teclado, por isso a inatividade é verificada quando o utilizador responde a um menu: se passaram mais de 15 minutos, a sessão é dada como terminada à hora em que o limite foi atingido.

## Emails

Não são enviados emails verdadeiros. O módulo `servicos/correio.py` escreve cada mensagem num ficheiro de texto da pasta `dados/caixa_saida`. Para enviar a sério, só esse módulo teria de mudar.

## Testes

Os testes usam o pytest e estão na pasta `tests`. Cada teste recebe uma base de dados em memória nova, e o relógio da aplicação pode ser substituído para simular a passagem do tempo. O GitHub Actions corre os testes em cada pull request.

Além dos testes de cada parte, há testes dos fluxos completos, com os três perfis, e testes que confirmam que todo o código tem docstring. Estão descritos em [Testes](Testes).

## Dados de demonstração

O módulo `dados_demo.py` cria as contas, as campanhas e os criativos de demonstração diretamente nos repositórios, e depois usa as regras de negócio para o que acontece a seguir: anexar o ficheiro, mudar o estado dos criativos, comentar e responder, e avisar o marketeer do pedido de budget. Assim, as notificações e a atividade de demonstração são as mesmas que a aplicação produziria. Cada parte só é criada se ainda não existir, por isso o comando pode ser repetido.
