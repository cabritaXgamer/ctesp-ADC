# Fase 0 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 0 (Arranque), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 0.1 (de Fabio) | Quando Fabio avisar que o pull request está aberto |
| 8 a 17 | Fazer a unidade 0.2 — Base de dados e menu inicial | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 0.4 (de Fabio) | Quando Fabio avisar que o pull request está aberto |
| 25 a 26 | Cria as 18 issues do perfil Marketeer; Cria a página "Fluxo Git" da wiki | Em qualquer altura depois da Preparação |

---

## Rever e juntar a unidade 0.1 — Estrutura do pacote Python

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 0.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Estrutura do pacote Python**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Fabio:

```bash
git fetch origin
git switch feature/0.1-estrutura-pacote
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/0.1-estrutura-pacote` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/0.1-estrutura-pacote'`.

Agora experimenta:

```bash
python -m gestor_campanhas
```

**Deves ver** `Gestor de Campanhas v0.0.0`, e o programa termina logo. Nesta unidade ainda não há menu.

Confirma também:

- O `.gitignore` tem as linhas `dados/`, `.venv/`, `__pycache__/` e `docs/_build/`.
- No ficheiro `gestor_campanhas/config.py`, as duas funções têm um texto entre `"""` logo a seguir ao nome. Esse texto é o docstring, a documentação da função.

### Passo 4 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

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
git branch -d feature/0.1-estrutura-pacote
python ../ctesp-ADC/verificar.py 0.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/0.1-estrutura-pacote` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 0.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 0.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 0.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Fabio](fabio.md)).

A unidade seguinte é tua: continua no passo 8.

---

## Fazer a unidade 0.2 — Base de dados e menu inicial

A aplicação passa a criar a base de dados quando arranca e a mostrar um menu inicial. Ficam também as funções que todos os menus vão usar.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Estrutura do pacote Python** (unidade 0.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Cria a issue da unidade 0.2

A issue é o registo, no GitHub, do trabalho que vai ser feito. O pull request que vais abrir mais à frente fecha-a sozinho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No campo do título, cola:

```text
[0.2] Base de dados e menu inicial
```

**c)** Na caixa grande de texto, cola:

```markdown
## Objetivo

Ter a base de dados SQLite criada no arranque e um menu inicial a funcionar, como base para os menus de cada perfil.

## O que inclui

- [ ] Módulo `bd` com a ligação SQLite e a criação das tabelas
- [ ] Funções comuns dos menus: títulos, leitura de texto, confirmações, escolha de opções
- [ ] Menu inicial com as opções Entrar e Sair
- [ ] Ponto de entrada ligado à base de dados e ao menu
- [ ] Acentos corretos em qualquer terminal
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
git switch -c feature/0.2-base-dados-menu
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/0.2-base-dados-menu` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/0.2-base-dados-menu'`.

### Passo 11 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 0.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 0.2. Eles estão na pasta `ctesp-ADC/fase-0/ficheiros/0.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 0.2 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/bd.py`.

```bash
git add -A
git commit -m "feat(bd): adicionar ligação SQLite e criação de tabelas"
```

**Deves ver** uma linha a terminar em `1 file changed, 79 insertions(+)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 0.2 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/__init__.py`, `gestor_campanhas/cli/comum.py`.

```bash
git add -A
git commit -m "feat(cli): adicionar funções comuns dos menus"
```

**Deves ver** uma linha a terminar em `2 files changed, 84 insertions(+)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 0.2 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/cli/principal.py`.

```bash
git add -A
git commit -m "feat(cli): adicionar menu inicial"
```

**Deves ver** uma linha a terminar em `1 file changed, 33 insertions(+)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 0.2 4
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__main__.py`.

```bash
git add -A
git commit -m "feat(nucleo): ligar o ponto de entrada à base de dados e ao menu inicial"
```

**Deves ver** uma linha a terminar em `1 file changed, 13 insertions(+), 2 deletions(-)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 0.2 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/__main__.py`, `gestor_campanhas/cli/comum.py`.

```bash
git add -A
git commit -m "fix(cli): ler e escrever acentos em UTF-8 em qualquer terminal"
```

**Deves ver** uma linha a terminar em `2 files changed, 22 insertions(+), 4 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 0.2
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 0.2` | `Tudo certo: o ramo 'feature/0.2-base-dados-menu' está igual ao original no fim da unidade 0.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx fix(cli): ler e escrever acentos em UTF-8 em qualquer terminal
xxxxxxx feat(nucleo): ligar o ponto de entrada à base de dados e ao menu inicial
xxxxxxx feat(cli): adicionar menu inicial
xxxxxxx feat(cli): adicionar funções comuns dos menus
xxxxxxx feat(bd): adicionar ligação SQLite e criação de tabelas
```

### Passo 13 — Experimenta o que gravaste

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

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/0.2-base-dados-menu
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

Na primeira vez pode abrir-se uma janela a pedir para entrares na tua conta do GitHub. Entra e volta ao terminal.

**Deves ver**, perto do fim: `* [new branch]      feature/0.2-base-dados-menu -> feature/0.2-base-dados-menu`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/0.2-base-dados-menu`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/0.2-base-dados-menu**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Base de dados e menu inicial
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue que apontaste:

```markdown
## O que muda

A aplicação passa a criar a base de dados SQLite no arranque e a mostrar um menu inicial. As funções comuns dos menus ficam em `cli/comum.py`, para serem reutilizadas pelos menus de cada perfil.

Inclui uma correção para os acentos aparecerem bem quando a aplicação corre no Git Bash.

Closes #N

## Como testar

1. `python -m gestor_campanhas`
2. Escolher `1`: aparece o aviso de que a autenticação ainda não está disponível.
3. Escrever uma opção que não existe: aparece `Opção inválida.`
4. Escolher `0`: aparece `Até breve!` e o programa termina.
5. Confirmar que foi criada a pasta `dados` com o ficheiro `app.db`.
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 0 — Arranque`

**f)** Clica no botão verde **Create pull request**.

**g)** Se aparecerem verificações automáticas no fundo da página (*Testes*, *Documentação*), espera um ou dois minutos até ficarem com um visto verde.

### Passo 16 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 0.2 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 1 a 7.

### Passo 17 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/0.2-base-dados-menu
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/0.2-base-dados-menu` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 0.4 — Documentação base

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 0.4 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Documentação base**.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Fabio:

```bash
git fetch origin
git switch feature/0.4-documentacao-base
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/0.4-documentacao-base` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/0.4-documentacao-base'`.

Agora experimenta:

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

Confirma também:

- Na página do pull request, ao fundo, aparecem duas verificações: **Testes** e **Documentação**. Espera até terem um visto verde.
- No separador **Files changed**, o ficheiro `README.md` tem as secções Requisitos, Instalação, Utilização, Configuração, Desenvolvimento e Equipa.

### Passo 21 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

### Passo 22 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas, se existirem, têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da unidade fica fechada sozinha.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/0.4-documentacao-base
python ../ctesp-ADC/verificar.py 0.4
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/0.4-documentacao-base` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 0.4` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 0.4 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 0.4.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Fabio](fabio.md)).

Esta era a última unidade da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 25 — Cria as 18 issues do perfil Marketeer

As 57 user stories do Trello passam a issues do repositório oficial, uma por story. Cada pessoa cria as de um perfil, com a sua conta. As tuas são as do **Marketeer**, de M01 a M18.

Podes fazer este passo em qualquer altura depois da Preparação, por exemplo enquanto esperas pela tua vez.

Os textos estão em https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/issues/issues.md, na secção **Marketeer**. Abre essa página num separador do browser e deixa-a aberta.

Para cada issue, de M01 a M18:

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica em **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No título, cola o bloco **Título** dessa issue. Cada bloco tem um botão de copiar no canto superior direito.

**c)** Na caixa grande de texto, cola o bloco **Texto**.

**d)** Na coluna da direita, escolhe as duas **Labels** (`user story` e `Marketeer`) e a **Milestone** indicada por baixo dos blocos. Deixa **Assignees** vazio: a issue é atribuída quando alguém pegar nela, na fase respetiva.

**e)** Clica em **Create**.

**Deves ver**, no fim, 18 issues em https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+label%3AMarketeer

### Passo 26 — Cria a página "Fluxo Git" da wiki

A wiki é a documentação do repositório, editada no próprio GitHub. Esta página explica como o grupo usa os ramos, os commits e os pull requests.

Faz este passo depois de Ricardo ter criado a página inicial da wiki. O GitHub só deixa criar outras páginas depois de a primeira existir.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Fluxo-Git.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New page**.

**c)** Em **Title**, escreve:

```text
Fluxo Git
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Fluxo Git` e clica em **Save page**.

**Deves ver** a página com as tabelas dos ramos e dos tipos de commit. Na página inicial da wiki, a ligação "Fluxo Git" passa a funcionar.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 0.2 — Base de dados e menu inicial

- **`gestor_campanhas/bd.py`** trata da base de dados.
  - `ligar()` abre a ligação e configura duas coisas. `row_factory = sqlite3.Row` permite ler as colunas pelo nome (`linha["chave"]`) em vez da posição. `PRAGMA foreign_keys = ON` liga a verificação das chaves estrangeiras, que o SQLite traz desligada. O SQLite cria o ficheiro mas não a pasta, por isso a função cria a pasta primeiro.
  - `ESQUEMA` tem as instruções `CREATE TABLE IF NOT EXISTS`. Por causa do `IF NOT EXISTS`, podem ser executadas em todos os arranques sem apagar dados. Para já existe só a tabela `configuracoes`; cada fase acrescenta as suas.
  - `EM_MEMORIA` (`":memory:"`) é um caminho especial do SQLite: a base de dados vive na memória e desaparece quando a ligação fecha. É usada nos testes.
  - `iniciar_bd()` junta as duas coisas: abre a ligação e cria as tabelas.
- **`gestor_campanhas/cli/comum.py`** junta o que todos os menus precisam. `escolher_opcao` recebe uma lista de pares `(chave, descrição)`, mostra-os e repete a pergunta até a resposta ser uma das chaves. `confirmar` e `ler_texto` seguem a mesma ideia: um ciclo `while True` que só termina com uma resposta válida.
- **`gestor_campanhas/cli/principal.py`** é o menu inicial. É um ciclo que mostra o menu, lê a escolha e só sai com `return` quando a opção é `0`.
- **`gestor_campanhas/__main__.py`** passa a abrir a base de dados e a chamar o menu. Usa `try / except / finally`: o `finally` garante que a ligação é fechada mesmo que o utilizador interrompa com Ctrl+C (`KeyboardInterrupt`) ou que a entrada acabe (`EOFError`).
- **O último commit é uma correção** (`fix`). No Git Bash os acentos apareciam trocados, porque o Python usava a codificação antiga do Windows. A função `configurar_terminal()` força o UTF-8 no teclado, na saída e nos erros.
