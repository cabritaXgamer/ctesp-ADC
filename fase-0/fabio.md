# Fase 0 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 0 (Arranque), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

## Antes de começares

Tens duas pastas lado a lado no teu computador, criadas na [Preparação](../preparacao.md):

| Pasta | O que é | O que fazes lá |
|---|---|---|
| `ADC-TrabGrupo` | O repositório oficial, o que é avaliado | **Tudo.** Todos os comandos desta página são corridos dentro desta pasta |
| `ctesp-ADC` | O repositório de trabalho, com os ficheiros preparados e estas páginas | Nada. Só se lê e se copia de lá |

Abre o terminal dentro da pasta `ADC-TrabGrupo` e deixa-o lá até ao fim. Os comandos funcionam no terminal do VS Code, no PowerShell e no Git Bash.

Se algum termo não for claro, vê [O que é o quê](../conceitos.md). A ordem geral da fase está na [página da fase](README.md).

## Os teus passos

| Passos | O que fazes | Quando |
|---|---|---|
| 1 a 10 | Fazer a unidade 0.1 — Estrutura do pacote Python | Logo a seguir à Preparação |
| 11 a 17 | Rever e juntar a unidade 0.3 (de Ricardo) | Quando Ricardo avisar que o pull request está aberto |
| 18 a 27 | Fazer a unidade 0.4 — Documentação base | A seguir ao teu passo anterior |
| 28 | Cria as 19 issues do perfil Administrador | Em qualquer altura depois da Preparação |

---

## Fazer a unidade 0.1 — Estrutura do pacote Python

Cria a estrutura base do projeto: a pasta do código, o ficheiro que arranca a aplicação e a configuração. No fim, `python -m gestor_campanhas` mostra a versão.

### Passo 1 — Confirma que podes começar

Antes do primeiro passo tens de ter feito a [Preparação](../preparacao.md), e o repositório oficial já tem de ter o ramo `develop` (passo B1 da Preparação, feito por Fabio).

### Passo 2 — Cria a issue da unidade 0.1

A issue é o registo, no GitHub, do trabalho que vai ser feito. O pull request que vais abrir mais à frente fecha-a sozinho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No campo do título, cola:

```text
[0.1] Estrutura do pacote Python
```

**c)** Na caixa grande de texto, cola:

```markdown
## Objetivo

Criar a estrutura base do projeto, para que a aplicação possa ser arrancada com `python -m gestor_campanhas`.

## O que inclui

- [ ] `.gitignore` e `.gitattributes`
- [ ] Pacote `gestor_campanhas` com a versão e o ponto de entrada
- [ ] Módulo `config` com os caminhos da pasta de dados e da base de dados
- [ ] `pyproject.toml` com a descrição do projeto
- [ ] README com a introdução do projeto, mensagens de commit e explicação do `pyproject.toml`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#3`. Aponta-o: vais precisar dele quando abrires o pull request.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/0.1-estrutura-pacote
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/0.1-estrutura-pacote` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/0.1-estrutura-pacote'`.

### Passo 4 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 0.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 0.1. Eles estão na pasta `ctesp-ADC/fase-0/ficheiros/0.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.1 1
```

**Deves ver** `Copiados 2 ficheiros`: `.gitattributes`, `.gitignore`.

```bash
git add -A
git commit -m "chore: adicionar .gitignore e .gitattributes"
```

**Deves ver** uma linha a terminar em `2 files changed, 31 insertions(+)`.

**Commit 2 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.1 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/__init__.py`, `gestor_campanhas/__main__.py`.

```bash
git add -A
git commit -m "feat(nucleo): criar pacote gestor_campanhas com ponto de entrada"
```

**Deves ver** uma linha a terminar em `2 files changed, 29 insertions(+)`.

**Commit 3 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.1 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/config.py`.

```bash
git add -A
git commit -m "feat(config): adicionar configuração dos caminhos de dados"
```

**Deves ver** uma linha a terminar em `1 file changed, 43 insertions(+)`.

**Commit 4 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.1 4
```

**Deves ver** `Copiados 1 ficheiro`: `pyproject.toml`.

```bash
git add -A
git commit -m "chore: adicionar pyproject.toml"
```

**Deves ver** uma linha a terminar em `1 file changed, 28 insertions(+)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 0.1 5
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs: atualizar introdução do README"
```

**Deves ver** uma linha a terminar em `1 file changed, 35 insertions(+), 1 deletion(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 0.1
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 0.1` | `Tudo certo: o ramo 'feature/0.1-estrutura-pacote' está igual ao original no fim da unidade 0.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: atualizar introdução do README
xxxxxxx chore: adicionar pyproject.toml
xxxxxxx feat(config): adicionar configuração dos caminhos de dados
xxxxxxx feat(nucleo): criar pacote gestor_campanhas com ponto de entrada
xxxxxxx chore: adicionar .gitignore e .gitattributes
```

### Passo 6 — Experimenta o que gravaste

```bash
python -m gestor_campanhas
```

**Deves ver** `Gestor de Campanhas v0.0.0`, e o programa termina logo. Nesta unidade ainda não há menu.

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/0.1-estrutura-pacote
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

Na primeira vez pode abrir-se uma janela a pedir para entrares na tua conta do GitHub. Entra e volta ao terminal.

**Deves ver**, perto do fim: `* [new branch]      feature/0.1-estrutura-pacote -> feature/0.1-estrutura-pacote`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/0.1-estrutura-pacote`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/0.1-estrutura-pacote**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Estrutura do pacote Python
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue que apontaste:

```markdown
## O que muda

Cria a estrutura base do projeto: o pacote `gestor_campanhas`, o ponto de entrada, a configuração dos caminhos de dados e o `pyproject.toml`. Acrescenta o `.gitignore`, o `.gitattributes` e atualiza o README com a introdução, as mensagens de commit e a explicação do `pyproject.toml`.

Closes #N

## Como testar

1. `python -m gestor_campanhas`
2. Deve aparecer `Gestor de Campanhas v0.0.0` e o programa termina.
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**f)** Clica no botão verde **Create pull request**.

**g)** Se aparecerem verificações automáticas no fundo da página (*Testes*, *Documentação*), espera um ou dois minutos até ficarem com um visto verde.

### Passo 9 — Avisa Tomas

Diz a Tomas que o pull request da unidade 0.1 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 1 a 7.

### Passo 10 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/0.1-estrutura-pacote
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/0.1-estrutura-pacote` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 0.3 — Testes automáticos e integração contínua

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 11 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 0.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Testes automáticos e integração contínua**.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Ricardo:

```bash
git fetch origin
git switch feature/0.3-testes-ci
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/0.3-testes-ci` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/0.3-testes-ci'`.

Agora experimenta:

```bash
python -m pytest
```

**Deves ver**, na última linha, `20 passed`. Cada ponto que aparece antes é um teste que passou.

Para ver o nome de cada teste:

```bash
python -m pytest -v
```

Confirma também:

- Na página do pull request, ao fundo, aparece pela primeira vez a verificação **Testes**, com duas linhas (Python 3.10 e Python 3.13). Espera até as duas terem um visto verde. É o GitHub a correr os mesmos 20 testes.

### Passo 14 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

### Passo 15 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas, se existirem, têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da unidade fica fechada sozinha.

### Passo 16 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/0.3-testes-ci
python ../ctesp-ADC/verificar.py 0.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/0.3-testes-ci` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 0.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 0.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 0.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 17 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Ricardo](ricardo.md)).

A unidade seguinte é tua: continua no passo 18.

---

## Fazer a unidade 0.4 — Documentação base

Configura o Sphinx, que gera a documentação do código, e acrescenta o README completo, o guia de contribuição e os modelos de issue e de pull request.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Testes automáticos e integração contínua** (unidade 0.3) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Cria a issue da unidade 0.4

A issue é o registo, no GitHub, do trabalho que vai ser feito. O pull request que vais abrir mais à frente fecha-a sozinho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No campo do título, cola:

```text
[0.4] Documentação base
```

**c)** Na caixa grande de texto, cola:

```markdown
## Objetivo

Ter a documentação do código gerada com o Sphinx e as regras de trabalho do repositório escritas.

## O que inclui

- [ ] Configuração do Sphinx (`docs/conf.py`)
- [ ] Páginas de instalação, arquitetura e testes
- [ ] Referência do código gerada a partir dos docstrings
- [ ] Workflow do GitHub Actions que gera a documentação
- [ ] README completo
- [ ] Guia de contribuição (`CONTRIBUTING.md`)
- [ ] Modelos de issue e de pull request
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#3`. Aponta-o: vais precisar dele quando abrires o pull request.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/0.4-documentacao-base
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/0.4-documentacao-base` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/0.4-documentacao-base'`.

### Passo 21 — Copia e grava os 7 commits

São 7 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 0.4 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 0.4. Eles estão na pasta `ctesp-ADC/fase-0/ficheiros/0.4/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 7**

```bash
python ../ctesp-ADC/copiar.py 0.4 1
```

**Deves ver** `Copiados 6 ficheiros`: `docs/Makefile`, `docs/conf.py`, `docs/index.rst`, `docs/instalacao.rst`, `docs/make.bat`, `requirements-dev.txt`.

```bash
git add -A
git commit -m "docs: configurar o Sphinx e documentar a instalação"
```

**Deves ver** uma linha a terminar em `6 files changed, 235 insertions(+)`.

**Commit 2 de 7**

```bash
python ../ctesp-ADC/copiar.py 0.4 2
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/index.rst`, `docs/testes.rst`.

```bash
git add -A
git commit -m "docs: descrever a arquitetura e os testes"
```

**Deves ver** uma linha a terminar em `3 files changed, 148 insertions(+)`.

**Commit 3 de 7**

```bash
python ../ctesp-ADC/copiar.py 0.4 3
```

**Deves ver** `Copiados 2 ficheiros`: `docs/index.rst`, `docs/referencia.rst`.

```bash
git add -A
git commit -m "docs: gerar a referência do código a partir dos docstrings"
```

**Deves ver** uma linha a terminar em `2 files changed, 48 insertions(+)`.

**Commit 4 de 7**

```bash
python ../ctesp-ADC/copiar.py 0.4 4
```

**Deves ver** `Copiados 1 ficheiro`: `.github/workflows/docs.yml`.

```bash
git add -A
git commit -m "ci: gerar a documentação no GitHub Actions"
```

**Deves ver** uma linha a terminar em `1 file changed, 34 insertions(+)`.

**Commit 5 de 7**

```bash
python ../ctesp-ADC/copiar.py 0.4 5
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs: escrever o README"
```

**Deves ver** uma linha a terminar em `1 file changed, 124 insertions(+), 2 deletions(-)`.

**Commit 6 de 7**

```bash
python ../ctesp-ADC/copiar.py 0.4 6
```

**Deves ver** `Copiados 1 ficheiro`: `CONTRIBUTING.md`.

```bash
git add -A
git commit -m "docs: adicionar o guia de contribuição"
```

**Deves ver** uma linha a terminar em `1 file changed, 148 insertions(+)`.

**Commit 7 de 7**

```bash
python ../ctesp-ADC/copiar.py 0.4 7
```

**Deves ver** `Copiados 4 ficheiros`: `.github/ISSUE_TEMPLATE/bug.md`, `.github/ISSUE_TEMPLATE/tarefa.md`, `.github/ISSUE_TEMPLATE/user_story.md`, `.github/pull_request_template.md`.

```bash
git add -A
git commit -m "chore: adicionar modelos de issue e de pull request"
```

**Deves ver** uma linha a terminar em `4 files changed, 94 insertions(+)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 0.4
git log --oneline -7
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 0.4` | `Tudo certo: o ramo 'feature/0.4-documentacao-base' está igual ao original no fim da unidade 0.4.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -7` | Os teus 7 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx chore: adicionar modelos de issue e de pull request
xxxxxxx docs: adicionar o guia de contribuição
xxxxxxx docs: escrever o README
xxxxxxx ci: gerar a documentação no GitHub Actions
xxxxxxx docs: gerar a referência do código a partir dos docstrings
xxxxxxx docs: descrever a arquitetura e os testes
xxxxxxx docs: configurar o Sphinx e documentar a instalação
```

### Passo 23 — Experimenta o que gravaste

Gera a documentação:

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.` e `The HTML pages are in docs\_build\html.`

Abre-a no browser:

```bash
start docs/_build/html/index.html
```

Percorre as quatro páginas do menu: Instalação e configuração, Arquitetura, Testes e Referência do código. Na Referência do código devem aparecer as funções de cada módulo, com a explicação de cada uma.

Confirma que os testes continuam a passar:

```bash
python -m pytest
```

**Deves ver** `20 passed`.

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/0.4-documentacao-base
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

Na primeira vez pode abrir-se uma janela a pedir para entrares na tua conta do GitHub. Entra e volta ao terminal.

**Deves ver**, perto do fim: `* [new branch]      feature/0.4-documentacao-base -> feature/0.4-documentacao-base`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/0.4-documentacao-base`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/0.4-documentacao-base**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Documentação base
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue que apontaste:

```markdown
## O que muda

Configura o Sphinx e escreve as primeiras páginas da documentação: instalação, arquitetura, testes e a referência do código, gerada a partir dos docstrings. Um workflow do GitHub Actions gera a documentação em cada pull request e falha se houver avisos.

Acrescenta também o README completo, o guia de contribuição e os modelos de issue e de pull request.

Closes #N

## Como testar

1. `python -m pip install -r requirements-dev.txt`
2. `python -m sphinx -W -b html docs docs/_build/html`
3. Abrir `docs/_build/html/index.html` e percorrer as quatro páginas.
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**f)** Clica no botão verde **Create pull request**.

**g)** Se aparecerem verificações automáticas no fundo da página (*Testes*, *Documentação*), espera um ou dois minutos até ficarem com um visto verde.

### Passo 26 — Avisa Tomas

Diz a Tomas que o pull request da unidade 0.4 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 18 a 24.

### Passo 27 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/0.4-documentacao-base
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/0.4-documentacao-base` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Outras tarefas desta fase

### Passo 28 — Cria as 19 issues do perfil Administrador

As 57 user stories do Trello passam a issues do repositório oficial, uma por story. Cada pessoa cria as de um perfil, com a sua conta. As tuas são as do **Administrador**, de A01 a A19.

Podes fazer este passo em qualquer altura depois da Preparação, por exemplo enquanto esperas pela tua vez.

Os textos estão em https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/issues/issues.md, na secção **Administrador**. Abre essa página num separador do browser e deixa-a aberta.

Para cada issue, de A01 a A19:

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica em **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No título, cola o bloco **Título** dessa issue. Cada bloco tem um botão de copiar no canto superior direito.

**c)** Na caixa grande de texto, cola o bloco **Texto**.

**d)** Na coluna da direita, escolhe as duas **Labels** (`user story` e `Administrador`) e a **Milestone** indicada por baixo dos blocos. Deixa **Assignees** vazio: a issue é atribuída quando alguém pegar nela, na fase respetiva.

**e)** Clica em **Create**.

**Deves ver**, no fim, 19 issues em https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+label%3AAdministrador

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 0.1 — Estrutura do pacote Python

- **`.gitignore`** lista o que o Git deve ignorar: a pasta `dados/` (a base de dados de cada pessoa), o ambiente virtual, os ficheiros que o Python e o Sphinx geram. Sem isto, esses ficheiros apareciam como alterações por gravar.
- **`.gitattributes`** obriga a que os ficheiros fiquem com o mesmo tipo de fim de linha (LF) em qualquer sistema. Sem isto, o mesmo ficheiro podia ficar diferente em Windows e em Linux. O `make.bat` é a exceção, porque os scripts do Windows precisam de CRLF.
- **`gestor_campanhas/__init__.py`** é o que faz da pasta `gestor_campanhas` um pacote Python, ou seja, algo que se pode importar. Guarda a versão em `__version__`, o único sítio onde ela está escrita.
- **`gestor_campanhas/__main__.py`** é o ficheiro que o Python executa quando se escreve `python -m gestor_campanhas`. A função `main()` devolve o código de saída (`0` quer dizer "correu bem") e a linha `raise SystemExit(main())` entrega esse código ao sistema operativo.
- **`gestor_campanhas/config.py`** diz onde ficam os dados. `Path(__file__).resolve().parent.parent` é a pasta do projeto, calculada a partir da localização do próprio ficheiro. `pasta_dados()` é uma função, e não um valor fixo, para que a variável de ambiente `GESTOR_CAMPANHAS_DADOS` seja lida no momento em que é precisa. É isso que permite aos testes usar uma pasta temporária.
- **`pyproject.toml`** descreve o projeto: nome, versão mínima do Python, autores. `dynamic = ["version"]` diz que a versão é lida de `gestor_campanhas.__version__`. `dependencies = []` deixa escrito que a aplicação não usa bibliotecas externas.

### Unidade 0.4 — Documentação base

- **`docs/conf.py`** é a configuração do Sphinx.
  - `sys.path.insert(0, os.path.abspath(".."))` acrescenta a pasta do projeto ao caminho do Python. É preciso porque o Sphinx importa os módulos para ler os docstrings, e o `conf.py` está dentro de `docs`.
  - `extensions`: `autodoc` gera a referência a partir dos docstrings; `viewcode` acrescenta a cada função uma ligação para o código-fonte.
  - `release` é lida de `gestor_campanhas.__version__`, para a versão da documentação acompanhar a do código.
  - `language = "pt_PT"` põe em português os textos que o próprio Sphinx escreve.
  - `autodoc_default_options` aplica `members` e `undoc-members` a todos os módulos, por isso em `referencia.rst` basta escrever `.. automodule:: nome_do_modulo`.
  - `autodoc_typehints = "description"` mostra os tipos na descrição dos parâmetros.
- **`docs/index.rst`** é a página inicial. A diretiva `toctree` lista as outras páginas e forma o menu.
- **`docs/referencia.rst`** tem uma diretiva `automodule` por módulo. Um módulo novo só aparece na documentação depois de ser acrescentado aqui.
- **`docs/Makefile` e `docs/make.bat`** são os atalhos habituais do Sphinx (`make html`). Fazem o mesmo que o comando `python -m sphinx -b html docs docs/_build/html`.
- **`.github/workflows/docs.yml`** gera a documentação no GitHub com a opção `-W`, que transforma avisos em erros. Um docstring mal formatado faz falhar a verificação do pull request.
- **Docstrings.** São os textos entre `"""` no início de cada módulo e de cada função. Seguem o formato do Sphinx: `:param nome:` descreve um parâmetro, `:return:` o que a função devolve. Um comentário `#:` por cima de uma constante é o docstring dessa constante.
- **`README.md`** é a página de entrada do repositório no GitHub: o que é a aplicação, como se instala, como se usa e quem a fez.
- **`CONTRIBUTING.md`** descreve as regras de trabalho: ramos, mensagens de commit, pull requests e releases.
- **`.github/ISSUE_TEMPLATE/`** e **`.github/pull_request_template.md`** são os modelos que o GitHub oferece ao criar uma issue ou um pull request. O cabeçalho entre `---` define o nome, o título sugerido e a label.
