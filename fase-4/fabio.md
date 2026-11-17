# Fase 4 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 4 (Criativos), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 4.2 (de Ricardo) | Quando Ricardo avisar |
| 8 a 17 | Fazer a unidade 4.3 — Criativos do cliente, com pesquisa e filtros | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 4.4 (de Tomas) | Quando Tomas avisar |
| 25 a 34 | Fazer a unidade 4.6 — Despesa face ao budget e aviso de budget ultrapassado | Quando Tomas avisar |
| 35 a 43 | Preparar a release v0.4.0 | Quando Ricardo avisar |
| 44 a 49 | Publicar a release v0.4.0 e pedir o regresso ao develop | Quando Ricardo avisar |
| 50 a 51 | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 4.2 — Custo, prazo, público-alvo e plataforma

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 4.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Custo, prazo, público-alvo e plataforma**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 4 linhas `Closes #` seguida de um número, uma por issue (M09, M10, M11, M12), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Ricardo para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/4.2-custo-prazo-publico-plataforma
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/4.2-custo-prazo-publico-plataforma` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/4.2-custo-prazo-publico-plataforma'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `442 passed`.

Cria os criativos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver**, entre as outras linhas, `Criativos criados: 4 (os restantes já existiam).`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`), escolhe `2` (Criativos) e escreve o número da campanha `Natal 2026`.

**Deves ver** pelo menos estas linhas (os números da primeira coluna podem ser outros):

```text
N.º  Nome             Custo     Prazo       Público-alvo               Plataforma  Estado
---  ---------------  --------  ----------  -------------------------  ----------  -------------
1    Banner de Natal  400,00 €  2026-11-25  Famílias da região de...   Facebook    Em preparação
2    Vídeo da montra  900,00 €  2026-11-28  Jovens adultos, 18 a 3...  Instagram   Em preparação
```

O menu tem agora `3. Ver criativo` e `4. Eliminar criativo`. Cria um criativo com todos os dados:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Criar criativo` e a pergunta `Nome do criativo` |
| `Folheto de Natal` | A pergunta `Descrição (opcional)` |
| `Folheto para a montra` | A pergunta `Custo estimado em euros (por exemplo 400 ou 399,90, opcional)` |
| `150,50` | A pergunta `Prazo (AAAA-MM-DD, opcional)` |
| `2026-12-20` | A pergunta `Público-alvo (opcional)` |
| `Famílias do bairro` | A lista `Plataformas:`, de `1. Facebook` a `6. YouTube`, e a pergunta `Número da plataforma (Enter para escolher mais tarde)` |
| `2` | `Criativo criado com o número ...` |
| Enter | A tabela com uma linha nova: `Folheto de Natal`, `150,50 €`, `2026-12-20`, `Famílias do bairro`, `Instagram`, `Em preparação` |

Aponta o número do `Folheto de Natal` e vê os dados dele:

| Escreves | Deves ver |
|---|---|
| `3` e Enter | O título `Ver criativo` e a pergunta `Número do criativo (Enter para cancelar)` |
| O número do `Folheto de Natal` | Os dados do criativo, como no quadro a seguir (o número pode ser outro) |

```text
Criativo n.º 5
  Nome:        Folheto de Natal
  Campanha:    Natal 2026
  Descrição:   Folheto para a montra
  Custo:       150,50 €
  Prazo:       2026-12-20
  Público:     Famílias do bairro
  Plataforma:  Instagram
  Estado:      Em preparação
```

Carrega em Enter. Agora apaga o custo e a plataforma:

| Escreves | Deves ver |
|---|---|
| `2` e Enter | A pergunta `Número do criativo (Enter para cancelar)` |
| O número do `Folheto de Natal` | `A editar o criativo Folheto de Natal.`, a frase `Para apagar um valor, escreva -` e a pergunta `Nome [Folheto de Natal]` |
| Enter | A pergunta `Descrição [Folheto para a montra]` |
| Enter | A pergunta `Custo estimado em euros [150,50 €]` |
| `-` | A pergunta `Prazo (AAAA-MM-DD) [2026-12-20]` |
| Enter | A pergunta `Público-alvo [Famílias do bairro]` |
| Enter | A lista das plataformas e a pergunta `Número da plataforma [Instagram]` |
| `-` | `Criativo guardado.` |
| Enter | Na linha do `Folheto de Natal`, o custo passa a `Por definir` e a plataforma a `-` |

Por fim, elimina o `Folheto de Natal`, para a campanha ficar só com os criativos de demonstração: `4`, o número dele e `s`. **Deves ver** `O criativo Folheto de Natal foi eliminado.`

Sai com Enter, `0`, Enter, `0` e `0`.

Confirma também:

- Corre `python -m gestor_campanhas.dados_demo` duas vezes. Da segunda, aparece `Criativos criados: 0 (os restantes já existiam).`
- Entra como marketeer, escolhe `2` e o número da campanha `Natal 2026`. Cria um criativo `Teste` com o prazo `2026-12-30` (Enter nas outras perguntas): aparece `O prazo não pode ser depois do fim da campanha (2026-12-24). O criativo não foi criado.`
- Cria um criativo `Teste` com o custo `abc`: aparece `O valor não é válido. Exemplos de valores válidos: 1500 ou 1500,50. O criativo não foi criado.`
- Cria um criativo `Teste` e, na plataforma, escreve `9`: aparece `Escreva um número entre 1 e 6.` e a pergunta repete-se. Carrega em Enter. Depois elimina o `Teste` (`4`, o número e `s`).
- Volta atrás e escolhe a campanha `Regresso às aulas`. Com `3` (Ver criativo) e o número do `Cartaz dos lanches`, aparece `Público:     Pais de alunos do básico` e `Plataforma:  Facebook`.

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

**f)** No Trello, move os cards das stories M09, M10, M11 e M12 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/4.2-custo-prazo-publico-plataforma
python ../ctesp-ADC/verificar.py 4.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/4.2-custo-prazo-publico-plataforma` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 4.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 4.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Ricardo](ricardo.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 4.3 — Criativos do cliente, com pesquisa e filtros

O Cliente ganha a opção "Criativos", com os criativos de todas as suas campanhas. Pode ver os dados de cada um e procurá-los por texto, campanha, plataforma e estado.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Custo, prazo, público-alvo e plataforma** (unidade 4.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 4.3

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: C10, C11. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C10** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC10%5D%22

```markdown
- [ ] O menu do Cliente tem a opção "Criativos", com os criativos de todas as campanhas dele
- [ ] A lista mostra, por criativo, o número, o nome, a campanha, o custo, o prazo, o público-alvo, a plataforma e o estado
- [ ] A opção "Ver criativo" mostra todos os dados de um criativo
- [ ] O cliente só vê os criativos das suas campanhas: com outro número aparece "Não tem nenhum criativo com o número ..."
- [ ] A lista é só de leitura: o cliente não cria, não edita e não elimina criativos
```

**Issue C11** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC11%5D%22

```markdown
- [ ] A opção "Filtrar e pesquisar" pede um texto, uma campanha, uma plataforma e um estado; com Enter, a pergunta não é usada
- [ ] O texto é procurado no nome, na descrição e no público-alvo, sem distinguir maiúsculas nem acentos
- [ ] A campanha, a plataforma e o estado escolhem-se de listas numeradas
- [ ] Só aparecem os criativos que respeitam todos os filtros; se não houver nenhum, aparece "Nenhum criativo corresponde aos filtros."
- [ ] Decisão do grupo: não há filtro por intervalo de datas
```

Por fim, no quadro Trello, move os cards das stories C10 e C11 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/4.3-criativos-do-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/4.3-criativos-do-cliente` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/4.3-criativos-do-cliente'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/4.3-criativos-do-cliente' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/4.3-criativos-do-cliente
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/4.3-criativos-do-cliente
git switch -c feature/4.3-criativos-do-cliente
```

  **Deves ver** `Deleted branch feature/4.3-criativos-do-cliente (was ...)` e depois `Switched to a new branch 'feature/4.3-criativos-do-cliente'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/4.3-criativos-do-cliente` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 4.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 4.3. Eles estão na pasta `ctesp-ADC/fase-4/ficheiros/4.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 4.3 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(repositorios): listar os criativos de um cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 41 insertions(+)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 4.3 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(criativos): criativos do cliente, com filtros e pesquisa"
```

**Deves ver** uma linha a terminar em `2 files changed, 108 insertions(+), 1 deletion(-)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 4.3 3
```

**Deves ver** `Copiados 4 ficheiros`: `gestor_campanhas/cli/criativos.py`, `gestor_campanhas/cli/perfis.py`, `gestor_campanhas/servicos/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): lista dos criativos do cliente"
```

**Deves ver** uma linha a terminar em `4 files changed, 171 insertions(+), 1 deletion(-)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 4.3 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): filtrar e pesquisar os criativos do cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 114 insertions(+), 4 deletions(-)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 4.3 5
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os criativos vistos pelo cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 48 insertions(+), 1 deletion(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 4.3
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 4.3` | `Tudo certo: o ramo 'feature/4.3-criativos-do-cliente' está igual ao original no fim da unidade 4.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os criativos vistos pelo cliente
xxxxxxx feat(cli): filtrar e pesquisar os criativos do cliente
xxxxxxx feat(cli): lista dos criativos do cliente
xxxxxxx feat(criativos): criativos do cliente, com filtros e pesquisa
xxxxxxx feat(repositorios): listar os criativos de um cliente
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `464 passed`.

Garante que tens os criativos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como cliente (`1`, depois `cliente@empresa.pt` e `cliente12345`). O menu tem agora a opção `3. Criativos`. Escolhe `3`.

**Deves ver** o título `Os meus criativos` e pelo menos estas linhas (os números da primeira coluna podem ser outros):

```text
N.º  Nome             Campanha    Custo     Prazo       Público-alvo               Plataforma  Estado
---  ---------------  ----------  --------  ----------  -------------------------  ----------  -------------
1    Banner de Natal  Natal 2026  400,00 €  2026-11-25  Famílias da região de...   Facebook    Em preparação
2    Vídeo da montra  Natal 2026  900,00 €  2026-11-28  Jovens adultos, 18 a 3...  Instagram   Em preparação
```

Por baixo está o menu `Criativos`, com `1. Filtrar e pesquisar` e `2. Ver criativo`. Pesquisa um texto sem acento:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Filtrar e pesquisar`, a frase `Carregue em Enter nas perguntas que não quer usar.` e a pergunta `Texto a procurar no nome, na descrição e no público-alvo` |
| `familias` | A lista `Campanhas:`, com as campanhas da Carla (pelo menos `Natal 2026`), e a pergunta `Número da campanha (Enter para todas)` |
| Enter | A lista das plataformas e a pergunta `Número da plataforma (Enter para todas)` |
| Enter | A lista `Estados:`, de `1. Em preparação` a `5. Publicado`, e a pergunta `Número do estado (Enter para todos)` |
| Enter | O título `Criativos encontrados`, só com a linha do `Banner de Natal` (o público dele é `Famílias da região de Lisboa`, com acento), e `1 criativo.` |
| Enter | A lista completa outra vez |

Agora filtra pela plataforma:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | A pergunta do texto |
| Enter | A pergunta da campanha |
| Enter | A pergunta da plataforma |
| `2` | A pergunta do estado |
| Enter | Só a linha do `Vídeo da montra`, que é para o Instagram |
| Enter | A lista completa outra vez |

Por fim, vê um criativo:

| Escreves | Deves ver |
|---|---|
| `2` e Enter | O título `Ver criativo` e a pergunta `Número do criativo (Enter para cancelar)` |
| O número do `Banner de Natal` | `Criativo n.º ...` com `Descrição:   Árvore de Natal com os produtos da loja` e `Público:     Famílias da região de Lisboa` |
| Enter | A lista outra vez |

Sai com `0`, `0` e `0`.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/4.3-criativos-do-cliente
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/4.3-criativos-do-cliente -> feature/4.3-criativos-do-cliente`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/4.3-criativos-do-cliente?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/4.3-criativos-do-cliente**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Criativos do cliente, com pesquisa e filtros
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Cliente passa a ver os criativos das suas campanhas.

- Repositório: criativos de todas as campanhas de um cliente
- Regras: só os criativos das campanhas do próprio cliente; filtros por texto, campanha, plataforma e estado
- Opção "Criativos" no menu do Cliente, com "Filtrar e pesquisar" e "Ver criativo"

Closes #(número da issue C10)
Closes #(número da issue C11)

## Como testar

1. `python -m pytest` (464 testes)
2. `python -m gestor_campanhas`, entrar como `cliente@empresa.pt` e escolher "Criativos"
3. Pesquisar `familias` e filtrar pela plataforma Instagram
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories C10 e C11 para **Ready to Verify**.

### Passo 16 — Avisa Tomas

Diz a Tomas que o pull request da unidade 4.3 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 11 a 17.

### Passo 17 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/4.3-criativos-do-cliente
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/4.3-criativos-do-cliente` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 4.4 — Estados do criativo e aprovação pelo cliente

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 4.4 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Estados do criativo e aprovação pelo cliente**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (M14, C13), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Tomas para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/4.4-estados-e-aprovacao
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/4.4-estados-e-aprovacao` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/4.4-estados-e-aprovacao'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `500 passed`.

Garante que tens os criativos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`), escolhe `2` (Criativos) e o número da campanha `Natal 2026`. O menu tem agora `5. Atualizar estado`. Envia os dois criativos para revisão:

| Escreves | Deves ver |
|---|---|
| `5` e Enter | O título `Atualizar estado` e a pergunta `Número do criativo (Enter para cancelar)` |
| O número do `Banner de Natal` | `O criativo Banner de Natal está Em preparação.` e o menu `Novo estado`, com `1. Enviar ao cliente para revisão` e `0. Deixar como está` |
| `1` | `O criativo passou a Em revisão.` e `O cliente já o pode aprovar ou rejeitar, na opção "Criativos" do menu dele.` |
| Enter | A tabela, com `Em revisão` na linha do `Banner de Natal` |
| `5`, o número do `Vídeo da montra` e `1` | `O criativo passou a Em revisão.` |
| Enter | A tabela, com os dois criativos `Em revisão` |

Sai com `0`, Enter e `0` (Terminar sessão). Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`) e escolhe `3` (Criativos).

**Deves ver** os dois criativos `Em revisão`, a frase `Há 2 criativos à espera da sua aprovação.` e, no menu, `3. Aprovar ou rejeitar criativo`.

| Escreves | Deves ver |
|---|---|
| `3` e Enter | O título `Aprovar ou rejeitar criativo` e a pergunta do número |
| O número do `Banner de Natal` | Os dados do criativo e o menu `Decisão`, com `1. Aprovar`, `2. Rejeitar` e `0. Decidir mais tarde` |
| `1` | `Criativo aprovado. O marketeer já o pode publicar.` |
| Enter | `Aprovado` na linha do `Banner de Natal` e `Há 1 criativo à espera da sua aprovação.` |
| `3` e o número do `Vídeo da montra` | Os dados do criativo e o menu `Decisão` |
| `2` | A pergunta `Motivo da rejeição (o que quer que mude)` |
| Enter | `Este campo é obrigatório.` e a mesma pergunta |
| `As cores não combinam com a loja` | `Criativo rejeitado. O marketeer vai ver o motivo e preparar uma versão nova.` |
| Enter | `Rejeitado` na linha do `Vídeo da montra` |
| `3` e o número do `Banner de Natal` | Os dados e `Só se pode aprovar ou rejeitar um criativo em revisão. Este criativo está Aprovado.` |
| Enter | A lista outra vez |

Sai com `0` e `0`. Entra outra vez como marketeer, escolhe `2` e a campanha `Natal 2026`:

| Escreves | Deves ver |
|---|---|
| `3` e o número do `Vídeo da montra` | Os dados do criativo, com `Estado:      Rejeitado` e `Motivo:      As cores não combinam com a loja` |
| Enter | A tabela |
| `5` e o número do `Banner de Natal` | `O criativo Banner de Natal está Aprovado.` e o menu com `1. Marcar como publicado` |
| `1` | `O criativo passou a Publicado.` |
| Enter | `Publicado` na linha do `Banner de Natal` |
| `4`, o número do `Banner de Natal` e `s` | `Um criativo publicado não pode ser eliminado.` |
| Enter | A tabela |

Por fim, vê o resumo na campanha: `0`, Enter, `1` (Campanhas), `3` (Ver campanha) e o número da campanha `Natal 2026`. **Deves ver**, no fim dos dados, `Criativos: 2 (Rejeitado: 1, Publicado: 1)`.

Sai com Enter, `0`, `0` e `0`.

Confirma também:

- Corre `python -m gestor_campanhas.dados_demo`, para teres os criativos de demonstração.
- Entra como marketeer, escolhe `2` e a campanha `Regresso às aulas`. Com `5` e o número do `Cartaz dos lanches`, envia-o para revisão (`1`).
- Ainda como marketeer, escolhe `2` (Editar criativo) e o número do `Cartaz dos lanches`: aparece `Só se pode editar um criativo em preparação ou rejeitado. Este criativo está Em revisão.`
- Entra como `jose@padaria.pt` / `jose12345` e escolhe `3`: aparece `Há 1 criativo à espera da sua aprovação.` Com `3`, o número do `Cartaz dos lanches` e `2` (Rejeitar), escreve o motivo `Faltam os preços`: aparece `Criativo rejeitado. ...`
- Ainda como José, tenta outra vez `3` com o mesmo criativo: aparece `Só se pode aprovar ou rejeitar um criativo em revisão. Este criativo está Rejeitado.`
- Entra como marketeer e, no `Cartaz dos lanches`, escolhe `5`: aparece `Motivo da rejeição: Faltam os preços` e duas escolhas, `1. Voltar a pôr em preparação` e `2. Enviar ao cliente para revisão`. Escolhe `1`: aparece `O criativo passou a Em preparação.`

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

**f)** No Trello, move os cards das stories M14 e C13 para **Ready**.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/4.4-estados-e-aprovacao
python ../ctesp-ADC/verificar.py 4.4
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/4.4-estados-e-aprovacao` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 4.4` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 4.4 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.4.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Tomas](tomas.md)).

Diz também a Ricardo que já pode avançar ([página de Ricardo](ricardo.md), passos 18 a 27).

---

## Fazer a unidade 4.6 — Despesa face ao budget e aviso de budget ultrapassado

A despesa de uma campanha é a soma do custo dos seus criativos. As listas e os detalhes das campanhas, do Marketeer e do Cliente, passam a mostrar a despesa e o budget restante. O Marketeer é avisado quando o custo dos criativos passa o budget.

### Passo 25 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Ficheiros dos criativos** (unidade 4.5) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 26 — Fica com as issues da unidade 4.6

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: C14, M15. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C14** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC14%5D%22

```markdown
- [ ] A lista das campanhas do Cliente ganha as colunas "Despesa" e "Restante"
- [ ] A despesa é a soma do custo estimado dos criativos da campanha, seja qual for o estado deles; um criativo sem custo conta como zero
- [ ] O restante é o budget menos a despesa; fica negativo, com `-` à frente, quando a despesa passa o budget; sem budget aparece `Por definir`
- [ ] "Ver campanha" mostra a despesa, o restante e a parte do budget já gasta, em percentagem
```

**Issue M15** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM15%5D%22

```markdown
- [ ] Por baixo da lista dos criativos de uma campanha aparece o custo dos criativos e o budget da campanha
- [ ] Quando o custo passa o budget, aparece um aviso com os dois valores e a diferença: na lista dos criativos, depois de criar ou editar um criativo, e em "Ver campanha"
- [ ] O aviso não impede guardar o criativo
- [ ] Uma campanha sem budget não tem aviso
- [ ] A lista e os detalhes das campanhas do Marketeer mostram também a despesa e o restante (parte de M04 que tinha ficado da Fase 3)
```

Por fim, no quadro Trello, move os cards das stories C14 e M15 de **Sprint Backlog** para **Work In Progress**.

### Passo 27 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/4.6-despesa-e-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/4.6-despesa-e-budget` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/4.6-despesa-e-budget'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/4.6-despesa-e-budget' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/4.6-despesa-e-budget
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/4.6-despesa-e-budget
git switch -c feature/4.6-despesa-e-budget
```

  **Deves ver** `Deleted branch feature/4.6-despesa-e-budget (was ...)` e depois `Switched to a new branch 'feature/4.6-despesa-e-budget'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/4.6-despesa-e-budget` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 28 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 4.6 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 4.6. Eles estão na pasta `ctesp-ADC/fase-4/ficheiros/4.6/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.6 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dinheiro.py`, `tests/test_dinheiro.py`.

```bash
git add -A
git commit -m "feat(dinheiro): escrever valores negativos"
```

**Deves ver** uma linha a terminar em `2 files changed, 19 insertions(+), 3 deletions(-)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.6 2
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/repositorios/criativos.py`, `gestor_campanhas/servicos/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(criativos): calcular a despesa e o budget restante de uma campanha"
```

**Deves ver** uma linha a terminar em `3 files changed, 108 insertions(+)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.6 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(cli): despesa e budget restante nas campanhas do marketeer"
```

**Deves ver** uma linha a terminar em `2 files changed, 84 insertions(+), 21 deletions(-)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.6 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `tests/test_campanhas_cliente.py`.

```bash
git add -A
git commit -m "feat(cli): despesa face ao budget nas campanhas do cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 73 insertions(+), 22 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.6 5
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): avisar quando o custo dos criativos ultrapassa o budget"
```

**Deves ver** uma linha a terminar em `3 files changed, 94 insertions(+), 2 deletions(-)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.6 6
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar a despesa e o aviso de budget ultrapassado"
```

**Deves ver** uma linha a terminar em `2 files changed, 62 insertions(+), 14 deletions(-)`.


### Passo 29 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 4.6
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 4.6` | `Tudo certo: o ramo 'feature/4.6-despesa-e-budget' está igual ao original no fim da unidade 4.6.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar a despesa e o aviso de budget ultrapassado
xxxxxxx feat(cli): avisar quando o custo dos criativos ultrapassa o budget
xxxxxxx feat(cli): despesa face ao budget nas campanhas do cliente
xxxxxxx feat(cli): despesa e budget restante nas campanhas do marketeer
xxxxxxx feat(criativos): calcular a despesa e o budget restante de uma campanha
xxxxxxx feat(dinheiro): escrever valores negativos
```

### Passo 30 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `566 passed`.

Garante que tens os criativos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

Os valores desta página são os que aparecem quando a campanha `Natal 2026` só tem os dois criativos de demonstração, `Banner de Natal` (400 €) e `Vídeo da montra` (900 €). Se tiveres lá outros criativos com custo, as somas são maiores.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`) e escolhe `1` (Campanhas).

**Deves ver** a tabela com duas colunas novas no fim (pode haver mais campanhas):

```text
N.º  Nome               Cliente        Início      Fim         Budget      Estado       Despesa     Restante
---  -----------------  -------------  ----------  ----------  ----------  -----------  ----------  --------
1    Natal 2026         Carla Cliente  2026-12-01  2026-12-24  1 500,00 €  Por começar  1 300,00 €  200,00 €
2    Regresso às aulas  José Padeiro   2026-09-01  2026-09-30  800,00 €    Terminada    300,00 €    500,00 €
```

Escolhe `0`, depois `2` (Criativos) e o número da campanha `Natal 2026`. **Deves ver**, por baixo da tabela dos criativos, `Custo dos criativos: 1 300,00 €. Budget da campanha: 1 500,00 €.`

O `Vídeo da montra` tem de estar `Em preparação` ou `Rejeitado`, para poder ser editado. Se no teu computador estiver noutro estado, muda o custo do `Banner de Natal` para `800` em vez disso: o resultado é o mesmo.

| Escreves | Deves ver |
|---|---|
| `2` e Enter | A pergunta `Número do criativo (Enter para cancelar)` |
| O número do `Vídeo da montra` | `A editar o criativo Vídeo da montra.` e a pergunta `Nome [Vídeo da montra]` |
| Enter | A pergunta `Descrição [Vídeo curto da montra decorada]` |
| Enter | A pergunta `Custo estimado em euros [900,00 €]` |
| `1300` | A pergunta `Prazo (AAAA-MM-DD) [2026-11-28]` |
| Enter | A pergunta `Público-alvo [Jovens adultos, 18 a 35 anos]` |
| Enter | A lista das plataformas e a pergunta `Número da plataforma [Instagram]` |
| Enter | `Criativo guardado.` e, por baixo, o aviso `Atenção: o custo dos criativos (1 700,00 €) ultrapassa o budget da campanha (1 500,00 €) em 200,00 €.` |
| Enter | A tabela, `Custo dos criativos: 1 700,00 €. Budget da campanha: 1 500,00 €.` e o mesmo aviso |

Volta às campanhas: `0`, Enter e `1`. **Deves ver**, na linha de `Natal 2026`, `1 700,00 €` na despesa e `-200,00 €` no restante.

Escolhe `3` (Ver campanha) e o número da campanha `Natal 2026`. **Deves ver** `Despesa:   1 700,00 €` e `Restante:  -200,00 €` nos dados, e o aviso no fim.

Carrega em Enter e sai com `0` e `0`. Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`) e escolhe `2` (Campanhas).

**Deves ver** as colunas `Despesa` e `Restante` no fim da tabela, com `1 700,00 €` e `-200,00 €` na linha de `Natal 2026`, e por baixo a frase `A despesa é a soma do custo estimado dos criativos de cada campanha.`

| Escreves | Deves ver |
|---|---|
| `1` e o número da campanha `Natal 2026` | Os dados da campanha, com `Despesa:   1 700,00 €`, `Restante:  -200,00 €` e `Gasto:     113% do budget` |
| Enter | A tabela outra vez |

Sai com `0` e `0`. Por fim, põe o custo do `Vídeo da montra` outra vez a `900` (entra como marketeer, `2`, a campanha `Natal 2026`, `2`, o número do vídeo, e `900` no custo), para os dados ficarem como os de demonstração. **Deves ver** `Custo dos criativos: 1 300,00 €. Budget da campanha: 1 500,00 €.` e nenhum aviso.

Sai com `0`, Enter, `0` e `0`.

### Passo 31 — Envia o ramo para o GitHub

```bash
git push -u origin feature/4.6-despesa-e-budget
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/4.6-despesa-e-budget -> feature/4.6-despesa-e-budget`.

### Passo 32 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/4.6-despesa-e-budget?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/4.6-despesa-e-budget**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Despesa face ao budget e aviso de budget ultrapassado
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

As campanhas passam a mostrar quanto já se gastou do budget.

- Valores negativos em euros escritos com o sinal à frente (`-200,00 €`)
- Soma do custo dos criativos de todas as campanhas numa só consulta
- Colunas "Despesa" e "Restante" nas listas de campanhas do Marketeer e do Cliente, e as mesmas linhas em "Ver campanha"
- Aviso ao Marketeer quando o custo dos criativos ultrapassa o budget
- Budget restante do Marketeer (parte de M04)

Closes #(número da issue C14)
Closes #(número da issue M15)

## Como testar

1. `python -m pytest` (566 testes)
2. `python -m gestor_campanhas`: como marketeer, ver as colunas novas em "Campanhas" e mudar o custo do Vídeo da montra para 1300
3. Ver o aviso e, como `cliente@empresa.pt`, a despesa e a percentagem gasta
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories C14 e M15 para **Ready to Verify**.

### Passo 33 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 4.6 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 28 a 34.

### Passo 34 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/4.6-despesa-e-budget
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/4.6-despesa-e-budget` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Preparar a release v0.4.0

Fecha a fase com a versão 0.4.0: sobe o número da versão, acrescenta a secção desta versão ao registo de alterações e atualiza o README. Esta unidade vai para o `main`, e não para o `develop`.

### Passo 35 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Despesa face ao budget e aviso de budget ultrapassado** (unidade 4.6) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 36 — Cria a issue da unidade 4.7

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[4.7] Release v0.4.0
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Publicar a versão 0.4.0, com as user stories da Fase 4 (criativos).

## O que inclui

- [ ] Versão 0.4.0 em `gestor_campanhas/__init__.py`
- [ ] Registo de alterações (`CHANGELOG.md`)
- [ ] README atualizado
- [ ] Pull request para `main`
- [ ] Tag e release `v0.4.0` no GitHub
- [ ] `main` de volta ao `develop`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 4 — Criativos`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 37 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c release/v0.4.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c release/v0.4.0` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'release/v0.4.0'`.

**Se em vez disso aparecer** `fatal: a branch named 'release/v0.4.0' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..release/v0.4.0
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D release/v0.4.0
git switch -c release/v0.4.0
```

  **Deves ver** `Deleted branch release/v0.4.0 (was ...)` e depois `Switched to a new branch 'release/v0.4.0'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch release/v0.4.0` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 38 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 4.7 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 4.7. Eles estão na pasta `ctesp-ADC/fase-4/ficheiros/4.7/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 4.7 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__init__.py`.

```bash
git add -A
git commit -m "chore(release): passar a versão para 0.4.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 4.7 2
```

**Deves ver** `Copiados 1 ficheiro`: `CHANGELOG.md`.

```bash
git add -A
git commit -m "docs(release): registar as alterações da versão 0.4.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 28 insertions(+)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 4.7 3
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(release): atualizar o README para a versão 0.4.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 25 insertions(+), 4 deletions(-)`.


### Passo 39 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 4.7
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 4.7` | `Tudo certo: o ramo 'release/v0.4.0' está igual ao original no fim da unidade 4.7.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(release): atualizar o README para a versão 0.4.0
xxxxxxx docs(release): registar as alterações da versão 0.4.0
xxxxxxx chore(release): passar a versão para 0.4.0
```

### Passo 40 — Experimenta o que gravaste

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `566 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v0.4.0`. Sai com `0`.

### Passo 41 — Envia o ramo para o GitHub

```bash
git push -u origin release/v0.4.0
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      release/v0.4.0 -> release/v0.4.0`.

### Passo 42 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `main`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/main...release/v0.4.0?expand=1

**b)** Confirma, no topo, que está **base: main** e **compare: release/v0.4.0**. O link do ponto a) já abre com o `main` escolhido. Se estiver **base: develop**, clica aí e escolhe `main`. Uma release vai para o `main`, que é o ramo das versões entregues.

**c)** No título, cola:

```text
Release v0.4.0
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Não é preciso trocar nada:

```markdown
## O que muda

Prepara a versão 0.4.0.

- Versão passa de 0.3.0 para 0.4.0
- `CHANGELOG.md` com a secção da versão 0.4.0
- README atualizado: tabela de versões, dados de demonstração, secção sobre os criativos, pasta `exemplos/` e pasta dos ficheiros

Este pull request vai para o `main`. A issue da release é fechada pelo pull request que leva a release de volta ao `develop`.

## Como testar

1. `python -m pytest` (566 testes)
2. `python -m sphinx -W -b html docs docs/_build/html`
3. `python -m gestor_campanhas`: o título mostra `v0.4.0`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** Confirma o destino. Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.4.0`. Se disser `into develop`, **não avises ninguém ainda**: clica em **Edit**, à direita do título, clica em **base: develop**, escolhe `main`, confirma em **Change base** e clica em **Save**.

### Passo 43 — Avisa Ricardo

Diz a Ricardo que o pull request da release v0.4.0 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 35 a 42.

---

## Publicar a release v0.4.0 e pedir o regresso ao develop

Com a release no `main`, falta marcá-la com uma tag e levar os commits dela de volta ao `develop`.

### Passo 44 — Confirma que o main já tem a versão 0.4.0

Faz este passo quando Ricardo te avisar que a release está no `main`.

A tag vai ser criada no `main`. Se o `main` ainda não tiver a versão nova, a tag fica a marcar o código da versão anterior. Foi o que aconteceu nas duas primeiras fases.

Abre https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py

**Deves ver** a linha `__version__ = "0.4.0"`.

Se vires outra versão, **não publiques a release**. O pull request foi junto ao `develop` em vez do `main`. Avisa Ricardo e corrijam assim: abre https://github.com/Blive77/ADC-TrabGrupo/compare/main...develop?expand=1, cria um pull request com o título `Release v0.4.0`, Ricardo aprova e junta, e só depois voltas a este passo.

### Passo 45 — Publica a release v0.4.0 no GitHub

Publicar a release cria a **tag**, uma etiqueta que marca para sempre o commit desta versão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/releases/new

**b)** Clica em **Choose a tag**, escreve `v0.4.0` e clica em **Create new tag: v0.4.0 on publish**.

**c)** Em **Target**, escolhe `main`.

**d)** Em **Release title**, cola:

```text
v0.4.0 — Criativos
```

**e)** Na caixa de texto, cola:

````markdown
## Criativos

Cada campanha passa a ter criativos: as peças a publicar. O Marketeer cria-os, com custo, prazo, público-alvo, plataforma e ficheiro, e envia-os ao cliente. O Cliente aprova-os ou rejeita-os e descarrega os ficheiros. As campanhas mostram a despesa face ao budget.

### Acrescentado

- Criativos: o Marketeer cria, edita, consulta e elimina os criativos das suas campanhas
- Custo estimado, prazo, público-alvo e plataforma de cada criativo
- Estados de um criativo: em preparação, em revisão, aprovado, rejeitado e publicado
- Aprovação pelo Cliente; a rejeição leva sempre um motivo, que o marketeer vê
- Ficheiros: o Marketeer anexa-os; o Marketeer e o Cliente pré-visualizam-nos; o Cliente descarrega uma cópia
- Lista dos criativos do Cliente, com pesquisa e filtros por campanha, plataforma e estado
- Despesa e budget restante de cada campanha, e aviso ao Marketeer quando o custo dos criativos passa o budget
- Número de criativos por estado em "Ver campanha"
- Criativos de demonstração e o ficheiro de exemplo `exemplos/banner-natal.svg`

### Alterado

- Uma campanha com criativos já não pode ser eliminada
- Os valores negativos em euros são escritos com o sinal à frente

### User stories

M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, C10, C11, C12, C13 e C14.

Ficam também concluídas as partes de M04 e de M05 adiadas na versão 0.3.0. Os pedidos de alteração de budget (C06 e C08) entram na versão 0.5.0.

### Como experimentar

```
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

Entrar com `marketeer@agencia.pt` / `marketeer12345` e escolher "Criativos", ou com `cliente@empresa.pt` / `cliente12345` e escolher "Criativos". As outras contas de demonstração estão no README.
````

**f)** Clica em **Publish release**.

**Deves ver** a página da release, e a tag `v0.4.0` em https://github.com/Blive77/ADC-TrabGrupo/tags. Na linha da tag aparece o commit `Merge pull request ... from .../release/v0.4.0`. Se aparecer outro commit, o **Target** ficou errado: avisa o grupo antes de continuar.

### Passo 46 — Abre o pull request que leva a release para o develop

A release está no `main`, mas o `develop` ainda não tem os commits dela (a versão nova e o registo de alterações). Este pull request leva-os para lá, para os dois ramos ficarem alinhados.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/compare/develop...main

**b)** Confirma, no topo, que está **base: develop** e **compare: main**, e clica em **Create pull request**.

**c)** No título, cola:

```text
Juntar a release v0.4.0 ao develop
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue da release, que apontaste no início:

```markdown
## O que muda

Traz para o `develop` os commits da release v0.4.0, que já estão no `main`: a versão nova, o registo de alterações e o README.

Closes #N
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica em **Create pull request**.

### Passo 47 — Avisa Ricardo

Diz a Ricardo que o pull request que leva a release v0.4.0 para o `develop` está aberto. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 43 a 46.

### Passo 48 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d release/v0.4.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d release/v0.4.0` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

### Passo 49 — Fecha a milestone da fase

Faz este passo depois de Ricardo juntar o último pull request. Nessa altura a issue da release já está fechada, e a milestone fica com todas as issues fechadas.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/milestones

**b)** Na linha `Fase 4 — Criativos`, confirma que a barra está a 100% e clica em **Close**.

Se a barra não estiver a 100%, clica no nome da milestone para ver que issues estão abertas. Uma issue fica aberta quando o pull request dela foi junto sem `Closes #número`. Para a fechar à mão, abre a issue, escreve na caixa de comentário `Resolvida pelo pull request #N` (com o número do pull request) e clica em **Close with comment**. Depois volta a este passo.

---

## Outras tarefas desta fase

### Passo 50 — Atualiza a página inicial da wiki

A página inicial passa a indicar a versão 0.4.0.

Faz este passo no fim da fase, depois de publicares a release.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 0.4.0` e clica em **Save page**.

**Deves ver** a linha `Versão atual: v0.4.0 (Fase 4 — Criativos).`

### Passo 51 — Atualiza a página "Registo das fases" da wiki

A página ganha a secção da Fase 4: quem fez e quem reviu cada unidade, as decisões tomadas e o que correu mal na Fase 3.

Faz este passo no fim da fase, depois de a release v0.4.0 estar publicada.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Registo das fases** na lista de páginas, à direita, e depois em **Edit**.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Registar a Fase 4` e clica em **Save page**.

**Deves ver** a secção `Fase 4 — Criativos`, com a tabela das sete unidades.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 4.3 — Criativos do cliente, com pesquisa e filtros

- **`gestor_campanhas/repositorios/criativos.py`** ganha `listar_por_cliente`. A consulta junta os criativos às campanhas e escolhe as linhas em que a campanha é do cliente. Ordena por campanha e depois por número, para os criativos da mesma campanha ficarem juntos.
- **`gestor_campanhas/servicos/criativos.py`**:
  - `obter_do_cliente` faz para o cliente o mesmo que `obter_do_marketeer` faz para o marketeer: lê o criativo e confirma que a campanha dele é do cliente.
  - `filtrar` recebe a lista e os filtros, e devolve os criativos que os respeitam a todos. Um filtro vazio não exclui nada. O texto é comparado com o `gestao.simplificar` que já se usava na pesquisa de clientes, que tira os acentos e passa tudo a minúsculas: por isso `familias` encontra `Famílias`.
  - Os filtros trabalham sobre a lista já lida da base de dados, e não com uma consulta SQL nova. Um cliente tem poucos criativos, e assim a regra fica numa função simples, fácil de testar sem base de dados.
- **`gestor_campanhas/cli/criativos.py`**:
  - `do_cliente` é o ciclo do menu do cliente, com a lista `ACOES_DO_CLIENTE`, tal como `ACOES` no menu do marketeer.
  - `escolher_da_lista` mostra uma lista numerada e devolve a posição escolhida, ou `None` com Enter. É usada nas três perguntas de escolha: campanha, plataforma e estado.
  - As campanhas que aparecem no filtro são as do cliente, lidas com o `campanhas.listar_do_cliente` da Fase 3. Os estados vêm do dicionário `NOMES_ESTADOS_CRIATIVO`, pela ordem em que lá estão.
- **`gestor_campanhas/cli/perfis.py`**: o menu do Cliente ganha a opção "Criativos", a seguir a "Campanhas".
- **`tests/test_criativos.py`** ganha os testes da lista do cliente, de cada filtro sozinho e de vários juntos, e da pesquisa sem acentos.
- **`docs/`**: o guia de utilização ganha a secção dos criativos do Cliente, com a pesquisa e os filtros, e a arquitetura diz que o módulo `cli/criativos.py` serve os dois menus.

### Unidade 4.6 — Despesa face ao budget e aviso de budget ultrapassado

- **`gestor_campanhas/dinheiro.py`**: `formatar` passa a aceitar valores negativos. O `divmod` de um número negativo dá um resultado inesperado (`divmod(-150, 100)` é `(-2, 50)`), por isso a conta é feita com o valor positivo (`abs`) e o sinal `-` é posto no fim.
- **`gestor_campanhas/repositorios/criativos.py`** ganha `somar_custos_por_campanha`, com uma só consulta: `SUM(COALESCE(custo_centimos, 0))` soma os custos e conta os vazios como zero, e `GROUP BY campanha_id` faz uma soma por campanha. Devolve um dicionário do número da campanha para a soma.
- **`gestor_campanhas/servicos/criativos.py`**:
  - `despesas` devolve as somas de todas as campanhas; `despesa` devolve a de uma.
  - `restante` é o budget menos a despesa, ou `None` se a campanha não tiver budget.
  - `aviso_budget` prepara o texto do aviso, ou devolve um texto vazio se não houver nada a avisar. Não mostra nada: quem mostra é o menu. Assim a regra pode ser testada sem ecrã.
  - A despesa não é guardada na base de dados: é calculada sempre que é precisa. Assim nunca fica desatualizada quando um criativo muda de custo ou é eliminado.
- **`gestor_campanhas/cli/campanhas.py`**:
  - `mostrar_campanhas` e `mostrar_do_cliente` ganham o parâmetro opcional `despesas`. Só quando é indicado é que a tabela ganha as duas colunas: a tabela de "Criativos — escolher a campanha" usa a mesma função e continua igual.
  - As colunas novas ficam no fim, para as tabelas que já existiam não mudarem de forma.
  - `mostrar_detalhes` ganha as linhas "Despesa" e "Restante". Para o cliente, a percentagem gasta é calculada com `//` (divisão inteira), porque uma percentagem com casas decimais não ajuda a decidir nada.
- **`gestor_campanhas/cli/criativos.py`**: `avisar_se_passar_o_budget` é chamado depois de criar, depois de editar e por baixo da lista.
- **`tests/`**: `test_dinheiro.py` testa os negativos; `test_criativos.py` testa as somas, o restante, o aviso (com e sem budget) e os ecrãs; `test_campanhas.py` e `test_campanhas_cliente.py` testam as colunas novas.
- **`docs/`**: o guia de utilização explica a despesa e o aviso, e a arquitetura ganha a secção "Despesa e budget restante".

### Unidade 4.7 — Release v0.4.0

- **`gestor_campanhas/__init__.py`**: `__version__` passa para `"0.4.0"`. O menu inicial, o `pyproject.toml` e a documentação leem a versão daqui.
- **`CHANGELOG.md`** ganha a secção `v0.4.0`, por cima das anteriores. A parte "User stories concluídas" diz também o que ficou fechado da fase anterior (M04 e M05), e a parte "Alterado" regista as mudanças que podem surpreender quem já usava a versão 0.3.0, como deixar de poder eliminar uma campanha com criativos.
- **`README.md`**: a tabela de versões ganha uma linha, o exemplo do menu passa a mostrar `v0.4.0`, e há uma secção nova sobre os criativos, com o desenho dos estados e o que cada perfil faz. A tabela da configuração diz que a pasta de dados guarda também os ficheiros dos criativos, e a estrutura do projeto ganha a pasta `exemplos/`.
- **Desta vez não há `fix`.** Na Fase 3, a revisão final encontrou uma mensagem a corrigir. Nesta fase, os pormenores foram corrigidos dentro de cada unidade, antes do merge, e o ramo da release tem só os três commits de preparação.
- **O caminho de uma release** é o mesmo da Fase 3, e na Fase 3 correu bem: o pull request do ramo `release/v0.4.0` para o `main`; a confirmação de que o `main` já tem a versão 0.4.0; a publicação da release, que cria a tag no `main`; o pull request do `main` para o `develop`; e o fecho da milestone.
