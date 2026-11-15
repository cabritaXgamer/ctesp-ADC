# Fase 2 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 2 (Clientes e marketeers), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 2.1 (de Fabio) | Quando Fabio avisar |
| 8 a 17 | Fazer a unidade 2.2 — Adicionar e editar clientes | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 2.4 (de Fabio) | Quando Fabio avisar |
| 25 a 34 | Fazer a unidade 2.5 — Desativar e reativar marketeers | A seguir ao teu passo anterior |
| 35 a 43 | Preparar a release v0.2.0 | Quando Ricardo avisar |
| 44 a 48 | Publicar a release v0.2.0 e pedir o regresso ao develop | Quando Ricardo avisar |
| 49 | Atualiza a página inicial da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 2.1 — Lista de clientes com pesquisa

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 2.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Lista de clientes com pesquisa**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/2.1-lista-clientes
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/2.1-lista-clientes` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/2.1-lista-clientes'`.

Agora experimenta:

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

Confirma também:

- Pesquisa `JOSÉ`, `josé` e `jose`: as três encontram `José Padeiro`.
- Entra como marketeer (`marketeer@agencia.pt` / `marketeer12345`): o menu dele não tem a opção "Clientes".
- Na tabela, as colunas estão alinhadas.

### Passo 4 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

### Passo 5 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move o card da story A04 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/2.1-lista-clientes
python ../ctesp-ADC/verificar.py 2.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/2.1-lista-clientes` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 2.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 2.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 2.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 2.2 — Adicionar e editar clientes

A lista de clientes ganha um menu de gestão por baixo. O Administrador passa a poder adicionar um cliente, que recebe as credenciais por email, e editar os dados de um cliente que já existe.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Lista de clientes com pesquisa** (unidade 2.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 2.2

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: A05, A06. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A05** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA05%5D%22

```markdown
- [ ] Por baixo da lista de clientes há a opção "Adicionar cliente"
- [ ] São pedidos o nome e o email (obrigatórios) e o telefone, a empresa e o NIF (opcionais)
- [ ] O email tem de ter a forma `nome@empresa.pt` e não pode ser igual ao de outra conta, de qualquer perfil
- [ ] O telefone, se for indicado, tem 9 a 15 algarismos; o NIF, se for indicado, tem 9 algarismos
- [ ] A conta é criada com uma password aleatória, que o Administrador não vê
- [ ] O cliente recebe um email com o email e a password de acesso
- [ ] Com dados inválidos aparece a mensagem do erro e nada é criado
- [ ] O cliente novo aparece logo na lista
```

**Issue A06** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA06%5D%22

```markdown
- [ ] Por baixo da lista de clientes há a opção "Editar cliente", que pede o número do cliente
- [ ] Cada dado é mostrado com o valor atual; com Enter, o valor mantém-se
- [ ] É possível alterar o nome, o email, o telefone, a empresa e o NIF, com as mesmas regras de quando se adiciona
- [ ] A password do cliente não é alterada
- [ ] Com dados inválidos aparece a mensagem do erro e nenhum dado é alterado
- [ ] Com um número que não é de um cliente aparece "Não existe nenhum cliente com o número ..."
- [ ] O estado da conta é alterado na opção "Desativar ou reativar cliente" (issue A07)
```

Por fim, no quadro Trello, move os cards das stories A05 e A06 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/2.2-adicionar-editar-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/2.2-adicionar-editar-cliente` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/2.2-adicionar-editar-cliente'`.

### Passo 11 — Copia e grava os 7 commits

São 7 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 2.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 2.2. Eles estão na pasta `ctesp-ADC/fase-2/ficheiros/2.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 7**

```bash
python ../ctesp-ADC/copiar.py 2.2 1
```

**Deves ver** `Copiados 3 ficheiros`: `docs/referencia.rst`, `gestor_campanhas/servicos/contas.py`, `gestor_campanhas/servicos/validacao.py`.

```bash
git add -A
git commit -m "refactor(validacao): juntar num módulo as validações dos dados de uma conta"
```

**Deves ver** uma linha a terminar em `3 files changed, 81 insertions(+), 8 deletions(-)`.

**Commit 2 de 7**

```bash
python ../ctesp-ADC/copiar.py 2.2 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/utilizadores.py`.

```bash
git add -A
git commit -m "feat(utilizadores): atualizar o email de um utilizador"
```

**Deves ver** uma linha a terminar em `1 file changed, 14 insertions(+)`.

**Commit 3 de 7**

```bash
python ../ctesp-ADC/copiar.py 2.2 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/gestao.py`.

```bash
git add -A
git commit -m "feat(gestao): criar contas e enviar as credenciais por email"
```

**Deves ver** uma linha a terminar em `1 file changed, 77 insertions(+)`.

**Commit 4 de 7**

```bash
python ../ctesp-ADC/copiar.py 2.2 4
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/gestao.py`.

```bash
git add -A
git commit -m "feat(gestao): editar os dados de uma conta"
```

**Deves ver** uma linha a terminar em `1 file changed, 50 insertions(+)`.

**Commit 5 de 7**

```bash
python ../ctesp-ADC/copiar.py 2.2 5
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/comum.py`, `gestor_campanhas/cli/gestao.py`, `tests/test_gestao.py`.

```bash
git add -A
git commit -m "feat(admin): adicionar e editar clientes a partir da lista"
```

**Deves ver** uma linha a terminar em `3 files changed, 111 insertions(+), 18 deletions(-)`.

**Commit 6 de 7**

```bash
python ../ctesp-ADC/copiar.py 2.2 6
```

**Deves ver** `Copiados 2 ficheiros`: `tests/test_gestao.py`, `tests/test_validacao.py`.

```bash
git add -A
git commit -m "test(gestao): testar a criação e a edição de clientes e as validações"
```

**Deves ver** uma linha a terminar em `2 files changed, 265 insertions(+), 3 deletions(-)`.

**Commit 7 de 7**

```bash
python ../ctesp-ADC/copiar.py 2.2 7
```

**Deves ver** `Copiados 1 ficheiro`: `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(gestao): documentar como adicionar e editar clientes"
```

**Deves ver** uma linha a terminar em `1 file changed, 49 insertions(+), 4 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 2.2
git log --oneline -7
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 2.2` | `Tudo certo: o ramo 'feature/2.2-adicionar-editar-cliente' está igual ao original no fim da unidade 2.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -7` | Os teus 7 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(gestao): documentar como adicionar e editar clientes
xxxxxxx test(gestao): testar a criação e a edição de clientes e as validações
xxxxxxx feat(admin): adicionar e editar clientes a partir da lista
xxxxxxx feat(gestao): editar os dados de uma conta
xxxxxxx feat(gestao): criar contas e enviar as credenciais por email
xxxxxxx feat(utilizadores): atualizar o email de um utilizador
xxxxxxx refactor(validacao): juntar num módulo as validações dos dados de uma conta
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `166 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`) e escolhe `1` (Clientes). **Deves ver** a tabela dos clientes e, por baixo, o menu `Gestão de clientes`.

Adiciona um cliente:

| Escreves | Deves ver |
|---|---|
| `2` e Enter | O título `Adicionar cliente` e a pergunta `Nome` |
| `Rita Reis` | A pergunta `Email` |
| `rita@loja.pt` | A pergunta `Telefone (opcional)` |
| Enter | A pergunta `Empresa (opcional)` |
| `Loja da Rita` | A pergunta `NIF (opcional)` |
| Enter | `Cliente criado com o número ...` e `As credenciais de acesso foram enviadas para rita@loja.pt.` |
| Enter | A tabela outra vez, agora com a linha de `Rita Reis` |

Aponta o número que aparece na primeira coluna da linha de `Rita Reis`. Agora edita esse cliente:

| Escreves | Deves ver |
|---|---|
| `3` e Enter | O título `Editar cliente` e a pergunta `Número do cliente (Enter para cancelar)` |
| O número de Rita Reis | `A editar Rita Reis.` e a pergunta `Nome [Rita Reis]` |
| Enter | A pergunta `Email [rita@loja.pt]` |
| Enter | A pergunta `Telefone []` |
| `912345678` | A pergunta `Empresa [Loja da Rita]` |
| Enter | A pergunta `NIF []` |
| Enter | `Dados guardados.` |
| Enter | A tabela, com o telefone `912345678` na linha de Rita Reis |

Sai com `0`, `0` e `0`.

Por fim, vê o email com as credenciais:

```bash
ls dados/caixa_saida
```

**Deves ver** um ficheiro cujo nome acaba em `rita_loja.pt.txt`. Abre-o no VS Code ou no Bloco de Notas: tem o email e a password da conta nova.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/2.2-adicionar-editar-cliente
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/2.2-adicionar-editar-cliente -> feature/2.2-adicionar-editar-cliente`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/2.2-adicionar-editar-cliente`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/2.2-adicionar-editar-cliente**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Adicionar e editar clientes
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a poder adicionar clientes e editar os dados deles, a partir da lista de clientes.

- Módulo novo com as validações do nome, do email, do telefone e do NIF, usado também na edição dos próprios dados
- Criação de contas com password aleatória e envio das credenciais por email
- Edição dos dados de uma conta, incluindo o email
- A opção "Clientes" passa a mostrar a lista com um menu de gestão por baixo

Closes #(número da issue A05)
Closes #(número da issue A06)

## Como testar

1. `python -m pytest` (166 testes)
2. `python -m gestor_campanhas`, entrar como administrador e escolher "Clientes"
3. Adicionar um cliente e abrir o email na pasta `dados/caixa_saida`
4. Editar esse cliente
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories A05 e A06 para **Ready to Verify**.

### Passo 16 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 2.2 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 1 a 7.

### Passo 17 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/2.2-adicionar-editar-cliente
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/2.2-adicionar-editar-cliente` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 2.4 — Adicionar e editar marketeers

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 2.4 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Adicionar e editar marketeers**.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/2.4-adicionar-editar-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/2.4-adicionar-editar-marketeer` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/2.4-adicionar-editar-marketeer'`.

Agora experimenta:

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

Confirma também:

- Na gestão de marketeers, as perguntas "Empresa" e "NIF" não aparecem, nem ao adicionar nem ao editar.
- Na opção "Editar marketeer", escreve o número de um cliente: aparece `Não existe nenhum marketeer com o número ...`
- A opção "Clientes" continua a funcionar como antes: lista com a coluna `Empresa` e quatro opções de gestão.
- O menu de gestão de marketeers ainda não tem a opção de desativar. Entra na unidade 2.5.

### Passo 21 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

### Passo 22 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move os cards das stories A08 e A09 para **Ready**.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/2.4-adicionar-editar-marketeer
python ../ctesp-ADC/verificar.py 2.4
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/2.4-adicionar-editar-marketeer` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 2.4` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 2.4 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 2.4.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 25.

---

## Fazer a unidade 2.5 — Desativar e reativar marketeers

O Administrador passa a poder desativar e reativar marketeers. Além disso, quem tem a conta desativada ou reativada, seja cliente ou marketeer, passa a ser avisado por email.

### Passo 25 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Adicionar e editar marketeers** (unidade 2.4) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 26 — Fica com as issues da unidade 2.5

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: A10. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A10** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA10%5D%22

```markdown
- [ ] Por baixo da lista de marketeers há a opção "Desativar ou reativar marketeer", que pede o número do marketeer
- [ ] São mostrados o nome, o email e o estado atual da conta, e é pedida uma confirmação (s/n)
- [ ] Um marketeer com a conta desativada não consegue entrar
- [ ] A conta desativada continua na lista, com o estado "Desativada"
- [ ] As sessões que o marketeer já fez continuam a aparecer nos horários de entrada e saída
- [ ] A mesma opção reativa a conta
- [ ] A pessoa recebe um email quando a conta é desativada e quando é reativada (clientes e marketeers)
- [ ] A reatribuição das campanhas do marketeer antes da desativação entra na Fase 3, quando existirem campanhas
```

Por fim, no quadro Trello, move o card da story A10 de **Sprint Backlog** para **Work In Progress**.

### Passo 27 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/2.5-desativar-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/2.5-desativar-marketeer` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/2.5-desativar-marketeer'`.

### Passo 28 — Copia e grava os 4 commits

São 4 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 2.5 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 2.5. Eles estão na pasta `ctesp-ADC/fase-2/ficheiros/2.5/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 4**

```bash
python ../ctesp-ADC/copiar.py 2.5 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/cli/gestao.py`.

```bash
git add -A
git commit -m "feat(admin): desativar e reativar marketeers, com confirmação"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+)`.

**Commit 2 de 4**

```bash
python ../ctesp-ADC/copiar.py 2.5 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/gestao.py`, `gestor_campanhas/servicos/gestao.py`.

```bash
git add -A
git commit -m "feat(gestao): avisar por email quem tem a conta desativada ou reativada"
```

**Deves ver** uma linha a terminar em `2 files changed, 14 insertions(+), 2 deletions(-)`.

**Commit 3 de 4**

```bash
python ../ctesp-ADC/copiar.py 2.5 3
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_gestao.py`.

```bash
git add -A
git commit -m "test(gestao): testar a desativação de marketeers e os avisos por email"
```

**Deves ver** uma linha a terminar em `1 file changed, 81 insertions(+), 1 deletion(-)`.

**Commit 4 de 4**

```bash
python ../ctesp-ADC/copiar.py 2.5 4
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(gestao): documentar a desativação de marketeers e as contas desativadas"
```

**Deves ver** uma linha a terminar em `2 files changed, 35 insertions(+)`.


### Passo 29 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 2.5
git log --oneline -4
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 2.5` | `Tudo certo: o ramo 'feature/2.5-desativar-marketeer' está igual ao original no fim da unidade 2.5.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -4` | Os teus 4 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(gestao): documentar a desativação de marketeers e as contas desativadas
xxxxxxx test(gestao): testar a desativação de marketeers e os avisos por email
xxxxxxx feat(gestao): avisar por email quem tem a conta desativada ou reativada
xxxxxxx feat(admin): desativar e reativar marketeers, com confirmação
```

### Passo 30 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `194 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`) e escolhe `2` (Marketeers). **Deves ver**, no menu de gestão, `4. Desativar ou reativar marketeer`. Aponta o número de `Marta Marques`.

| Escreves | Deves ver |
|---|---|
| `4` e Enter | O título `Desativar ou reativar marketeer` e a pergunta do número |
| O número de Marta Marques | `Marta Marques (marta@agencia.pt) tem a conta ativa.` e a pergunta `Desativar a conta? (s/n)` |
| `s` | `Conta desativada.` e `Foi enviado um aviso para marta@agencia.pt.` |
| Enter | A tabela, com `Desativada` na linha de Marta Marques |

Sai da gestão e termina a sessão com `0` e `0`. Tenta entrar com a conta desativada:

| Escreves | Deves ver |
|---|---|
| `1`, `marta@agencia.pt`, `marta12345` | `Esta conta está desativada. Fale com o administrador.` |

Carrega em Enter, entra outra vez como administrador e reativa a conta: `2`, `4`, o número de Marta Marques, `s`. **Deves ver** `Conta reativada.`

Sai com Enter, `0`, `0` e `0`. Por fim, vê os emails:

```bash
ls dados/caixa_saida
```

**Deves ver** dois ficheiros com `marta_agencia.pt` no nome. Um tem o assunto `A sua conta foi desativada` e o outro `A sua conta foi reativada`.

### Passo 31 — Envia o ramo para o GitHub

```bash
git push -u origin feature/2.5-desativar-marketeer
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/2.5-desativar-marketeer -> feature/2.5-desativar-marketeer`.

### Passo 32 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/2.5-desativar-marketeer`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/2.5-desativar-marketeer**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Desativar e reativar marketeers
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a poder desativar e reativar a conta de um marketeer. Quem tem a conta desativada ou reativada é avisado por email.

- Opção "Desativar ou reativar marketeer" no menu de gestão de marketeers
- Email de aviso em `definir_estado`, para clientes e marketeers
- Documentação: exemplo das camadas ao adicionar um cliente e secção sobre contas desativadas

A verificação das campanhas por reatribuir fica para a Fase 3, quando existirem campanhas.

Closes #(número da issue A10)

## Como testar

1. `python -m pytest` (194 testes)
2. `python -m gestor_campanhas`, entrar como administrador e escolher "Marketeers"
3. Desativar um marketeer e ver o email na pasta `dados/caixa_saida`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move o card da story A10 para **Ready to Verify**.

### Passo 33 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 2.5 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 18 a 24.

### Passo 34 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/2.5-desativar-marketeer
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/2.5-desativar-marketeer` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Preparar a release v0.2.0

Fecha a fase com a versão 0.2.0: o número da versão sobe, o registo de alterações ganha a secção desta versão e o README é atualizado. Esta unidade vai para o `main`, e não para o `develop`.

### Passo 35 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Desativar e reativar marketeers** (unidade 2.5) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 36 — Cria a issue da unidade 2.6

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[2.6] Release v0.2.0
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Publicar a versão 0.2.0, com as user stories da Fase 2 (gestão de clientes e marketeers).

## O que inclui

- [ ] Versão 0.2.0 em `gestor_campanhas/__init__.py`
- [ ] Registo de alterações (`CHANGELOG.md`)
- [ ] README atualizado
- [ ] Pull request para `main`
- [ ] Tag e release `v0.2.0` no GitHub
- [ ] `main` de volta ao `develop`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 37 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c release/v0.2.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c release/v0.2.0` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'release/v0.2.0'`.

### Passo 38 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 2.6 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 2.6. Eles estão na pasta `ctesp-ADC/fase-2/ficheiros/2.6/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 2.6 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__init__.py`.

```bash
git add -A
git commit -m "chore(release): passar a versão para 0.2.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 2.6 2
```

**Deves ver** `Copiados 1 ficheiro`: `CHANGELOG.md`.

```bash
git add -A
git commit -m "docs(release): registar as alterações da versão 0.2.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 23 insertions(+)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 2.6 3
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(release): atualizar o README para a versão 0.2.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 13 insertions(+), 3 deletions(-)`.


### Passo 39 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 2.6
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 2.6` | `Tudo certo: o ramo 'release/v0.2.0' está igual ao original no fim da unidade 2.6.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(release): atualizar o README para a versão 0.2.0
xxxxxxx docs(release): registar as alterações da versão 0.2.0
xxxxxxx chore(release): passar a versão para 0.2.0
```

### Passo 40 — Experimenta o que gravaste

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `194 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v0.2.0`. Sai com `0`.

### Passo 41 — Envia o ramo para o GitHub

```bash
git push -u origin release/v0.2.0
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      release/v0.2.0 -> release/v0.2.0`.

### Passo 42 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `main`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `release/v0.2.0`.

**b)** No topo, a base tem de ser `main`, e não `develop`. Clica em **base: develop**, escolhe `main` e confirma que fica **base: main** e **compare: release/v0.2.0**. Uma release vai para o `main`, que é o ramo das versões entregues.

**c)** No título, cola:

```text
Release v0.2.0
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Não é preciso trocar nada:

```markdown
## O que muda

Prepara a versão 0.2.0.

- Versão passa de 0.1.0 para 0.2.0
- `CHANGELOG.md` com a secção da versão 0.2.0
- README atualizado: tabela de versões, contas de demonstração e secção sobre clientes e marketeers

Este pull request vai para o `main`. A issue da release é fechada pelo pull request que leva a release de volta ao `develop`.

## Como testar

1. `python -m pytest` (194 testes)
2. `python -m sphinx -W -b html docs docs/_build/html`
3. `python -m gestor_campanhas`: o título mostra `v0.2.0`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** Confirma o destino. Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.2.0`. Se disser `into develop`, **não avises ninguém ainda**: clica em **Edit**, à direita do título, clica em **base: develop**, escolhe `main`, confirma em **Change base** e clica em **Save**.

### Passo 43 — Avisa Ricardo

Diz a Ricardo que o pull request da release v0.2.0 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 25 a 32.

---

## Publicar a release v0.2.0 e pedir o regresso ao develop

Com a release no `main`, falta marcá-la com uma tag e levar os commits dela de volta ao `develop`.

### Passo 44 — Publica a release v0.2.0 no GitHub

Faz este passo quando Ricardo te avisar que a release está no `main`.

Publicar a release cria a **tag**, uma etiqueta que marca para sempre o commit desta versão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/releases/new

**b)** Clica em **Choose a tag**, escreve `v0.2.0` e clica em **Create new tag: v0.2.0 on publish**.

**c)** Em **Target**, escolhe `main`.

**d)** Em **Release title**, cola:

```text
v0.2.0 — Clientes e marketeers
```

**e)** Na caixa de texto, cola:

````markdown
## Clientes e marketeers

O Administrador passa a gerir as contas dos clientes e dos marketeers.

### Acrescentado

- Lista de clientes, por ordem alfabética, com pesquisa por nome que não distingue maiúsculas nem acentos
- Adicionar clientes: a conta começa com uma password aleatória e as credenciais são enviadas por email
- Editar os dados de um cliente: nome, email, telefone, empresa e NIF
- Desativar e reativar clientes, com pedido de confirmação
- Lista de marketeers, com as mesmas opções: pesquisar, adicionar, editar, desativar e reativar
- Aviso por email a quem tem a conta desativada ou reativada
- Mais contas de demonstração: três clientes e dois marketeers

### User stories

A04, A05, A06, A07, A08, A09 e A10.

O número de campanhas ativas na lista de clientes (A04) e a reatribuição das campanhas antes de desativar um marketeer (A10) entram na versão 0.3.0, com as campanhas.

### Como experimentar

```
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

Entrar com `admin@agencia.pt` / `admin12345` e escolher "Clientes" ou "Marketeers".
````

**f)** Clica em **Publish release**.

**Deves ver** a página da release, e a tag `v0.2.0` em https://github.com/Blive77/ADC-TrabGrupo/tags. Na linha da tag aparece o commit `Merge pull request ... from .../release/v0.2.0`. Se aparecer outro commit, o **Target** ficou errado: avisa o grupo antes de continuar.

### Passo 45 — Abre o pull request que leva a release para o develop

A release está no `main`, mas o `develop` ainda não tem os commits dela (a versão nova e o registo de alterações). Este pull request leva-os para lá, para os dois ramos ficarem alinhados.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/compare/develop...main

**b)** Confirma, no topo, que está **base: develop** e **compare: main**, e clica em **Create pull request**.

**c)** No título, cola:

```text
Juntar a release v0.2.0 ao develop
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue da release, que apontaste no início:

```markdown
## O que muda

Traz para o `develop` os commits da release v0.2.0, que já estão no `main`: a versão nova, o registo de alterações e o README.

Closes #N
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**f)** Clica em **Create pull request**.

### Passo 46 — Avisa Ricardo

Diz a Ricardo que o pull request que leva a release v0.2.0 para o `develop` está aberto. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 33 a 36.

### Passo 47 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d release/v0.2.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d release/v0.2.0` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

### Passo 48 — Fecha a milestone da fase

Faz este passo depois de Ricardo juntar o último pull request. Nessa altura a issue da release já está fechada, e a milestone fica com todas as issues fechadas.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/milestones

**b)** Na linha `Fase 2 — Clientes e marketeers`, confirma que a barra está a 100% e clica em **Close**.

Se a barra não estiver a 100%, clica no nome da milestone para ver que issues estão abertas e avisa o grupo.

---

## Outras tarefas desta fase

### Passo 49 — Atualiza a página inicial da wiki

A página inicial passa a indicar a versão 0.2.0.

Faz este passo no fim da fase, depois de publicares a release.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 0.2.0` e clica em **Save page**.

**Deves ver** a linha `Versão atual: v0.2.0 (Fase 2 — Clientes e marketeers).`

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 2.2 — Adicionar e editar clientes

- **`gestor_campanhas/servicos/validacao.py`** é um módulo novo. Cada função (`nome`, `email`, `telefone`, `nif`) recebe o valor como foi escrito, devolve-o arrumado e lança `ErroValidacao` se não respeitar as regras. O email é verificado com uma expressão regular simples: texto, `@`, texto, ponto, texto, sem espaços.
- **`gestor_campanhas/servicos/contas.py`** passou a usar essas funções. Antes, as regras do nome, do telefone e do NIF estavam escritas dentro de `atualizar_dados`. O primeiro commit é um *refactor*: muda a organização do código sem mudar o que ele faz, e por isso os 120 testes que já existiam continuam a passar sem alterações.
- **`gestor_campanhas/repositorios/utilizadores.py`** ganha `atualizar_email`. Estava de fora porque o próprio utilizador não pode mudar o seu email; o Administrador pode.
- **`gestor_campanhas/servicos/gestao.py`** ganha quatro funções.
  - `gerar_password_inicial` usa `secrets.token_urlsafe(9)`, que devolve 12 caracteres aleatórios. O módulo `secrets` serve para valores que não podem ser adivinhados; o `random` não serve para isso.
  - `criar` valida os dados, confirma que o email ainda não existe, cria a conta com o hash da password e envia o email. A password só existe dentro desta função e no email: não é devolvida nem mostrada no ecrã.
  - `obter` procura uma conta pelo número e confirma que é do perfil pedido. É o que impede editar um marketeer a partir da lista dos clientes.
  - `editar` valida tudo antes de guardar. Se um valor estiver errado, o erro é lançado antes do primeiro `UPDATE`, por isso nunca fica metade dos dados alterada.
- **A constante `PERFIS_GERIDOS`** diz que perfis o Administrador pode gerir: clientes e marketeers. Pedir para criar um administrador dá `ValueError`, que é um erro de programação e não uma mensagem para o utilizador.
- **`gestor_campanhas/cli/comum.py`** ganha `ler_numero`, que só aceita algarismos e devolve `None` com Enter, para se poder cancelar.
- **`gestor_campanhas/cli/gestao.py`**: a função `clientes` passa a ser um ciclo. Mostra a lista, mostra o menu e, depois de cada opção, volta ao início e mostra a lista outra vez, já atualizada. Os quatro testes do ecrã que vinham da unidade 2.1 foram ajustados, porque a pesquisa deixou de ser a primeira pergunta e passou a ser a opção 1.
- **`tests/test_validacao.py`** testa as validações sozinhas. **`tests/test_gestao.py`** lê a password do ficheiro do email com uma expressão regular e usa-a para entrar: é a prova de que a password enviada é a que ficou guardada.

### Unidade 2.5 — Desativar e reativar marketeers

- **O primeiro commit tem uma linha.** Em `ACOES`, a lista dos marketeers ganha o par `("Desativar ou reativar", alterar_estado)`. A função já existia e já recebia o perfil; o serviço também já aceitava marketeers. Foi para isto que a unidade 2.4 reorganizou os ecrãs: acrescentar uma opção a um perfil passou a ser acrescentar uma linha a uma lista.
- **`gestor_campanhas/servicos/gestao.py`**: `definir_estado` passa a enviar um email depois de alterar o estado. O email só é enviado se a alteração for feita: quando a função lança um erro (por exemplo, a conta já está desativada), a execução para antes de chegar a `correio.enviar`. O teste `test_alteracao_recusada_nao_envia_email` confirma isso.
- **Os testes dos emails não dependem da ordem dos ficheiros.** Os dois avisos podem ser criados no mesmo segundo, e nesse caso a ordem alfabética dos nomes dos ficheiros não é a ordem em que foram escritos. Por isso o teste verifica que existem dois emails, um com cada assunto, sem assumir qual vem primeiro.
- **`gestor_campanhas/cli/gestao.py`** mostra mais uma linha depois de alterar o estado: `Foi enviado um aviso para ...`.
- **Os horários não se perdem.** Como a conta é desativada e não apagada, as linhas da tabela `sessoes` continuam ligadas a um utilizador que existe. O teste `test_marketeer_desativado_continua_nos_horarios` regista uma sessão, desativa o marketeer e confirma que a sessão continua a aparecer.
- **`docs/arquitetura.rst`** ganha duas secções: um exemplo que segue um pedido pelas camadas (adicionar um cliente) e a explicação de porque é que as contas são desativadas em vez de apagadas.
- **O que fica para a Fase 3.** A descrição da A10 diz que as campanhas do marketeer têm de ser reatribuídas antes da remoção. Ainda não há campanhas, por isso não há nada para verificar. Quando houver, a regra entra em `definir_estado`, que é o único sítio por onde passa a desativação.

### Unidade 2.6 — Release v0.2.0

- **`gestor_campanhas/__init__.py`**: `__version__` passa para `"0.2.0"`. O menu inicial, o `pyproject.toml` e a documentação leem a versão daqui.
- **`CHANGELOG.md`** ganha a secção `v0.2.0`, por cima da anterior: a versão mais recente fica sempre em primeiro. Tem três partes: o que foi acrescentado, o que foi alterado em coisas que já existiam, e as user stories concluídas.
- **`README.md`**: a tabela de versões ganha uma linha, o exemplo do menu passa a mostrar `v0.2.0`, a tabela das contas de demonstração tem as seis contas e há uma secção nova sobre a gestão de clientes e marketeers.
- **O caminho de uma release.** São quatro momentos, sempre pela mesma ordem: o pull request do ramo `release/v0.2.0` para o `main`; a publicação da release, que cria a tag no `main`; o pull request do `main` para o `develop`; e o fecho da milestone.
- **O que correu mal na Fase 1.** O GitHub propõe sempre o ramo por omissão como destino de um pull request, e neste repositório é o `develop`. O pull request da release ficou com esse destino e foi junto ao `develop`. O `main` ficou sem a versão, e a tag, criada a seguir no `main`, ficou a marcar um commit sem código. Corrigiu-se com um pull request do `develop` para o `main` e refazendo a tag. Nesta fase há dois passos de confirmação do destino para isso não se repetir.
- **Porque é que a tag tem de estar no `main`.** A tag é o que diz "a versão 0.2.0 é exatamente este commit". Quem descarregar a versão pela página das releases recebe o código desse commit. Se a tag estiver no sítio errado, recebe outra coisa.
