# Fase 5 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 5 (Budget), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 10 | Fazer a unidade 5.1 — Pedido de alteração de budget | No início da fase |
| 11 a 17 | Rever e juntar a unidade 5.3 (de Fabio) | Quando Fabio avisar |
| 18 a 27 | Fazer a unidade 5.4 — Resumo global do budget | A seguir ao teu passo anterior |
| 28 a 36 | Preparar a release v0.5.0 | Quando Ricardo avisar |
| 37 a 42 | Publicar a release v0.5.0 e pedir o regresso ao develop | Quando Fabio avisar |
| 43 a 44 | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | Em qualquer altura durante a fase |

---

## Fazer a unidade 5.1 — Pedido de alteração de budget

O Cliente passa a poder pedir a alteração do budget de uma campanha, com o valor que pretende e o motivo. Os pedidos aparecem na opção "Pedidos de campanha", numa segunda lista, por baixo dos pedidos de nova campanha, e podem ser vistos e cancelados enquanto estão pendentes.

### Passo 1 — Confirma que podes começar

A fase anterior tem de estar fechada: todos os pull requests juntos e o `develop` do teu computador atualizado. Se for a primeira fase, tens de ter feito a [Preparação](../preparacao.md).

### Passo 2 — Fica com as issues da unidade 5.1

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: C15. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C15** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC15%5D%22

```markdown
- [ ] A opção "Pedidos de campanha" do Cliente mostra duas listas: "Pedidos de nova campanha" e "Pedidos de alteração de budget" (parte de C06 que tinha ficado da Fase 3)
- [ ] A lista dos pedidos de budget tem o número, a data, a campanha, o budget de partida (`De`), o budget pedido (`Para`) e o estado
- [ ] "Pedir alteração de budget" mostra as campanhas do cliente que ainda não terminaram e pede a campanha, o budget pretendido e o motivo
- [ ] O budget pretendido tem de ser maior do que zero e diferente do atual; o motivo é obrigatório
- [ ] Uma campanha que já terminou, ou que já tem um pedido por decidir, não aceita outro pedido; o aviso aparece logo depois de escolher a campanha
- [ ] Uma campanha sem budget também aceita pedidos (o budget atual aparece como `Por definir`)
- [ ] O pedido fica `Pendente`; "Ver pedido de budget" mostra todos os dados, incluindo o motivo
- [ ] "Cancelar pedido de budget" só cancela pedidos pendentes, com confirmação; o pedido fica na lista com o estado `Cancelado`
- [ ] As opções dos pedidos de campanha passam a chamar-se "Novo pedido de campanha", "Ver pedido de campanha" e "Cancelar pedido de campanha"
```

Por fim, no quadro Trello, move o card da story C15 de **Sprint Backlog** para **Work In Progress**.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/5.1-pedido-alteracao-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/5.1-pedido-alteracao-budget` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/5.1-pedido-alteracao-budget'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/5.1-pedido-alteracao-budget' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/5.1-pedido-alteracao-budget
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/5.1-pedido-alteracao-budget
git switch -c feature/5.1-pedido-alteracao-budget
```

  **Deves ver** `Deleted branch feature/5.1-pedido-alteracao-budget (was ...)` e depois `Switched to a new branch 'feature/5.1-pedido-alteracao-budget'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/5.1-pedido-alteracao-budget` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 4 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 5.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 5.1. Eles estão na pasta `ctesp-ADC/fase-5/ficheiros/5.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 5.1 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela dos pedidos de alteração de budget"
```

**Deves ver** uma linha a terminar em `2 files changed, 71 insertions(+)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 5.1 2
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/pedidos_budget.py`, `tests/test_budget.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar e ler pedidos de alteração de budget"
```

**Deves ver** uma linha a terminar em `3 files changed, 312 insertions(+)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 5.1 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/budget.py`, `tests/test_budget.py`.

```bash
git add -A
git commit -m "feat(budget): pedir e cancelar uma alteração de budget"
```

**Deves ver** uma linha a terminar em `2 files changed, 246 insertions(+)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 5.1 4
```

**Deves ver** `Copiados 5 ficheiros`: `gestor_campanhas/cli/budget.py`, `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/cli/pedidos.py`, `gestor_campanhas/servicos/budget.py`, `tests/test_budget.py`.

```bash
git add -A
git commit -m "feat(cli): pedidos de alteração de budget no menu do cliente"
```

**Deves ver** uma linha a terminar em `5 files changed, 412 insertions(+), 23 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 5.1 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dados_demo.py`, `tests/test_budget.py`.

```bash
git add -A
git commit -m "feat(demo): acrescentar um pedido de alteração de budget de demonstração"
```

**Deves ver** uma linha a terminar em `2 files changed, 77 insertions(+), 5 deletions(-)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 5.1 6
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os pedidos de alteração de budget"
```

**Deves ver** uma linha a terminar em `3 files changed, 114 insertions(+), 15 deletions(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 5.1
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 5.1` | `Tudo certo: o ramo 'feature/5.1-pedido-alteracao-budget' está igual ao original no fim da unidade 5.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os pedidos de alteração de budget
xxxxxxx feat(demo): acrescentar um pedido de alteração de budget de demonstração
xxxxxxx feat(cli): pedidos de alteração de budget no menu do cliente
xxxxxxx feat(budget): pedir e cancelar uma alteração de budget
xxxxxxx feat(repositorios): guardar e ler pedidos de alteração de budget
xxxxxxx feat(bd): criar a tabela dos pedidos de alteração de budget
```

### Passo 6 — Experimenta o que gravaste

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

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/5.1-pedido-alteracao-budget
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/5.1-pedido-alteracao-budget -> feature/5.1-pedido-alteracao-budget`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/5.1-pedido-alteracao-budget?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/5.1-pedido-alteracao-budget**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Pedido de alteração de budget
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Cliente passa a poder pedir a alteração do budget das suas campanhas.

- Tabela `pedidos_budget` na base de dados, já com as colunas do parecer e da decisão (unidades 5.2 e 5.3)
- Classe `PedidoBudget` e repositório dos pedidos de budget
- Regras para pedir e cancelar: valor válido e diferente do atual, motivo obrigatório, campanha do cliente e por terminar, um pedido por decidir de cada vez
- Segunda lista e três opções novas em "Pedidos de campanha" do Cliente (completa C06)
- Um pedido de budget de demonstração

Closes #(número da issue C15)

## Como testar

1. `python -m pytest` (620 testes)
2. `python -m gestor_campanhas.dados_demo` e depois `python -m gestor_campanhas`
3. Como `cliente@empresa.pt`, ver o pedido de budget da campanha Natal 2026; como `beatriz@bicicletas.pt`, pedir 900 € para a campanha Bicicletas de primavera e cancelar o pedido
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 5 — Budget`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move o card da story C15 para **Ready to Verify**.

### Passo 9 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 5.1 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 1 a 7.

### Passo 10 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/5.1-pedido-alteracao-budget
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/5.1-pedido-alteracao-budget` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 5.3 — Decisão dos pedidos de budget e histórico do budget

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 11 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 5.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Decisão dos pedidos de budget e histórico do budget**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 3 linhas `Closes #` seguida de um número, uma por issue (A14, A15, C16), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Fabio para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/5.3-decisao-e-historico-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/5.3-decisao-e-historico-budget` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/5.3-decisao-e-historico-budget'`.

Agora experimenta:

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

Confirma também:

- Entra como `beatriz@bicicletas.pt` / `beatriz12345`, `1`, `4`, a campanha `Bicicletas de primavera`, `900` e o motivo `Começar a campanha`. Aponta o número do pedido. Sai e entra como `marta@agencia.pt` / `marta12345`, `3`, `1`, o número do pedido, `n` e a justificação `Ainda não há criativos com custo`.
- Entra como administrador, `4`, `1` e o número do pedido da Beatriz. Escolhe `2` (Rejeitar), escreve o motivo `Sem orçamento este mês` e responde `s`: aparece `Pedido rejeitado. O budget da campanha não mudou.`, e na lista o pedido fica `Rejeitado`, com o parecer `Não viável`.
- Entra como Beatriz, `1`, `5` e o número do pedido: aparece `Estado:       Rejeitado` e `Rejeição:     Sem orçamento este mês`. Ainda como Beatriz, faz outro pedido (`4`, a mesma campanha, `700`, `Outra tentativa`) e aponta o número.
- Entra como administrador, `4`, `1` e o número do pedido novo da Beatriz: aparece `Este pedido ainda não tem o parecer do marketeer. Só pode ser decidido depois do parecer.`, sem o menu da decisão. Depois, como Beatriz, cancela esse pedido (`1`, `6`, o número e `s`).
- Como administrador, `5`, `1`, a campanha `Natal 2026`, `1500` e um motivo qualquer: aparece `O budget novo é igual ao budget atual. O budget não foi alterado.`

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

**f)** No Trello, move os cards das stories A14, A15 e C16 para **Ready**.

### Passo 16 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/5.3-decisao-e-historico-budget
python ../ctesp-ADC/verificar.py 5.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/5.3-decisao-e-historico-budget` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 5.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 5.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 5.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 17 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 18.

---

## Fazer a unidade 5.4 — Resumo global do budget

O Administrador ganha a opção "Resumo do budget": para cada cliente, o budget atribuído, a despesa e o restante, com os totais por baixo e as campanhas acima do budget em destaque. Daqui vê também as campanhas de um cliente, uma a uma.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Decisão dos pedidos de budget e histórico do budget** (unidade 5.3) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 5.4

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: A16. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A16** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA16%5D%22

```markdown
- [ ] O menu do Administrador tem a opção "Resumo do budget", a seguir a "Campanhas"
- [ ] O resumo tem uma linha por cliente com campanhas, por ordem alfabética, com o número de campanhas, o budget, a despesa, o restante, as campanhas sem budget e as campanhas acima do budget
- [ ] O budget de um cliente é a soma das campanhas que já têm budget; a despesa é a soma de todas as campanhas; o restante é o budget menos a despesa e pode ser negativo
- [ ] Por baixo aparecem os totais de todos os clientes
- [ ] As campanhas com despesa maior do que o budget aparecem em destaque, numa tabela própria; se não houver nenhuma, aparece "Nenhuma campanha está acima do budget."
- [ ] Uma campanha sem budget nunca conta como acima do budget
- [ ] "Ver as campanhas de um cliente" mostra as campanhas desse cliente, com o budget, a despesa, o restante e a situação ("Dentro do budget", "Acima do budget" ou "Sem budget")
```

Por fim, no quadro Trello, move o card da story A16 de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/5.4-resumo-do-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/5.4-resumo-do-budget` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/5.4-resumo-do-budget'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/5.4-resumo-do-budget' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/5.4-resumo-do-budget
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/5.4-resumo-do-budget
git switch -c feature/5.4-resumo-do-budget
```

  **Deves ver** `Deleted branch feature/5.4-resumo-do-budget (was ...)` e depois `Switched to a new branch 'feature/5.4-resumo-do-budget'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/5.4-resumo-do-budget` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 21 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 5.4 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 5.4. Eles estão na pasta `ctesp-ADC/fase-5/ficheiros/5.4/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 5.4 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/budget.py`, `tests/test_resumo_budget.py`.

```bash
git add -A
git commit -m "feat(budget): calcular o resumo global do budget por cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 285 insertions(+), 1 deletion(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 5.4 2
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/budget.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_resumo_budget.py`.

```bash
git add -A
git commit -m "feat(cli): resumo global do budget no menu do administrador"
```

**Deves ver** uma linha a terminar em `3 files changed, 203 insertions(+), 1 deletion(-)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 5.4 3
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar o resumo global do budget"
```

**Deves ver** uma linha a terminar em `2 files changed, 66 insertions(+)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 5.4
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 5.4` | `Tudo certo: o ramo 'feature/5.4-resumo-do-budget' está igual ao original no fim da unidade 5.4.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar o resumo global do budget
xxxxxxx feat(cli): resumo global do budget no menu do administrador
xxxxxxx feat(budget): calcular o resumo global do budget por cliente
```

### Passo 23 — Experimenta o que gravaste

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

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/5.4-resumo-do-budget
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/5.4-resumo-do-budget -> feature/5.4-resumo-do-budget`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/5.4-resumo-do-budget?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/5.4-resumo-do-budget**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Resumo global do budget
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a ter uma visão financeira de todas as campanhas.

- Cálculo do resumo por cliente, dos totais e das campanhas acima do budget, a partir da despesa de cada campanha
- Regra "acima do budget" numa só função
- Opção "Resumo do budget" no menu do Administrador, com o detalhe das campanhas de cada cliente

Closes #(número da issue A16)

## Como testar

1. `python -m pytest` (707 testes)
2. `python -m gestor_campanhas`, entrar como `admin@agencia.pt` e escolher "Resumo do budget"
3. Passar o budget da campanha Natal 2026 para 1000 € e ver a campanha em destaque; repor os 1500 €
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 5 — Budget`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move o card da story A16 para **Ready to Verify**.

### Passo 26 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 5.4 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 18 a 24.

### Passo 27 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/5.4-resumo-do-budget
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/5.4-resumo-do-budget` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Preparar a release v0.5.0

Fecha a fase com a versão 0.5.0: sobe o número da versão, acrescenta a secção desta versão ao registo de alterações e atualiza o README. Esta unidade vai para o `main`, e não para o `develop`.

### Passo 28 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Resumo global do budget** (unidade 5.4) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 29 — Cria a issue da unidade 5.5

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[5.5] Release v0.5.0
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Publicar a versão 0.5.0, com as user stories da Fase 5 (budget).

## O que inclui

- [ ] Versão 0.5.0 em `gestor_campanhas/__init__.py`
- [ ] Registo de alterações (`CHANGELOG.md`)
- [ ] README atualizado
- [ ] Pull request para `main`
- [ ] Tag e release `v0.5.0` no GitHub
- [ ] `main` de volta ao `develop`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 5 — Budget`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 30 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c release/v0.5.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c release/v0.5.0` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'release/v0.5.0'`.

**Se em vez disso aparecer** `fatal: a branch named 'release/v0.5.0' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..release/v0.5.0
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D release/v0.5.0
git switch -c release/v0.5.0
```

  **Deves ver** `Deleted branch release/v0.5.0 (was ...)` e depois `Switched to a new branch 'release/v0.5.0'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch release/v0.5.0` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 31 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 5.5 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 5.5. Eles estão na pasta `ctesp-ADC/fase-5/ficheiros/5.5/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 5.5 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__init__.py`.

```bash
git add -A
git commit -m "chore(release): passar a versão para 0.5.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 5.5 2
```

**Deves ver** `Copiados 1 ficheiro`: `CHANGELOG.md`.

```bash
git add -A
git commit -m "docs(release): registar as alterações da versão 0.5.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 27 insertions(+)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 5.5 3
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(release): atualizar o README para a versão 0.5.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 22 insertions(+), 4 deletions(-)`.


### Passo 32 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 5.5
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 5.5` | `Tudo certo: o ramo 'release/v0.5.0' está igual ao original no fim da unidade 5.5.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(release): atualizar o README para a versão 0.5.0
xxxxxxx docs(release): registar as alterações da versão 0.5.0
xxxxxxx chore(release): passar a versão para 0.5.0
```

### Passo 33 — Experimenta o que gravaste

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

### Passo 34 — Envia o ramo para o GitHub

```bash
git push -u origin release/v0.5.0
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      release/v0.5.0 -> release/v0.5.0`.

### Passo 35 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `main`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/main...release/v0.5.0?expand=1

**b)** Confirma, no topo, que está **base: main** e **compare: release/v0.5.0**. O link do ponto a) já abre com o `main` escolhido. Se estiver **base: develop**, clica aí e escolhe `main`. Uma release vai para o `main`, que é o ramo das versões entregues.

**c)** No título, cola:

```text
Release v0.5.0
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Não é preciso trocar nada:

```markdown
## O que muda

Prepara a versão 0.5.0.

- Versão passa de 0.4.0 para 0.5.0
- `CHANGELOG.md` com a secção da versão 0.5.0
- README atualizado: tabela de versões, dados de demonstração e secção nova sobre o budget

Este pull request vai para o `main`. A issue da release é fechada pelo pull request que leva a release de volta ao `develop`.

## Como testar

1. `python -m pytest` (707 testes)
2. `python -m sphinx -W -b html docs docs/_build/html`
3. `python -m gestor_campanhas`: o título mostra `v0.5.0`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 5 — Budget`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** Confirma o destino. Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.5.0`. Se disser `into develop`, **não avises ninguém ainda**: clica em **Edit**, à direita do título, clica em **base: develop**, escolhe `main`, confirma em **Change base** e clica em **Save**.

### Passo 36 — Avisa Fabio

Diz a Fabio que o pull request da release v0.5.0 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 18 a 25.

---

## Publicar a release v0.5.0 e pedir o regresso ao develop

Com a release no `main`, falta marcá-la com uma tag e levar os commits dela de volta ao `develop`.

### Passo 37 — Confirma que o main já tem a versão 0.5.0

Faz este passo quando Fabio te avisar que a release está no `main`.

A tag vai ser criada no `main`. Se o `main` ainda não tiver a versão nova, a tag fica a marcar o código da versão anterior. Foi o que aconteceu nas duas primeiras fases.

Abre https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py

**Deves ver** a linha `__version__ = "0.5.0"`.

Se vires outra versão, **não publiques a release**. O pull request foi junto ao `develop` em vez do `main`. Avisa Fabio e corrijam assim: abre https://github.com/Blive77/ADC-TrabGrupo/compare/main...develop?expand=1, cria um pull request com o título `Release v0.5.0`, Fabio aprova e junta, e só depois voltas a este passo.

### Passo 38 — Publica a release v0.5.0 no GitHub

Publicar a release cria a **tag**, uma etiqueta que marca para sempre o commit desta versão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/releases/new

**b)** Clica em **Choose a tag**, escreve `v0.5.0` e clica em **Create new tag: v0.5.0 on publish**.

**c)** Em **Target**, escolhe `main`.

**d)** Em **Release title**, cola:

```text
v0.5.0 — Budget
```

**e)** Na caixa de texto, cola:

````markdown
## Budget

O Cliente passa a pedir a alteração do budget das suas campanhas. O Marketeer responsável dá parecer e o Administrador decide. Cada campanha tem um histórico do budget, e o Administrador tem um resumo global do budget face à despesa.

### Acrescentado

- Pedidos de alteração de budget: o Cliente pede um valor e indica o motivo, na opção "Pedidos de campanha"
- Parecer do Marketeer sobre cada pedido, na opção nova "Pedidos de budget"
- Decisão do Administrador, na opção nova "Pedidos de budget": aprovar altera logo o budget; rejeitar pede o motivo
- Histórico do budget de cada campanha, para o Cliente e o Administrador
- Resumo global do budget por cliente, com as campanhas acima do budget em destaque
- Um pedido de budget de demonstração e o budget inicial das campanhas de demonstração no histórico

### Alterado

- "Definir budget" pede o motivo quando a campanha já tem budget, e recusa um valor igual ao atual
- As opções de pedidos do Cliente passam a dizer "de campanha" ou "de budget"
- Os menus do Marketeer e do Administrador ganharam opções; as que vinham a seguir mudaram de número

### User stories

C15, M16, A14, A15, C16 e A16.

Fica também concluída a parte de C06 adiada na versão 0.3.0. Os avisos sobre os pedidos de budget (C17 e M18) entram na versão 0.6.0, com as notificações.

### Como experimentar

```
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

Entrar com `cliente@empresa.pt` / `cliente12345` e escolher "Pedidos de campanha"; com `marketeer@agencia.pt` / `marketeer12345` e escolher "Pedidos de budget"; ou com `admin@agencia.pt` / `admin12345` e escolher "Pedidos de budget" ou "Resumo do budget". As outras contas de demonstração estão no README.
````

**f)** Clica em **Publish release**.

**Deves ver** a página da release, e a tag `v0.5.0` em https://github.com/Blive77/ADC-TrabGrupo/tags. Na linha da tag aparece o commit `Merge pull request ... from .../release/v0.5.0`. Se aparecer outro commit, o **Target** ficou errado: avisa o grupo antes de continuar.

### Passo 39 — Abre o pull request que leva a release para o develop

A release está no `main`, mas o `develop` ainda não tem os commits dela (a versão nova e o registo de alterações). Este pull request leva-os para lá, para os dois ramos ficarem alinhados.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/compare/develop...main

**b)** Confirma, no topo, que está **base: develop** e **compare: main**, e clica em **Create pull request**.

**c)** No título, cola:

```text
Juntar a release v0.5.0 ao develop
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue da release, que apontaste no início:

```markdown
## O que muda

Traz para o `develop` os commits da release v0.5.0, que já estão no `main`: a versão nova, o registo de alterações e o README.

Closes #N
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 5 — Budget`

**f)** Clica em **Create pull request**.

### Passo 40 — Avisa Fabio

Diz a Fabio que o pull request que leva a release v0.5.0 para o `develop` está aberto. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 26 a 29.

### Passo 41 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d release/v0.5.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d release/v0.5.0` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

### Passo 42 — Fecha a milestone da fase

Faz este passo depois de Fabio juntar o último pull request. Nessa altura a issue da release já está fechada, e a milestone fica com todas as issues fechadas.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/milestones

**b)** Na linha `Fase 5 — Budget`, confirma que a barra está a 100% e clica em **Close**.

Se a barra não estiver a 100%, clica no nome da milestone para ver que issues estão abertas. Uma issue fica aberta quando o pull request dela foi junto sem `Closes #número`. Para a fechar à mão, abre a issue, escreve na caixa de comentário `Resolvida pelo pull request #N` (com o número do pull request) e clica em **Close with comment**. Depois volta a este passo.

---

## Outras tarefas desta fase

### Passo 43 — Atualiza a página inicial da wiki

A página inicial passa a indicar a versão 0.5.0.

Faz este passo no fim da fase, depois de publicares a release.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 0.5.0` e clica em **Save page**.

**Deves ver** a linha `Versão atual: v0.5.0 (Fase 5 — Budget).`

### Passo 44 — Atualiza a página "Registo das fases" da wiki

A página ganha a secção da Fase 5: quem fez e quem reviu cada unidade, e as decisões tomadas.

Faz este passo no fim da fase, depois de a release v0.5.0 estar publicada.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Registo das fases** na lista de páginas, à direita, e depois em **Edit**.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Registar a Fase 5` e clica em **Save page**.

**Deves ver** a secção `Fase 5 — Budget`, com a tabela das cinco unidades.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 5.1 — Pedido de alteração de budget

- **`gestor_campanhas/bd.py`** ganha a tabela `pedidos_budget`. A coluna `campanha_id` tem `ON DELETE CASCADE`: se a campanha for apagada, os pedidos dela são apagados com ela (ao contrário dos criativos, que impedem apagar a campanha). A tabela não tem a coluna do cliente: o cliente é sempre o da campanha. Já tem as colunas do parecer (`parecer_viavel`, `parecer_justificacao`) e da decisão (`motivo_rejeicao`, `decidido_em`), que só vão ser usadas nas unidades 5.2 e 5.3, pela mesma razão da Fase 4: o `CREATE TABLE IF NOT EXISTS` não acrescenta colunas a uma tabela que já existe.
- **`gestor_campanhas/modelos.py`** ganha a classe `PedidoBudget`. Usa os mesmos estados de um `PedidoCampanha`. Guarda `budget_atual_centimos`, o budget que a campanha tinha quando o pedido foi feito: assim, a lista continua a mostrar de onde se partiu mesmo depois de o budget mudar. A propriedade `nome_parecer` escreve o parecer como aparece no ecrã (`Por dar`, `Viável` ou `Não viável`).
- **`gestor_campanhas/repositorios/pedidos_budget.py`** é novo. A consulta `_SELECIONAR` junta o pedido à campanha e a duas cópias da tabela `utilizadores` (uma para o cliente, outra para o marketeer), para trazer os nomes de uma vez. `obter_por_decidir` procura o pedido pendente ou em análise de uma campanha.
- **`gestor_campanhas/servicos/budget.py`** é novo e tem as regras. `campanha_para_pedido` confirma que a campanha é do cliente, que não terminou e que não tem outro pedido por decidir; o menu chama-a logo depois de o cliente escolher a campanha, para avisar antes de pedir o valor. `pedir` volta a fazer as mesmas verificações e valida o valor (com `budget_validado`, das campanhas) e o motivo.
- **`gestor_campanhas/cli/budget.py`** é novo: os ecrãs de pedir, ver e cancelar um pedido de budget. A função `valor` escreve `Por definir` quando não há valor.
- **`gestor_campanhas/cli/pedidos.py`**: `do_cliente` passa a mostrar as duas listas (`mostrar_todos_do_cliente`), e a lista `ACOES` ganha as três opções novas, que chamam as funções de `cli/budget.py`. As três opções antigas ganham "de campanha" no nome, porque os dois tipos de pedido têm numerações próprias.
- **`gestor_campanhas/cli/campanhas.py`**: a lista das campanhas do Cliente diz onde se pede outro valor de budget.
- **`gestor_campanhas/dados_demo.py`** ganha `PEDIDOS_BUDGET` e `criar_pedidos_budget`, com o pedido da Carla para a campanha `Natal 2026`.
- **`tests/test_budget.py`** é novo: base de dados, regras, ecrãs e dados de demonstração. `tests/test_bd.py` testa a tabela nova, incluindo o `ON DELETE CASCADE`.
- **`docs/`**: o guia de utilização explica os pedidos de budget do Cliente, a arquitetura ganha a tabela nova, e a referência os três módulos novos.

### Unidade 5.4 — Resumo global do budget

- **`gestor_campanhas/servicos/budget.py`** ganha o resumo. Não há tabela nova: tudo é calculado na altura, a partir das campanhas e da despesa, como a despesa da Fase 4.
  - `campanhas_com_despesa` junta cada campanha à sua despesa, com as duas consultas de sempre (`campanhas.listar_todas` e `criativos.despesas`), e ordena-as pelo nome do cliente. As outras funções trabalham sobre esta lista.
  - `ResumoCliente` é uma `dataclass` com as contas de um cliente. O restante é uma propriedade (`restante_centimos`), calculada a partir do budget e da despesa, para nunca ficar desencontrado deles.
  - `resumo_por_cliente` percorre as campanhas e vai somando no resumo do cliente de cada uma (`setdefault` cria o resumo na primeira campanha de cada cliente). Um cliente sem campanhas não aparece.
  - `acima_do_budget` é a regra num só sítio: uma campanha sem budget nunca está acima do budget.
  - `somar` faz a linha do total; `campanhas_acima_do_budget` e `campanhas_do_cliente` filtram a lista.
- **`gestor_campanhas/cli/budget.py`** ganha `resumo`, o ciclo do menu, `mostrar_resumo` (a tabela por cliente e os totais), `mostrar_campanhas_com_despesa` (a tabela das campanhas, usada no destaque e no detalhe de um cliente) e `situacao`, que escreve a última coluna.
- **`gestor_campanhas/cli/perfis.py`**: o menu do Administrador ganha "Resumo do budget", a seguir a "Campanhas".
- **`tests/test_resumo_budget.py`** é novo. A fixture `campanhas_demo` monta um caso com uma campanha sem budget e outra acima do budget, e os testes conferem as contas e os ecrãs.
- **`docs/`**: o guia de utilização ganha a secção "Resumo do budget", e a arquitetura a secção "Resumo global do budget".

### Unidade 5.5 — Release v0.5.0

- **`gestor_campanhas/__init__.py`**: `__version__` passa para `"0.5.0"`. O menu inicial, o `pyproject.toml` e a documentação leem a versão daqui.
- **`CHANGELOG.md`** ganha a secção `v0.5.0`, por cima das anteriores. A parte "Alterado" regista o que pode surpreender quem já usava a versão 0.4.0: o motivo em "Definir budget", os nomes novos das opções de pedidos do Cliente e os números novos das opções dos menus.
- **`README.md`**: a tabela de versões ganha uma linha, o exemplo do menu passa a mostrar `v0.5.0`, os dados de demonstração incluem o pedido de budget, e há uma secção nova, `Budget`, com o caminho de um pedido e o que cada perfil faz.
- **O caminho de uma release** é o mesmo das fases anteriores: o pull request do ramo `release/v0.5.0` para o `main`; a confirmação de que o `main` já tem a versão 0.5.0; a publicação da release, que cria a tag no `main`; o pull request do `main` para o `develop`; e o fecho da milestone.
