# Fluxo Git

Esta página descreve como a equipa usa o Git e o GitHub. As regras completas estão no ficheiro `CONTRIBUTING.md` do repositório.

## Ramos

Segue-se o modelo Git Flow.

```
main      ●───────────────────────●──────────  só releases (v0.1.0, v0.2.0, ...)
           \                     /
develop     ●───●───────●───────●────────────  integração
                 \     /
feature/...       ●───●                        uma funcionalidade ou tarefa
```

| Ramo | Para que serve |
|---|---|
| `main` | Versões entregues. Cada commit corresponde a uma release |
| `develop` | Integração do trabalho em curso |
| `feature/<ID>-<descrição>` | Uma funcionalidade ou tarefa |
| `fix/<descrição>` | Correção de um erro |
| `release/vX.Y.Z` | Preparação de uma release |

Nunca se faz commit diretamente em `main` nem em `develop`. Os dois ramos só recebem alterações por pull request.

## Do pedido ao merge

1. **Issue.** Cada user story e cada tarefa tem uma issue, com label e milestone.
2. **Ramo.** Quem pega na issue cria um ramo `feature/` a partir do `develop`.
3. **Commits.** Commits pequenos, cada um com um só propósito.
4. **Pull request.** Aberto para `develop`, com `Closes #<issue>` na descrição.
5. **Verificações automáticas.** O GitHub Actions corre os testes e gera a documentação.
6. **Revisão.** Outro membro da equipa lê as alterações, experimenta a aplicação e aprova.
7. **Merge.** Com *merge commit*, para o histórico mostrar de onde veio cada alteração.

## Mensagens de commit

```
tipo(área): descrição curta no infinitivo
```

| Tipo | Quando usar |
|---|---|
| `feat` | Funcionalidade nova |
| `fix` | Correção de um erro |
| `test` | Testes |
| `docs` | Documentação |
| `ci` | Integração contínua |
| `chore` | Manutenção que não altera o comportamento |
| `refactor` | Reorganização do código sem alterar o comportamento |

Exemplos:

```
feat(bd): adicionar ligação SQLite e criação de tabelas
test(cli): testar os menus e o ponto de entrada
docs: descrever a arquitetura e os testes
```

## Revisão de pull requests

A revisão é rotativa: Fabio revê o trabalho de Ricardo, Tomas revê o de Fabio, Ricardo revê o de Tomas.

Quem revê:

- lê as alterações no separador *Files changed*;
- obtém o ramo e corre `python -m pytest` e `python -m gestor_campanhas`;
- confirma que as verificações automáticas estão a verde;
- aprova, ou pede correções com um comentário na linha em causa.

## Releases

Cada fase termina com uma release.

1. Ramo `release/vX.Y.0` a partir do `develop`.
2. Atualização da versão e do registo de alterações.
3. Pull request para `main`.
4. Tag `vX.Y.0` e release no GitHub.
5. Pull request de `main` para `develop`, para os dois ramos ficarem alinhados.

## Issues, labels e milestones

| Label | Significado |
|---|---|
| `user story` | Funcionalidade descrita do ponto de vista de um utilizador |
| `tarefa` | Trabalho técnico que não corresponde a uma user story |
| `bug` | Algo não funciona como devia |
| `Administrador`, `Marketeer`, `Cliente` | Perfil a que a user story pertence |

Cada fase do projeto é uma milestone. A página da milestone mostra quantas issues estão fechadas e quantas faltam.

## Quadro Trello

| Lista | Quando o card lá está |
|---|---|
| Backlog do Produto | Ainda não foi planeado |
| Sprint Backlog | Faz parte da fase em curso |
| Work In Progress | Alguém está a trabalhar no ramo |
| Ready to Verify | O pull request está aberto, à espera de revisão |
| Debug in Progress | A revisão encontrou problemas e estão a ser corrigidos |
| Ready | O pull request foi aprovado e fundido |
