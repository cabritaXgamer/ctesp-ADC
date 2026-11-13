# Fase 1 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 1 (Autenticação e sessões), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 1.2 (de Ricardo) | Quando Ricardo avisar |
| 8 a 17 | Fazer a unidade 1.3 — Horários de entrada e saída dos marketeers | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 1.5 (de Ricardo) | Quando Ricardo avisar |
| 25 a 33 | Preparar a release v0.1.0 | A seguir ao teu passo anterior |
| 34 a 37 | Publicar a release v0.1.0 e pedir o regresso ao develop | Quando Tomas avisar |
| 38 a 39 | Cria a página "Guia de utilização" da wiki; Atualiza a página inicial da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 1.2 — Registo de sessões e saída por inatividade

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 1.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Registo de sessões e saída por inatividade**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Ricardo:

```bash
git fetch origin
git switch feature/1.2-sessoes-inatividade
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/1.2-sessoes-inatividade` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/1.2-sessoes-inatividade'`.

Agora experimenta:

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

Confirma também:

- A inatividade demora 15 minutos a acontecer, por isso não se experimenta à mão. Os testes simulam a passagem do tempo: `python -m pytest -v tests/test_sessoes.py` mostra, entre outros, `test_menu_termina_a_sessao_por_inatividade` e `test_saida_por_inatividade_fica_com_a_hora_do_limite` a passar.

### Passo 4 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

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
git branch -d feature/1.2-sessoes-inatividade
python ../ctesp-ADC/verificar.py 1.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/1.2-sessoes-inatividade` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 1.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 1.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 1.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Ricardo](ricardo.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 1.3 — Horários de entrada e saída dos marketeers

O Administrador ganha a primeira opção do seu menu: uma tabela com as entradas e saídas dos marketeers, que pode filtrar por datas.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Registo de sessões e saída por inatividade** (unidade 1.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 1.3

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. São 1 issue: A03. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A03** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA03%5D%22

```markdown
- [ ] O menu do Administrador tem a opção "Horários de entrada e saída dos marketeers"
- [ ] A tabela mostra, por sessão, o marketeer, a entrada, a saída, a duração e o motivo da saída
- [ ] As sessões aparecem da mais recente para a mais antiga
- [ ] É possível filtrar por data inicial e data final; as duas são opcionais e o último dia conta por inteiro
- [ ] Uma sessão ainda aberta aparece como "(em curso)"
- [ ] Só aparecem sessões de marketeers
- [ ] A opção não existe nos menus do Marketeer e do Cliente
```

Por fim, no quadro Trello, move os cards destas stories de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/1.3-horarios-marketeers
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/1.3-horarios-marketeers` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/1.3-horarios-marketeers'`.

### Passo 11 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 1.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 1.3. Eles estão na pasta `ctesp-ADC/fase-1/ficheiros/1.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 1.3 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/cli/comum.py`.

```bash
git add -A
git commit -m "feat(cli): ler datas e mostrar tabelas de texto"
```

**Deves ver** uma linha a terminar em `1 file changed, 41 insertions(+)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 1.3 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/sessoes.py`.

```bash
git add -A
git commit -m "feat(sessoes): listar as sessões dos utilizadores de um perfil"
```

**Deves ver** uma linha a terminar em `1 file changed, 30 insertions(+)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 1.3 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/sessoes.py`.

```bash
git add -A
git commit -m "feat(sessoes): consultar os horários dos marketeers por período"
```

**Deves ver** uma linha a terminar em `1 file changed, 32 insertions(+), 2 deletions(-)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 1.3 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/admin.py`, `gestor_campanhas/cli/perfis.py`.

```bash
git add -A
git commit -m "feat(admin): mostrar os horários de entrada e saída dos marketeers"
```

**Deves ver** uma linha a terminar em `2 files changed, 71 insertions(+), 2 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 1.3 5
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_horarios.py`.

```bash
git add -A
git commit -m "test(horarios): testar a consulta de horários e a tabela"
```

**Deves ver** uma linha a terminar em `1 file changed, 137 insertions(+)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 1.3 6
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(horarios): documentar a consulta de horários"
```

**Deves ver** uma linha a terminar em `3 files changed, 30 insertions(+)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 1.3
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 1.3` | `Tudo certo: o ramo 'feature/1.3-horarios-marketeers' está igual ao original no fim da unidade 1.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(horarios): documentar a consulta de horários
xxxxxxx test(horarios): testar a consulta de horários e a tabela
xxxxxxx feat(admin): mostrar os horários de entrada e saída dos marketeers
xxxxxxx feat(sessoes): consultar os horários dos marketeers por período
xxxxxxx feat(sessoes): listar as sessões dos utilizadores de um perfil
xxxxxxx feat(cli): ler datas e mostrar tabelas de texto
```

### Passo 13 — Experimenta o que gravaste

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

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/1.3-horarios-marketeers
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/1.3-horarios-marketeers -> feature/1.3-horarios-marketeers`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/1.3-horarios-marketeers`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/1.3-horarios-marketeers**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Horários de entrada e saída dos marketeers
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a poder consultar os horários de entrada e saída dos marketeers, numa tabela com filtro por datas.

- Listagem das sessões por perfil, no repositório
- Serviço com o filtro por período e o cálculo da duração
- Funções comuns para ler datas e mostrar tabelas de texto
- Primeira opção do menu do Administrador

Closes #(número da issue A03)

## Como testar

1. `python -m pytest` (67 testes)
2. `python -m gestor_campanhas`, entrar e sair como marketeer, e depois entrar como administrador
3. Escolher "Horários de entrada e saída dos marketeers"
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards destas stories para **Ready to Verify**.

### Passo 16 — Avisa Tomas

Diz a Tomas que o pull request da unidade 1.3 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 11 a 17.

### Passo 17 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/1.3-horarios-marketeers
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/1.3-horarios-marketeers` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 1.5 — Recuperar a password

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 1.5 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Recuperar a password**.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, traz o ramo de Ricardo:

```bash
git fetch origin
git switch feature/1.5-recuperar-password
```

| Comando | O que faz |
|---|---|
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/1.5-recuperar-password` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/1.5-recuperar-password'`.

Agora experimenta:

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

Confirma também:

- Pede outro código (opção `2`) e, em vez do código certo, escreve `000000`. Aparece `O código não é válido ou já passou do prazo. A password não foi alterada.`
- Pede um código para `ninguem@empresa.pt`. A aplicação responde da mesma maneira, mas não aparece nenhum ficheiro novo em `dados/caixa_saida`.
- `git status` continua a responder `nothing to commit`: os emails ficam dentro de `dados`, que o Git ignora.

### Passo 21 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

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
git branch -d feature/1.5-recuperar-password
python ../ctesp-ADC/verificar.py 1.5
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/1.5-recuperar-password` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 1.5` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 1.5 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 1.5.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 34 da [página de Ricardo](ricardo.md)).

A vez seguinte é tua: continua no passo 25.

---

## Preparar a release v0.1.0

Fecha a fase com uma versão: o número da versão passa para 0.1.0, cria-se o registo de alterações e atualiza-se o README. Esta unidade vai para o `main`, o ramo das versões entregues.

### Passo 25 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Recuperar a password** (unidade 1.5) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 26 — Cria a issue da unidade 1.6

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[1.6] Release v0.1.0
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Publicar a versão 0.1.0, com as user stories da Fase 1 (autenticação e sessões).

## O que inclui

- [ ] Versão 0.1.0 em `gestor_campanhas/__init__.py`
- [ ] Registo de alterações (`CHANGELOG.md`)
- [ ] README atualizado
- [ ] Pull request para `main`
- [ ] Tag e release `v0.1.0` no GitHub
- [ ] `main` de volta ao `develop`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 27 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c release/v0.1.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c release/v0.1.0` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'release/v0.1.0'`.

### Passo 28 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 1.6 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 1.6. Eles estão na pasta `ctesp-ADC/fase-1/ficheiros/1.6/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 1.6 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__init__.py`.

```bash
git add -A
git commit -m "chore(release): passar a versão para 0.1.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 1.6 2
```

**Deves ver** `Copiados 1 ficheiro`: `CHANGELOG.md`.

```bash
git add -A
git commit -m "docs(release): criar o registo de alterações"
```

**Deves ver** uma linha a terminar em `1 file changed, 32 insertions(+)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 1.6 3
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(release): atualizar o README para a versão 0.1.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 18 insertions(+), 3 deletions(-)`.


### Passo 29 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 1.6
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 1.6` | `Tudo certo: o ramo 'release/v0.1.0' está igual ao original no fim da unidade 1.6.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(release): atualizar o README para a versão 0.1.0
xxxxxxx docs(release): criar o registo de alterações
xxxxxxx chore(release): passar a versão para 0.1.0
```

### Passo 30 — Experimenta o que gravaste

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

### Passo 31 — Envia o ramo para o GitHub

```bash
git push -u origin release/v0.1.0
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      release/v0.1.0 -> release/v0.1.0`.

### Passo 32 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `main`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `release/v0.1.0`.

**b)** No topo, a base tem de ser `main`, e não `develop`. Clica em **base: develop**, escolhe `main` e confirma que fica **base: main** e **compare: release/v0.1.0**. Uma release vai para o `main`, que é o ramo das versões entregues.

**c)** No título, cola:

```text
Release v0.1.0
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Não é preciso trocar nada:

```markdown
## O que muda

Prepara a versão 0.1.0, a primeira release da aplicação.

- Versão passa de 0.0.0 para 0.1.0
- Novo `CHANGELOG.md`, com o que cada versão acrescenta
- README atualizado: menu inicial, emails simulados, sessões e estrutura do projeto

Este pull request vai para o `main`. A issue da release é fechada pelo pull request que leva a release de volta ao `develop`.

## Como testar

1. `python -m pytest` (104 testes)
2. `python -m sphinx -W -b html docs docs/_build/html`
3. `python -m gestor_campanhas`: o título mostra `v0.1.0`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

### Passo 33 — Avisa Tomas

Diz a Tomas que o pull request da release v0.1.0 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 28 a 34.

---

## Publicar a release v0.1.0 e pedir o regresso ao develop

Com a release no `main`, falta marcá-la com uma tag e levar os commits dela de volta ao `develop`.

### Passo 34 — Publica a release v0.1.0 no GitHub

Faz este passo quando Tomas te avisar que a release está no `main`.

Publicar a release cria a **tag**, uma etiqueta que marca para sempre o commit desta versão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/releases/new

**b)** Clica em **Choose a tag**, escreve `v0.1.0` e clica em **Create new tag: v0.1.0 on publish**.

**c)** Em **Target**, escolhe `main`.

**d)** Em **Release title**, cola:

```text
v0.1.0 — Autenticação e sessões
```

**e)** Na caixa de texto, cola:

```markdown
## Autenticação e sessões

Primeira versão da aplicação com contas de utilizador.

### Acrescentado

- Entrada com email e password para os três perfis: Administrador, Marketeer e Cliente
- Menu próprio de cada perfil
- Passwords guardadas com hash e salt
- Registo de todas as entradas e saídas, e saída automática ao fim de 15 minutos sem atividade
- Consulta dos horários de entrada e saída dos marketeers, pelo Administrador
- Edição dos próprios dados e alteração da password
- Recuperação da password com um código enviado por email (simulado em ficheiros de texto)

### User stories

A01, A02, A03, M01, C01, C02, C03 e C04.

### Como experimentar

```
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```
```

**f)** Clica em **Publish release**.

**Deves ver** a página da release, e a tag `v0.1.0` em https://github.com/Blive77/ADC-TrabGrupo/tags

**g)** Fecha a milestone da fase: abre https://github.com/Blive77/ADC-TrabGrupo/milestones, e na linha `Fase 1 — Autenticação e sessões` clica em **Close**. Se ainda tiver issues abertas, não a feches e avisa o grupo.

### Passo 35 — Abre o pull request que leva a release para o develop

A release está no `main`, mas o `develop` ainda não tem os commits dela (a versão nova e o registo de alterações). Este pull request leva-os para lá, para os dois ramos ficarem alinhados.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/compare/develop...main

**b)** Confirma, no topo, que está **base: develop** e **compare: main**, e clica em **Create pull request**.

**c)** No título, cola:

```text
Juntar a release v0.1.0 ao develop
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue da release, que apontaste no início:

```markdown
## O que muda

Traz para o `develop` os commits da release v0.1.0, que já estão no `main`: a versão nova, o registo de alterações e o README.

Closes #N
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 1 — Autenticação e sessões`

**f)** Clica em **Create pull request**.

### Passo 36 — Avisa Tomas

Diz a Tomas que o pull request que leva a release v0.1.0 para o `develop` está aberto. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 35 a 38.

### Passo 37 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d release/v0.1.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d release/v0.1.0` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Outras tarefas desta fase

### Passo 38 — Cria a página "Guia de utilização" da wiki

A wiki ganha uma página que explica como usar a aplicação: entrar, o que cada perfil pode fazer e como recuperar a password.

Podes fazer este passo em qualquer altura durante a fase.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Guia-de-utilizacao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New page**.

**c)** Em **Title**, escreve:

```text
Guia de utilização
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Guia de utilização` e clica em **Save page**.

**Deves ver** a página nova, com as tabelas formatadas, e o nome dela na lista de páginas, à direita.

### Passo 39 — Atualiza a página inicial da wiki

A página inicial passa a ter as ligações para as três páginas novas e a indicar a versão atual.

Faz este passo no fim da fase, depois de publicares a release.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 0.1.0` e clica em **Save page**.

**Deves ver**, na tabela "Páginas desta wiki", quatro ligações, e a linha `Versão atual: v0.1.0`. As ligações só funcionam depois de Tomas e Ricardo criarem as páginas deles.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 1.3 — Horários de entrada e saída dos marketeers

- **`gestor_campanhas/cli/comum.py`** ganha duas funções. `ler_data` usa `datetime.strptime(resposta, "%Y-%m-%d")` para converter o texto numa data; se o texto não for uma data, `strptime` lança `ValueError` e a pergunta repete-se. `mostrar_tabela` calcula a largura de cada coluna (o texto mais comprido) e alinha com `ljust`.
- **`gestor_campanhas/repositorios/sessoes.py`** ganha `listar_por_perfil`. O `JOIN` junta cada sessão ao utilizador a que pertence, para se poder filtrar pelo perfil e mostrar o nome. Os filtros de data só são acrescentados à consulta quando são pedidos.
- **`gestor_campanhas/servicos/sessoes.py`** ganha `horarios_dos_marketeers`. A regra do "último dia inteiro" está aqui: o filtro é "antes das 00:00 do dia seguinte". Se a data inicial for depois da final, lança `ErroValidacao`. `duracao` devolve a diferença entre a saída e a entrada, ou `None` se a sessão ainda está aberta.
- **`gestor_campanhas/cli/admin.py`** é o primeiro módulo de opções de um perfil. A função `horarios` pede as datas, chama o serviço e mostra a tabela. Não tem regras: se o serviço lançar um erro, mostra a mensagem.
- **`gestor_campanhas/cli/perfis.py`**: a opção é acrescentada à lista do Administrador em `OPCOES`. Não foi preciso mexer no ciclo do menu, que percorre a lista.
- **`tests/test_horarios.py`** tem a fixture `historico`, que cria sessões em dias diferentes para testar os filtros. O teste `test_mostrar_tabela_alinha_as_colunas` compara a saída linha a linha.

### Unidade 1.6 — Release v0.1.0

- **`gestor_campanhas/__init__.py`**: `__version__` passa para `"0.1.0"`. É o único sítio onde a versão está escrita; o menu inicial, o `pyproject.toml` e a documentação leem-na daqui.
- **`CHANGELOG.md`** é o registo de alterações: o que cada versão trouxe, escrito para quem usa a aplicação e não para quem a programa.
- **`README.md`** acompanha a versão: o exemplo do menu, as secções sobre emails e sessões e a estrutura do projeto.
- **Porque é que a release vai para o `main`.** No modelo Git Flow, o `develop` junta o trabalho em curso e o `main` só recebe versões prontas. Cada commit do `main` corresponde a uma versão entregue.
- **A tag `v0.1.0`** marca o commit exato da versão. Mesmo que o projeto continue, é sempre possível voltar a ver o código tal como estava nesta versão.
- **Porque é que a release volta ao `develop`.** Os três commits da release foram feitos num ramo à parte e juntos ao `main`. O `develop` ainda não os tem. O último pull request da fase leva-os para lá, para a fase seguinte já partir da versão 0.1.0.
- **Números das versões.** `0.1.0` lê-se "versão 0, fase 1, correção 0". O número do meio sobe em cada fase; a versão `1.0.0` é a entrega final.
