# Como contribuir

Este documento descreve a forma de trabalhar neste repositório: ramos, commits, pull requests e releases.

## Ramos

Segue-se o modelo Git Flow.

| Ramo | Para que serve | Como recebe alterações |
|---|---|---|
| `main` | Versões entregues. Cada commit corresponde a uma release | Só por pull request de um ramo `release/*` |
| `develop` | Integração do trabalho em curso | Só por pull request de ramos `feature/*` e `fix/*` |
| `feature/<ID>-<descrição>` | Uma funcionalidade ou tarefa | Commits diretos de quem a desenvolve |
| `fix/<descrição>` | Correção de um erro | Commits diretos de quem a corrige |
| `release/vX.Y.Z` | Preparação de uma release | Commits de atualização da versão e do registo de alterações |

Nomes de ramos em minúsculas, sem acentos e com hífenes. O ID é o da user story ou da tarefa:

```
feature/A01-login-administrador
feature/0.3-testes-ci
fix/menu-opcao-invalida
release/v0.1.0
```

Nunca se faz commit diretamente em `main` nem em `develop`.

## Ciclo de uma funcionalidade

1. **Issue.** Confirmar que existe uma issue para o trabalho e atribuí-la a quem o vai fazer.
2. **Ramo.** Criar o ramo a partir do `develop` atualizado:

   ```bash
   git switch develop
   git pull
   git switch -c feature/A01-login-administrador
   ```

3. **Commits.** Fazer commits pequenos, cada um com um só propósito (ver a secção seguinte).
4. **Testes.** Antes de enviar, correr `python -m pytest`.
5. **Push.** Enviar o ramo:

   ```bash
   git push -u origin feature/A01-login-administrador
   ```

6. **Pull request.** Abrir o pull request para `develop`, preencher o modelo e escrever `Closes #<número da issue>` na descrição.
7. **Revisão.** Outro membro da equipa lê as alterações, corre a aplicação e aprova ou pede correções.
8. **Merge.** Depois de aprovado e com as verificações automáticas a verde, fazer o merge com *merge commit* (opção "Create a merge commit") e apagar o ramo.

## Mensagens de commit

Formato:

```
tipo(área): descrição curta no infinitivo
```

| Tipo | Quando usar |
|---|---|
| `feat` | Funcionalidade nova |
| `fix` | Correção de um erro |
| `test` | Testes novos ou alterados |
| `docs` | Documentação: docstrings, Sphinx, README, este ficheiro |
| `ci` | Integração contínua (GitHub Actions) |
| `chore` | Manutenção que não altera o comportamento: configuração, versão |
| `refactor` | Reorganização do código sem alterar o comportamento |

A área é a parte do código afetada (`bd`, `cli`, `config`, `auth`, ...) e pode ser omitida quando a alteração é geral.

Exemplos:

```
feat(bd): adicionar ligação SQLite e criação de tabelas
test(cli): testar os menus e o ponto de entrada
docs: descrever a arquitetura e os testes
fix(cli): ler e escrever acentos em UTF-8 em qualquer terminal
```

Regras:

- Um commit, um propósito. Código, testes e documentação vão em commits separados.
- A descrição diz o que o commit faz, não como.
- Não se faz commit de ficheiros gerados (`dados/`, `docs/_build/`, `__pycache__/`).

## Código

- Todos os módulos, classes e funções têm docstring, no formato do Sphinx:

  ```python
  def ficheiro_bd() -> Path:
      """Devolve o caminho do ficheiro da base de dados SQLite.

      :return: Caminho do ficheiro ``app.db`` dentro da pasta de dados.
      """
  ```

- Um módulo novo tem de ser acrescentado a `docs/referencia.rst`.
- Os menus (`gestor_campanhas/cli/`) só perguntam e mostram. As regras da aplicação ficam fora dos menus, para poderem ser testadas.
- Código novo vem acompanhado de testes.

## Releases

Cada fase do projeto termina com uma release.

1. Criar o ramo a partir do `develop`:

   ```bash
   git switch develop
   git pull
   git switch -c release/v0.1.0
   ```

2. Atualizar a versão em `gestor_campanhas/__init__.py` e o registo de alterações.
3. Abrir um pull request de `release/v0.1.0` para `main`.
4. Depois do merge, criar a tag e a release no GitHub:

   ```bash
   git switch main
   git pull
   git tag -a v0.1.0 -m "Versão 0.1.0"
   git push origin v0.1.0
   ```

5. Trazer a release de volta para o `develop` com um pull request de `main` para `develop`.

As versões seguem o formato `vX.Y.Z`: `Y` aumenta em cada fase, `Z` em correções, e `v1.0.0` é a versão entregue.

## Issues

- Cada user story é uma issue, com o ID no título: `[A01] Como Administrador, quero ...`.
- Labels de perfil: `Administrador`, `Marketeer`, `Cliente`.
- Labels de tipo: `user story`, `tarefa`, `bug`.
- Cada issue pertence à milestone da fase em que é implementada.
- Um erro encontrado depois do merge é registado numa issue nova com a label `bug`.

## Quadro Trello

O estado de cada user story é acompanhado no quadro Trello do projeto.

| Lista | Quando o card lá está |
|---|---|
| Backlog do Produto | Ainda não foi planeado |
| Sprint Backlog | Faz parte da fase em curso |
| Work In Progress | Alguém está a trabalhar no ramo |
| Ready to Verify | O pull request está aberto, à espera de revisão |
| Debug in Progress | A revisão encontrou problemas e estão a ser corrigidos |
| Ready | O pull request foi aprovado e fundido |
