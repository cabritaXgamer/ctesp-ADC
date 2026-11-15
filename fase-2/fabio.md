# Fase 2 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 2 (Clientes e marketeers), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 10 | Fazer a unidade 2.1 — Lista de clientes com pesquisa | No início da fase |
| 11 a 17 | Rever e juntar a unidade 2.3 (de Ricardo) | Quando Ricardo avisar |
| 18 a 27 | Fazer a unidade 2.4 — Adicionar e editar marketeers | A seguir ao teu passo anterior |
| 28 | Atualiza a página "Arquitetura" da wiki | Em qualquer altura durante a fase |

---

## Fazer a unidade 2.1 — Lista de clientes com pesquisa

O Administrador ganha a opção "Clientes": uma tabela com todos os clientes, por ordem alfabética, que pode pesquisar por nome. As contas de demonstração passam a ter três clientes.

### Passo 1 — Confirma que podes começar

A fase anterior tem de estar fechada: todos os pull requests juntos e o `develop` do teu computador atualizado. Se for a primeira fase, tens de ter feito a [Preparação](../preparacao.md).

### Passo 2 — Fica com as issues da unidade 2.1

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: A04. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A04** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA04%5D%22

```markdown
- [ ] O menu do Administrador tem a opção "Clientes"
- [ ] A tabela mostra, por cliente, o número, o nome, a empresa, o email, o telefone e o estado da conta (Ativa ou Desativada)
- [ ] Os clientes aparecem por ordem alfabética do nome, e os nomes com acento ficam no sítio certo
- [ ] É possível pesquisar por parte do nome, sem distinguir maiúsculas nem acentos
- [ ] Por baixo da tabela aparece o total de clientes
- [ ] Quando não há clientes, ou a pesquisa não encontra nenhum, aparece uma mensagem a dizê-lo
- [ ] A opção não existe nos menus do Marketeer e do Cliente
- [ ] O número de campanhas ativas de cada cliente entra na Fase 3, quando existirem campanhas
```

Por fim, no quadro Trello, move o card da story A04 de **Sprint Backlog** para **Work In Progress**.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/2.1-lista-clientes
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/2.1-lista-clientes` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/2.1-lista-clientes'`.

### Passo 4 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 2.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 2.1. Eles estão na pasta `ctesp-ADC/fase-2/ficheiros/2.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 2.1 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/utilizadores.py`.

```bash
git add -A
git commit -m "feat(utilizadores): listar os utilizadores de um perfil"
```

**Deves ver** uma linha a terminar em `1 file changed, 15 insertions(+)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 2.1 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/gestao.py`.

```bash
git add -A
git commit -m "feat(gestao): listar as contas de um perfil com pesquisa por nome"
```

**Deves ver** uma linha a terminar em `1 file changed, 45 insertions(+)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 2.1 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/gestao.py`, `gestor_campanhas/cli/perfis.py`.

```bash
git add -A
git commit -m "feat(admin): mostrar a lista de clientes no menu do Administrador"
```

**Deves ver** uma linha a terminar em `2 files changed, 52 insertions(+), 1 deletion(-)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 2.1 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dados_demo.py`, `tests/test_autenticacao.py`.

```bash
git add -A
git commit -m "feat(demo): acrescentar dois clientes às contas de demonstração"
```

**Deves ver** uma linha a terminar em `2 files changed, 25 insertions(+), 6 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 2.1 5
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_gestao.py`.

```bash
git add -A
git commit -m "test(gestao): testar a lista de clientes e a pesquisa por nome"
```

**Deves ver** uma linha a terminar em `1 file changed, 124 insertions(+)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 2.1 6
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(gestao): documentar a lista de clientes"
```

**Deves ver** uma linha a terminar em `3 files changed, 41 insertions(+), 1 deletion(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 2.1
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 2.1` | `Tudo certo: o ramo 'feature/2.1-lista-clientes' está igual ao original no fim da unidade 2.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(gestao): documentar a lista de clientes
xxxxxxx test(gestao): testar a lista de clientes e a pesquisa por nome
xxxxxxx feat(demo): acrescentar dois clientes às contas de demonstração
xxxxxxx feat(admin): mostrar a lista de clientes no menu do Administrador
xxxxxxx feat(gestao): listar as contas de um perfil com pesquisa por nome
xxxxxxx feat(utilizadores): listar os utilizadores de um perfil
```

### Passo 6 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `120 passed`.

Cria os clientes de demonstração novos:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver** `Contas criadas: 2 (as restantes já existiam).` e a lista das contas, agora com três clientes. Se a tua pasta `dados` estava vazia, o número é `5`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`):

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Clientes` e a pergunta `Pesquisar por nome (Enter para ver todos)` |
| Enter | A tabela com os três clientes, por ordem alfabética (Beatriz, Carla, José), e `3 clientes.` |
| Enter | O menu do Administrador |
| `1`, depois `jose` | Só a linha de `José Padeiro` e `1 cliente.` |
| Enter, `1`, depois `zzz` | `Não há clientes com "zzz" no nome.` |

Sai com Enter, `0` e `0`.

Se não conseguires entrar como administrador, a password foi alterada num teste anterior. Fecha a aplicação, apaga a pasta `dados` e corre outra vez `python -m gestor_campanhas.dados_demo`.

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/2.1-lista-clientes
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/2.1-lista-clientes -> feature/2.1-lista-clientes`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/2.1-lista-clientes`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/2.1-lista-clientes**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Lista de clientes com pesquisa
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a poder consultar a lista de clientes, com pesquisa por nome.

- Listagem dos utilizadores de um perfil, no repositório
- Serviço novo de gestão de contas, com a pesquisa e a ordenação sem acentos
- Opção "Clientes" no menu do Administrador
- Mais dois clientes nas contas de demonstração

A coluna com o número de campanhas ativas fica para a Fase 3, quando existirem campanhas.

Closes #(número da issue A04)

## Como testar

1. `python -m pytest` (120 testes)
2. `python -m gestor_campanhas.dados_demo`, para criar os clientes novos
3. `python -m gestor_campanhas`, entrar como administrador e escolher "Clientes"
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move o card da story A04 para **Ready to Verify**.

### Passo 9 — Avisa Tomas

Diz a Tomas que o pull request da unidade 2.1 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 1 a 7.

### Passo 10 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/2.1-lista-clientes
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/2.1-lista-clientes` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 2.3 — Desativar e reativar clientes

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 11 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 2.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Desativar e reativar clientes**.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/2.3-desativar-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/2.3-desativar-cliente` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/2.3-desativar-cliente'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `175 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`) e escolhe `1` (Clientes). Aponta o número que está na primeira coluna da linha de `Beatriz Lopes`.

| Escreves | Deves ver |
|---|---|
| `4` e Enter | O título `Desativar ou reativar cliente` e a pergunta `Número do cliente (Enter para cancelar)` |
| O número de Beatriz Lopes | `Beatriz Lopes (beatriz@bicicletas.pt) tem a conta ativa.` e a pergunta `Desativar a conta? (s/n)` |
| `n` | `Nada foi alterado.` |
| Enter, `4`, o mesmo número, `s` | `Conta desativada.` |
| Enter | A tabela, com `Desativada` na linha de Beatriz Lopes |

Sai da gestão e termina a sessão com `0` e `0`. Agora tenta entrar com a conta desativada:

| Escreves | Deves ver |
|---|---|
| `1`, `beatriz@bicicletas.pt`, `beatriz12345` | `Esta conta está desativada. Fale com o administrador.` |

Carrega em Enter, entra outra vez como administrador e reativa a conta: `1`, `4`, o número de Beatriz Lopes, `s`. **Deves ver** `Conta reativada.` e, na tabela, `Ativa`.

Sai com Enter, `0`, `0` e `0`.

Confirma também:

- Na opção 4, escreve o número de um marketeer (por exemplo `2`): aparece `Não existe nenhum cliente com o número 2.`
- Depois de reativar a conta, entra com `beatriz@bicicletas.pt` / `beatriz12345`: abre o menu "Cliente".
- Na opção 4, carrega em Enter sem escrever um número: volta à lista sem alterar nada.

### Passo 14 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

### Passo 15 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move o card da story A07 para **Ready**.

### Passo 16 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/2.3-desativar-cliente
python ../ctesp-ADC/verificar.py 2.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/2.3-desativar-cliente` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 2.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 2.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 2.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 17 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Ricardo](ricardo.md)).

A vez seguinte é tua: continua no passo 18.

---

## Fazer a unidade 2.4 — Adicionar e editar marketeers

O Administrador ganha a opção "Marketeers", igual à dos clientes: lista, pesquisa, adicionar e editar. Em vez de copiar os ecrãs dos clientes, os ecrãs que já existem passam a servir para os dois perfis.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Desativar e reativar clientes** (unidade 2.3) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 2.4

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: A08, A09. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A08** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA08%5D%22

```markdown
- [ ] O menu do Administrador tem a opção "Marketeers", que mostra a lista dos marketeers com pesquisa por nome
- [ ] Por baixo da lista há a opção "Adicionar marketeer"
- [ ] São pedidos o nome e o email (obrigatórios) e o telefone (opcional); a empresa e o NIF não são pedidos
- [ ] As regras do email e do telefone são as mesmas dos clientes
- [ ] A conta é criada com uma password aleatória e o marketeer recebe as credenciais por email
- [ ] Com dados inválidos aparece a mensagem do erro e nada é criado
```

**Issue A09** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA09%5D%22

```markdown
- [ ] Por baixo da lista há a opção "Editar marketeer", que pede o número do marketeer
- [ ] É possível alterar o nome, o email e o telefone; com Enter, o valor mantém-se
- [ ] A password do marketeer não é alterada
- [ ] Com dados inválidos aparece a mensagem do erro e nenhum dado é alterado
- [ ] Com o número de um cliente aparece "Não existe nenhum marketeer com o número ..."
- [ ] O estado da conta é alterado na opção "Desativar ou reativar marketeer" (issue A10)
```

Por fim, no quadro Trello, move os cards das stories A08 e A09 de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/2.4-adicionar-editar-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/2.4-adicionar-editar-marketeer` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/2.4-adicionar-editar-marketeer'`.

### Passo 21 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 2.4 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 2.4. Eles estão na pasta `ctesp-ADC/fase-2/ficheiros/2.4/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.4 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/cli/gestao.py`.

```bash
git add -A
git commit -m "refactor(cli): preparar os ecrãs de gestão para mais do que um perfil"
```

**Deves ver** uma linha a terminar em `1 file changed, 129 insertions(+), 75 deletions(-)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.4 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/gestao.py`, `gestor_campanhas/cli/perfis.py`.

```bash
git add -A
git commit -m "feat(admin): listar, pesquisar, adicionar e editar marketeers"
```

**Deves ver** uma linha a terminar em `2 files changed, 15 insertions(+)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.4 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/dados_demo.py`.

```bash
git add -A
git commit -m "feat(demo): acrescentar um segundo marketeer às contas de demonstração"
```

**Deves ver** uma linha a terminar em `1 file changed, 8 insertions(+), 1 deletion(-)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.4 4
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_gestao.py`.

```bash
git add -A
git commit -m "test(gestao): testar a gestão de marketeers"
```

**Deves ver** uma linha a terminar em `1 file changed, 117 insertions(+)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.4 5
```

**Deves ver** `Copiados 1 ficheiro`: `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(gestao): documentar a gestão de marketeers"
```

**Deves ver** uma linha a terminar em `1 file changed, 25 insertions(+)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 2.4
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 2.4` | `Tudo certo: o ramo 'feature/2.4-adicionar-editar-marketeer' está igual ao original no fim da unidade 2.4.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(gestao): documentar a gestão de marketeers
xxxxxxx test(gestao): testar a gestão de marketeers
xxxxxxx feat(demo): acrescentar um segundo marketeer às contas de demonstração
xxxxxxx feat(admin): listar, pesquisar, adicionar e editar marketeers
xxxxxxx refactor(cli): preparar os ecrãs de gestão para mais do que um perfil
```

### Passo 23 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `187 passed`.

Cria o marketeer de demonstração novo:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver** `Contas criadas: 1 (as restantes já existiam).` e a lista das contas, agora com dois marketeers.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`). **Deves ver** o menu com `2. Marketeers`.

| Escreves | Deves ver |
|---|---|
| `2` e Enter | A tabela com `Marta Marques` e `Miguel Marketeer`, sem a coluna `Empresa`, e o menu `Gestão de marketeers` |
| `2` | O título `Adicionar marketeer` e a pergunta `Nome` |
| `Nuno Neves`, `nuno@agencia.pt`, Enter | `Marketeer criado com o número ...` e `As credenciais de acesso foram enviadas para nuno@agencia.pt.` |
| Enter | A tabela, agora com três marketeers |
| `3`, o número de Nuno Neves | `A editar Nuno Neves.` e a pergunta `Nome [Nuno Neves]` |
| Enter, Enter, `912345678` | `Dados guardados.` |
| Enter | A tabela, com o telefone na linha de Nuno Neves |
| `1`, depois `mar` | Só `Marta Marques` e `Miguel Marketeer` (os dois nomes têm "mar") |

Sai com `0`, `0` e `0`.

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/2.4-adicionar-editar-marketeer
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/2.4-adicionar-editar-marketeer -> feature/2.4-adicionar-editar-marketeer`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/2.4-adicionar-editar-marketeer`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/2.4-adicionar-editar-marketeer**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Adicionar e editar marketeers
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a poder ver a lista dos marketeers, adicionar marketeers e editar os dados deles.

- Os ecrãs de gestão deixam de ser só dos clientes: recebem o perfil e adaptam os textos, as colunas e as perguntas
- Opção "Marketeers" no menu do Administrador
- Mais um marketeer nas contas de demonstração

O serviço não precisou de alterações: já recebia o perfil desde a unidade 2.2.

Closes #(número da issue A08)
Closes #(número da issue A09)

## Como testar

1. `python -m pytest` (187 testes)
2. `python -m gestor_campanhas.dados_demo`, para criar o marketeer novo
3. `python -m gestor_campanhas`, entrar como administrador e escolher "Marketeers"
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories A08 e A09 para **Ready to Verify**.

### Passo 26 — Avisa Tomas

Diz a Tomas que o pull request da unidade 2.4 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 18 a 24.

### Passo 27 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/2.4-adicionar-editar-marketeer
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/2.4-adicionar-editar-marketeer` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Outras tarefas desta fase

### Passo 28 — Atualiza a página "Arquitetura" da wiki

A página ganha três secções: um exemplo que segue um pedido pelas camadas (adicionar um cliente), a validação dos dados e as contas desativadas.

Faz este passo depois de a unidade 2.5 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Arquitetura.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki/Arquitetura e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a Arquitetura para a versão 0.2.0` e clica em **Save page**.

**Deves ver** a página com as secções novas `Exemplo: adicionar um cliente`, `Validação dos dados` e `Contas desativadas`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 2.1 — Lista de clientes com pesquisa

- **`gestor_campanhas/repositorios/utilizadores.py`** ganha `listar_por_perfil`: um `SELECT` com `WHERE perfil = ?`, que devolve uma lista de objetos `Utilizador`. Devolve também as contas desativadas.
- **`gestor_campanhas/servicos/gestao.py`** é um módulo novo, com as regras da gestão de contas pelo Administrador. Nesta unidade tem duas funções.
  - `simplificar` tira os acentos e as maiúsculas de um texto. `unicodedata.normalize("NFD", texto)` separa cada letra do seu acento ("é" passa a "e" seguido do acento), e depois os acentos são deixados de fora. `casefold()` é uma versão mais forte de `lower()`.
  - `listar` vai buscar as contas do perfil, filtra as que têm o texto procurado no nome (comparando os dois textos já simplificados) e ordena-as.
- **Porque é que a ordenação não é feita no SQL.** O SQLite ordena pelas posições das letras na tabela de caracteres, onde "Á" vem depois de "z". Com `ORDER BY nome`, o "Álvaro" ficava no fim da lista. Ordenar em Python pelo nome simplificado resolve isso. Há um teste que apanhou este erro durante o desenvolvimento.
- **`gestor_campanhas/cli/gestao.py`** é o módulo dos ecrãs de gestão. `mostrar_clientes` transforma cada conta numa linha de textos e usa `comum.mostrar_tabela`, feita na Fase 1. `clientes` é a função da opção do menu: pergunta a pesquisa, chama o serviço e mostra o resultado.
- **`gestor_campanhas/cli/perfis.py`**: a opção "Clientes" é acrescentada no início da lista do Administrador, em `OPCOES`. As outras opções passam a ter o número seguinte.
- **`gestor_campanhas/dados_demo.py`** ganha dois clientes, um deles com acento no nome, para se poder experimentar a pesquisa. Os dois testes que contavam "3 contas" passaram a contar pelo tamanho da lista `CONTAS`, para não terem de ser alterados sempre que se acrescenta uma conta.
- **`tests/test_gestao.py`**: a fixture `clientes` cria três clientes com nomes escolhidos para testar a ordem e a pesquisa (um começa por "Á", outro está em minúsculas). O teste da pesquisa usa `parametrize`, que corre o mesmo teste com vários pares de pesquisa e resultado esperado.

### Unidade 2.4 — Adicionar e editar marketeers

- **O primeiro commit é um refactor.** Os ecrãs da gestão de clientes tinham a palavra "cliente" escrita em todo o lado. Em vez de os copiar para os marketeers (e ficar com dois sítios para corrigir de cada vez), as funções passaram a receber o perfil. Os 175 testes que já existiam passam sem alterações depois deste commit: é isso que mostra que nada se estragou.
- **`NOMES`**, em `gestor_campanhas/cli/gestao.py`, é um dicionário com o nome de cada perfil no singular e no plural. As mensagens são construídas com ele: `f"Adicionar {singular}"` dá "Adicionar cliente" ou "Adicionar marketeer".
- **`ACOES`** diz que opções de gestão cada perfil tem. Cada opção é um par com a descrição e a função a chamar. O menu é construído a partir desta lista, e a escolha do utilizador é convertida na posição da lista. É a mesma ideia de `OPCOES`, em `perfis.py`. Nesta unidade, os marketeers têm duas opções e os clientes três.
- **`mostrar_contas`** monta a tabela com todas as colunas e, se o perfil não for cliente, apaga a coluna da empresa dos cabeçalhos e de cada linha.
- **`pedir_conta`** junta o que `editar` e `alterar_estado` tinham repetido: pedir o número, procurar a conta e mostrar o erro se não existir.
- **`gerir`** é o ciclo que mostra a lista e o menu. `clientes` e `marketeers`, as funções chamadas pelo menu do Administrador, ficaram com uma linha cada: chamam `gerir` com o perfil.
- **O serviço não mudou.** As funções de `servicos/gestao.py` já recebiam o perfil, e `_dados_validados` já punha a empresa e o NIF vazios quando o perfil não é cliente. O teste `test_criar_marketeer_ignora_a_empresa_e_o_nif` confirma essa regra.
- **`gestor_campanhas/dados_demo.py`** ganha a marketeer `Marta Marques`, para a lista não ter só uma linha.
