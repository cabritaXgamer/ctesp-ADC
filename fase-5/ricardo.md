# Fase 5 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 5 (Budget), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 5.1 (de Tomas) | Quando Tomas avisar |
| 8 a 17 | Fazer a unidade 5.2 — Parecer do marketeer sobre os pedidos de budget | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 5.4 (de Tomas) | Quando Tomas avisar |
| 25 | Atualiza a página "Arquitetura" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 5.1 — Pedido de alteração de budget

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 5.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Pedido de alteração de budget**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 1 linha `Closes #` seguida de um número, uma por issue (C15), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Tomas para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/5.1-pedido-alteracao-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/5.1-pedido-alteracao-budget` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/5.1-pedido-alteracao-budget'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `620 passed`.

Cria o pedido de budget de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver**, entre as outras linhas, `Pedidos de alteração de budget criados: 1 (os restantes já existiam).` Se aparecer `0`, já tinhas corrido este comando com o código desta unidade, e o pedido já existe.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como cliente (`1`, depois `cliente@empresa.pt` e `cliente12345`) e escolhe `1` (Pedidos de campanha).

**Deves ver** duas listas. A primeira, `Pedidos de nova campanha`, diz `Nenhum.` (a Carla não tem pedidos de campanha). A segunda tem o pedido de demonstração:

```text
Pedidos de alteração de budget

N.º  Feito em    Campanha    De          Para        Estado
---  ----------  ----------  ----------  ----------  --------
1    2026-11-18  Natal 2026  1 500,00 €  2 000,00 €  Pendente

1 pedido de alteração de budget.
```

A data é a do dia em que correste o `dados_demo`. Por baixo, o menu tem seis opções, de `1. Novo pedido de campanha` a `6. Cancelar pedido de budget`.

| Escreves | Deves ver |
|---|---|
| `4` e Enter | O título `Pedir alteração de budget`, uma tabela com a linha `Natal 2026  1 500,00 €  Por começar` e a pergunta `Número da campanha (Enter para cancelar)` |
| O número da campanha `Natal 2026` (primeira coluna) | `A campanha Natal 2026 já tem um pedido de alteração de budget por decidir (n.º 1).` A aplicação não chega a pedir o valor |
| Enter | As duas listas outra vez |
| `5` e Enter | O título `Ver pedido de budget` e a pergunta `Número do pedido de budget (Enter para cancelar)` |
| `1` | Os dados do pedido, com `Budget de:    1 500,00 €`, `Budget para:  2 000,00 €`, `Motivo:       Reforçar os anúncios em vídeo na última semana antes do Natal` e `Estado:       Pendente` |
| Enter, `0` e `2` | A lista das campanhas da Carla e, por baixo, a frase nova `Para pedir outro valor, use a opção "Pedidos de campanha".` |

Sai com `0` e `0`. Agora entra como a cliente Beatriz (`1`, `beatriz@bicicletas.pt` e `beatriz12345`), que tem uma campanha sem budget, e escolhe `1`.

| Escreves | Deves ver |
|---|---|
| `4` e Enter | A tabela com a linha `Bicicletas de primavera  Por definir  Em curso` |
| O número da campanha `Bicicletas de primavera` | `Budget atual da campanha Bicicletas de primavera: Por definir.` e a pergunta `Budget pretendido em euros (por exemplo 2000 ou 2000,50)` |
| `900` | A pergunta `Motivo do pedido` |
| `Começar a campanha` | `Pedido registado com o número ...` e `Fica pendente até o marketeer dar o parecer e o administrador o decidir.` |
| Enter | Na segunda lista, a linha `Bicicletas de primavera  Por definir  900,00 €  Pendente` |

Aponta o número do pedido da Beatriz (primeira coluna). Agora cancela-o:

| Escreves | Deves ver |
|---|---|
| `6` e Enter | O título `Cancelar pedido de budget` e a pergunta do número |
| O número do pedido da Beatriz | Os dados do pedido e a pergunta `Cancelar este pedido? (s/n)` |
| `s` | `Pedido cancelado.` |
| Enter | O pedido continua na lista, com o estado `Cancelado` |

Sai com `0` e `0`. Um pedido cancelado não se apaga, por isso fica nos teus dados; nas unidades seguintes vais vê-lo nas listas, com o estado `Cancelado`.

Confirma também:

- Entra como `beatriz@bicicletas.pt` / `beatriz12345`, escolhe `1` e depois `4` e o número da `Bicicletas de primavera`. No valor escreve `0` e no motivo `Teste`: aparece `O budget tem de ser maior do que zero. O pedido não foi registado.`
- Ainda como Beatriz, `4`, a mesma campanha, `500` e, no motivo, só Enter: aparece `Este campo é obrigatório.` e o motivo é pedido outra vez. Escreve `Teste`: o pedido fica registado. Cancela-o logo: `6`, o número dele e `s`.
- Entra como `jose@padaria.pt` / `jose12345`, escolhe `1` e depois `4`: aparece `Não tem campanhas a decorrer ou por começar.`, porque a campanha `Regresso às aulas` já terminou.
- Ainda como José, escolhe `5` e escreve `1` (o pedido de budget da Carla): aparece `Não tem nenhum pedido de budget com o número 1.`
- Entra como `cliente@empresa.pt` / `cliente12345`, escolhe `1` e depois `2` (Ver pedido de campanha): a opção continua a funcionar como antes, para os pedidos de nova campanha.

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

**f)** No Trello, move o card da story C15 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/5.1-pedido-alteracao-budget
python ../ctesp-ADC/verificar.py 5.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/5.1-pedido-alteracao-budget` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 5.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 5.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 5.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 5.2 — Parecer do marketeer sobre os pedidos de budget

O Marketeer ganha a opção "Pedidos de budget", com os pedidos de alteração de budget das campanhas de que é responsável. Em cada um, diz se é viável e porquê. Com o parecer, o pedido passa a "Em análise", à espera da decisão do Administrador, e o cliente deixa de o poder cancelar.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Pedido de alteração de budget** (unidade 5.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 5.2

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: M16. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue M16** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM16%5D%22

```markdown
- [ ] O menu do Marketeer tem a opção "Pedidos de budget", a seguir a "Criativos"
- [ ] A lista mostra só os pedidos das campanhas de que o marketeer é responsável, com o cliente, o budget de partida, o budget pedido, o estado e o parecer; os que estão por decidir aparecem primeiro
- [ ] "Dar parecer" mostra o pedido, com o motivo do cliente e a despesa atual da campanha
- [ ] O parecer é "viável" ou "não viável" (`s`/`n`), com uma justificação obrigatória
- [ ] Com o parecer, o pedido passa a `Em análise` e o cliente já não o pode cancelar
- [ ] Enquanto o pedido não for decidido, o marketeer pode dar outro parecer, que substitui o anterior
- [ ] Um pedido aprovado, rejeitado ou cancelado já não aceita parecer
- [ ] Se a campanha mudar de marketeer, os pedidos dela passam para o marketeer novo
- [ ] O parecer fica visível para o Administrador (a lista do Administrador entra na issue A14)
```

Por fim, no quadro Trello, move o card da story M16 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/5.2-parecer-do-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/5.2-parecer-do-marketeer` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/5.2-parecer-do-marketeer'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/5.2-parecer-do-marketeer' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/5.2-parecer-do-marketeer
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/5.2-parecer-do-marketeer
git switch -c feature/5.2-parecer-do-marketeer
```

  **Deves ver** `Deleted branch feature/5.2-parecer-do-marketeer (was ...)` e depois `Switched to a new branch 'feature/5.2-parecer-do-marketeer'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/5.2-parecer-do-marketeer` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 4 commits

São 4 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 5.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 5.2. Eles estão na pasta `ctesp-ADC/fase-5/ficheiros/5.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 4**

```bash
python ../ctesp-ADC/copiar.py 5.2 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/pedidos_budget.py`, `tests/test_budget.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar o parecer do marketeer"
```

**Deves ver** uma linha a terminar em `2 files changed, 64 insertions(+)`.

**Commit 2 de 4**

```bash
python ../ctesp-ADC/copiar.py 5.2 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/budget.py`, `tests/test_budget.py`.

```bash
git add -A
git commit -m "feat(budget): dar parecer sobre um pedido de alteração de budget"
```

**Deves ver** uma linha a terminar em `2 files changed, 136 insertions(+)`.

**Commit 3 de 4**

```bash
python ../ctesp-ADC/copiar.py 5.2 3
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/budget.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_budget.py`.

```bash
git add -A
git commit -m "feat(cli): pedidos de budget e parecer no menu do marketeer"
```

**Deves ver** uma linha a terminar em `3 files changed, 199 insertions(+), 3 deletions(-)`.

**Commit 4 de 4**

```bash
python ../ctesp-ADC/copiar.py 5.2 4
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar o parecer do marketeer sobre os pedidos de budget"
```

**Deves ver** uma linha a terminar em `2 files changed, 67 insertions(+), 3 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 5.2
git log --oneline -4
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 5.2` | `Tudo certo: o ramo 'feature/5.2-parecer-do-marketeer' está igual ao original no fim da unidade 5.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -4` | Os teus 4 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar o parecer do marketeer sobre os pedidos de budget
xxxxxxx feat(cli): pedidos de budget e parecer no menu do marketeer
xxxxxxx feat(budget): dar parecer sobre um pedido de alteração de budget
xxxxxxx feat(repositorios): guardar o parecer do marketeer
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `640 passed`.

Garante que tens o pedido de budget de demonstração (se já existir, aparece `0` e não faz mal):

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`). O menu tem agora a opção `3. Pedidos de budget`. Escolhe `3`.

**Deves ver** a lista dos pedidos das campanhas do Miguel:

```text
N.º  Feito em    Campanha    Cliente        De          Para        Estado    Parecer
---  ----------  ----------  -------------  ----------  ----------  --------  -------
1    2026-11-18  Natal 2026  Carla Cliente  1 500,00 €  2 000,00 €  Pendente  Por dar

1 pedido, 1 por decidir.
```

O pedido da Beatriz, se o fizeste na unidade 5.1, não aparece: é de uma campanha da Marta.

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Dar parecer` e a pergunta `Número do pedido de budget (Enter para cancelar)` |
| `1` | Os dados do pedido, com `Cliente:      Carla Cliente`, o motivo e `Parecer:      Por dar`; por baixo, `Despesa atual da campanha: 1 300,00 €.` e a pergunta `O pedido é viável? (s/n)` |
| `s` | A pergunta `Justificação` |
| `Os anúncios em vídeo da semana do Natal são os que dão mais vendas` | `Parecer guardado. O pedido fica em análise, à espera da decisão do administrador.` |
| Enter | A lista, agora com `Em análise` no estado e `Viável` no parecer, e `1 pedido, 1 por decidir.` |

A despesa é a do teu computador: se mudaste os criativos da campanha `Natal 2026`, o valor pode ser outro.

Sai com `0` e `0`. Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`), escolhe `1` (Pedidos de campanha). **Deves ver** o pedido `1` com o estado `Em análise`.

| Escreves | Deves ver |
|---|---|
| `6` e Enter | O título `Cancelar pedido de budget` e a pergunta do número |
| `1` | Os dados do pedido e `Só é possível cancelar um pedido pendente. Este pedido está no estado Em análise.` |
| Enter | A lista outra vez |

Sai com `0` e `0`. Deixa o pedido com o parecer: a unidade 5.3 precisa dele.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/5.2-parecer-do-marketeer
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/5.2-parecer-do-marketeer -> feature/5.2-parecer-do-marketeer`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/5.2-parecer-do-marketeer?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/5.2-parecer-do-marketeer**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Parecer do marketeer sobre os pedidos de budget
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Marketeer passa a dar parecer sobre os pedidos de alteração de budget das suas campanhas.

- Guardar o parecer e a justificação no pedido, que passa a "Em análise"
- Lista dos pedidos das campanhas do marketeer, com os por decidir em primeiro lugar
- Regras do parecer: só nas campanhas do próprio, só em pedidos por decidir, justificação obrigatória
- Opção "Pedidos de budget" no menu do Marketeer, com a despesa atual da campanha no ecrã do parecer

Closes #(número da issue M16)

## Como testar

1. `python -m pytest` (640 testes)
2. `python -m gestor_campanhas`, entrar como `marketeer@agencia.pt` e escolher "Pedidos de budget"
3. Dar parecer favorável ao pedido da campanha Natal 2026 e confirmar, como `cliente@empresa.pt`, que já não pode ser cancelado
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 5 — Budget`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move o card da story M16 para **Ready to Verify**.

### Passo 16 — Avisa Fabio

Diz a Fabio que o pull request da unidade 5.2 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 1 a 7.

### Passo 17 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/5.2-parecer-do-marketeer
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/5.2-parecer-do-marketeer` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 5.4 — Resumo global do budget

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 5.4 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Resumo global do budget**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 1 linha `Closes #` seguida de um número, uma por issue (A16), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Tomas para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/5.4-resumo-do-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/5.4-resumo-do-budget` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/5.4-resumo-do-budget'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `707 passed`.

Garante que tens os dados de demonstração completos (se já existirem, aparecem zeros e não faz mal):

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, `admin@agencia.pt` e `admin12345`). O menu tem agora `6. Resumo do budget`, e os horários passaram para `7`. Escolhe `6`.

**Deves ver** (os números da primeira coluna podem ser outros no teu computador):

```text
N.º  Cliente        Campanhas  Budget      Despesa     Restante  Sem budget  Acima do budget
---  -------------  ---------  ----------  ----------  --------  ----------  ---------------
6    Beatriz Lopes  1          0,00 €      0,00 €      0,00 €    1           0
4    Carla Cliente  1          1 500,00 €  1 300,00 €  200,00 €  0           0
5    José Padeiro   1          800,00 €    300,00 €    500,00 €  0           0

Total: 3 campanhas, budget atribuído 2 300,00 €, despesa 1 600,00 €, restante 700,00 €.
O budget é a soma das campanhas que já têm budget; a despesa conta todas as campanhas.

Nenhuma campanha está acima do budget.
```

Estes são os valores dos dados de demonstração. Se a campanha `Natal 2026` não tiver 1500 € de budget, ou se mudaste os custos dos criativos, os valores são outros: o que importa é que o restante seja o budget menos a despesa.

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Budget das campanhas de um cliente` e a pergunta `Número do cliente (Enter para cancelar)` |
| O número da `Carla Cliente` (primeira coluna) | `Campanhas de Carla Cliente` e a linha `Natal 2026  1 500,00 €  1 300,00 €  200,00 €  Dentro do budget`; por baixo, `1 campanha.` |
| Enter | O resumo outra vez |
| `1` e o número da `Beatriz Lopes` | A linha `Bicicletas de primavera  Por definir  0,00 €   Por definir  Sem budget` |
| Enter e `0` | O menu do administrador |

Agora põe a campanha `Natal 2026` acima do budget, mudando o budget para um valor mais baixo do que a despesa:

| Escreves | Deves ver |
|---|---|
| `5`, `1` e o número da `Natal 2026` | `Budget atual: 1 500,00 €.` e a pergunta do budget |
| `1000` e o motivo `Teste do resumo` | `Budget definido: 1 000,00 €. A alteração ficou registada no histórico do budget.` |
| Enter, `0` e `6` | Na linha da Carla, `-300,00 €` no restante e `1` em `Acima do budget`; o total passa a `budget atribuído 1 800,00 €, despesa 1 600,00 €, restante 200,00 €.`; e, por baixo, a tabela `Acima do budget` com a linha `Natal 2026  Carla Cliente  1 000,00 €  1 300,00 €  -300,00 €  Acima do budget` |

Repõe o budget: `0`, `5`, `1`, o número da `Natal 2026`, `1500` e o motivo `Repor o valor dos dados de demonstração`. **Deves ver** `Budget definido: 1 500,00 €.` Sai com Enter, `0` e `0`.

Confirma também:

- Entra como administrador e escolhe `6`. Escolhe `1` e escreve `999`: aparece `Não há nenhum cliente com campanhas com o número 999.`
- Escolhe `1` e escreve `1`, que nos dados de demonstração é o número da administradora: aparece `Não há nenhum cliente com campanhas com o número 1.`, porque esse número não é de um cliente.
- Confirma, de cabeça, a linha do José: budget `800,00 €`, despesa `300,00 €` (o `Cartaz dos lanches`), restante `500,00 €`.
- Volta ao menu e escolhe `5` e depois `3`, com a campanha `Natal 2026`: o histórico tem as duas linhas do teste (`Teste do resumo` e `Repor o valor dos dados de demonstração`).

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

**f)** No Trello, move o card da story A16 para **Ready**.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/5.4-resumo-do-budget
python ../ctesp-ADC/verificar.py 5.4
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/5.4-resumo-do-budget` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 5.4` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 5.4 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 5.4.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Tomas](tomas.md)).

Diz também a Tomas que já pode avançar ([página de Tomas](tomas.md), passos 28 a 36).

---

## Outras tarefas desta fase

### Passo 25 — Atualiza a página "Arquitetura" da wiki

A página ganha a secção `Budget`, sobre os pedidos, o histórico e o resumo. A tabela das tabelas ganha as linhas `pedidos_budget` e `alteracoes_budget`.

Faz este passo depois de a unidade 5.4 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Arquitetura.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki/Arquitetura e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a Arquitetura para a versão 0.5.0` e clica em **Save page**.

**Deves ver** a página com a secção nova `Budget`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 5.2 — Parecer do marketeer sobre os pedidos de budget

- **`gestor_campanhas/repositorios/pedidos_budget.py`** ganha duas funções. `listar_por_marketeer` filtra pela coluna `marketeer_id` da tabela `campanhas`: o pedido não guarda o marketeer, por isso, se a campanha mudar de responsável, os pedidos mudam com ela. `definir_parecer` guarda o parecer (`1` ou `0`, porque o SQLite não tem verdadeiro/falso), a justificação e o estado novo, de uma vez.
- **`gestor_campanhas/servicos/budget.py`** ganha `listar_do_marketeer` (por decidir primeiro, com o mesmo `sorted` dos pedidos de campanha), `obter_do_marketeer` (só devolve o pedido se a campanha for do marketeer; a mensagem é a mesma quando o pedido não existe e quando é de outro) e `dar_parecer`. Esta recusa pedidos já decididos ou cancelados e justificações vazias, e passa o pedido a `Em análise`. Não recusa um pedido que já tem parecer: o novo substitui o anterior.
- **`gestor_campanhas/cli/budget.py`**: `mostrar_detalhes` ganha o parâmetro `com_parecer`, que acrescenta o cliente, o parecer e a justificação (o cliente vê o pedido sem eles). `mostrar_pedidos_com_parecer` é a tabela do Marketeer, e vai servir também para o Administrador, na unidade 5.3. `dar_parecer` mostra a despesa atual da campanha, calculada com `criativos.despesa`, para o marketeer comparar com o valor pedido. `do_marketeer` é o ciclo do menu.
- **`gestor_campanhas/cli/perfis.py`**: o menu do Marketeer ganha a opção "Pedidos de budget", a seguir a "Criativos". As opções da conta passam para 4 e 5.
- **`tests/test_budget.py`** ganha os testes do repositório, das regras do parecer e dos ecrãs do Marketeer.
- **`docs/`**: o guia de utilização ganha a secção "Pedidos de budget" do Marketeer, e a arquitetura a secção "Pedidos de alteração de budget", com o desenho dos estados.
