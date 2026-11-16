# Fase 3 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 3 (Campanhas e pedidos), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 3.2 (de Fabio) | Quando Fabio avisar |
| 8 a 17 | Fazer a unidade 3.3 — Pedidos de nova campanha | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 3.4 (de Ricardo) | Quando Ricardo avisar |
| 25 | Atualiza a página "Guia de utilização" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 3.2 — Campanhas atribuídas e eliminar campanha

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 3.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Campanhas atribuídas e eliminar campanha**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (M04, M05), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Fabio para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/3.2-campanhas-atribuidas-eliminar
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/3.2-campanhas-atribuidas-eliminar` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/3.2-campanhas-atribuidas-eliminar'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `274 passed`.

Cria as campanhas de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver** a linha `Campanhas criadas: 3 (as restantes já existiam).`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`) e escolhe `1` (Campanhas). **Deves ver** pelo menos estas duas campanhas. Os números da primeira coluna podem ser outros e, se criaste campanhas quando reviste a unidade 3.1, essas também aparecem:

```text
N.º  Nome               Cliente        Início      Fim         Budget      Estado
---  -----------------  -------------  ----------  ----------  ----------  -----------
1    Natal 2026         Carla Cliente  2026-12-01  2026-12-24  1 500,00 €  Por começar
2    Regresso às aulas  José Padeiro   2026-09-01  2026-09-30  800,00 €    Terminada

2 campanhas.
```

Por baixo, o menu tem agora quatro opções: `1. Criar campanha`, `2. Editar campanha`, `3. Ver campanha` e `4. Eliminar campanha`.

Vê os detalhes de uma campanha:

| Escreves | Deves ver |
|---|---|
| `3` e Enter | O título `Ver campanha` e a pergunta `Número da campanha (Enter para cancelar)` |
| O número da campanha `Natal 2026` | Os dados da campanha, um por linha, com `Objetivo:  Aumentar as vendas de dezembro` e `Estado:    Por começar` |
| Enter | A tabela outra vez |

Cria uma campanha só para a apagar. Escolhe `1`, escreve o número de um cliente, o nome `Para apagar` e carrega em Enter nas três perguntas seguintes. **Deves ver** `Campanha criada com o número ...`. Carrega em Enter e aponta o número da campanha `Para apagar`. Na tabela, ela aparece com o budget `Por definir` e o estado `Em curso`.

Agora elimina-a:

| Escreves | Deves ver |
|---|---|
| `4` e Enter | O título `Eliminar campanha` e a pergunta `Número da campanha (Enter para cancelar)` |
| O número da campanha `Para apagar` | Os dados da campanha, o aviso `Uma campanha eliminada não pode ser recuperada.` e a pergunta `Eliminar esta campanha? (s/n)` |
| `n` | `Nada foi alterado.` |
| Enter, `4`, o mesmo número, `s` | `A campanha Para apagar foi eliminada.` |
| Enter | A tabela, já sem a campanha `Para apagar` |

Sai com `0`, `0` e `0`.

Confirma também:

- Corre `python -m gestor_campanhas.dados_demo` duas vezes: da segunda vez aparece `Campanhas criadas: 0 (as restantes já existiam).`
- Entra como `marta@agencia.pt` / `marta12345` e escolhe `1`: aparece só a campanha `Bicicletas de primavera`, com o budget `Por definir` e o estado `Em curso`.
- Ainda como Marta, escolhe `4` e escreve o número da campanha `Natal 2026`: aparece `Não tem nenhuma campanha com o número ...`, porque a campanha é de outro marketeer.
- Na opção `3`, carrega em Enter sem escrever um número: volta à lista.

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

**f)** No Trello, move os cards das stories M04 e M05 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/3.2-campanhas-atribuidas-eliminar
python ../ctesp-ADC/verificar.py 3.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/3.2-campanhas-atribuidas-eliminar` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 3.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 3.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 3.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 3.3 — Pedidos de nova campanha

O Cliente ganha a opção "Pedidos de campanha": faz um pedido de nova campanha, acompanha o estado dos seus pedidos e cancela os que ainda estão pendentes. Há dois pedidos de demonstração.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Campanhas atribuídas e eliminar campanha** (unidade 3.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 3.3

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 3 issues: C05, C06, C07. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C05** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC05%5D%22

```markdown
- [ ] O menu do Cliente tem a opção "Pedidos de campanha", com a opção "Novo pedido"
- [ ] São pedidos o objetivo, o orçamento em euros, o prazo pretendido (`AAAA-MM-DD`) e as plataformas
- [ ] O objetivo é obrigatório, o orçamento tem de ser maior do que zero e o prazo não pode ser um dia que já passou
- [ ] As plataformas são escolhidas de uma lista numerada, e tem de ser escolhida pelo menos uma
- [ ] O pedido fica registado no estado "Pendente"
- [ ] Com dados inválidos aparece a mensagem do erro e o pedido não é registado
```

**Issue C06** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC06%5D%22

```markdown
- [ ] A lista mostra os pedidos do cliente, do mais recente para o mais antigo, com a data, o objetivo, o orçamento, o prazo e o estado
- [ ] Os estados são Pendente, Em análise, Aprovado, Rejeitado e Cancelado
- [ ] A opção "Ver pedido" mostra todos os dados de um pedido; num pedido rejeitado mostra o motivo
- [ ] Um cliente só vê os seus pedidos
- [ ] Os pedidos de alteração de budget entram na Fase 5
```

**Issue C07** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC07%5D%22

```markdown
- [ ] A opção "Cancelar pedido" pede o número do pedido, mostra os dados dele e pede uma confirmação (s/n)
- [ ] Só um pedido "Pendente" pode ser cancelado; nos outros estados aparece uma mensagem a explicar
- [ ] Sem confirmação, nada é alterado
- [ ] O pedido cancelado continua na lista, com o estado "Cancelado"
```

Por fim, no quadro Trello, move os cards das stories C05, C06 e C07 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/3.3-pedidos-de-campanha
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/3.3-pedidos-de-campanha` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/3.3-pedidos-de-campanha'`.

### Passo 11 — Copia e grava os 9 commits

São 9 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 3.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 3.3. Eles estão na pasta `ctesp-ADC/fase-3/ficheiros/3.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela dos pedidos de campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 25 insertions(+)`.

**Commit 2 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/modelos.py`.

```bash
git add -A
git commit -m "feat(modelos): acrescentar a classe PedidoCampanha"
```

**Deves ver** uma linha a terminar em `1 file changed, 62 insertions(+), 1 deletion(-)`.

**Commit 3 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/pedidos.py`, `tests/test_pedidos.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar e ler pedidos de campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 202 insertions(+)`.

**Commit 4 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/pedidos.py`, `tests/test_pedidos.py`.

```bash
git add -A
git commit -m "feat(pedidos): pedir uma campanha nova"
```

**Deves ver** uma linha a terminar em `2 files changed, 151 insertions(+)`.

**Commit 5 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/pedidos.py`, `tests/test_pedidos.py`.

```bash
git add -A
git commit -m "feat(pedidos): cancelar um pedido pendente"
```

**Deves ver** uma linha a terminar em `2 files changed, 54 insertions(+)`.

**Commit 6 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 6
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/pedidos.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_pedidos.py`.

```bash
git add -A
git commit -m "feat(cli): menu de pedidos de campanha do cliente"
```

**Deves ver** uma linha a terminar em `3 files changed, 201 insertions(+), 2 deletions(-)`.

**Commit 7 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 7
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/pedidos.py`, `tests/test_pedidos.py`.

```bash
git add -A
git commit -m "feat(cli): ver e cancelar um pedido de campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 154 insertions(+)`.

**Commit 8 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 8
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dados_demo.py`, `tests/test_pedidos.py`.

```bash
git add -A
git commit -m "feat(demo): acrescentar pedidos de campanha de demonstração"
```

**Deves ver** uma linha a terminar em `2 files changed, 71 insertions(+), 5 deletions(-)`.

**Commit 9 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.3 9
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os pedidos de campanha do cliente"
```

**Deves ver** uma linha a terminar em `3 files changed, 104 insertions(+), 4 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 3.3
git log --oneline -9
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 3.3` | `Tudo certo: o ramo 'feature/3.3-pedidos-de-campanha' está igual ao original no fim da unidade 3.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -9` | Os teus 9 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os pedidos de campanha do cliente
xxxxxxx feat(demo): acrescentar pedidos de campanha de demonstração
xxxxxxx feat(cli): ver e cancelar um pedido de campanha
xxxxxxx feat(cli): menu de pedidos de campanha do cliente
xxxxxxx feat(pedidos): cancelar um pedido pendente
xxxxxxx feat(pedidos): pedir uma campanha nova
xxxxxxx feat(repositorios): guardar e ler pedidos de campanha
xxxxxxx feat(modelos): acrescentar a classe PedidoCampanha
xxxxxxx feat(bd): criar a tabela dos pedidos de campanha
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `312 passed`.

Cria os pedidos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver** a linha `Pedidos de campanha criados: 2 (os restantes já existiam).`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como cliente (`1`, depois `cliente@empresa.pt` e `cliente12345`) e escolhe `1` (Pedidos de campanha). **Deves ver** `Ainda não fez nenhum pedido.` e o menu, com as opções `1. Novo pedido`, `2. Ver pedido` e `3. Cancelar pedido`.

Faz um pedido:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Novo pedido de campanha` e a pergunta `Objetivo da campanha` |
| `Promover os saldos de janeiro` | A pergunta `Orçamento em euros (por exemplo 1500 ou 1500,50)` |
| `750,50` | A pergunta `Prazo pretendido (AAAA-MM-DD)` |
| `2027-01-10` | A lista das seis plataformas, numeradas, e a pergunta `Números das plataformas, separados por vírgulas (por exemplo 1,2)` |
| `1,2` | `Pedido registado com o número .... Fica pendente até ser analisado.` |
| Enter | Uma tabela com a linha `Promover os saldos de janeiro  750,50 €   2027-01-10  Pendente` |

Aponta o número que aparece na primeira coluna. Vê o pedido:

| Escreves | Deves ver |
|---|---|
| `2` e Enter | O título `Ver pedido` e a pergunta `Número do pedido (Enter para cancelar)` |
| O número do pedido | Os dados do pedido, um por linha, com `Plataformas:  Facebook, Instagram` e `Estado:       Pendente` |
| Enter | A tabela outra vez |

Cancela o pedido:

| Escreves | Deves ver |
|---|---|
| `3` e Enter | O título `Cancelar pedido` e a pergunta `Número do pedido (Enter para cancelar)` |
| O número do pedido | Os dados do pedido e a pergunta `Cancelar este pedido? (s/n)` |
| `n` | `Nada foi alterado.` |
| Enter, `3`, o mesmo número, `s` | `Pedido cancelado.` |
| Enter | A tabela, com `Cancelado` na coluna `Estado` |

Sai com `0`, `0` e `0`.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/3.3-pedidos-de-campanha
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/3.3-pedidos-de-campanha -> feature/3.3-pedidos-de-campanha`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/3.3-pedidos-de-campanha?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/3.3-pedidos-de-campanha**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Pedidos de nova campanha
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Cliente passa a poder pedir campanhas novas, acompanhar o estado dos pedidos e cancelar os que ainda estão pendentes.

- Tabela `pedidos_campanha` e classe `PedidoCampanha`, com cinco estados
- Lista fixa de plataformas, escolhidas por número
- Regras para pedir (objetivo, orçamento, prazo, plataformas) e para cancelar (só pedidos pendentes)
- Opção "Pedidos de campanha" no menu do Cliente, com "Novo pedido", "Ver pedido" e "Cancelar pedido"
- Dois pedidos de demonstração

A decisão dos pedidos pelo Administrador é a unidade 3.4.

Closes #(número da issue C05)
Closes #(número da issue C06)
Closes #(número da issue C07)

## Como testar

1. `python -m pytest` (312 testes)
2. `python -m gestor_campanhas`, entrar como cliente e escolher "Pedidos de campanha"
3. Fazer um pedido, vê-lo e cancelá-lo
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories C05, C06 e C07 para **Ready to Verify**.

### Passo 16 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 3.3 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 11 a 17.

### Passo 17 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/3.3-pedidos-de-campanha
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/3.3-pedidos-de-campanha` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 3.4 — Decidir pedidos, budget e marketeer responsável

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 3.4 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Decidir pedidos, budget e marketeer responsável**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 3 linhas `Closes #` seguida de um número, uma por issue (A11, A12, A13), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Ricardo para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/3.4-decisao-budget-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/3.4-decisao-budget-marketeer` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/3.4-decisao-budget-marketeer'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `370 passed`.

Garante que tens as campanhas e os pedidos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`). O menu tem agora sete opções: `3` é `Pedidos de campanha` e `4` é `Campanhas`.

Escolhe `3`. **Deves ver** uma tabela com, pelo menos, os pedidos `Divulgar o bolo-rei no Natal` (de José Padeiro) e `Dar a conhecer a loja nova de Faro` (de Beatriz Lopes), os dois `Pendente`. Aponta os números dos dois.

Aprova o primeiro:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Analisar pedido` e a pergunta `Número do pedido (Enter para cancelar)` |
| O número do pedido `Divulgar o bolo-rei no Natal` | Os dados do pedido, com `Estado:       Em análise`, e o menu `Decisão` |
| `1` | O título `Aprovar pedido` e a pergunta `Nome da campanha` |
| `Bolo-rei 2026` | A pergunta `Budget inicial em euros [600,00 €]` |
| Enter | A tabela dos marketeers e a pergunta `Número do marketeer responsável (Enter para cancelar)` |
| O número que está na linha de `Marta Marques` | `Pedido aprovado. Foi criada a campanha n.º ...` e `O cliente e o marketeer foram avisados por email.` |
| Enter | A tabela dos pedidos, com esse pedido no fim e o estado `Aprovado` |

Rejeita o segundo:

| Escreves | Deves ver |
|---|---|
| `1`, e depois o número do pedido `Dar a conhecer a loja nova de Faro` | Os dados do pedido e o menu `Decisão` |
| `2` | O título `Rejeitar pedido` e a pergunta `Motivo da rejeição` |
| `O orçamento não chega para as duas plataformas` | A pergunta `Rejeitar este pedido? (s/n)` |
| `s` | `Pedido rejeitado. O cliente foi avisado por email.` |
| Enter | A tabela dos pedidos, com esse pedido no estado `Rejeitado` |

Sai dos pedidos com `0` e escolhe `4` (Campanhas). **Deves ver** uma tabela com as campanhas de todos os marketeers, incluindo a `Bolo-rei 2026`, que acabou de ser criada, com o budget `600,00 €` e a marketeer `Marta Marques`. Aponta o número da campanha `Bicicletas de primavera`.

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Definir budget` e a pergunta `Número da campanha (Enter para cancelar)` |
| O número da campanha `Bicicletas de primavera` | `Campanha Bicicletas de primavera, de Beatriz Lopes. Budget atual: Por definir.` e a pergunta `Budget em euros (por exemplo 1500 ou 1500,50)` |
| `900` | `Budget definido: 900,00 €.` |
| Enter, `2` | O título `Atribuir marketeer` |
| O número da campanha `Bicicletas de primavera` | `Responsável atual: Marta Marques.` e a tabela dos marketeers |
| O número que está na linha de `Miguel Marketeer` | `A campanha passou para Miguel Marketeer, que foi avisado por email.` |
| Enter | A tabela, com `Miguel Marketeer` e `900,00 €` na linha de `Bicicletas de primavera` |

Sai das campanhas com `0` e escolhe `2` (Marketeers). **Deves ver** a coluna nova `Campanhas ativas`. Tenta desativar o Miguel:

| Escreves | Deves ver |
|---|---|
| `4`, e depois o número que está na linha de `Miguel Marketeer` | `Miguel Marketeer (marketeer@agencia.pt) tem a conta ativa.` e a pergunta `Desativar a conta? (s/n)` |
| `s` | `Miguel Marketeer é responsável por 2 campanhas que ainda não terminaram. Atribua-as a outro marketeer antes de desativar a conta. Nada foi alterado.` (o número de campanhas pode ser outro) |

Sai com Enter, `0`, `0` e `0`.

Por fim, vê os emails:

```bash
ls dados/caixa_saida
```

**Deves ver**, entre outros, ficheiros cujo nome acaba em `jose_padaria.pt.txt`, `marta_agencia.pt.txt`, `beatriz_bicicletas.pt.txt` e `marketeer_agencia.pt.txt`. Abre o de `beatriz_bicicletas.pt`: tem o motivo da rejeição.

Confirma também:

- Entra como administrador e escolhe `3`. Em "Analisar pedido", escreve o número de um pedido já aprovado ou rejeitado: aparecem os dados e `Este pedido já não pode ser decidido.`, sem o menu `Decisão`.
- Em "Analisar pedido", escreve `999`: aparece `Não existe nenhum pedido com o número 999.`
- Em `4` (Campanhas), "Definir budget", escreve o número de uma campanha e o valor `zero`: aparece `O valor não é válido. Exemplos de valores válidos: 1500 ou 1500,50. O budget não foi alterado.`
- Em "Atribuir marketeer", escolhe o marketeer que já é o responsável: aparece `... já é responsável por esta campanha. O responsável não foi alterado.`
- Em `1` (Clientes), a tabela tem a coluna `Campanhas ativas`.
- Sai e entra como `jose@padaria.pt` / `jose12345`. Se aprovaste o pedido dele, em "Pedidos de campanha" o pedido aparece `Aprovado`, e a opção "Ver pedido" mostra a linha `Campanha:     n.º ...`.

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

**f)** No Trello, move os cards das stories A11, A12 e A13 para **Ready**.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/3.4-decisao-budget-marketeer
python ../ctesp-ADC/verificar.py 3.4
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/3.4-decisao-budget-marketeer` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 3.4` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 3.4 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 3.4.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Ricardo](ricardo.md)).

Diz também a Fabio que já pode avançar ([página de Fabio](fabio.md), passos 18 a 27).

---

## Outras tarefas desta fase

### Passo 25 — Atualiza a página "Guia de utilização" da wiki

A página passa a explicar as campanhas e os pedidos de campanha, com o que cada perfil pode fazer.

Faz este passo depois de a unidade 3.5 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Guia-de-utilizacao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Guia de utilização** na lista de páginas, à direita, e depois em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar o Guia de utilização para a versão 0.3.0` e clica em **Save page**.

**Deves ver** a página com as secções novas `Como nasce uma campanha`, `Campanhas (Marketeer)`, `Pedidos de campanha (Cliente)`, `Pedidos de campanha (Administrador)`, `Campanhas (Administrador)` e `Campanhas (Cliente)`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 3.3 — Pedidos de nova campanha

- **`gestor_campanhas/bd.py`** ganha a tabela `pedidos_campanha`. A coluna `estado` tem um `CHECK` com os cinco estados possíveis: a base de dados recusa qualquer outro valor. A coluna `campanha_id` aponta para a campanha criada quando o pedido é aprovado e tem `ON DELETE SET NULL`: se essa campanha for eliminada, o pedido não é apagado, fica só sem a ligação. As colunas `motivo_rejeicao` e `campanha_id` só vão ser preenchidas na unidade 3.4.
- **`gestor_campanhas/modelos.py`** ganha os cinco estados de um pedido, o dicionário `NOMES_ESTADOS_PEDIDO` (o nome que aparece no ecrã, por exemplo `"Em análise"`), a lista `PLATAFORMAS` e a classe `PedidoCampanha`. A lista de plataformas dentro da classe usa `field(default_factory=list)`: é a forma de dar a cada pedido a sua própria lista vazia.
- **`gestor_campanhas/repositorios/pedidos.py`** é novo. As plataformas são guardadas num só texto, separadas por vírgulas, e voltam a ser uma lista ao ler. Os pedidos de um cliente são lidos com `ORDER BY ... DESC`, para o mais recente aparecer primeiro.
- **`gestor_campanhas/servicos/pedidos.py`** é novo e tem as regras.
  - `criar` valida os quatro dados pela ordem em que são pedidos. O orçamento passa por `dinheiro.para_centimos`, da unidade 3.2. O prazo é comparado com `relogio.hoje()`: o próprio dia é aceite, um dia anterior não.
  - `_plataformas_validadas` tira as repetições e põe as plataformas pela ordem da lista `PLATAFORMAS`, escolha o cliente a ordem que escolher.
  - `cancelar` só aceita pedidos pendentes. O pedido não é apagado: passa ao estado "Cancelado", para o cliente continuar a ver o que pediu.
- **`gestor_campanhas/cli/pedidos.py`** é novo. `ler_plataformas` mostra a lista numerada e repete a pergunta enquanto a resposta não for uma lista de números válidos. `resumir` corta os objetivos com mais de 40 caracteres, para a tabela não ficar demasiado larga; o texto completo vê-se em "Ver pedido".
- **Porque é que o ecrã de cancelar verifica o estado antes de perguntar.** A regra está no serviço, mas o ecrã olha primeiro para o estado para não pedir uma confirmação que depois ia dar erro.
- **`tests/test_pedidos.py`** tem uma fixture `autouse` que fixa o dia em 16 de novembro de 2026. Sem isso, os testes do prazo deixavam de passar com o passar do tempo.
- **Estados "Em análise", "Aprovado" e "Rejeitado".** Já existem e já aparecem na lista, mas ainda nada põe um pedido nesses estados: é o Administrador que o faz, na unidade 3.4.
