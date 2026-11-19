# Fase 7 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 7 (Fecho e entrega), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 7.2 (de Tomas) | Quando Tomas avisar |
| 8 a 16 | Preparar a release v1.0.0 | A seguir ao teu passo anterior |
| 17 a 22 | Publicar a release v1.0.0 e pedir o regresso ao develop | Quando Fabio avisar |
| 23 a 26 | Cria a página "Backlog e user stories" da wiki; Cria a página "Changelog" da wiki; Atualiza a página "Registo das fases" da wiki; Atualiza a página inicial da wiki | No fim da fase, depois de publicares a release |

---

## Rever e juntar a unidade 7.2 — Revisão dos docstrings, Sphinx e README final

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 7.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Revisão dos docstrings, Sphinx e README final**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/7.2-documentacao-final
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/7.2-documentacao-final` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/7.2-documentacao-final'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `987 passed`. São mais 109 do que no fim da unidade 7.1: os testes da documentação, um por ficheiro de código.

Corre só os testes da documentação:

```bash
python -m pytest tests/test_documentacao.py
```

**Deves ver** `109 passed`.

Gera a documentação:

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Abre a documentação gerada: no Explorador de Ficheiros, entra na pasta `ADC-TrabGrupo`, depois em `docs`, `_build` e `html`, e faz duplo clique em `index.html`.

**Deves ver**, na lista "Conteúdo", a página nova **Modelo de dados**, entre **Arquitetura** e **Testes**. Abre-a: tem as secções `Relações entre as tabelas`, `Tabelas`, `Como os valores são guardados`, `O que acontece quando se apaga` e `Tabelas novas numa base de dados que já existe`.

Abre também a página **Arquitetura** e desce até `Base de dados`.

**Deves ver** só um parágrafo, com uma ligação para o **Modelo de dados**.

Confirma também:

- No separador **Files changed** aparecem oito ficheiros: os novos `docs/modelo_dados.rst` e `tests/test_documentacao.py`, e `README.md`, `docs/arquitetura.rst`, `docs/index.rst`, `docs/instalacao.rst`, `gestor_campanhas/cli/comum.py` e `gestor_campanhas/servicos/sessoes.py`.
- Nos dois ficheiros de `gestor_campanhas` só mudam docstrings: nenhuma linha de código.
- Na descrição está `Closes #` seguido do número da issue da unidade, e não `#N`.

### Passo 4 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 5 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/7.2-documentacao-final
python ../ctesp-ADC/verificar.py 7.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/7.2-documentacao-final` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 7.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 7.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 7.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 8.

---

## Preparar a release v1.0.0

Fecha o projeto com a versão 1.0.0, a que é entregue: sobe o número da versão, acrescenta a secção desta versão ao registo de alterações e atualiza o README. Esta unidade vai para o `main`, e não para o `develop`.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Revisão dos docstrings, Sphinx e README final** (unidade 7.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Cria a issue da unidade 7.3

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[7.3] Release v1.0.0
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Publicar a versão 1.0.0, a primeira versão completa, com as 57 user stories, os testes dos fluxos completos e a documentação final.

## O que inclui

- [ ] Versão 1.0.0 em `gestor_campanhas/__init__.py`
- [ ] Registo de alterações (`CHANGELOG.md`)
- [ ] README atualizado
- [ ] Pull request para `main`
- [ ] Tag e release `v1.0.0` no GitHub
- [ ] `main` de volta ao `develop`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 7 — Fecho e entrega`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c release/v1.0.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c release/v1.0.0` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'release/v1.0.0'`.

**Se em vez disso aparecer** `fatal: a branch named 'release/v1.0.0' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..release/v1.0.0
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D release/v1.0.0
git switch -c release/v1.0.0
```

  **Deves ver** `Deleted branch release/v1.0.0 (was ...)` e depois `Switched to a new branch 'release/v1.0.0'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch release/v1.0.0` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 7.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 7.3. Eles estão na pasta `ctesp-ADC/fase-7/ficheiros/7.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 7.3 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__init__.py`.

```bash
git add -A
git commit -m "chore(release): passar a versão para 1.0.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 7.3 2
```

**Deves ver** `Copiados 1 ficheiro`: `CHANGELOG.md`.

```bash
git add -A
git commit -m "docs(release): registar as alterações da versão 1.0.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 19 insertions(+)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 7.3 3
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(release): atualizar o README para a versão 1.0.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 2 insertions(+), 1 deletion(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 7.3
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 7.3` | `Tudo certo: o ramo 'release/v1.0.0' está igual ao original no fim da unidade 7.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(release): atualizar o README para a versão 1.0.0
xxxxxxx docs(release): registar as alterações da versão 1.0.0
xxxxxxx chore(release): passar a versão para 1.0.0
```

### Passo 13 — Experimenta o que gravaste

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `987 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v1.0.0`. Sai com `0`.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin release/v1.0.0
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      release/v1.0.0 -> release/v1.0.0`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `main`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/main...release/v1.0.0?expand=1

**b)** Confirma, no topo, que está **base: main** e **compare: release/v1.0.0**. O link do ponto a) já abre com o `main` escolhido. Se estiver **base: develop**, clica aí e escolhe `main`. Uma release vai para o `main`, que é o ramo das versões entregues.

**c)** No título, cola:

```text
Release v1.0.0
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Não é preciso trocar nada:

```markdown
## O que muda

Prepara a versão 1.0.0, a versão de entrega.

- Versão passa de 0.6.0 para 1.0.0
- `CHANGELOG.md` com a secção da versão 1.0.0
- README atualizado: tabela de versões e exemplo do menu

Este pull request vai para o `main`. A issue da release é fechada pelo pull request que leva a release de volta ao `develop`.

## Como testar

1. `python -m pytest` (987 testes)
2. `python -m sphinx -W -b html docs docs/_build/html`
3. `python -m gestor_campanhas`: o título mostra `v1.0.0`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 7 — Fecho e entrega`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** Confirma o destino. Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v1.0.0`. Se disser `into develop`, **não avises ninguém ainda**: clica em **Edit**, à direita do título, clica em **base: develop**, escolhe `main`, confirma em **Change base** e clica em **Save**.

### Passo 16 — Avisa Fabio

Diz a Fabio que o pull request da release v1.0.0 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 11 a 18.

---

## Publicar a release v1.0.0 e pedir o regresso ao develop

Com a release no `main`, falta marcá-la com uma tag e levar os commits dela de volta ao `develop`.

### Passo 17 — Confirma que o main já tem a versão 1.0.0

Faz este passo quando Fabio te avisar que a release está no `main`.

A tag vai ser criada no `main`. Se o `main` ainda não tiver a versão nova, a tag fica a marcar o código da versão anterior. Foi o que aconteceu nas duas primeiras fases.

Abre https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py

**Deves ver** a linha `__version__ = "1.0.0"`.

Se vires outra versão, **não publiques a release**. O pull request foi junto ao `develop` em vez do `main`. Avisa Fabio e corrijam assim: abre https://github.com/Blive77/ADC-TrabGrupo/compare/main...develop?expand=1, cria um pull request com o título `Release v1.0.0`, Fabio aprova e junta, e só depois voltas a este passo.

### Passo 18 — Publica a release v1.0.0 no GitHub

Publicar a release cria a **tag**, uma etiqueta que marca para sempre o commit desta versão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/releases/new

**b)** Clica em **Choose a tag**, escreve `v1.0.0` e clica em **Create new tag: v1.0.0 on publish**.

**c)** Em **Target**, escolhe `main`.

**d)** Em **Release title**, cola:

```text
v1.0.0 — Fecho e entrega
```

**e)** Na caixa de texto, cola:

````markdown
## Fecho e entrega

Primeira versão completa do Gestor de Campanhas, com as 57 user stories do projeto: 19 do Administrador, 18 do Marketeer e 20 do Cliente. Esta versão não traz funcionalidades novas: confirma que as peças funcionam juntas, completa os dados de demonstração e fecha a documentação.

### Acrescentado

- Testes dos fluxos completos, com os três perfis: da conta nova à primeira entrada; do pedido de campanha ao criativo publicado, passando pelo ficheiro, pelos comentários, pelas notificações e emails, pelo painel de marketeers e pelo relatório; do criativo rejeitado à aprovação; e do pedido de budget à decisão do Administrador
- Testes da documentação: todos os módulos, classes e funções têm docstring, e a referência inclui todos os módulos
- Página "Modelo de dados" na documentação

### Alterado

- Dados de demonstração finais: criativos em estados diferentes, um deles com ficheiro e à espera da aprovação da cliente, um segundo comentário já respondido e as notificações de cada conta
- Documentação revista: arquitetura, configuração, testes e README

### Versões anteriores

v0.1.0 (autenticação e sessões), v0.2.0 (clientes e marketeers), v0.3.0 (campanhas e pedidos), v0.4.0 (criativos), v0.5.0 (budget) e v0.6.0 (comentários, notificações, painel e relatório). O detalhe de cada uma está no `CHANGELOG.md`.

### Como experimentar

```
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

Entrar com `cliente@empresa.pt` / `cliente12345` e aprovar o criativo `Banner de Natal`, em "Criativos"; com `marketeer@agencia.pt` / `marketeer12345` e responder ao comentário do `Vídeo da montra`; ou com `admin@agencia.pt` / `admin12345` e abrir o "Painel de marketeers". As outras contas de demonstração estão no README.
````

**f)** Clica em **Publish release**.

**Deves ver** a página da release, e a tag `v1.0.0` em https://github.com/Blive77/ADC-TrabGrupo/tags. Na linha da tag aparece o commit `Merge pull request ... from .../release/v1.0.0`. Se aparecer outro commit, o **Target** ficou errado: avisa o grupo antes de continuar.

### Passo 19 — Abre o pull request que leva a release para o develop

A release está no `main`, mas o `develop` ainda não tem os commits dela (a versão nova e o registo de alterações). Este pull request leva-os para lá, para os dois ramos ficarem alinhados.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/compare/develop...main

**b)** Confirma, no topo, que está **base: develop** e **compare: main**, e clica em **Create pull request**.

**c)** No título, cola:

```text
Juntar a release v1.0.0 ao develop
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue da release, que apontaste no início:

```markdown
## O que muda

Traz para o `develop` os commits da release v1.0.0, que já estão no `main`: a versão nova, o registo de alterações e o README.

Closes #N
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 7 — Fecho e entrega`

**f)** Clica em **Create pull request**.

### Passo 20 — Avisa Fabio

Diz a Fabio que o pull request que leva a release v1.0.0 para o `develop` está aberto. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 19 a 22.

### Passo 21 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d release/v1.0.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d release/v1.0.0` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

### Passo 22 — Fecha a milestone da fase

Faz este passo depois de Fabio juntar o último pull request. Nessa altura a issue da release já está fechada, e a milestone fica com todas as issues fechadas.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/milestones

**b)** Na linha `Fase 7 — Fecho e entrega`, confirma que a barra está a 100% e clica em **Close**.

Se a barra não estiver a 100%, clica no nome da milestone para ver que issues estão abertas. Uma issue fica aberta quando o pull request dela foi junto sem `Closes #número`. Para a fechar à mão, abre a issue, escreve na caixa de comentário `Resolvida pelo pull request #N` (com o número do pull request) e clica em **Close with comment**. Depois volta a este passo.

---

## Outras tarefas desta fase

### Passo 23 — Cria a página "Backlog e user stories" da wiki

Uma página nova, com as 57 user stories do projeto, por fase e por perfil, e para cada uma a unidade em que foi feita e quem a fez.

Faz os teus passos da wiki no fim da fase, depois de publicares a release `v1.0.0`.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Backlog-e-user-stories.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New Page**, no canto superior direito.

**c)** Em **Title**, escreve exatamente:

```text
Backlog e user stories
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Backlog e user stories` e clica em **Save page**.

**Deves ver** a página com a tabela `Por fase` e uma tabela por perfil: `Administrador` (19 linhas), `Marketeer` (18) e `Cliente` (20).

### Passo 24 — Cria a página "Changelog" da wiki

Uma página nova, com as alterações de cada versão, da v0.1.0 à v1.0.0. É uma cópia do ficheiro `CHANGELOG.md` do repositório.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Changelog.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New Page**, no canto superior direito.

**c)** Em **Title**, escreve exatamente:

```text
Changelog
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Changelog` e clica em **Save page**.

**Deves ver** a página a começar pela secção `v1.0.0 — Fecho e entrega (2026-11-21)` e a acabar na `v0.1.0`.

### Passo 25 — Atualiza a página "Registo das fases" da wiki

A página ganha o que correu mal na Fase 6, a secção da Fase 7 e, no fim, o resumo do projeto.

Na Fase 6, o texto desta página foi colado na página inicial, e esta página ficou com uma versão antiga, só com as Fases 0 e 1. Este passo e o da página inicial substituem as duas por inteiro, por isso ficam corrigidas. Antes de colar, confirma no topo que a página aberta é a certa: o título tem de ser **Registo das fases**.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Registo das fases** na lista de páginas, à direita, e depois em **Edit**.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Registar a Fase 7` e clica em **Save page**.

**Deves ver** a secção `Fase 7 — Fecho e entrega`, com a tabela das três unidades, e no fim a secção `Resumo do projeto`.

### Passo 26 — Atualiza a página inicial da wiki

A página inicial passa a indicar a versão 1.0.0 e a ligar para as dez páginas da wiki. É o último passo da wiki: faz este passo depois de Fabio e Tomas criarem as páginas deles ("Testes", "Instalação e configuração" e "Modelo de dados"), para todas as ligações abrirem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Edit**, no canto superior direito. Confirma que estás a editar a página **Home**: é o título que aparece no topo.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 1.0.0` e clica em **Save page**.

**Deves ver** a linha `Versão atual: v1.0.0 (Fase 7 — Fecho e entrega). As 57 user stories estão implementadas.`

**e)** Na tabela `Páginas desta wiki`, clica em cada uma das nove ligações e confirma que abre a página certa. Se uma abrir uma página vazia a pedir para a criar, não a cries: o título da página verdadeira ficou diferente. Avisa quem a criou, que corrige o título no **Edit** dessa página.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 7.3 — Release v1.0.0

- **`gestor_campanhas/__init__.py`**: `__version__` passa para `"1.0.0"`. O menu inicial, o `pyproject.toml` e a documentação leem a versão daqui. O primeiro número passa a 1 porque é a primeira versão completa: até aqui, cada versão `0.N.0` acrescentava as user stories de uma fase.
- **`CHANGELOG.md`** ganha a secção `v1.0.0`, por cima das anteriores. Como não há funcionalidades novas, a parte "User stories" diz que nenhuma é nova e que ficam entregues as 57.
- **`README.md`**: a tabela de versões ganha a linha `v1.0.0`, a negrito por ser a versão de entrega, e o exemplo do menu passa a mostrar `v1.0.0`.
- **O caminho de uma release** é o mesmo das fases anteriores: o pull request do ramo `release/v1.0.0` para o `main`; a confirmação de que o `main` já tem a versão 1.0.0; a publicação da release, que cria a tag no `main`; o pull request do `main` para o `develop`; e o fecho da milestone. Por ser a última, a milestone `Fase 7 — Fecho e entrega` é a última a fechar: no fim, ficam fechadas as oito.
