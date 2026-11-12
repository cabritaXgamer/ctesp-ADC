# Fase 0 — Passo a passo de Fabio

> **Atenção:** ainda não sei o endereço do vosso repositório oficial. Onde aparecer `https://github.com/DONO/REPOSITORIO-OFICIAL`, usa o endereço verdadeiro.

Esta página tem tudo o que **Fabio** faz na Fase 0 (Arranque), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

Se algum termo não for claro, vê [O que é o quê](../conceitos.md). A ordem geral da fase está na [página da fase](README.md).

## Os teus passos

| Passos | O que fazes | Quando |
|---|---|---|
| 1 a 10 | Fazer a unidade 0.1 — Estrutura do pacote Python | Logo a seguir à Preparação |
| 11 a 17 | Rever e juntar a unidade 0.3 (de Ricardo) | Quando Ricardo avisar que o pull request está aberto |
| 18 a 27 | Fazer a unidade 0.4 — Documentação base | A seguir ao teu passo anterior |
| 28 | Cria as 19 issues do perfil Administrador | Em qualquer altura depois da Preparação |

Os comandos são para colar no terminal, dentro da pasta do repositório oficial. Funcionam no terminal do VS Code, no PowerShell e no Git Bash.

---

## Fazer a unidade 0.1 — Estrutura do pacote Python

Cria a estrutura base do projeto: a pasta do código, o ficheiro que arranca a aplicação e a configuração. No fim, `python -m gestor_campanhas` mostra a versão.

### Passo 1 — Confirma que podes começar

Antes do primeiro passo tens de ter feito a [Preparação](../preparacao.md), e o repositório oficial já tem de ter o ramo `develop` (Parte B da Preparação).

### Passo 2 — Cria a issue da unidade 0.1

A issue é o registo, no GitHub, do trabalho que vai ser feito. O pull request que vais abrir mais à frente fecha-a sozinho.

**a)** Abre https://github.com/DONO/REPOSITORIO-OFICIAL/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

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
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#3`. Aponta-o: vais precisar dele quando abrires o pull request.

### Passo 3 — Atualiza o teu computador e cria o ramo

Abre o terminal na pasta do repositório oficial e corre:

```bash
git fetch origin
git fetch trabalho
git switch develop
git pull
git switch -c feature/0.1-estrutura-pacote
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no repositório oficial. Não mexe nos teus ficheiros |
| `git fetch trabalho` | Vai buscar ao repositório de trabalho os commits que lá estão. Também não mexe nos teus ficheiros |
| `git switch develop` | Muda para o ramo `develop` |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/0.1-estrutura-pacote` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/0.1-estrutura-pacote'`.

### Passo 4 — Copia os 4 commits

São 4 commits. Para cada um há dois comandos:

| Comando | O que faz |
|---|---|
| `git cherry-pick -n <código>` | Copia para a tua pasta as alterações de um commit do repositório de trabalho, sem as gravar. O `-n` quer dizer "ainda não faças commit". Se correr bem, não mostra nada |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Cola as duas linhas, carrega em Enter e confirma o que aparece antes de passares ao seguinte.

**Commit 1 de 4** — `.gitattributes`, `.gitignore`

```bash
git cherry-pick -n 32635df
git commit -m "chore: adicionar .gitignore e .gitattributes"
```

**Deves ver** uma linha a terminar em `2 files changed, 31 insertions(+)`.

**Commit 2 de 4** — `gestor_campanhas/__init__.py`, `gestor_campanhas/__main__.py`

```bash
git cherry-pick -n 39511bf
git commit -m "feat(nucleo): criar pacote gestor_campanhas com ponto de entrada"
```

**Deves ver** uma linha a terminar em `2 files changed, 29 insertions(+)`.

**Commit 3 de 4** — `gestor_campanhas/config.py`

```bash
git cherry-pick -n 30fb481
git commit -m "feat(config): adicionar configuração dos caminhos de dados"
```

**Deves ver** uma linha a terminar em `1 file changed, 43 insertions(+)`.

**Commit 4 de 4** — `pyproject.toml`

```bash
git cherry-pick -n eb954a1
git commit -m "chore: adicionar pyproject.toml"
```

**Deves ver** uma linha a terminar em `1 file changed, 28 insertions(+)`.

Se o `git cherry-pick` mostrar a palavra `CONFLICT`, para. Vê a secção "Se algo correr mal" na [página da fase](README.md).

### Passo 5 — Confirma que ficou igual ao original

```bash
git status
git diff --stat trabalho/feature/0.1-estrutura-pacote
git log --oneline -4
```

| Comando | O que deves ver |
|---|---|
| `git status` | `nothing to commit, working tree clean`: não ficou nada por gravar |
| `git diff --stat trabalho/feature/0.1-estrutura-pacote` | Nada. Este comando compara o teu ramo com o do repositório de trabalho; se não mostra nada, estão iguais |
| `git log --oneline -4` | Os teus 4 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. Os códigos à esquerda vão ser diferentes dos do repositório de trabalho, porque os commits agora são teus:

```text
xxxxxxx chore: adicionar pyproject.toml
xxxxxxx feat(config): adicionar configuração dos caminhos de dados
xxxxxxx feat(nucleo): criar pacote gestor_campanhas com ponto de entrada
xxxxxxx chore: adicionar .gitignore e .gitattributes
```

### Passo 6 — Experimenta o que copiaste

```bash
python -m gestor_campanhas
```

**Deves ver** `Gestor de Campanhas v0.0.0`, e o programa termina logo. Nesta unidade ainda não há menu.

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/0.1-estrutura-pacote
```

O `push` envia o teu ramo e os teus commits para o repositório oficial. O `-u` liga o ramo do teu computador ao do GitHub, para os próximos `push` e `pull` não precisarem de mais nada.

Na primeira vez pode abrir-se uma janela a pedir para entrares na tua conta do GitHub. Entra e volta ao terminal.

**Deves ver**, perto do fim: `* [new branch]      feature/0.1-estrutura-pacote -> feature/0.1-estrutura-pacote`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/DONO/REPOSITORIO-OFICIAL/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/0.1-estrutura-pacote`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/0.1-estrutura-pacote**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Estrutura do pacote Python
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue que apontaste:

```markdown
## O que muda

Cria a estrutura base do projeto: o pacote `gestor_campanhas`, o ponto de entrada, a configuração dos caminhos de dados e o `pyproject.toml`. Acrescenta também o `.gitignore` e o `.gitattributes`.

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

Abre https://github.com/DONO/REPOSITORIO-OFICIAL/pulls e clica em **Testes automáticos e integração contínua**.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

Traz para o teu computador o ramo de Ricardo:

```bash
git fetch origin
git switch --track origin/feature/0.3-testes-ci
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai buscar ao repositório oficial os ramos novos, incluindo o de Ricardo |
| `git switch --track origin/feature/0.3-testes-ci` | Cria no teu computador uma cópia desse ramo e muda para ela |

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
git fetch trabalho
git diff --stat 200a279 develop
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/0.3-testes-ci` | Apaga a cópia do ramo que criaste para experimentar |
| `git fetch trabalho` | Atualiza a informação do repositório de trabalho |
| `git diff --stat 200a279 develop` | Compara o vosso `develop` com o do repositório de trabalho neste mesmo ponto |

**Deves ver:** o último comando não mostra nada. Se mostrar nomes de ficheiros, os dois repositórios ficaram diferentes: não avancem e digam-me que ficheiros aparecem.

### Passo 17 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Ricardo](ricardo.md)).

A unidade seguinte é tua: continua no passo 18.

---

## Fazer a unidade 0.4 — Documentação base

Configura o Sphinx, que gera a documentação do código, e acrescenta o README completo, o guia de contribuição e os modelos de issue e de pull request.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Testes automáticos e integração contínua** (unidade 0.3) tem de estar junto ao `develop`.

Abre https://github.com/DONO/REPOSITORIO-OFICIAL/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Cria a issue da unidade 0.4

A issue é o registo, no GitHub, do trabalho que vai ser feito. O pull request que vais abrir mais à frente fecha-a sozinho.

**a)** Abre https://github.com/DONO/REPOSITORIO-OFICIAL/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

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

### Passo 20 — Atualiza o teu computador e cria o ramo

Abre o terminal na pasta do repositório oficial e corre:

```bash
git fetch origin
git fetch trabalho
git switch develop
git pull
git switch -c feature/0.4-documentacao-base
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no repositório oficial. Não mexe nos teus ficheiros |
| `git fetch trabalho` | Vai buscar ao repositório de trabalho os commits que lá estão. Também não mexe nos teus ficheiros |
| `git switch develop` | Muda para o ramo `develop` |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/0.4-documentacao-base` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/0.4-documentacao-base'`.

### Passo 21 — Copia os 7 commits

São 7 commits. Para cada um há dois comandos:

| Comando | O que faz |
|---|---|
| `git cherry-pick -n <código>` | Copia para a tua pasta as alterações de um commit do repositório de trabalho, sem as gravar. O `-n` quer dizer "ainda não faças commit". Se correr bem, não mostra nada |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Cola as duas linhas, carrega em Enter e confirma o que aparece antes de passares ao seguinte.

**Commit 1 de 7** — `docs/Makefile`, `docs/conf.py`, `docs/index.rst`, `docs/instalacao.rst`, `docs/make.bat`, `requirements-dev.txt`

```bash
git cherry-pick -n 67b6bb0
git commit -m "docs: configurar o Sphinx e documentar a instalação"
```

**Deves ver** uma linha a terminar em `6 files changed, 235 insertions(+)`.

**Commit 2 de 7** — `docs/arquitetura.rst`, `docs/index.rst`, `docs/testes.rst`

```bash
git cherry-pick -n b5dd4ad
git commit -m "docs: descrever a arquitetura e os testes"
```

**Deves ver** uma linha a terminar em `3 files changed, 148 insertions(+)`.

**Commit 3 de 7** — `docs/index.rst`, `docs/referencia.rst`

```bash
git cherry-pick -n 08e1cc0
git commit -m "docs: gerar a referência do código a partir dos docstrings"
```

**Deves ver** uma linha a terminar em `2 files changed, 48 insertions(+)`.

**Commit 4 de 7** — `.github/workflows/docs.yml`

```bash
git cherry-pick -n 6d2e427
git commit -m "ci: gerar a documentação no GitHub Actions"
```

**Deves ver** uma linha a terminar em `1 file changed, 34 insertions(+)`.

**Commit 5 de 7** — `README.md`

```bash
git cherry-pick -n 64458cc
git commit -m "docs: escrever o README"
```

**Deves ver** uma linha a terminar em `1 file changed, 120 insertions(+), 1 deletion(-)`.

**Commit 6 de 7** — `CONTRIBUTING.md`

```bash
git cherry-pick -n ad311fd
git commit -m "docs: adicionar o guia de contribuição"
```

**Deves ver** uma linha a terminar em `1 file changed, 148 insertions(+)`.

**Commit 7 de 7** — `.github/ISSUE_TEMPLATE/bug.md`, `.github/ISSUE_TEMPLATE/tarefa.md`, `.github/ISSUE_TEMPLATE/user_story.md`, `.github/pull_request_template.md`

```bash
git cherry-pick -n 50f15da
git commit -m "chore: adicionar modelos de issue e de pull request"
```

**Deves ver** uma linha a terminar em `4 files changed, 94 insertions(+)`.

Se o `git cherry-pick` mostrar a palavra `CONFLICT`, para. Vê a secção "Se algo correr mal" na [página da fase](README.md).

### Passo 22 — Confirma que ficou igual ao original

```bash
git status
git diff --stat trabalho/feature/0.4-documentacao-base
git log --oneline -7
```

| Comando | O que deves ver |
|---|---|
| `git status` | `nothing to commit, working tree clean`: não ficou nada por gravar |
| `git diff --stat trabalho/feature/0.4-documentacao-base` | Nada. Este comando compara o teu ramo com o do repositório de trabalho; se não mostra nada, estão iguais |
| `git log --oneline -7` | Os teus 7 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. Os códigos à esquerda vão ser diferentes dos do repositório de trabalho, porque os commits agora são teus:

```text
xxxxxxx chore: adicionar modelos de issue e de pull request
xxxxxxx docs: adicionar o guia de contribuição
xxxxxxx docs: escrever o README
xxxxxxx ci: gerar a documentação no GitHub Actions
xxxxxxx docs: gerar a referência do código a partir dos docstrings
xxxxxxx docs: descrever a arquitetura e os testes
xxxxxxx docs: configurar o Sphinx e documentar a instalação
```

### Passo 23 — Experimenta o que copiaste

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

O `push` envia o teu ramo e os teus commits para o repositório oficial. O `-u` liga o ramo do teu computador ao do GitHub, para os próximos `push` e `pull` não precisarem de mais nada.

Na primeira vez pode abrir-se uma janela a pedir para entrares na tua conta do GitHub. Entra e volta ao terminal.

**Deves ver**, perto do fim: `* [new branch]      feature/0.4-documentacao-base -> feature/0.4-documentacao-base`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/DONO/REPOSITORIO-OFICIAL/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/0.4-documentacao-base`.

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

**a)** Abre https://github.com/DONO/REPOSITORIO-OFICIAL/issues e clica em **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No título, cola o bloco **Título** dessa issue. Cada bloco tem um botão de copiar no canto superior direito.

**c)** Na caixa grande de texto, cola o bloco **Texto**.

**d)** Na coluna da direita, escolhe as duas **Labels** (`user story` e `Administrador`) e a **Milestone** indicada por baixo dos blocos. Deixa **Assignees** vazio: a issue é atribuída quando alguém pegar nela, na fase respetiva.

**e)** Clica em **Create**.

**Deves ver**, no fim, 19 issues em https://github.com/DONO/REPOSITORIO-OFICIAL/issues?q=is%3Aissue+label%3AAdministrador

**Atalho opcional.** Há um script que cria as 19 de uma vez. Precisa do GitHub CLI, um programa que deixa usar o GitHub pelo terminal. Só foi testado em modo de simulação, por isso corre primeiro com `--simular` e confirma a lista antes de o correr a sério. Numa pasta **fora** do repositório oficial:

```bash
winget install GitHub.cli
```

Fecha o terminal, abre outro, e inicia sessão (escolhe *GitHub.com*, *HTTPS* e *Login with a web browser*):

```bash
gh auth login
```

```bash
git clone -b guias https://github.com/cabritaXgamer/ctesp-ADC guias-adc
```

```bash
cd guias-adc/issues
```

```bash
python criar_issues.py --repo DONO/NOME --perfil Administrador --simular
```

```bash
python criar_issues.py --repo DONO/NOME --perfil Administrador
```

Troca `DONO/NOME` pela parte final do endereço do repositório oficial. Se o script parar com um erro, as issues anteriores já ficaram criadas: cria as restantes à mão.

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
