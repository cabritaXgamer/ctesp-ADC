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

## Tabelas

| Tabela | Conteúdo |
|---|---|
| `utilizadores` | Uma linha por conta: nome, email (único), hash da password, perfil, se está ativa, telefone, empresa e NIF |
| `sessoes` | Uma linha por entrada na aplicação: utilizador, hora de entrada, hora de saída e motivo da saída |
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
