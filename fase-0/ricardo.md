# Fase 0 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 0 (Arranque), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 0.2 (de Tomas) | Quando Tomas avisar que o pull request está aberto |
| 8 a 17 | Fazer a unidade 0.3 — Testes automáticos e integração contínua | A seguir ao teu passo anterior |
| 18 a 19 | Cria as 20 issues do perfil Cliente; Cria a página inicial da wiki | Em qualquer altura depois da Preparação |

---

## Rever e juntar a unidade 0.2 — Base de dados e menu inicial

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 0.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Base de dados e menu inicial**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Tomas:

```bash
git fetch origin
git switch feature/0.2-base-dados-menu
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/0.2-base-dados-menu` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/0.2-base-dados-menu'`.

Agora experimenta:

```bash
python -m gestor_campanhas
```

Aparece o menu inicial. Experimenta, por esta ordem:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | `A autenticação ainda não está disponível nesta versão.` |
| Enter | O menu outra vez |
| `9` e Enter | `Opção inválida.` |
| `0` e Enter | `Até breve!`, e o programa termina |

Depois confirma que a base de dados foi criada e que o Git a ignora:

```bash
git status
```

**Deves ver** `nothing to commit, working tree clean`. A aplicação criou a pasta `dados` com o ficheiro `app.db`, mas ela está no `.gitignore` e por isso não aparece.

Confirma também:

- Arranca a aplicação outra vez e, com o menu à espera, carrega em Ctrl+C. Deve aparecer `A sair...` e o programa termina, sem mensagens de erro.
- Os acentos do menu (`Opção`) aparecem bem.

### Passo 4 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 5 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas, se existirem, têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da unidade fica fechada sozinha.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/0.2-base-dados-menu
python ../ctesp-ADC/verificar.py 0.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/0.2-base-dados-menu` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 0.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 0.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 0.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Tomas](tomas.md)).

A unidade seguinte é tua: continua no passo 8.

---

## Fazer a unidade 0.3 — Testes automáticos e integração contínua

Acrescenta 20 testes automáticos e põe o GitHub a corrê-los sozinho em cada pull request.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Base de dados e menu inicial** (unidade 0.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Cria a issue da unidade 0.3

A issue é o registo, no GitHub, do trabalho que vai ser feito. O pull request que vais abrir mais à frente fecha-a sozinho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No campo do título, cola:

```text
[0.3] Testes automáticos e integração contínua
```

**c)** Na caixa grande de texto, cola:

```markdown
## Objetivo

Ter testes automáticos a correr no computador de cada pessoa e em cada pull request, para apanhar erros antes do merge.

## O que inclui

- [ ] Configuração do pytest e `requirements-dev.txt`
- [ ] Fixtures comuns: base de dados em memória e teclado simulado
- [ ] Testes da base de dados e dos caminhos de dados
- [ ] Testes dos menus e do ponto de entrada
- [ ] Workflow do GitHub Actions que corre os testes
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#3`. Aponta-o: vais precisar dele quando abrires o pull request.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/0.3-testes-ci
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/0.3-testes-ci` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/0.3-testes-ci'`.

### Passo 11 — Copia e grava os 4 commits

São 4 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 0.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 0.3. Eles estão na pasta `ctesp-ADC/fase-0/ficheiros/0.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.3 1
```

**Deves ver** `Copiados 3 ficheiros`: `pyproject.toml`, `requirements-dev.txt`, `tests/conftest.py`.

```bash
git add -A
git commit -m "test: configurar o pytest e as fixtures comuns"
```

**Deves ver** uma linha a terminar em `3 files changed, 55 insertions(+)`.

**Commit 2 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.3 2
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_bd.py`.

```bash
git add -A
git commit -m "test(bd): testar a ligação, as tabelas e os caminhos de dados"
```

**Deves ver** uma linha a terminar em `1 file changed, 78 insertions(+)`.

**Commit 3 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.3 3
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_cli.py`.

```bash
git add -A
git commit -m "test(cli): testar os menus e o ponto de entrada"
```

**Deves ver** uma linha a terminar em `1 file changed, 93 insertions(+)`.

**Commit 4 de 4**

```bash
python ../ctesp-ADC/copiar.py 0.3 4
```

**Deves ver** `Copiados 1 ficheiro`: `.github/workflows/testes.yml`.

```bash
git add -A
git commit -m "ci: correr os testes no GitHub Actions"
```

**Deves ver** uma linha a terminar em `1 file changed, 31 insertions(+)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 0.3
git log --oneline -4
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 0.3` | `Tudo certo: o ramo 'feature/0.3-testes-ci' está igual ao original no fim da unidade 0.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -4` | Os teus 4 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx ci: correr os testes no GitHub Actions
xxxxxxx test(cli): testar os menus e o ponto de entrada
xxxxxxx test(bd): testar a ligação, as tabelas e os caminhos de dados
xxxxxxx test: configurar o pytest e as fixtures comuns
```

### Passo 13 — Experimenta o que gravaste

```bash
python -m pytest
```

**Deves ver**, na última linha, `20 passed`. Cada ponto que aparece antes é um teste que passou.

Para ver o nome de cada teste:

```bash
python -m pytest -v
```

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/0.3-testes-ci
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

Na primeira vez pode abrir-se uma janela a pedir para entrares na tua conta do GitHub. Entra e volta ao terminal.

**Deves ver**, perto do fim: `* [new branch]      feature/0.3-testes-ci -> feature/0.3-testes-ci`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/0.3-testes-ci`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/0.3-testes-ci**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Testes automáticos e integração contínua
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue que apontaste:

```markdown
## O que muda

Acrescenta 20 testes com o pytest, que cobrem a base de dados, os caminhos de dados, as funções comuns dos menus, o menu inicial e o ponto de entrada. Um workflow do GitHub Actions passa a correr os testes em cada push e em cada pull request para `main` e `develop`.

Closes #N

## Como testar

1. `python -m pip install -r requirements-dev.txt`
2. `python -m pytest`
3. Devem passar os 20 testes.
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**f)** Clica no botão verde **Create pull request**.

**g)** Se aparecerem verificações automáticas no fundo da página (*Testes*, *Documentação*), espera um ou dois minutos até ficarem com um visto verde.

### Passo 16 — Avisa Fabio

Diz a Fabio que o pull request da unidade 0.3 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 11 a 17.

### Passo 17 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/0.3-testes-ci
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/0.3-testes-ci` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Outras tarefas desta fase

### Passo 18 — Cria as 20 issues do perfil Cliente

As 57 user stories do Trello passam a issues do repositório oficial, uma por story. Cada pessoa cria as de um perfil, com a sua conta. As tuas são as do **Cliente**, de C01 a C20.

Podes fazer este passo em qualquer altura depois da Preparação, por exemplo enquanto esperas pela tua vez.

Os textos estão em https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/issues/issues.md, na secção **Cliente**. Abre essa página num separador do browser e deixa-a aberta.

Para cada issue, de C01 a C20:

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica em **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No título, cola o bloco **Título** dessa issue. Cada bloco tem um botão de copiar no canto superior direito.

**c)** Na caixa grande de texto, cola o bloco **Texto**.

**d)** Na coluna da direita, escolhe as duas **Labels** (`user story` e `Cliente`) e a **Milestone** indicada por baixo dos blocos. Deixa **Assignees** vazio: a issue é atribuída quando alguém pegar nela, na fase respetiva.

**e)** Clica em **Create**.

**Deves ver**, no fim, 20 issues em https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+label%3ACliente

### Passo 19 — Cria a página inicial da wiki

A wiki é a documentação do repositório, editada no próprio GitHub. A página inicial apresenta o projeto, a equipa e o plano das fases.

Podes fazer este passo em qualquer altura depois da Preparação. Tem de ser feito antes de Tomas criar a segunda página.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Create the first page**.

**c)** Deixa o **Title** como está (`Home`). Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**d)** Em **Edit message**, escreve `Criar a página inicial` e clica em **Save page**.

**Deves ver** a página com as tabelas da equipa, dos perfis e das fases. A ligação "Fluxo Git" ainda não funciona: passa a funcionar quando Tomas criar essa página.

**e)** Avisa Tomas de que já pode criar a página "Fluxo Git" ([página de Tomas](tomas.md)).

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 0.3 — Testes automáticos e integração contínua

- **`requirements-dev.txt`** lista as ferramentas de desenvolvimento. Instalam-se com `python -m pip install -r requirements-dev.txt`.
- **`pyproject.toml`** ganha a secção `[tool.pytest.ini_options]`. `testpaths` diz onde estão os testes. `pythonpath = ["."]` deixa os testes importar `gestor_campanhas` sem ser preciso instalar o pacote.
- **`tests/conftest.py`** define as *fixtures*: peças que o pytest prepara antes de cada teste e entrega aos testes que as pedem pelo nome do parâmetro.
  - `ligacao` cria uma base de dados em memória, já com as tabelas. O `yield` entrega-a ao teste; o que vem depois do `yield` corre no fim, para a fechar.
  - `teclado` substitui a função `input` por outra que devolve respostas preparadas. Quando as respostas acabam, lança `EOFError`, tal como o `input` verdadeiro quando a entrada termina.
- **Fixtures do próprio pytest** usadas nos testes: `monkeypatch` (altera variáveis de ambiente e funções só durante o teste), `tmp_path` (uma pasta temporária), `capsys` (lê o que foi escrito no ecrã).
- **`tests/test_bd.py`** e **`tests/test_cli.py`** têm os testes. Cada teste é uma função começada por `test_`, com três partes: preparar, executar e verificar com `assert`. `pytest.raises(sqlite3.IntegrityError)` verifica que uma instrução falha como esperado.
- **`.github/workflows/testes.yml`** é a integração contínua. `on` define quando corre (push e pull request para `main` e `develop`); `matrix` repete o trabalho para duas versões do Python; os `steps` obtêm o código, instalam o Python, instalam as ferramentas e correm os testes.
