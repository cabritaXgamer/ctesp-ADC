# Fase 1 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 1 (Autenticação e sessões), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 10 | Fazer a unidade 1.1 — Login e logout dos três perfis | No início da fase |
| 11 a 17 | Rever e juntar a unidade 1.3 (de Fabio) | Quando Fabio avisar |
| 18 a 27 | Fazer a unidade 1.4 — Alterar a password e editar os meus dados | A seguir ao teu passo anterior |
| 28 a 34 | Rever a release v0.1.0 e juntá-la ao main | Quando Fabio avisar |
| 35 a 38 | Juntar a release v0.1.0 ao develop | Quando Fabio avisar |
| 39 | Cria a página "Arquitetura" da wiki | Em qualquer altura durante a fase |

---

## Fazer a unidade 1.1 — Login e logout dos três perfis

A aplicação passa a ter contas. Quem entra com o email e a password certos vê o menu do seu perfil; no fim, termina a sessão. As passwords ficam guardadas de forma segura.

### Passo 1 — Confirma que podes começar

A fase anterior tem de estar fechada: todos os pull requests juntos e o `develop` do teu computador atualizado. Se for a primeira fase, tens de ter feito a [Preparação](../preparacao.md).

### Passo 2 — Fica com as issues da unidade 1.1

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 3 issues: A01, M01, C01. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A01** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA01%5D%22

```markdown
- [ ] No menu inicial, a opção Entrar pede o email e a password
- [ ] Com as credenciais de um Administrador, abre o menu "Administrador", com o nome da pessoa
- [ ] Com o email ou a password errados, aparece "Email ou password incorretos." e volta ao menu inicial
- [ ] A opção "Terminar sessão" volta ao menu inicial
- [ ] A password é guardada com hash e salt, nunca em texto
```

**Issue M01** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM01%5D%22

```markdown
- [ ] Com as credenciais de um Marketeer, abre o menu "Marketeer", com o nome da pessoa
- [ ] Uma conta desativada não consegue entrar e vê o aviso de conta desativada
- [ ] A opção "Terminar sessão" volta ao menu inicial
```

**Issue C01** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC01%5D%22

```markdown
- [ ] Com as credenciais de um Cliente, abre o menu "Cliente", com o nome da pessoa
- [ ] A mensagem de erro é a mesma quando o email não existe e quando a password está errada
- [ ] A opção "Terminar sessão" volta ao menu inicial
```

Por fim, no quadro Trello, move os cards destas stories de **Sprint Backlog** para **Work In Progress**.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/1.1-login-perfis
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/1.1-login-perfis` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/1.1-login-perfis'`.

### Passo 4 — Copia e grava os 9 commits

São 9 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 1.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 1.1. Eles estão na pasta `ctesp-ADC/fase-1/ficheiros/1.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/bd.py`.

```bash
git add -A
git commit -m "feat(bd): adicionar a tabela de utilizadores"
```

**Deves ver** uma linha a terminar em `1 file changed, 13 insertions(+)`.

**Commit 2 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 2
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/erros.py`, `gestor_campanhas/modelos.py`, `gestor_campanhas/relogio.py`.

```bash
git add -A
git commit -m "feat(modelos): adicionar utilizador, perfis, erros e relógio"
```

**Deves ver** uma linha a terminar em `3 files changed, 106 insertions(+)`.

**Commit 3 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/seguranca.py`.

```bash
git add -A
git commit -m "feat(seguranca): guardar as passwords com hash e salt"
```

**Deves ver** uma linha a terminar em `1 file changed, 63 insertions(+)`.

**Commit 4 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/__init__.py`, `gestor_campanhas/repositorios/utilizadores.py`.

```bash
git add -A
git commit -m "feat(utilizadores): adicionar o repositório de utilizadores"
```

**Deves ver** uma linha a terminar em `2 files changed, 127 insertions(+)`.

**Commit 5 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/__init__.py`, `gestor_campanhas/servicos/autenticacao.py`.

```bash
git add -A
git commit -m "feat(auth): autenticar por email e password"
```

**Deves ver** uma linha a terminar em `2 files changed, 43 insertions(+)`.

**Commit 6 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 6
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/comum.py`, `gestor_campanhas/cli/perfis.py`, `gestor_campanhas/cli/principal.py`.

```bash
git add -A
git commit -m "feat(cli): entrar na aplicação e mostrar o menu do perfil"
```

**Deves ver** uma linha a terminar em `3 files changed, 82 insertions(+), 3 deletions(-)`.

**Commit 7 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 7
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/dados_demo.py`.

```bash
git add -A
git commit -m "feat(dados): criar contas de demonstração"
```

**Deves ver** uma linha a terminar em `1 file changed, 95 insertions(+)`.

**Commit 8 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 8
```

**Deves ver** `Copiados 3 ficheiros`: `tests/conftest.py`, `tests/test_autenticacao.py`, `tests/test_cli.py`.

```bash
git add -A
git commit -m "test(auth): testar passwords, utilizadores, autenticação e menus"
```

**Deves ver** uma linha a terminar em `3 files changed, 186 insertions(+), 11 deletions(-)`.

**Commit 9 de 9**

```bash
python ../ctesp-ADC/copiar.py 1.1 9
```

**Deves ver** `Copiados 5 ficheiros`: `README.md`, `docs/arquitetura.rst`, `docs/index.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(auth): documentar a entrada na aplicação e a arquitetura em camadas"
```

**Deves ver** uma linha a terminar em `5 files changed, 161 insertions(+), 6 deletions(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 1.1
git log --oneline -9
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 1.1` | `Tudo certo: o ramo 'feature/1.1-login-perfis' está igual ao original no fim da unidade 1.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -9` | Os teus 9 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(auth): documentar a entrada na aplicação e a arquitetura em camadas
xxxxxxx test(auth): testar passwords, utilizadores, autenticação e menus
xxxxxxx feat(dados): criar contas de demonstração
xxxxxxx feat(cli): entrar na aplicação e mostrar o menu do perfil
xxxxxxx feat(auth): autenticar por email e password
xxxxxxx feat(utilizadores): adicionar o repositório de utilizadores
xxxxxxx feat(seguranca): guardar as passwords com hash e salt
xxxxxxx feat(modelos): adicionar utilizador, perfis, erros e relógio
xxxxxxx feat(bd): adicionar a tabela de utilizadores
```

### Passo 6 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `40 passed`.

Cria as contas de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver** a lista das três contas, com o email e a password de cada uma.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Entrar` e o pedido do email |
| `admin@agencia.pt` e Enter | O pedido da password |
| `admin12345` e Enter (a password não aparece enquanto escreves, exceto no Git Bash) | `Bem-vindo, Ana Administradora.` e o menu `Administrador — Ana Administradora` |
| `0` e Enter | `Sessão terminada.` e o menu inicial |
| `1`, `admin@agencia.pt`, `errada` | `Email ou password incorretos.` |
| Enter e depois `0` | `Até breve!` |

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/1.1-login-perfis
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/1.1-login-perfis -> feature/1.1-login-perfis`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/1.1-login-perfis`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/1.1-login-perfis**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Login e logout dos três perfis
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

A aplicação passa a ter utilizadores com três perfis (Administrador, Marketeer e Cliente). A opção Entrar pede o email e a password e abre o menu do perfil; a opção Terminar sessão volta ao menu inicial.

- Tabela `utilizadores` e repositório de utilizadores
- Passwords guardadas com hash e salt (PBKDF2)
- Serviço de autenticação, com erros próprios
- Menu de cada perfil
- Contas de demonstração: `python -m gestor_campanhas.dados_demo`

Closes #(número da issue A01)
Closes #(número da issue M01)
Closes #(número da issue C01)

## Como testar

1. `python -m pytest` (40 testes)
2. `python -m gestor_campanhas.dados_demo`
3. `python -m gestor_campanhas`, entrar com cada uma das três contas e terminar a sessão
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards destas stories para **Ready to Verify**.

### Passo 9 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 1.1 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 1 a 7.

### Passo 10 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/1.1-login-perfis
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/1.1-login-perfis` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 1.3 — Horários de entrada e saída dos marketeers

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 11 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 1.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Horários de entrada e saída dos marketeers**.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Fabio:

```bash
git fetch origin
git switch feature/1.3-horarios-marketeers
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/1.3-horarios-marketeers` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/1.3-horarios-marketeers'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `67 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Primeiro cria uma sessão de marketeer: escolhe `1`, entra com `marketeer@agencia.pt` / `marketeer12345` e termina a sessão com `0`. Se as contas ainda não existirem no teu computador, sai e corre `python -m gestor_campanhas.dados_demo`.

Depois entra como administrador (`admin@agencia.pt` / `admin12345`):

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Horários de entrada e saída dos marketeers` e a pergunta `Desde` |
| Enter | A pergunta `Até` |
| Enter | A tabela, com pelo menos uma linha de `Miguel Marketeer`, e o total de sessões |
| Enter | O menu do Administrador |
| `1`, depois `2020-01-01` e `2020-12-31` | `Não há sessões de marketeers neste período.` |
| Enter, `1`, depois `amanha` | `Data inválida.` e a pergunta outra vez |

Confirma também:

- Entra como marketeer e como cliente: o menu deles não tem a opção dos horários.
- Na tabela, as colunas estão alinhadas e a sessão do administrador que estás a usar não aparece.

### Passo 14 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

### Passo 15 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move os cards destas stories para **Ready**.

### Passo 16 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/1.3-horarios-marketeers
python ../ctesp-ADC/verificar.py 1.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/1.3-horarios-marketeers` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 1.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 1.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 1.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 17 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 18.

---

## Fazer a unidade 1.4 — Alterar a password e editar os meus dados

Cada pessoa passa a poder alterar a sua password e os seus dados. O cliente altera também os dados da empresa.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Horários de entrada e saída dos marketeers** (unidade 1.3) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 1.4

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: C03, C04. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C03** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC03%5D%22

```markdown
- [ ] O menu tem a opção "Alterar a password"
- [ ] São pedidas a password atual e a nova, duas vezes
- [ ] Com a password atual errada, a password não é alterada
- [ ] A password nova tem de ter pelo menos 8 caracteres e ser diferente da atual
- [ ] Se a confirmação for diferente da password nova, a password não é alterada
- [ ] Depois da alteração, só a password nova permite entrar
```

**Issue C04** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC04%5D%22

```markdown
- [ ] O menu tem a opção "Editar os meus dados"
- [ ] Para cada dado é mostrado o valor atual; com Enter, o valor mantém-se
- [ ] O cliente pode alterar o nome, o telefone, a empresa e o NIF
- [ ] O email não pode ser alterado
- [ ] O nome não pode ficar vazio; o telefone tem 9 a 15 algarismos; o NIF tem 9 algarismos
- [ ] Se um valor for inválido, nenhum dado é alterado
```

Por fim, no quadro Trello, move os cards destas stories de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/1.4-password-perfil
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/1.4-password-perfil` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/1.4-password-perfil'`.

### Passo 21 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 1.4 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 1.4. Eles estão na pasta `ctesp-ADC/fase-1/ficheiros/1.4/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 1.4 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/utilizadores.py`.

```bash
git add -A
git commit -m "feat(utilizadores): atualizar a password e os dados de um utilizador"
```

**Deves ver** uma linha a terminar em `1 file changed, 33 insertions(+)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 1.4 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/contas.py`.

```bash
git add -A
git commit -m "feat(conta): validar e aplicar alterações à própria conta"
```

**Deves ver** uma linha a terminar em `1 file changed, 84 insertions(+)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 1.4 3
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/comum.py`, `gestor_campanhas/cli/conta.py`, `gestor_campanhas/cli/perfis.py`.

```bash
git add -A
git commit -m "feat(cli): editar os meus dados e alterar a password em todos os perfis"
```

**Deves ver** uma linha a terminar em `3 files changed, 79 insertions(+), 3 deletions(-)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 1.4 4
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_contas.py`.

```bash
git add -A
git commit -m "test(conta): testar a alteração da password e dos dados"
```

**Deves ver** uma linha a terminar em `1 file changed, 147 insertions(+)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 1.4 5
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(conta): documentar as opções da conta"
```

**Deves ver** uma linha a terminar em `3 files changed, 47 insertions(+)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 1.4
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 1.4` | `Tudo certo: o ramo 'feature/1.4-password-perfil' está igual ao original no fim da unidade 1.4.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(conta): documentar as opções da conta
xxxxxxx test(conta): testar a alteração da password e dos dados
xxxxxxx feat(cli): editar os meus dados e alterar a password em todos os perfis
xxxxxxx feat(conta): validar e aplicar alterações à própria conta
xxxxxxx feat(utilizadores): atualizar a password e os dados de um utilizador
```

### Passo 23 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `85 passed`.

Arranca a aplicação e entra como cliente (`cliente@empresa.pt` / `cliente12345`):

```bash
python -m gestor_campanhas
```

| Escreves | Deves ver |
|---|---|
| `1` e Enter | `Editar os meus dados`, o email (que não pode ser alterado) e a pergunta `Nome [Carla Cliente]` |
| Enter | A pergunta do telefone, com o valor atual |
| `912345678` e Enter | A pergunta da empresa |
| Enter, Enter | `Dados guardados.` |
| Enter, `1`, Enter, `123`, Enter, Enter | `O telefone tem de ter entre 9 e 15 algarismos. Os dados não foram alterados.` |
| Enter, `2` | `Alterar a password` e o pedido da password atual |
| `cliente12345`, `nova-password-1`, `nova-password-1` | `Password alterada.` |
| Enter, `0` | O menu inicial |

Entra outra vez com `cliente@empresa.pt` e a password `nova-password-1`: tem de funcionar. Com `cliente12345` já não funciona.

No fim, repõe a password de demonstração, para os passos seguintes: entra, escolhe `2` e troca `nova-password-1` por `cliente12345`.

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/1.4-password-perfil
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/1.4-password-perfil -> feature/1.4-password-perfil`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/1.4-password-perfil`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/1.4-password-perfil**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Alterar a password e editar os meus dados
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O menu de todos os perfis ganha duas opções: "Editar os meus dados" e "Alterar a password". As user stories são do Cliente, mas as opções ficam disponíveis para os três perfis; a empresa e o NIF só são pedidos aos clientes.

- Atualização da password e dos dados no repositório de utilizadores
- Serviço com as validações (password atual, tamanho mínimo, telefone, NIF)
- Opções da conta nos menus

Closes #(número da issue C03)
Closes #(número da issue C04)

## Como testar

1. `python -m pytest` (85 testes)
2. `python -m gestor_campanhas`, entrar como cliente
3. Editar os dados e alterar a password; sair e entrar com a password nova
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards destas stories para **Ready to Verify**.

### Passo 26 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 1.4 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 18 a 24.

### Passo 27 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/1.4-password-perfil
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/1.4-password-perfil` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever a release v0.1.0 e juntá-la ao main

Quem fez: Fabio. Tu confirmas que a versão está pronta e juntas o ramo da release ao `main`.

### Passo 28 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 1.6 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Release v0.1.0**.

### Passo 29 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 30 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Fabio:

```bash
git fetch origin
git switch release/v0.1.0
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch release/v0.1.0` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'release/v0.1.0'`.

Agora experimenta:

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `104 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v0.1.0`. Sai com `0`.

Confirma também:

- No separador **Files changed** do pull request aparecem só três ficheiros: `gestor_campanhas/__init__.py`, `CHANGELOG.md` e `README.md`.
- No topo do pull request está escrito que o destino é o `main` (`... wants to merge 3 commits into main from release/v0.1.0`). Se disser `develop`, avisa Fabio antes de aprovar.

### Passo 31 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

### Passo 32 — Junta o pull request ao main (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `main`.

**Deves ver** o símbolo roxo **Merged** no topo da página.

### Passo 33 — Arruma o teu computador

```bash
git switch develop
git branch -D release/v0.1.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git branch -D release/v0.1.0` | Apaga a cópia do ramo que criaste para experimentar. O `-D` maiúsculo é preciso porque o `develop` ainda não tem estes commits: chegam lá no pull request seguinte |

### Passo 34 — Avisa Fabio

Diz a Fabio que a release v0.1.0 já está no `main`. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 34 a 37.

---

## Juntar a release v0.1.0 ao develop

É o último pull request da fase.

### Passo 35 — Aprova o pull request que leva a release para o develop

Faz este passo quando Fabio te avisar.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Juntar a release v0.1.0 ao develop**.

**b)** No separador **Files changed**, confirma que as alterações são as da release: o número da versão, o `CHANGELOG.md` e o `README.md`.

**c)** Clica em **Review changes**, escolhe **Approve** e clica em **Submit review**.

### Passo 36 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** **Não cliques em Delete branch.** O ramo deste pull request é o `main`, que tem de continuar a existir.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da release fica fechada sozinha.

### Passo 37 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 1.6
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `python ../ctesp-ADC/verificar.py 1.6` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 1.6 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 1.6.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 38 — Avisa o grupo

Diz a Fabio que a release está no `develop` e que já pode arrumar o computador (passo 37 da [página de Fabio](fabio.md)).

Esta era a última vez da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 39 — Cria a página "Arquitetura" da wiki

A wiki ganha uma página que explica como o código está organizado: as camadas, as tabelas e as decisões sobre passwords, sessões e emails.

Podes fazer este passo em qualquer altura durante a fase.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Arquitetura.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New page**.

**c)** Em **Title**, escreve:

```text
Arquitetura
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Arquitetura` e clica em **Save page**.

**Deves ver** a página nova, com as tabelas formatadas, e o nome dela na lista de páginas, à direita.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 1.1 — Login e logout dos três perfis

- **`gestor_campanhas/bd.py`** ganha a tabela `utilizadores`. `email TEXT NOT NULL UNIQUE` impede dois utilizadores com o mesmo email. `CHECK (perfil IN (...))` só deixa guardar um dos três perfis.
- **`gestor_campanhas/modelos.py`** tem a classe `Utilizador`, feita com `@dataclass`: basta declarar os campos e o Python cria sozinho o construtor e a comparação. As constantes `ADMINISTRADOR`, `MARKETEER` e `CLIENTE` evitam escrever os nomes dos perfis à mão pelo código fora.
- **`gestor_campanhas/erros.py`** define os erros da aplicação. `ErroAutenticacao` herda de `ErroAplicacao`, que herda de `Exception`. Os serviços lançam-nos com `raise`; os menus apanham-nos com `try / except` e mostram a mensagem.
- **`gestor_campanhas/relogio.py`** é o único sítio que pergunta as horas ao sistema. Parece a mais, mas é o que permite aos testes "avançar o tempo" sem esperar.
- **`gestor_campanhas/seguranca.py`** trata das passwords. `gerar_hash` cria um *salt* aleatório e calcula o hash com PBKDF2, repetindo a conta 200 000 vezes para ser lento de adivinhar. O resultado tem o formato `algoritmo$iterações$salt$hash`. `verificar_password` repete a conta com o mesmo salt e compara com `hmac.compare_digest`. A password em si nunca é guardada.
- **`gestor_campanhas/repositorios/utilizadores.py`** é o único sítio com SQL sobre utilizadores. Os `?` nas instruções são substituídos pelos valores pelo próprio SQLite, o que evita injeção de SQL. `_de_linha` converte uma linha da tabela num `Utilizador`.
- **`gestor_campanhas/servicos/autenticacao.py`** tem a regra: procura o utilizador, confirma a password, confirma que a conta está ativa. A mensagem é igual para email desconhecido e password errada, para não revelar que emails têm conta.
- **`gestor_campanhas/cli/principal.py`** ganha a função `entrar`, que pede as credenciais e chama o serviço. **`cli/perfis.py`** mostra o menu do perfil: as opções vêm do dicionário `OPCOES`, que nesta unidade ainda está vazio, e "Terminar sessão" é acrescentada no fim.
- **`gestor_campanhas/cli/comum.py`** ganha `ler_password`, que usa `getpass` para a password não aparecer no ecrã.
- **`gestor_campanhas/dados_demo.py`** cria uma conta de cada perfil. Pode ser corrido várias vezes: salta as contas que já existem.
- **`tests/conftest.py`** ganha a fixture `contas` (uma conta de cada perfil) e `hash_rapido`, que baixa as repetições do hash para os testes não demorarem. `@pytest.mark.parametrize` corre o mesmo teste com vários valores.

### Unidade 1.4 — Alterar a password e editar os meus dados

- **`gestor_campanhas/repositorios/utilizadores.py`** ganha `atualizar_password` e `atualizar_dados`, duas instruções `UPDATE`.
- **`gestor_campanhas/servicos/contas.py`** tem as regras. `alterar_password` confirma primeiro a password atual, para garantir que é o próprio a pedir. `atualizar_dados` valida o nome, o telefone e o NIF antes de guardar; se um falhar, lança `ErroValidacao` e nada é guardado. Quem não é cliente fica com a empresa e o NIF como estavam.
- **Porque é que o objeto `utilizador` é atualizado.** Depois de guardar, o serviço copia os dados novos para o objeto que o menu está a usar. Assim, o título do menu mostra logo o nome novo, sem ser preciso sair e entrar.
- **`gestor_campanhas/cli/conta.py`** tem as duas opções. `try / except / else`: o bloco `else` só corre quando não houve erro, e é aí que aparece "Dados guardados.".
- **`gestor_campanhas/cli/comum.py`** ganha `ler_texto_com_valor`, que mostra o valor atual entre parênteses retos e o devolve se a resposta ficar vazia.
- **`gestor_campanhas/cli/perfis.py`**: a lista `OPCOES_DA_CONTA` é acrescentada aos três perfis com `*OPCOES_DA_CONTA`, que "desembrulha" a lista dentro de outra.
- **`tests/test_contas.py`** usa `@pytest.mark.parametrize` para testar de uma vez todos os casos em que a alteração é recusada, cada um com a mensagem esperada.
