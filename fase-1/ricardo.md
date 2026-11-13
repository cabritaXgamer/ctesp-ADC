# Fase 1 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 1 (Autenticação e sessões), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 1.1 (de Tomas) | Quando Tomas avisar |
| 8 a 17 | Fazer a unidade 1.2 — Registo de sessões e saída por inatividade | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 1.4 (de Tomas) | Quando Tomas avisar |
| 25 a 34 | Fazer a unidade 1.5 — Recuperar a password | A seguir ao teu passo anterior |
| 35 | Cria a página "Registo das fases" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 1.1 — Login e logout dos três perfis

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 1.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Login e logout dos três perfis**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Tomas:

```bash
git fetch origin
git switch feature/1.1-login-perfis
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/1.1-login-perfis` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/1.1-login-perfis'`.

Agora experimenta:

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

Confirma também:

- Repete a entrada com `marketeer@agencia.pt` / `marketeer12345` e com `cliente@empresa.pt` / `cliente12345`. O título do menu muda para `Marketeer — ...` e `Cliente — ...`.
- `git status` responde `nothing to commit, working tree clean`: a base de dados com as contas ficou na pasta `dados`, que o Git ignora.

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

**f)** No Trello, move os cards destas stories para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/1.1-login-perfis
python ../ctesp-ADC/verificar.py 1.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/1.1-login-perfis` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 1.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 1.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 1.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 1.2 — Registo de sessões e saída por inatividade

Cada entrada e cada saída passam a ficar registadas, com data e hora. Quem estiver mais de 15 minutos sem fazer nada é posto fora, e essa saída também fica registada.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Login e logout dos três perfis** (unidade 1.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 1.2

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: A02. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A02** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA02%5D%22

```markdown
- [ ] Ao entrar, fica registada uma sessão com o utilizador e a data e hora de entrada
- [ ] Ao terminar a sessão, fica registada a data e hora de saída, com o motivo "logout"
- [ ] Depois de 15 minutos sem atividade, a sessão termina sozinha e o utilizador tem de entrar de novo
- [ ] A saída por inatividade fica registada com o motivo "inatividade" e com a hora em que os 15 minutos se completaram
- [ ] Se o programa for interrompido a meio, a saída fica registada na mesma
- [ ] Uma entrada falhada (password errada) não cria sessão
```

Por fim, no quadro Trello, move os cards destas stories de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/1.2-sessoes-inatividade
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/1.2-sessoes-inatividade` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/1.2-sessoes-inatividade'`.

### Passo 11 — Copia e grava os 8 commits

São 8 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 1.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 1.2. Eles estão na pasta `ctesp-ADC/fase-1/ficheiros/1.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/bd.py`.

```bash
git add -A
git commit -m "feat(bd): adicionar a tabela de sessões"
```

**Deves ver** uma linha a terminar em `1 file changed, 8 insertions(+)`.

**Commit 2 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/config.py`, `gestor_campanhas/modelos.py`.

```bash
git add -A
git commit -m "feat(modelos): adicionar a sessão e o limite de inatividade por omissão"
```

**Deves ver** uma linha a terminar em `2 files changed, 29 insertions(+)`.

**Commit 3 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/configuracoes.py`.

```bash
git add -A
git commit -m "feat(config): ler e guardar definições na base de dados"
```

**Deves ver** uma linha a terminar em `1 file changed, 36 insertions(+)`.

**Commit 4 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 4
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/sessoes.py`.

```bash
git add -A
git commit -m "feat(sessoes): adicionar o repositório de sessões"
```

**Deves ver** uma linha a terminar em `1 file changed, 66 insertions(+)`.

**Commit 5 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 5
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/sessoes.py`.

```bash
git add -A
git commit -m "feat(sessoes): registar entradas e saídas e detetar inatividade"
```

**Deves ver** uma linha a terminar em `1 file changed, 115 insertions(+)`.

**Commit 6 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 6
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/perfis.py`, `gestor_campanhas/cli/principal.py`.

```bash
git add -A
git commit -m "feat(cli): abrir sessão ao entrar e terminá-la por logout ou inatividade"
```

**Deves ver** uma linha a terminar em `2 files changed, 30 insertions(+), 7 deletions(-)`.

**Commit 7 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 7
```

**Deves ver** `Copiados 2 ficheiros`: `tests/test_autenticacao.py`, `tests/test_sessoes.py`.

```bash
git add -A
git commit -m "test(sessoes): testar o registo de sessões e a inatividade"
```

**Deves ver** uma linha a terminar em `2 files changed, 191 insertions(+), 2 deletions(-)`.

**Commit 8 de 8**

```bash
python ../ctesp-ADC/copiar.py 1.2 8
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(sessoes): documentar as sessões e a inatividade"
```

**Deves ver** uma linha a terminar em `3 files changed, 44 insertions(+)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 1.2
git log --oneline -8
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 1.2` | `Tudo certo: o ramo 'feature/1.2-sessoes-inatividade' está igual ao original no fim da unidade 1.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -8` | Os teus 8 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(sessoes): documentar as sessões e a inatividade
xxxxxxx test(sessoes): testar o registo de sessões e a inatividade
xxxxxxx feat(cli): abrir sessão ao entrar e terminá-la por logout ou inatividade
xxxxxxx feat(sessoes): registar entradas e saídas e detetar inatividade
xxxxxxx feat(sessoes): adicionar o repositório de sessões
xxxxxxx feat(config): ler e guardar definições na base de dados
xxxxxxx feat(modelos): adicionar a sessão e o limite de inatividade por omissão
xxxxxxx feat(bd): adicionar a tabela de sessões
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `54 passed`.

Entra e sai uma vez, para criar um registo:

```bash
python -m gestor_campanhas
```

Escolhe `1`, entra com `marketeer@agencia.pt` / `marketeer12345`, escolhe `0` para terminar a sessão e `0` para sair. Se a aplicação disser que o email ou a password estão incorretos, falta criar as contas: corre `python -m gestor_campanhas.dados_demo` e repete.

Agora vê o que ficou registado. Este comando lê a tabela `sessoes` diretamente:

```bash
python -c "import sqlite3; [print(tuple(l)) for l in sqlite3.connect('dados/app.db').execute('SELECT * FROM sessoes')]"
```

**Deves ver** uma linha por cada vez que entraste, com o número do utilizador, a hora de entrada, a hora de saída e `logout`.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/1.2-sessoes-inatividade
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/1.2-sessoes-inatividade -> feature/1.2-sessoes-inatividade`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/1.2-sessoes-inatividade`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/1.2-sessoes-inatividade**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Registo de sessões e saída por inatividade
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

Todas as entradas e saídas passam a ficar registadas na tabela `sessoes`. Uma sessão sem atividade durante mais de 15 minutos termina sozinha quando o utilizador volta a responder a um menu, e a saída fica registada com o motivo `inatividade`.

- Tabela `sessoes` e repositório de sessões
- Repositório de definições (tabela `configuracoes`), onde o limite de inatividade pode ser alterado
- Serviço de sessões: iniciar, terminar, detetar inatividade
- O menu de cada perfil passa a verificar a inatividade e a registar a saída

Closes #(número da issue A02)

## Como testar

1. `python -m pytest` (54 testes)
2. `python -m gestor_campanhas`, entrar e terminar a sessão
3. Confirmar o registo na base de dados (ver o comando na descrição da unidade)
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards destas stories para **Ready to Verify**.

### Passo 16 — Avisa Fabio

Diz a Fabio que o pull request da unidade 1.2 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 1 a 7.

### Passo 17 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/1.2-sessoes-inatividade
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/1.2-sessoes-inatividade` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 1.4 — Alterar a password e editar os meus dados

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 1.4 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Alterar a password e editar os meus dados**.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Tomas:

```bash
git fetch origin
git switch feature/1.4-password-perfil
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/1.4-password-perfil` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/1.4-password-perfil'`.

Agora experimenta:

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

Confirma também:

- Entra como administrador: o menu tem agora três opções (os horários e as duas da conta), e "Editar os meus dados" não pergunta pela empresa nem pelo NIF.

### Passo 21 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 22 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move os cards destas stories para **Ready**.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/1.4-password-perfil
python ../ctesp-ADC/verificar.py 1.4
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/1.4-password-perfil` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 1.4` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 1.4 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 1.4.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 25.

---

## Fazer a unidade 1.5 — Recuperar a password

Quem se esquecer da password pode definir uma nova, com um código enviado para o seu email. Os emails são simulados: cada um é um ficheiro de texto.

### Passo 25 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Alterar a password e editar os meus dados** (unidade 1.4) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 26 — Fica com as issues da unidade 1.5

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: C02. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C02** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC02%5D%22

```markdown
- [ ] O menu inicial tem a opção "Recuperar a password"
- [ ] Depois de indicar o email, é enviado para lá um código de 6 algarismos (na linha de comandos, o código substitui o link)
- [ ] O email é simulado: fica num ficheiro de texto na pasta `dados/caixa_saida`
- [ ] Com o código certo, o cliente define uma password nova e passa a entrar com ela
- [ ] O código vale durante 15 minutos e só pode ser usado uma vez
- [ ] Um pedido novo anula o código anterior
- [ ] A resposta é a mesma quer o email tenha conta quer não
```

Por fim, no quadro Trello, move os cards destas stories de **Sprint Backlog** para **Work In Progress**.

### Passo 27 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/1.5-recuperar-password
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/1.5-recuperar-password` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/1.5-recuperar-password'`.

### Passo 28 — Copia e grava os 7 commits

São 7 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 1.5 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 1.5. Eles estão na pasta `ctesp-ADC/fase-1/ficheiros/1.5/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 7**

```bash
python ../ctesp-ADC/copiar.py 1.5 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `gestor_campanhas/config.py`.

```bash
git add -A
git commit -m "feat(bd): adicionar a tabela de códigos de recuperação e a caixa de saída"
```

**Deves ver** uma linha a terminar em `2 files changed, 22 insertions(+)`.

**Commit 2 de 7**

```bash
python ../ctesp-ADC/copiar.py 1.5 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/correio.py`.

```bash
git add -A
git commit -m "feat(correio): simular o envio de emails com ficheiros de texto"
```

**Deves ver** uma linha a terminar em `1 file changed, 40 insertions(+)`.

**Commit 3 de 7**

```bash
python ../ctesp-ADC/copiar.py 1.5 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/recuperacoes.py`.

```bash
git add -A
git commit -m "feat(recuperacao): guardar os códigos de recuperação"
```

**Deves ver** uma linha a terminar em `1 file changed, 53 insertions(+)`.

**Commit 4 de 7**

```bash
python ../ctesp-ADC/copiar.py 1.5 4
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/recuperacao.py`.

```bash
git add -A
git commit -m "feat(recuperacao): pedir um código e repor a password"
```

**Deves ver** uma linha a terminar em `1 file changed, 84 insertions(+)`.

**Commit 5 de 7**

```bash
python ../ctesp-ADC/copiar.py 1.5 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/principal.py`, `gestor_campanhas/cli/recuperacao.py`.

```bash
git add -A
git commit -m "feat(cli): recuperar a password a partir do menu inicial"
```

**Deves ver** uma linha a terminar em `2 files changed, 45 insertions(+), 1 deletion(-)`.

**Commit 6 de 7**

```bash
python ../ctesp-ADC/copiar.py 1.5 6
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_recuperacao.py`.

```bash
git add -A
git commit -m "test(recuperacao): testar a recuperação da password e os emails"
```

**Deves ver** uma linha a terminar em `1 file changed, 230 insertions(+)`.

**Commit 7 de 7**

```bash
python ../ctesp-ADC/copiar.py 1.5 7
```

**Deves ver** `Copiados 4 ficheiros`: `docs/arquitetura.rst`, `docs/instalacao.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(recuperacao): documentar a recuperação da password e os emails simulados"
```

**Deves ver** uma linha a terminar em `4 files changed, 55 insertions(+), 1 deletion(-)`.


### Passo 29 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 1.5
git log --oneline -7
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 1.5` | `Tudo certo: o ramo 'feature/1.5-recuperar-password' está igual ao original no fim da unidade 1.5.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -7` | Os teus 7 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(recuperacao): documentar a recuperação da password e os emails simulados
xxxxxxx test(recuperacao): testar a recuperação da password e os emails
xxxxxxx feat(cli): recuperar a password a partir do menu inicial
xxxxxxx feat(recuperacao): pedir um código e repor a password
xxxxxxx feat(recuperacao): guardar os códigos de recuperação
xxxxxxx feat(correio): simular o envio de emails com ficheiros de texto
xxxxxxx feat(bd): adicionar a tabela de códigos de recuperação e a caixa de saída
```

### Passo 30 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `104 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

| Escreves | Deves ver |
|---|---|
| `2` e Enter | `Recuperar a password` e o pedido do email |
| `cliente@empresa.pt` e Enter | O aviso de que foi enviado um código, o caminho da pasta dos emails e o pedido do código |

Sem fechar a aplicação, abre no Explorador de Ficheiros a pasta `dados/caixa_saida`, dentro de `ADC-TrabGrupo`. Abre o ficheiro de texto mais recente: é o "email", e tem o código de 6 algarismos.

| Escreves | Deves ver |
|---|---|
| O código e Enter | O pedido da password nova |
| `nova-password-1`, duas vezes | `Password alterada. Já pode entrar com a password nova.` |

Entra com `cliente@empresa.pt` e `nova-password-1`: tem de funcionar.

No fim, repõe a password de demonstração: no menu do cliente, escolhe "Alterar a password" e troca `nova-password-1` por `cliente12345`.

### Passo 31 — Envia o ramo para o GitHub

```bash
git push -u origin feature/1.5-recuperar-password
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/1.5-recuperar-password -> feature/1.5-recuperar-password`.

### Passo 32 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/1.5-recuperar-password`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/1.5-recuperar-password**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Recuperar a password
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O menu inicial ganha a opção "Recuperar a password". A aplicação envia um código de 6 algarismos para o email da conta; com esse código define-se uma password nova. Numa aplicação web seria um link; na linha de comandos, o código faz o mesmo papel.

A aplicação não envia emails verdadeiros: cada mensagem é escrita num ficheiro de texto em `dados/caixa_saida`.

- Tabela `recuperacoes` e repositório dos códigos
- Serviço de correio simulado
- Serviço de recuperação: pedir o código e repor a password
- Opção no menu inicial

Closes #(número da issue C02)

## Como testar

1. `python -m pytest` (104 testes)
2. `python -m gestor_campanhas`, opção 2, com o email `cliente@empresa.pt`
3. Abrir o ficheiro mais recente de `dados/caixa_saida`, copiar o código e definir a password nova
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards destas stories para **Ready to Verify**.

### Passo 33 — Avisa Fabio

Diz a Fabio que o pull request da unidade 1.5 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 18 a 24.

### Passo 34 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/1.5-recuperar-password
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/1.5-recuperar-password` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Outras tarefas desta fase

### Passo 35 — Cria a página "Registo das fases" da wiki

A wiki ganha uma página com o que foi feito em cada fase, quem fez e quem reviu, e as decisões tomadas.

Podes fazer este passo em qualquer altura durante a fase.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New page**.

**c)** Em **Title**, escreve:

```text
Registo das fases
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Registo das fases` e clica em **Save page**.

**Deves ver** a página nova, com as tabelas formatadas, e o nome dela na lista de páginas, à direita.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 1.2 — Registo de sessões e saída por inatividade

- **`gestor_campanhas/bd.py`** ganha a tabela `sessoes`. `REFERENCES utilizadores (id)` é uma chave estrangeira: só deixa guardar sessões de utilizadores que existem. A coluna `saida` pode ficar vazia (`NULL`) enquanto a sessão está aberta.
- **`gestor_campanhas/repositorios/configuracoes.py`** lê e guarda definições na tabela `configuracoes`. `ON CONFLICT (chave) DO UPDATE` quer dizer "se a chave já existir, substitui o valor".
- **`gestor_campanhas/repositorios/sessoes.py`** regista a entrada (`abrir`) e a saída (`fechar`). O `WHERE ... AND saida IS NULL` em `fechar` garante que uma sessão já fechada não é alterada.
- **`gestor_campanhas/servicos/sessoes.py`** tem a classe `SessaoAtiva`, que guarda o momento da última atividade e o limite. `expirou()` compara a hora atual com `ultima_atividade + limite`. `terminar` regista a saída; quando o motivo é a inatividade, a hora registada é a do limite e não a do momento em que se deu por isso.
- **Porque é que a inatividade só é detetada quando o utilizador responde.** Um programa de linha de comandos fica parado dentro do `input()` à espera do teclado. Não há forma simples de o interromper ao fim de 15 minutos. Por isso a verificação é feita logo a seguir à resposta: se o limite passou, a resposta é ignorada e a sessão termina.
- **`gestor_campanhas/cli/perfis.py`** passa a receber a `SessaoAtiva`. Depois de cada resposta ao menu chama `sessao.expirou()`; se não expirou, chama `registar_atividade()`.
- **`gestor_campanhas/cli/principal.py`** usa `try / finally` à volta do menu do perfil: aconteça o que acontecer, incluindo Ctrl+C, `sessoes.terminar` é chamado e a saída fica registada.
- **`tests/test_sessoes.py`** tem a fixture `relogio_falso`, que substitui `relogio.agora` por uma função controlada pelo teste. `relogio_falso.avancar(minutes=20)` faz "passar" 20 minutos num instante.

### Unidade 1.5 — Recuperar a password

- **`gestor_campanhas/bd.py`** ganha a tabela `recuperacoes`: de quem é o código, o hash do código, até quando vale e se já foi usado.
- **`gestor_campanhas/config.py`** ganha `MINUTOS_VALIDADE_CODIGO` e `pasta_caixa_saida()`.
- **`gestor_campanhas/servicos/correio.py`** simula o envio de emails. Em vez de enviar, escreve um ficheiro de texto com o destinatário, a data, o assunto e o texto. O nome do ficheiro tem a data e a hora, para ficarem por ordem. O resto da aplicação chama `correio.enviar` como se o email fosse mesmo enviado; para enviar a sério, só este módulo teria de mudar.
- **`gestor_campanhas/repositorios/recuperacoes.py`** guarda os códigos. `criar` anula primeiro os códigos anteriores do mesmo utilizador. `obter_ativa` só devolve um código que não tenha sido usado e ainda esteja dentro do prazo.
- **`gestor_campanhas/servicos/recuperacao.py`** tem as regras.
  - `gerar_codigo` usa `secrets.randbelow`, que é próprio para segurança (ao contrário de `random`). `f"{numero:06d}"` escreve o número com seis algarismos, com zeros à esquerda.
  - `pedir_codigo` não devolve nada nem dá erro quando o email não tem conta. É de propósito: assim ninguém fica a saber que emails estão registados.
  - O código é guardado com hash, tal como as passwords. Quem conseguisse ler a base de dados não ficava a saber os códigos.
  - `repor_password` confirma o código, valida a password nova e só então marca o código como usado. Se a password nova for inválida, o código continua a valer.
- **Porque é um código e não um link.** A user story fala num link enviado por email. Numa aplicação de linha de comandos não há onde clicar, por isso o link é substituído por um código, que prova a mesma coisa: quem pede tem acesso ao email da conta.
- **`gestor_campanhas/cli/recuperacao.py`** conduz os dois passos e mostra onde está a pasta dos emails. **`cli/principal.py`** ganha a opção `2`.
- **`tests/test_recuperacao.py`**: a fixture `pasta_de_dados` aponta a pasta de dados para uma pasta temporária, para os emails dos testes não se misturarem com os verdadeiros. `codigo_do_ultimo_email` lê o código do ficheiro com uma expressão regular.
