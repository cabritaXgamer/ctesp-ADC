# Fase 3 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 3 (Campanhas e pedidos), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 3.1 (de Ricardo) | Quando Ricardo avisar |
| 8 a 17 | Fazer a unidade 3.2 — Campanhas atribuídas e eliminar campanha | A seguir ao teu passo anterior |
| 18 a 27 | Fazer a unidade 3.5 — Campanhas do cliente e marketeer responsável | Quando Tomas avisar |
| 28 a 35 | Rever a release v0.3.0 e juntá-la ao main | Quando Ricardo avisar |
| 36 a 39 | Juntar a release v0.3.0 ao develop | Quando Ricardo avisar |
| 40 | Atualiza a página "Arquitetura" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 3.1 — Criar e editar campanhas

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 3.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Criar e editar campanhas**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (M02, M03), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Ricardo para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/3.1-criar-editar-campanha
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/3.1-criar-editar-campanha` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/3.1-criar-editar-campanha'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `234 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`) e escolhe `1` (Campanhas). **Deves ver** `Ainda não tem campanhas.` e o menu `Campanhas`, com as opções `1. Criar campanha` e `2. Editar campanha`.

Cria uma campanha:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Criar campanha`, uma tabela com os três clientes e a pergunta `Número do cliente (Enter para cancelar)` |
| O número que está na primeira coluna da linha de `Carla Cliente` | A pergunta `Nome da campanha` |
| `Dia da Mãe` | A pergunta `Objetivo (opcional)` |
| `Vender cabazes` | A pergunta `Data de início (AAAA-MM-DD, opcional)` |
| `2027-04-20` | A pergunta `Data de fim (AAAA-MM-DD, opcional)` |
| `2027-05-02` | `Campanha criada com o número ..., para Carla Cliente.` |
| Enter | Uma tabela com a linha `Dia da Mãe  Carla Cliente  2027-04-20  2027-05-02` |

Aponta o número que aparece na primeira coluna da linha de `Dia da Mãe`. Agora edita essa campanha:

| Escreves | Deves ver |
|---|---|
| `2` e Enter | O título `Editar campanha` e a pergunta `Número da campanha (Enter para cancelar)` |
| O número da campanha `Dia da Mãe` | `A editar a campanha Dia da Mãe, de Carla Cliente.` e a pergunta `Nome [Dia da Mãe]` |
| Enter | A pergunta `Objetivo [Vender cabazes]` |
| `Vender cabazes e flores` | A pergunta `Data de início (AAAA-MM-DD) [2027-04-20]` |
| Enter | A pergunta `Data de fim (AAAA-MM-DD) [2027-05-02]` |
| `-` | `Campanha guardada.` |
| Enter | A tabela, com `-` na coluna `Fim` da linha de `Dia da Mãe` |

Sai com `0`, `0` e `0`.

Confirma também:

- Entra como marketeer, escolhe `1` e depois `1` (Criar campanha). No número do cliente escreve `1` (é o administrador): no fim das perguntas aparece `Não existe nenhum cliente com o número 1. A campanha não foi criada.`
- Cria uma campanha com a data de início `2027-05-10` e a data de fim `2027-05-01`: aparece `A data de fim não pode ser anterior à data de início. A campanha não foi criada.`
- Cria uma campanha com a data de início `10-05-2027`: aparece `A data de início não é válida.`
- Na opção "Editar campanha", escreve `999`: aparece `Não tem nenhuma campanha com o número 999.`
- Sai e entra como `marta@agencia.pt` / `marta12345`. Em "Campanhas" **não** aparece a campanha criada pelo outro marketeer.

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

**f)** No Trello, move os cards das stories M02 e M03 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/3.1-criar-editar-campanha
python ../ctesp-ADC/verificar.py 3.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/3.1-criar-editar-campanha` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 3.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 3.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 3.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Ricardo](ricardo.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 3.2 — Campanhas atribuídas e eliminar campanha

A lista de campanhas do Marketeer fica completa: passa a mostrar o budget e o estado de cada campanha. O Marketeer ganha as opções "Ver campanha" e "Eliminar campanha". Há três campanhas de demonstração.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Criar e editar campanhas** (unidade 3.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 3.2

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: M04, M05. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue M04** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM04%5D%22

```markdown
- [ ] A lista mostra, por campanha, o número, o nome, o cliente, as datas de início e de fim, o budget e o estado
- [ ] O budget aparece em euros (por exemplo `1 500,00 €`), ou `Por definir` se ainda não foi atribuído
- [ ] O estado é calculado a partir das datas: `Por começar`, `Em curso` ou `Terminada`
- [ ] Um marketeer só vê as campanhas que lhe estão atribuídas
- [ ] A opção "Ver campanha" mostra todos os dados de uma campanha, incluindo o objetivo
- [ ] O budget restante e o número de criativos por estado entram na Fase 4, quando existirem criativos
```

**Issue M05** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM05%5D%22

```markdown
- [ ] A opção "Eliminar campanha" pede o número da campanha, mostra os dados dela e pede uma confirmação (s/n)
- [ ] Sem confirmação, nada é alterado
- [ ] Um marketeer só elimina as suas campanhas
- [ ] A campanha eliminada deixa de aparecer na lista
- [ ] A verificação de que a campanha não tem criativos entra na Fase 4, quando existirem criativos
```

Por fim, no quadro Trello, move os cards das stories M04 e M05 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/3.2-campanhas-atribuidas-eliminar
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/3.2-campanhas-atribuidas-eliminar` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/3.2-campanhas-atribuidas-eliminar'`.

### Passo 11 — Copia e grava os 7 commits

São 7 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 3.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 3.2. Eles estão na pasta `ctesp-ADC/fase-3/ficheiros/3.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 7**

```bash
python ../ctesp-ADC/copiar.py 3.2 1
```

**Deves ver** `Copiados 4 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `gestor_campanhas/dinheiro.py`, `tests/test_dinheiro.py`.

```bash
git add -A
git commit -m "feat(dinheiro): converter e formatar valores em euros"
```

**Deves ver** uma linha a terminar em `4 files changed, 92 insertions(+)`.

**Commit 2 de 7**

```bash
python ../ctesp-ADC/copiar.py 3.2 2
```

**Deves ver** `Copiados 4 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/relogio.py`, `gestor_campanhas/servicos/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(campanhas): calcular o estado a partir das datas"
```

**Deves ver** uma linha a terminar em `4 files changed, 68 insertions(+), 4 deletions(-)`.

**Commit 3 de 7**

```bash
python ../ctesp-ADC/copiar.py 3.2 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(cli): mostrar o budget, o estado e os detalhes das campanhas"
```

**Deves ver** uma linha a terminar em `2 files changed, 121 insertions(+), 3 deletions(-)`.

**Commit 4 de 7**

```bash
python ../ctesp-ADC/copiar.py 3.2 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/campanhas.py`, `gestor_campanhas/servicos/campanhas.py`.

```bash
git add -A
git commit -m "feat(campanhas): eliminar uma campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 24 insertions(+)`.

**Commit 5 de 7**

```bash
python ../ctesp-ADC/copiar.py 3.2 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(cli): opção para eliminar uma campanha, com confirmação"
```

**Deves ver** uma linha a terminar em `2 files changed, 82 insertions(+), 1 deletion(-)`.

**Commit 6 de 7**

```bash
python ../ctesp-ADC/copiar.py 3.2 6
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dados_demo.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(demo): acrescentar campanhas de demonstração"
```

**Deves ver** uma linha a terminar em `2 files changed, 97 insertions(+), 6 deletions(-)`.

**Commit 7 de 7**

```bash
python ../ctesp-ADC/copiar.py 3.2 7
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar a lista, os detalhes e a eliminação de campanhas"
```

**Deves ver** uma linha a terminar em `2 files changed, 42 insertions(+), 6 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 3.2
git log --oneline -7
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 3.2` | `Tudo certo: o ramo 'feature/3.2-campanhas-atribuidas-eliminar' está igual ao original no fim da unidade 3.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -7` | Os teus 7 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar a lista, os detalhes e a eliminação de campanhas
xxxxxxx feat(demo): acrescentar campanhas de demonstração
xxxxxxx feat(cli): opção para eliminar uma campanha, com confirmação
xxxxxxx feat(campanhas): eliminar uma campanha
xxxxxxx feat(cli): mostrar o budget, o estado e os detalhes das campanhas
xxxxxxx feat(campanhas): calcular o estado a partir das datas
xxxxxxx feat(dinheiro): converter e formatar valores em euros
```

### Passo 13 — Experimenta o que gravaste

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

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/3.2-campanhas-atribuidas-eliminar
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/3.2-campanhas-atribuidas-eliminar -> feature/3.2-campanhas-atribuidas-eliminar`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/3.2-campanhas-atribuidas-eliminar?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/3.2-campanhas-atribuidas-eliminar**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Campanhas atribuídas e eliminar campanha
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

A lista de campanhas do Marketeer passa a mostrar o budget e o estado, e há duas opções novas: ver os detalhes e eliminar uma campanha.

- Módulo `dinheiro`, que converte valores em euros para cêntimos e vice-versa
- Estado da campanha (por começar, em curso, terminada), calculado a partir das datas
- Opções "Ver campanha" e "Eliminar campanha", esta com pedido de confirmação
- Três campanhas de demonstração

O budget restante, o número de criativos por estado e a verificação "sem criativos" dependem dos criativos e ficam para a Fase 4.

Closes #(número da issue M04)
Closes #(número da issue M05)

## Como testar

1. `python -m pytest` (274 testes)
2. `python -m gestor_campanhas.dados_demo`
3. `python -m gestor_campanhas`, entrar como marketeer e escolher "Campanhas"
4. Ver uma campanha; criar uma campanha e eliminá-la
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories M04 e M05 para **Ready to Verify**.

### Passo 16 — Avisa Tomas

Diz a Tomas que o pull request da unidade 3.2 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 1 a 7.

### Passo 17 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/3.2-campanhas-atribuidas-eliminar
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/3.2-campanhas-atribuidas-eliminar` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Fazer a unidade 3.5 — Campanhas do cliente e marketeer responsável

O Cliente ganha a opção "Campanhas": vê as suas campanhas, com o budget de cada uma, e os contactos do marketeer responsável.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Decidir pedidos, budget e marketeer responsável** (unidade 3.4) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 3.5

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: C08, C09. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C08** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC08%5D%22

```markdown
- [ ] O menu do Cliente tem a opção "Campanhas"
- [ ] A lista mostra, por campanha, o número, o nome, as datas, o budget, o estado e o marketeer responsável
- [ ] Um cliente só vê as suas campanhas
- [ ] As campanhas que ainda não têm budget aparecem na lista, com `Por definir`
- [ ] O cliente não altera o budget; a lista diz que o budget é definido pelo administrador
- [ ] Os pedidos de alteração de budget entram na Fase 5
```

**Issue C09** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC09%5D%22

```markdown
- [ ] A opção "Ver campanha e marketeer responsável" pede o número da campanha
- [ ] São mostrados os dados da campanha, incluindo o objetivo
- [ ] São mostrados o nome, o email e o telefone do marketeer responsável
- [ ] Com o número de uma campanha de outro cliente aparece "Não tem nenhuma campanha com o número ..."
```

Por fim, no quadro Trello, move os cards das stories C08 e C09 de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/3.5-campanhas-do-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/3.5-campanhas-do-cliente` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/3.5-campanhas-do-cliente'`.

### Passo 21 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 3.5 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 3.5. Eles estão na pasta `ctesp-ADC/fase-3/ficheiros/3.5/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 3.5 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/campanhas.py`, `tests/test_campanhas_cliente.py`.

```bash
git add -A
git commit -m "feat(repositorios): listar as campanhas de um cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 72 insertions(+)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 3.5 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/campanhas.py`, `tests/test_campanhas_cliente.py`.

```bash
git add -A
git commit -m "feat(campanhas): campanhas do cliente e marketeer responsável"
```

**Deves ver** uma linha a terminar em `2 files changed, 71 insertions(+)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 3.5 3
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_campanhas_cliente.py`.

```bash
git add -A
git commit -m "feat(cli): lista das campanhas do cliente, com o budget"
```

**Deves ver** uma linha a terminar em `3 files changed, 84 insertions(+), 1 deletion(-)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 3.5 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `tests/test_campanhas_cliente.py`.

```bash
git add -A
git commit -m "feat(cli): mostrar ao cliente o marketeer responsável e os contactos"
```

**Deves ver** uma linha a terminar em `2 files changed, 80 insertions(+), 3 deletions(-)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 3.5 5
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar as campanhas vistas pelo cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 30 insertions(+), 1 deletion(-)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 3.5
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 3.5` | `Tudo certo: o ramo 'feature/3.5-campanhas-do-cliente' está igual ao original no fim da unidade 3.5.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar as campanhas vistas pelo cliente
xxxxxxx feat(cli): mostrar ao cliente o marketeer responsável e os contactos
xxxxxxx feat(cli): lista das campanhas do cliente, com o budget
xxxxxxx feat(campanhas): campanhas do cliente e marketeer responsável
xxxxxxx feat(repositorios): listar as campanhas de um cliente
```

### Passo 23 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `382 passed`.

Garante que tens as campanhas de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como cliente (`1`, depois `jose@padaria.pt` e `jose12345`). O menu tem agora a opção `2. Campanhas`. Escolhe `2`.

**Deves ver** pelo menos esta campanha (o número da primeira coluna pode ser outro):

```text
N.º  Nome               Início      Fim         Budget    Estado     Marketeer
---  -----------------  ----------  ----------  --------  ---------  ----------------
2    Regresso às aulas  2026-09-01  2026-09-30  800,00 €  Terminada  Miguel Marketeer

1 campanha.
O budget de cada campanha é definido pelo administrador.
```

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Ver campanha` e a pergunta `Número da campanha (Enter para cancelar)` |
| O número da campanha `Regresso às aulas` | Os dados da campanha, com `Objetivo:  Divulgar os lanches para a escola`, e por baixo `Marketeer responsável`, com `Nome:      Miguel Marketeer`, `Email:     marketeer@agencia.pt` e `Telefone:  910000002` |
| Enter | A tabela outra vez |

Sai com `0`, `0` e `0`.

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/3.5-campanhas-do-cliente
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/3.5-campanhas-do-cliente -> feature/3.5-campanhas-do-cliente`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/3.5-campanhas-do-cliente?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/3.5-campanhas-do-cliente**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Campanhas do cliente e marketeer responsável
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Cliente passa a ver as suas campanhas, com o budget atribuído a cada uma, e os contactos do marketeer responsável.

- Função do repositório que lista as campanhas de um cliente
- Regras: um cliente só vê as suas campanhas
- Opção "Campanhas" no menu do Cliente, com a lista e os detalhes de cada campanha

Closes #(número da issue C08)
Closes #(número da issue C09)

## Como testar

1. `python -m pytest` (382 testes)
2. `python -m gestor_campanhas.dados_demo`
3. `python -m gestor_campanhas`, entrar como cliente e escolher "Campanhas"
4. Ver uma campanha
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories C08 e C09 para **Ready to Verify**.

### Passo 26 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 3.5 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 28 a 34.

### Passo 27 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/3.5-campanhas-do-cliente
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/3.5-campanhas-do-cliente` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever a release v0.3.0 e juntá-la ao main

Quem fez: Ricardo. Tu confirmas que a versão está pronta e juntas o ramo da release ao `main`.

### Passo 28 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 3.6 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Release v0.3.0**.

### Passo 29 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 30 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch release/v0.3.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch release/v0.3.0` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'release/v0.3.0'`.

Agora experimenta:

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `382 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v0.3.0`. Sai com `0`.

Confirma também:

- No separador **Files changed** do pull request aparecem só cinco ficheiros: `gestor_campanhas/cli/campanhas.py`, `tests/test_administracao.py`, `gestor_campanhas/__init__.py`, `CHANGELOG.md` e `README.md`.
- O `CHANGELOG.md` tem a secção `v0.3.0` por cima da `v0.2.0`.

### Passo 31 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

### Passo 32 — Confirma que o pull request vai para o main

Este é o único pull request da fase que não vai para o `develop`. Se for junto ao ramo errado, o `main` fica sem a versão e a tag fica no sítio errado.

Por baixo do título do pull request tem de estar escrito `... wants to merge 4 commits into main from release/v0.3.0`.

Se disser `into develop`, **não juntes**. Avisa Ricardo, que corrige o destino no botão **Edit**, à direita do título. Depois de corrigido, atualiza a página e confirma outra vez.

### Passo 33 — Junta o pull request ao main (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `main`.

**Deves ver** o símbolo roxo **Merged** no topo da página.

### Passo 34 — Arruma o teu computador

```bash
git switch develop
git branch -D release/v0.3.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git branch -D release/v0.3.0` | Apaga a cópia do ramo que criaste para experimentar. O `-D` maiúsculo é preciso porque o `develop` ainda não tem estes commits: chegam lá no pull request seguinte |

### Passo 35 — Avisa Ricardo

Diz a Ricardo que a release v0.3.0 já está no `main`. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 44 a 49.

---

## Juntar a release v0.3.0 ao develop

É o último pull request da fase.

### Passo 36 — Aprova o pull request que leva a release para o develop

Faz este passo quando Ricardo te avisar.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Juntar a release v0.3.0 ao develop**.

**b)** Confirma que na descrição está `Closes #` seguido do número da issue da release, e não `#N`. Se estiver `#N`, pede a Ricardo para editar a descrição antes de juntares.

**c)** No separador **Files changed**, confirma que as alterações são as da release: o número da versão, o `CHANGELOG.md` e o `README.md`.

**d)** Clica em **Review changes**, escolhe **Approve** e clica em **Submit review**.

### Passo 37 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** **Não cliques em Delete branch.** O ramo deste pull request é o `main`, que tem de continuar a existir.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da release fica fechada sozinha.

### Passo 38 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 3.6
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `python ../ctesp-ADC/verificar.py 3.6` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 3.6 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 3.6.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 39 — Avisa o grupo

Diz a Ricardo que a release está no `develop` e que já pode arrumar o computador (passo 49 da [página de Ricardo](ricardo.md)).

Esta era a última vez da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 40 — Atualiza a página "Arquitetura" da wiki

A página ganha três secções: um exemplo que segue a aprovação de um pedido pelas camadas, as campanhas e os pedidos (com os estados de um pedido) e o dinheiro em cêntimos. A tabela das tabelas ganha duas linhas.

Faz este passo depois de a unidade 3.5 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Arquitetura.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki/Arquitetura e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a Arquitetura para a versão 0.3.0` e clica em **Save page**.

**Deves ver** a página com as secções novas `Exemplo: aprovar um pedido de campanha`, `Campanhas e pedidos` e `Dinheiro`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 3.2 — Campanhas atribuídas e eliminar campanha

- **`gestor_campanhas/dinheiro.py`** é novo. A aplicação guarda o dinheiro em cêntimos, como números inteiros, porque as contas com números decimais podem dar resultados inesperados (em Python, `0.1 + 0.2` não dá exatamente `0.3`). `para_centimos` aceita `1500`, `1500,50`, `1500.5` e `1 500,50 €`; `formatar` faz o caminho inverso e escreve `1 500,50 €`. Em `"1500,5"`, o `5` são 50 cêntimos, por isso completa-se com um zero à direita (`ljust(2, "0")`).
- **`gestor_campanhas/relogio.py`** ganha `hoje`, que devolve o dia atual a partir de `agora`. Como os testes já substituem `agora` para simular a hora, passam a simular também o dia.
- **`gestor_campanhas/modelos.py`** ganha três constantes com os nomes dos estados de uma campanha.
- **`gestor_campanhas/servicos/campanhas.py`** ganha `estado` e `eliminar`. O estado não é guardado na base de dados: é calculado a partir das datas sempre que é preciso. Assim, uma campanha passa a "Terminada" sozinha no dia a seguir à data de fim, sem ninguém ter de a alterar. Uma campanha sem datas está "Em curso".
- **`gestor_campanhas/repositorios/campanhas.py`** ganha `eliminar`, um `DELETE` pelo identificador.
- **`gestor_campanhas/cli/campanhas.py`**: a tabela ganha as colunas `Budget` e `Estado`. A função `budget` escreve `Por definir` quando o valor é `None`. `mostrar_detalhes` escreve os dados um por linha e é usada em dois sítios: em "Ver campanha" e antes da pergunta de confirmação de "Eliminar campanha", para se ver bem o que se vai apagar.
- **`gestor_campanhas/dados_demo.py`** ganha a lista `CAMPANHAS` e a função `criar_campanhas`. Tal como as contas, as campanhas só são criadas se ainda não existirem, por isso o comando pode ser repetido.
- **Os testes dos ecrãs que vinham da unidade 3.1 não mudaram.** Os testes procuram um bocado de texto na saída (`"N.º  Nome   Cliente        Início      Fim" in saida`), e esse bocado continua lá: as colunas novas ficaram à direita.
- **`tests/test_dinheiro.py`** usa `pytest.mark.parametrize`: o mesmo teste corre uma vez por cada linha da lista de exemplos.
- **O que fica para a Fase 4.** A story M04 pede também o budget restante e o número de criativos por estado, e a M05 só deixa eliminar campanhas sem criativos. Como os criativos só existem na Fase 4, essas partes ficam escritas nos critérios das duas issues e entram nessa fase.

### Unidade 3.5 — Campanhas do cliente e marketeer responsável

- **`gestor_campanhas/repositorios/campanhas.py`** ganha `listar_por_cliente`. É a mesma consulta de `listar_por_marketeer`, com o filtro noutra coluna.
- **`gestor_campanhas/servicos/campanhas.py`** ganha três funções.
  - `listar_do_cliente` devolve todas as campanhas do cliente, tenham ou não budget.
  - `obter_do_cliente` devolve uma campanha só se for do cliente que a pede, tal como `obter_do_marketeer` faz para o marketeer.
  - `responsavel` vai buscar a conta do marketeer da campanha. A classe `Campanha` só tem o nome dele; o email e o telefone estão na conta.
- **`gestor_campanhas/cli/campanhas.py`** ganha `mostrar_do_cliente`, `ver_do_cliente` e `do_cliente`. A tabela do cliente não tem a coluna do cliente (é sempre ele) e tem a do marketeer. Os detalhes reutilizam `mostrar_detalhes`, da unidade 3.2, e acrescentam o bloco `Marketeer responsável`.
- **O mesmo nome, três menus.** A opção chama-se "Campanhas" nos três perfis, mas cada perfil tem a sua função: `do_marketeer`, `do_administrador` e `do_cliente`. O dicionário `OPCOES`, em `perfis.py`, é que liga cada perfil à função certa. O teste `test_opcao_campanhas_esta_no_menu_do_cliente` confirma essa ligação.
- **O cliente só lê.** Neste menu não há nenhuma opção que altere dados. O budget muda-se na opção "Campanhas" do Administrador; os pedidos de alteração de budget feitos pelo cliente são da Fase 5.
- **`tests/test_campanhas_cliente.py`** é novo. A fixture `miguel` dá um telefone ao marketeer, para o teste poder confirmar que o telefone aparece; outro teste confirma que aparece `-` quando não há telefone.
