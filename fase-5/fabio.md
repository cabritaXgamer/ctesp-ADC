# Fase 5 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 5 (Budget), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 5.2 (de Ricardo) | Quando Ricardo avisar |
| 8 a 17 | Fazer a unidade 5.3 — Decisão dos pedidos de budget e histórico do budget | A seguir ao teu passo anterior |
| 18 a 25 | Rever a release v0.5.0 e juntá-la ao main | Quando Tomas avisar |
| 26 a 29 | Juntar a release v0.5.0 ao develop | Quando Tomas avisar |
| 30 | Atualiza a página "Guia de utilização" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 5.2 — Parecer do marketeer sobre os pedidos de budget

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 5.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Parecer do marketeer sobre os pedidos de budget**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 1 linha `Closes #` seguida de um número, uma por issue (M16), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Ricardo para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/5.2-parecer-do-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/5.2-parecer-do-marketeer` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/5.2-parecer-do-marketeer'`.

Agora experimenta:

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

Confirma também:

- Entra como marketeer, `3`, `1` e outra vez o pedido `1`. Aparece `Parecer:      Viável`, a justificação, e a frase `Já deu parecer sobre este pedido. O parecer novo substitui o anterior.` Responde `s` e escreve a mesma justificação: o parecer fica como estava.
- Ainda como marketeer, `1` e `999`: aparece `Não há nenhum pedido de budget com o número 999 nas suas campanhas.`
- Ainda em "Dar parecer", escolhe o pedido `1`, responde `n` e, na justificação, carrega só em Enter: aparece `Este campo é obrigatório.` Escreve `Teste` e depois volta a dar o parecer `s` com a justificação `Os anúncios em vídeo da semana do Natal são os que dão mais vendas`, para o pedido ficar viável.
- Sai e entra como `marta@agencia.pt` / `marta12345`. Escolhe `3`: aparecem só os pedidos das campanhas da Marta (o pedido cancelado da Beatriz, se o fizeste na unidade 5.1, ou `Ainda não há pedidos de alteração de budget nas suas campanhas.`). Escolhe `1` e escreve `1`: aparece `Não há nenhum pedido de budget com o número 1 nas suas campanhas.`

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

**f)** No Trello, move o card da story M16 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/5.2-parecer-do-marketeer
python ../ctesp-ADC/verificar.py 5.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/5.2-parecer-do-marketeer` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 5.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 5.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 5.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Ricardo](ricardo.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 5.3 — Decisão dos pedidos de budget e histórico do budget

O Administrador ganha a opção "Pedidos de budget", com os pedidos de todas as campanhas e o parecer do marketeer, e aprova-os ou rejeita-os. Aprovar altera logo o budget da campanha. Cada alteração do budget fica num histórico, que o Administrador e o Cliente consultam na opção "Campanhas".

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Parecer do marketeer sobre os pedidos de budget** (unidade 5.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 5.3

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 3 issues: A14, A15, C16. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A14** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA14%5D%22

```markdown
- [ ] O menu do Administrador tem a opção "Pedidos de budget", a seguir a "Pedidos de campanha"
- [ ] A lista mostra os pedidos de todas as campanhas, com o cliente, a campanha, o budget de partida, o budget pedido, o estado e o parecer do marketeer; os que estão por decidir aparecem primeiro
- [ ] "Analisar pedido" mostra o motivo do cliente, o parecer e a justificação do marketeer, e o budget e a despesa atuais da campanha
- [ ] Um pedido sem parecer não pode ser decidido: aparece um aviso
- [ ] A decisão é "Aprovar", "Rejeitar" ou "Decidir mais tarde"; rejeitar pede o motivo, obrigatório, e uma confirmação
- [ ] Um pedido aprovado, rejeitado ou cancelado já não pode ser decidido
```

**Issue A15** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA15%5D%22

```markdown
- [ ] Aprovar um pedido muda logo o budget da campanha para o valor pedido; um parecer "Não viável" não impede aprovar
- [ ] Fica registado o valor anterior, o valor novo, a data e o motivo (o número e o motivo do pedido)
- [ ] "Definir budget", em "Campanhas", passa a pedir o motivo quando a campanha já tem budget, e recusa um valor igual ao atual; a alteração fica também registada
- [ ] O budget inicial de uma campanha criada a partir de um pedido de campanha fica registado
```

**Issue C16** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC16%5D%22

```markdown
- [ ] A opção "Campanhas" do Cliente ganha "Histórico do budget", que pede o número de uma das suas campanhas
- [ ] O histórico é uma tabela com a data, o valor anterior (`De`), o valor novo (`Para`) e o motivo, da alteração mais antiga para a mais recente
- [ ] O Administrador vê o mesmo histórico, de qualquer campanha, em "Campanhas", "Histórico do budget"
- [ ] Um cliente só vê o histórico das suas campanhas
- [ ] O budget das campanhas de demonstração fica no histórico como "Budget inicial"
```

Por fim, no quadro Trello, move os cards das stories A14, A15 e C16 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/5.3-decisao-e-historico-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/5.3-decisao-e-historico-budget` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/5.3-decisao-e-historico-budget'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/5.3-decisao-e-historico-budget' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/5.3-decisao-e-historico-budget
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/5.3-decisao-e-historico-budget
git switch -c feature/5.3-decisao-e-historico-budget
```

  **Deves ver** `Deleted branch feature/5.3-decisao-e-historico-budget (was ...)` e depois `Switched to a new branch 'feature/5.3-decisao-e-historico-budget'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/5.3-decisao-e-historico-budget` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 8 commits

São 8 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 5.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 5.3. Eles estão na pasta `ctesp-ADC/fase-5/ficheiros/5.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela do histórico do budget"
```

**Deves ver** uma linha a terminar em `2 files changed, 43 insertions(+)`.

**Commit 2 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 2
```

**Deves ver** `Copiados 4 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/alteracoes_budget.py`, `gestor_campanhas/repositorios/pedidos_budget.py`, `tests/test_decisao_budget.py`.

```bash
git add -A
git commit -m "feat(repositorios): registar o histórico do budget e as decisões dos pedidos"
```

**Deves ver** uma linha a terminar em `4 files changed, 209 insertions(+)`.

**Commit 3 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 3
```

**Deves ver** `Copiados 5 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/servicos/campanhas.py`, `gestor_campanhas/servicos/pedidos.py`, `tests/test_administracao.py`, `tests/test_decisao_budget.py`.

```bash
git add -A
git commit -m "feat(campanhas): registar no histórico cada alteração do budget"
```

**Deves ver** uma linha a terminar em `5 files changed, 163 insertions(+), 10 deletions(-)`.

**Commit 4 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/budget.py`, `tests/test_decisao_budget.py`.

```bash
git add -A
git commit -m "feat(budget): decidir os pedidos de alteração de budget"
```

**Deves ver** uma linha a terminar em `2 files changed, 178 insertions(+), 1 deletion(-)`.

**Commit 5 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 5
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/budget.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_decisao_budget.py`.

```bash
git add -A
git commit -m "feat(cli): decidir os pedidos de budget no menu do administrador"
```

**Deves ver** uma linha a terminar em `3 files changed, 231 insertions(+)`.

**Commit 6 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 6
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `tests/test_decisao_budget.py`.

```bash
git add -A
git commit -m "feat(cli): histórico do budget de cada campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 131 insertions(+), 5 deletions(-)`.

**Commit 7 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 7
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dados_demo.py`, `tests/test_decisao_budget.py`.

```bash
git add -A
git commit -m "feat(demo): registar o budget inicial das campanhas de demonstração"
```

**Deves ver** uma linha a terminar em `2 files changed, 70 insertions(+), 2 deletions(-)`.

**Commit 8 de 8**

```bash
python ../ctesp-ADC/copiar.py 5.3 8
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar a decisão dos pedidos de budget e o histórico do budget"
```

**Deves ver** uma linha a terminar em `3 files changed, 118 insertions(+), 8 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 5.3
git log --oneline -8
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 5.3` | `Tudo certo: o ramo 'feature/5.3-decisao-e-historico-budget' está igual ao original no fim da unidade 5.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -8` | Os teus 8 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar a decisão dos pedidos de budget e o histórico do budget
xxxxxxx feat(demo): registar o budget inicial das campanhas de demonstração
xxxxxxx feat(cli): histórico do budget de cada campanha
xxxxxxx feat(cli): decidir os pedidos de budget no menu do administrador
xxxxxxx feat(budget): decidir os pedidos de alteração de budget
xxxxxxx feat(campanhas): registar no histórico cada alteração do budget
xxxxxxx feat(repositorios): registar o histórico do budget e as decisões dos pedidos
xxxxxxx feat(bd): criar a tabela do histórico do budget
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `686 passed`.

Regista o budget inicial das campanhas de demonstração no histórico. Faz isto **antes** de aprovar o pedido, porque o comando só regista o budget inicial de uma campanha que ainda não tem histórico:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver**, entre as outras linhas, `Budgets iniciais registados no histórico: 2 (os restantes já estavam).`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Primeiro, garante que o pedido de budget tem parecer. Se fizeste a unidade 5.2, já tem, e o que fazes a seguir só o confirma. Entra como marketeer (`1`, `marketeer@agencia.pt` e `marketeer12345`):

| Escreves | Deves ver |
|---|---|
| `3`, `1` e `1` | Os dados do pedido `1`. Se já tinha parecer, aparece também `Já deu parecer sobre este pedido. O parecer novo substitui o anterior.` |
| `s` e `Os anúncios em vídeo da semana do Natal são os que dão mais vendas` | `Parecer guardado. O pedido fica em análise, à espera da decisão do administrador.` |
| Enter, `0` e `0` | O menu inicial |

Entra como administrador (`1`, `admin@agencia.pt` e `admin12345`). O menu tem agora `4. Pedidos de budget`, e `Campanhas` passou para `5`. Escolhe `4`.

**Deves ver** os pedidos de todas as campanhas. O da `Natal 2026` está em primeiro, `Em análise`, com o parecer `Viável`. Se fizeste os testes da unidade 5.1, aparece também o pedido cancelado da Beatriz, no fim.

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Analisar pedido de budget` e a pergunta do número |
| `1` | Os dados do pedido, com `Parecer:      Viável` e a justificação; por baixo, `Budget atual da campanha: 1 500,00 €. Despesa: 1 300,00 €.` e o menu `Decisão`, com `1. Aprovar e passar o budget para 2 000,00 €` |
| `1` | `Pedido aprovado. O budget da campanha Natal 2026 passou a 2 000,00 €.` e `A alteração ficou registada no histórico do budget.` |
| Enter | A lista, com o pedido `1` no estado `Aprovado` e `0 por decidir` (ou mais, se tiveres outros pedidos por decidir) |
| `0` e `5` | A tabela das campanhas, com `2 000,00 €` no budget da `Natal 2026`, e o menu com a opção nova `3. Histórico do budget` |
| `3` e o número da `Natal 2026` | `Campanha Natal 2026. Budget atual: 2 000,00 €.` e a tabela do histórico (ver a seguir) |

```text
Data              De           Para        Motivo
----------------  -----------  ----------  -------------------------------------------------------------------------------------
2026-11-18 10:00  Por definir  1 500,00 €  Budget inicial
2026-11-18 10:05  1 500,00 €   2 000,00 €  Pedido de budget n.º 1: Reforçar os anúncios em vídeo na última semana antes do Natal

2 alterações.
```

As datas e as horas são as do teu computador. Agora põe o budget outra vez em 1500 €, para os valores das unidades seguintes baterem certo:

| Escreves | Deves ver |
|---|---|
| Enter, `1` e o número da `Natal 2026` | `Campanha Natal 2026, de Carla Cliente. Budget atual: 2 000,00 €.` e a pergunta do budget |
| `1500` | A pergunta nova `Motivo da alteração` |
| `Repor o valor dos dados de demonstração` | `Budget definido: 1 500,00 €. A alteração ficou registada no histórico do budget.` |

Sai com Enter, `0` e `0`. Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`) e escolhe `2` (Campanhas). O menu tem agora `2. Histórico do budget`.

| Escreves | Deves ver |
|---|---|
| `2` e o número da `Natal 2026` | `Campanha Natal 2026. Budget atual: 1 500,00 €.` e o histórico com três linhas: `Budget inicial`, o pedido de budget n.º 1 e, por fim, `2 000,00 €   1 500,00 €  Repor o valor dos dados de demonstração`; por baixo, `3 alterações.` |

Sai com Enter, `0` e `0`.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/5.3-decisao-e-historico-budget
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/5.3-decisao-e-historico-budget -> feature/5.3-decisao-e-historico-budget`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/5.3-decisao-e-historico-budget?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/5.3-decisao-e-historico-budget**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Decisão dos pedidos de budget e histórico do budget
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a decidir os pedidos de alteração de budget, e cada campanha passa a ter um histórico do budget.

- Tabela `alteracoes_budget`, com o histórico, e classe `AlteracaoBudget`
- Uma só função, `alterar_budget`, por onde passam todas as alterações do budget, para nenhuma ficar fora do histórico
- "Definir budget" pede o motivo e recusa o valor atual; o budget inicial de um pedido de campanha aprovado fica registado
- Regras da decisão: só com parecer, aprovar altera o budget, rejeitar pede o motivo
- Opção "Pedidos de budget" no menu do Administrador
- "Histórico do budget" nas campanhas do Cliente e do Administrador
- Budget inicial das campanhas de demonstração no histórico

Closes #(número da issue A14)
Closes #(número da issue A15)
Closes #(número da issue C16)

## Como testar

1. `python -m pytest` (686 testes)
2. `python -m gestor_campanhas.dados_demo` e depois `python -m gestor_campanhas`
3. Como administrador, aprovar o pedido da campanha Natal 2026 e ver o histórico; repor o budget em 1500 € com "Definir budget"; como `cliente@empresa.pt`, ver o histórico
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 5 — Budget`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories A14, A15 e C16 para **Ready to Verify**.

### Passo 16 — Avisa Tomas

Diz a Tomas que o pull request da unidade 5.3 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 11 a 17.

### Passo 17 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/5.3-decisao-e-historico-budget
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/5.3-decisao-e-historico-budget` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever a release v0.5.0 e juntá-la ao main

Quem fez: Tomas. Tu confirmas que a versão está pronta e juntas o ramo da release ao `main`.

### Passo 18 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 5.5 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Release v0.5.0**.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch release/v0.5.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch release/v0.5.0` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'release/v0.5.0'`.

Agora experimenta:

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `707 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v0.5.0`. Sai com `0`.

Confirma também:

- No separador **Files changed** do pull request aparecem só três ficheiros: `gestor_campanhas/__init__.py`, `CHANGELOG.md` e `README.md`.
- O `CHANGELOG.md` tem a secção `v0.5.0` por cima da `v0.4.0`.
- O README tem a secção nova `Budget`, com o desenho do caminho de um pedido.

### Passo 21 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 22 — Confirma que o pull request vai para o main

Este é o único pull request da fase que não vai para o `develop`. Se for junto ao ramo errado, o `main` fica sem a versão e a tag fica no sítio errado.

Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.5.0`.

Se disser `into develop`, **não juntes**. Avisa Tomas, que corrige o destino no botão **Edit**, à direita do título. Depois de corrigido, atualiza a página e confirma outra vez.

### Passo 23 — Junta o pull request ao main (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `main`.

**Deves ver** o símbolo roxo **Merged** no topo da página.

### Passo 24 — Arruma o teu computador

```bash
git switch develop
git branch -D release/v0.5.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git branch -D release/v0.5.0` | Apaga a cópia do ramo que criaste para experimentar. O `-D` maiúsculo é preciso porque o `develop` ainda não tem estes commits: chegam lá no pull request seguinte |

### Passo 25 — Avisa Tomas

Diz a Tomas que a release v0.5.0 já está no `main`. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 37 a 42.

---

## Juntar a release v0.5.0 ao develop

É o último pull request da fase.

### Passo 26 — Aprova o pull request que leva a release para o develop

Faz este passo quando Tomas te avisar.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Juntar a release v0.5.0 ao develop**.

**b)** Confirma que na descrição está `Closes #` seguido do número da issue da release, e não `#N`. Se estiver `#N`, pede a Tomas para editar a descrição antes de juntares.

**c)** No separador **Files changed**, confirma que as alterações são as da release: o número da versão, o `CHANGELOG.md` e o `README.md`.

**d)** Clica em **Review changes**, escolhe **Approve** e clica em **Submit review**.

### Passo 27 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** **Não cliques em Delete branch.** O ramo deste pull request é o `main`, que tem de continuar a existir.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da release fica fechada sozinha.

### Passo 28 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 5.5
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `python ../ctesp-ADC/verificar.py 5.5` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 5.5 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 5.5.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 29 — Avisa o grupo

Diz a Tomas que a release está no `develop` e que já pode arrumar o computador (passo 42 da [página de Tomas](tomas.md)).

Esta era a última vez da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 30 — Atualiza a página "Guia de utilização" da wiki

A página passa a explicar os pedidos de alteração de budget, o histórico e o resumo do budget.

Faz este passo depois de a unidade 5.4 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Guia-de-utilizacao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Guia de utilização** na lista de páginas, à direita, e depois em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar o Guia de utilização para a versão 0.5.0` e clica em **Save page**.

**Deves ver** a página a começar por `Como usar a aplicação, na versão 0.5.0.` e com as secções novas `Pedidos de alteração de budget` e `Resumo do budget (Administrador)`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 5.3 — Decisão dos pedidos de budget e histórico do budget

- **`gestor_campanhas/bd.py`** ganha a tabela `alteracoes_budget`, o histórico. Tem `ON DELETE CASCADE` para a campanha, como os pedidos de budget, e `ON DELETE SET NULL` para o pedido que deu origem à alteração: se um dia um pedido desaparecer, a linha do histórico fica, só sem o número do pedido.
- **`gestor_campanhas/modelos.py`** ganha a classe `AlteracaoBudget`. Cada linha guarda o valor anterior e o novo, e não a diferença, para se perceber cada linha sem ler as outras.
- **`gestor_campanhas/repositorios/alteracoes_budget.py`** é novo, com `registar` e `listar_por_campanha`. O histórico só cresce: não há funções para alterar ou apagar linhas.
- **`gestor_campanhas/repositorios/pedidos_budget.py`** ganha `listar_todos` e `decidir`, que guarda o estado, o motivo da rejeição e a data da decisão.
- **`gestor_campanhas/servicos/campanhas.py`** ganha `alterar_budget`, a única função que muda o budget de uma campanha que já existe: muda a coluna da tabela `campanhas` e acrescenta a linha ao histórico. Se cada sítio que muda o budget escrevesse no histórico por si, bastava um esquecer-se para o histórico ficar errado. `definir_budget` passa a usá-la, recusa um valor igual ao atual e exige o motivo quando já havia budget; sem budget anterior, o motivo fica `Budget inicial` (a constante `MOTIVO_BUDGET_INICIAL`). `historico_budget` devolve as linhas de uma campanha.
- **`gestor_campanhas/servicos/pedidos.py`**: ao aprovar um pedido de campanha, regista o budget inicial no histórico, com o número do pedido de campanha.
- **`gestor_campanhas/servicos/budget.py`** ganha a decisão. `_para_decidir` confirma que o pedido está por decidir e que já tem parecer. `aprovar` chama `alterar_budget`, com o motivo `Pedido de budget n.º ...: ...`, e só depois marca o pedido como aprovado; se a campanha já tiver o budget pedido (por exemplo, porque o Administrador o mudou à mão), recusa, porque a aprovação não alteraria nada. `rejeitar` exige o motivo e não mexe no budget.
- **`gestor_campanhas/cli/budget.py`** ganha `decidir`, `aprovar`, `rejeitar` e `do_administrador`. A lista do Administrador usa a mesma tabela do Marketeer (`mostrar_pedidos_com_parecer`).
- **`gestor_campanhas/cli/campanhas.py`**: "Definir budget" pergunta o motivo só quando a campanha já tem budget. `mostrar_historico` é a tabela do histórico, usada pelo Administrador (`historico`) e pelo Cliente (`historico_do_cliente`, que confirma que a campanha é dele).
- **`gestor_campanhas/cli/perfis.py`**: o menu do Administrador ganha "Pedidos de budget", a seguir a "Pedidos de campanha".
- **`gestor_campanhas/dados_demo.py`** ganha `registar_budgets_iniciais`. As campanhas de demonstração são criadas diretamente no repositório, já com budget, sem passar por `alterar_budget`; esta função acrescenta a linha `Budget inicial` às que ainda não têm histórico.
- **`tests/test_decisao_budget.py`** é novo: histórico, decisão, ecrãs do Administrador e do Cliente, e dados de demonstração. Em `tests/test_administracao.py`, o teste que altera um budget já definido passa a indicar o motivo.
- **`docs/`**: o guia de utilização ganha a secção "Pedidos de budget" do Administrador e o histórico do budget; a arquitetura ganha a tabela nova e a secção "Histórico do budget"; a referência ganha o módulo novo.
