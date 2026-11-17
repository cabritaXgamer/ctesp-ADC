# Fase 4 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 4 (Criativos), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 10 | Fazer a unidade 4.1 — Criar, editar e eliminar criativos | No início da fase |
| 11 a 17 | Rever e juntar a unidade 4.3 (de Fabio) | Quando Fabio avisar |
| 18 a 27 | Fazer a unidade 4.4 — Estados do criativo e aprovação pelo cliente | A seguir ao teu passo anterior |
| 28 a 34 | Rever e juntar a unidade 4.5 (de Ricardo) | Quando Ricardo avisar |
| 35 | Atualiza a página "Guia de utilização" da wiki | Em qualquer altura durante a fase |

---

## Fazer a unidade 4.1 — Criar, editar e eliminar criativos

Aparecem os criativos. O Marketeer ganha a opção "Criativos", onde escolhe uma das suas campanhas e cria, edita e elimina os criativos dessa campanha. Uma campanha com criativos deixa de poder ser eliminada.

### Passo 1 — Confirma que podes começar

A fase anterior tem de estar fechada: todos os pull requests juntos e o `develop` do teu computador atualizado. Se for a primeira fase, tens de ter feito a [Preparação](../preparacao.md).

### Passo 2 — Fica com as issues da unidade 4.1

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 3 issues: M06, M07, M08. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue M06** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM06%5D%22

```markdown
- [ ] O menu do Marketeer tem a opção "Criativos", que mostra as campanhas dele e pede o número de uma
- [ ] Depois de escolher a campanha, aparecem os criativos dela e as opções "Criar criativo", "Editar criativo" e "Eliminar criativo"
- [ ] Ao criar, são pedidos o nome (obrigatório) e a descrição (opcional)
- [ ] Um criativo novo fica no estado "Em preparação"
- [ ] Um marketeer só cria criativos nas suas campanhas: com o número de uma campanha de outro aparece "Não tem nenhuma campanha com o número ..."
- [ ] O custo, o prazo, o público-alvo e a plataforma entram nas issues M09 a M12
```

**Issue M07** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM07%5D%22

```markdown
- [ ] A opção "Editar criativo" pede o número do criativo
- [ ] Cada dado é mostrado com o valor atual; com Enter, o valor mantém-se
- [ ] Um marketeer só edita os criativos das suas campanhas: com outro número aparece "Não tem nenhum criativo com o número ..."
- [ ] Decisão do grupo: não se guarda a data da última alteração
```

**Issue M08** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM08%5D%22

```markdown
- [ ] A opção "Eliminar criativo" pede o número do criativo, mostra os dados dele e pede uma confirmação (s/n)
- [ ] Sem confirmação aparece "Nada foi alterado."
- [ ] O criativo eliminado deixa de aparecer na lista
- [ ] Uma campanha com criativos não pode ser eliminada: aparece quantos criativos tem e que têm de ser eliminados primeiro (parte de M05 que tinha ficado da Fase 3)
```

Por fim, no quadro Trello, move os cards das stories M06, M07 e M08 de **Sprint Backlog** para **Work In Progress**.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/4.1-criar-editar-eliminar-criativo
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/4.1-criar-editar-eliminar-criativo` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/4.1-criar-editar-eliminar-criativo'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/4.1-criar-editar-eliminar-criativo' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/4.1-criar-editar-eliminar-criativo
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/4.1-criar-editar-eliminar-criativo
git switch -c feature/4.1-criar-editar-eliminar-criativo
```

  **Deves ver** `Deleted branch feature/4.1-criar-editar-eliminar-criativo (was ...)` e depois `Switched to a new branch 'feature/4.1-criar-editar-eliminar-criativo'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/4.1-criar-editar-eliminar-criativo` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 4 — Copia e grava os 7 commits

São 7 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 4.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 4.1. Eles estão na pasta `ctesp-ADC/fase-4/ficheiros/4.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.1 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela dos criativos"
```

**Deves ver** uma linha a terminar em `2 files changed, 51 insertions(+)`.

**Commit 2 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.1 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/modelos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(modelos): acrescentar a classe Criativo e os estados de um criativo"
```

**Deves ver** uma linha a terminar em `2 files changed, 65 insertions(+)`.

**Commit 3 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.1 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar, ler e eliminar criativos"
```

**Deves ver** uma linha a terminar em `2 files changed, 192 insertions(+), 2 deletions(-)`.

**Commit 4 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.1 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(criativos): criar, editar e eliminar criativos de uma campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 179 insertions(+)`.

**Commit 5 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.1 5
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/criativos.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): menu de criativos do marketeer"
```

**Deves ver** uma linha a terminar em `3 files changed, 311 insertions(+), 1 deletion(-)`.

**Commit 6 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.1 6
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/servicos/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(campanhas): só eliminar campanhas sem criativos"
```

**Deves ver** uma linha a terminar em `3 files changed, 53 insertions(+), 4 deletions(-)`.

**Commit 7 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.1 7
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os criativos do marketeer"
```

**Deves ver** uma linha a terminar em `3 files changed, 76 insertions(+), 1 deletion(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 4.1
git log --oneline -7
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 4.1` | `Tudo certo: o ramo 'feature/4.1-criar-editar-eliminar-criativo' está igual ao original no fim da unidade 4.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -7` | Os teus 7 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os criativos do marketeer
xxxxxxx feat(campanhas): só eliminar campanhas sem criativos
xxxxxxx feat(cli): menu de criativos do marketeer
xxxxxxx feat(criativos): criar, editar e eliminar criativos de uma campanha
xxxxxxx feat(repositorios): guardar, ler e eliminar criativos
xxxxxxx feat(modelos): acrescentar a classe Criativo e os estados de um criativo
xxxxxxx feat(bd): criar a tabela dos criativos
```

### Passo 6 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `414 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`). O menu tem agora a opção `2. Criativos`. Escolhe `2`.

**Deves ver** o título `Criativos — escolher a campanha`, uma tabela com as campanhas do Miguel (pelo menos `Natal 2026` e `Regresso às aulas`) e a pergunta `Número da campanha (Enter para voltar)`.

Escreve o número que está na primeira coluna da linha de `Natal 2026`. **Deves ver** o título `Criativos da campanha Natal 2026 (Carla Cliente)`, a frase `Esta campanha ainda não tem criativos.` e o menu `Criativos`, com `1. Criar criativo`, `2. Editar criativo` e `3. Eliminar criativo`.

Cria dois criativos:

| Escreves | Deves ver |
|---|---|
| `1` e Enter | O título `Criar criativo` e a pergunta `Nome do criativo` |
| `Cartaz de teste` | A pergunta `Descrição (opcional)` |
| `Primeira versão` | `Criativo criado com o número ...` |
| Enter | Uma tabela com a linha `Cartaz de teste  Em preparação` |
| `1` e Enter | A pergunta `Nome do criativo` |
| `Postal de teste` | A pergunta `Descrição (opcional)` |
| Enter | `Criativo criado com o número ...` |
| Enter | A tabela com as duas linhas e, por baixo, `2 criativos.` |

Aponta o número que aparece na primeira coluna da linha de `Cartaz de teste`. Agora edita esse criativo:

| Escreves | Deves ver |
|---|---|
| `2` e Enter | O título `Editar criativo` e a pergunta `Número do criativo (Enter para cancelar)` |
| O número do `Cartaz de teste` | `A editar o criativo Cartaz de teste.` e a pergunta `Nome [Cartaz de teste]` |
| Enter | A pergunta `Descrição [Primeira versão]` |
| `Segunda versão` | `Criativo guardado.` |
| Enter | A tabela outra vez |

Agora confirma que a campanha já não pode ser eliminada:

| Escreves | Deves ver |
|---|---|
| `0` e Enter | A tabela das campanhas e a pergunta `Número da campanha (Enter para voltar)` |
| Enter | O menu do marketeer |
| `1` e Enter | O menu `Campanhas` |
| `4` e Enter | O título `Eliminar campanha` e a pergunta do número |
| O número da campanha `Natal 2026` | Os dados da campanha e a pergunta `Eliminar esta campanha? (s/n)` |
| `s` | `A campanha Natal 2026 tem 2 criativos. Elimine primeiro os criativos, na opção "Criativos".` |
| Enter e depois `0` | O menu do marketeer |

Por fim, elimina os dois criativos de teste, para a campanha ficar como estava:

| Escreves | Deves ver |
|---|---|
| `2`, e depois o número da campanha `Natal 2026` | A tabela com os dois criativos |
| `3` e Enter | O título `Eliminar criativo` e a pergunta do número |
| O número do `Cartaz de teste` | Os dados do criativo, com `Descrição:   Segunda versão`, e a pergunta `Eliminar este criativo? (s/n)` |
| `s` | `O criativo Cartaz de teste foi eliminado.` |
| Enter | A tabela só com o `Postal de teste` |
| `3`, o número do `Postal de teste` e `s` | `O criativo Postal de teste foi eliminado.` |
| Enter | `Esta campanha ainda não tem criativos.` |

Sai com `0`, Enter, `0` e `0`.

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/4.1-criar-editar-eliminar-criativo
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/4.1-criar-editar-eliminar-criativo -> feature/4.1-criar-editar-eliminar-criativo`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/4.1-criar-editar-eliminar-criativo?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/4.1-criar-editar-eliminar-criativo**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Criar, editar e eliminar criativos
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Marketeer passa a poder criar, editar e eliminar os criativos das suas campanhas.

- Tabela `criativos` na base de dados, já com todas as colunas da fase
- Classe `Criativo` e os cinco estados de um criativo
- Repositório dos criativos, que lê cada criativo já com o nome da campanha
- Regras para criar, editar e eliminar: nome obrigatório, só nas campanhas do próprio marketeer
- Opção "Criativos" no menu do Marketeer
- Uma campanha com criativos já não pode ser eliminada (parte de M05)

Closes #(número da issue M06)
Closes #(número da issue M07)
Closes #(número da issue M08)

## Como testar

1. `python -m pytest` (414 testes)
2. `python -m gestor_campanhas`, entrar como marketeer e escolher "Criativos"
3. Criar dois criativos na campanha Natal 2026, editar um, tentar eliminar a campanha e eliminar os criativos
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories M06, M07 e M08 para **Ready to Verify**.

### Passo 9 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 4.1 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 1 a 7.

### Passo 10 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/4.1-criar-editar-eliminar-criativo
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/4.1-criar-editar-eliminar-criativo` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 4.3 — Criativos do cliente, com pesquisa e filtros

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 11 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 4.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Criativos do cliente, com pesquisa e filtros**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (C10, C11), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Fabio para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/4.3-criativos-do-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/4.3-criativos-do-cliente` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/4.3-criativos-do-cliente'`.

Agora experimenta:

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

Confirma também:

- Corre `python -m gestor_campanhas.dados_demo`, para teres os criativos de demonstração.
- Entra como `jose@padaria.pt` / `jose12345` e escolhe `3`. Aparece o `Cartaz dos lanches`, da campanha `Regresso às aulas`, e não aparecem os criativos da campanha `Natal 2026`.
- Escolhe `2` e escreve o número do `Banner de Natal` (nos dados de demonstração é o `1`): aparece `Não tem nenhum criativo com o número 1.`
- Escolhe `1` e, no estado, escreve `3` (Aprovado), com Enter nas outras perguntas: aparece `Nenhum criativo corresponde aos filtros.`
- Entra como marketeer: a opção "Criativos" continua a mostrar o menu do marketeer, com as opções de criar, editar, ver e eliminar.

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

**f)** No Trello, move os cards das stories C10 e C11 para **Ready**.

### Passo 16 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/4.3-criativos-do-cliente
python ../ctesp-ADC/verificar.py 4.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/4.3-criativos-do-cliente` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 4.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 4.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 17 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 18.

---

## Fazer a unidade 4.4 — Estados do criativo e aprovação pelo cliente

Os criativos ganham estados. O Marketeer envia um criativo ao cliente para revisão e, depois de aprovado, marca-o como publicado. O Cliente aprova ou rejeita os criativos em revisão, e a rejeição leva sempre um motivo. "Ver campanha" passa a mostrar quantos criativos a campanha tem em cada estado.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Criativos do cliente, com pesquisa e filtros** (unidade 4.3) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 4.4

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: M14, C13. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue M14** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM14%5D%22

```markdown
- [ ] O menu de criativos do Marketeer tem a opção "Atualizar estado", que mostra o estado atual e só oferece os estados seguintes possíveis
- [ ] Em preparação passa a Em revisão (enviar ao cliente); Em revisão pode voltar a Em preparação; Aprovado passa a Publicado; Rejeitado passa a Em preparação ou Em revisão
- [ ] Aprovar e rejeitar não estão no menu do Marketeer: são decisões do Cliente (issue C13)
- [ ] Um criativo rejeitado mostra o motivo da rejeição, em "Ver criativo" e em "Atualizar estado"
- [ ] Só se edita um criativo em preparação ou rejeitado, e um criativo publicado não pode ser eliminado
- [ ] "Ver campanha" mostra o número de criativos da campanha em cada estado (parte de M04 que tinha ficado da Fase 3)
```

**Issue C13** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC13%5D%22

```markdown
- [ ] O menu de criativos do Cliente tem a opção "Aprovar ou rejeitar criativo" e diz quantos criativos estão à espera de aprovação
- [ ] A opção mostra os dados do criativo e as escolhas "Aprovar", "Rejeitar" e "Decidir mais tarde"
- [ ] Só se aprova ou rejeita um criativo em revisão; nos outros casos aparece o estado em que ele está
- [ ] Para rejeitar, o motivo é obrigatório
- [ ] Decisão do grupo: o criativo rejeitado fica no estado "Rejeitado", com o motivo à vista, e é o marketeer que o põe de novo em preparação
```

Por fim, no quadro Trello, move os cards das stories M14 e C13 de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/4.4-estados-e-aprovacao
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/4.4-estados-e-aprovacao` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/4.4-estados-e-aprovacao'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/4.4-estados-e-aprovacao' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/4.4-estados-e-aprovacao
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/4.4-estados-e-aprovacao
git switch -c feature/4.4-estados-e-aprovacao
```

  **Deves ver** `Deleted branch feature/4.4-estados-e-aprovacao (was ...)` e depois `Switched to a new branch 'feature/4.4-estados-e-aprovacao'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/4.4-estados-e-aprovacao` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 21 — Copia e grava os 7 commits

São 7 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 4.4 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 4.4. Eles estão na pasta `ctesp-ADC/fase-4/ficheiros/4.4/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.4 1
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(repositorios): mudar o estado de um criativo"
```

**Deves ver** uma linha a terminar em `3 files changed, 40 insertions(+), 1 deletion(-)`.

**Commit 2 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.4 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(criativos): mudar o estado de um criativo"
```

**Deves ver** uma linha a terminar em `2 files changed, 127 insertions(+), 3 deletions(-)`.

**Commit 3 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.4 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): atualizar o estado de um criativo no menu do marketeer"
```

**Deves ver** uma linha a terminar em `2 files changed, 141 insertions(+), 3 deletions(-)`.

**Commit 4 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.4 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(criativos): aprovar ou rejeitar um criativo em revisão"
```

**Deves ver** uma linha a terminar em `2 files changed, 89 insertions(+)`.

**Commit 5 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.4 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): aprovar ou rejeitar criativos no menu do cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 96 insertions(+), 4 deletions(-)`.

**Commit 6 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.4 6
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/servicos/criativos.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(campanhas): mostrar os criativos por estado de cada campanha"
```

**Deves ver** uma linha a terminar em `3 files changed, 57 insertions(+), 3 deletions(-)`.

**Commit 7 de 7**

```bash
python ../ctesp-ADC/copiar.py 4.4 7
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os estados dos criativos e a aprovação pelo cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 79 insertions(+), 2 deletions(-)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 4.4
git log --oneline -7
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 4.4` | `Tudo certo: o ramo 'feature/4.4-estados-e-aprovacao' está igual ao original no fim da unidade 4.4.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -7` | Os teus 7 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os estados dos criativos e a aprovação pelo cliente
xxxxxxx feat(campanhas): mostrar os criativos por estado de cada campanha
xxxxxxx feat(cli): aprovar ou rejeitar criativos no menu do cliente
xxxxxxx feat(criativos): aprovar ou rejeitar um criativo em revisão
xxxxxxx feat(cli): atualizar o estado de um criativo no menu do marketeer
xxxxxxx feat(criativos): mudar o estado de um criativo
xxxxxxx feat(repositorios): mudar o estado de um criativo
```

### Passo 23 — Experimenta o que gravaste

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

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/4.4-estados-e-aprovacao
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/4.4-estados-e-aprovacao -> feature/4.4-estados-e-aprovacao`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/4.4-estados-e-aprovacao?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/4.4-estados-e-aprovacao**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Estados do criativo e aprovação pelo cliente
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

Os criativos passam a ter um ciclo de vida, e o Cliente passa a aprová-los ou rejeitá-los.

- Regras das passagens de estado, num só dicionário
- Opção "Atualizar estado" no menu do Marketeer
- Opção "Aprovar ou rejeitar criativo" no menu do Cliente, com motivo obrigatório na rejeição
- Editar só em preparação ou depois de rejeitado; um criativo publicado não pode ser eliminado
- Número de criativos por estado em "Ver campanha" (parte de M04)

Closes #(número da issue M14)
Closes #(número da issue C13)

## Como testar

1. `python -m pytest` (500 testes)
2. `python -m gestor_campanhas`: como marketeer, enviar os dois criativos da campanha Natal 2026 para revisão
3. Como `cliente@empresa.pt`, aprovar um e rejeitar o outro; de volta ao marketeer, ver o motivo e publicar o aprovado
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories M14 e C13 para **Ready to Verify**.

### Passo 26 — Avisa Fabio

Diz a Fabio que o pull request da unidade 4.4 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 18 a 24.

### Passo 27 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/4.4-estados-e-aprovacao
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/4.4-estados-e-aprovacao` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 4.5 — Ficheiros dos criativos

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 28 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 4.5 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Ficheiros dos criativos**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (M13, C12), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Ricardo para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 29 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 30 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/4.5-ficheiros-dos-criativos
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/4.5-ficheiros-dos-criativos` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/4.5-ficheiros-dos-criativos'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `546 passed`.

Garante que tens os criativos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como marketeer (`1`, depois `marketeer@agencia.pt` e `marketeer12345`), escolhe `2` (Criativos) e o número da campanha `Natal 2026`. O menu tem agora `6. Anexar ficheiro` e `7. Pré-visualizar ficheiro`.

O `Banner de Natal` tem de estar `Em preparação` ou `Rejeitado`. Se no teu computador estiver noutro estado, usa o `Vídeo da montra` em vez dele.

| Escreves | Deves ver |
|---|---|
| `6` e Enter | O título `Anexar ficheiro` e a pergunta `Número do criativo (Enter para cancelar)` |
| O número do `Banner de Natal` | Uma explicação sobre "Copiar como caminho" e a pergunta `Caminho do ficheiro (Enter para cancelar)` |
| `exemplos/banner-natal.svg` | `Ficheiro banner-natal.svg anexado ao criativo Banner de Natal.` |
| Enter | A tabela |
| `7` e o número do `Banner de Natal` | O quadro a seguir e a pergunta `Abrir o ficheiro no programa predefinido? (s/n)` |

```text
Ficheiro do criativo Banner de Natal
  Nome:     banner-natal.svg
  Tipo:     Imagem (image/svg+xml)
  Tamanho:  639 bytes
```

Responde `s`. **Deves ver** `O ficheiro foi aberto noutra janela.` e, numa janela nova (normalmente o navegador), um banner vermelho com uma árvore e o texto `Natal 2026`. Fecha essa janela e volta ao terminal.

Carrega em Enter. Sai com `0`, Enter e `0` (Terminar sessão). Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`) e escolhe `3` (Criativos). O menu tem agora `4. Pré-visualizar ficheiro` e `5. Descarregar ficheiro`.

| Escreves | Deves ver |
|---|---|
| `2` e o número do `Banner de Natal` | Os dados do criativo, com a linha nova `Ficheiro:    banner-natal.svg` |
| Enter | A lista |
| `4`, o número do `Banner de Natal` e `n` | O mesmo quadro que o marketeer viu, com `Tamanho:  639 bytes` |
| Enter | A lista |
| `5` e o número do `Banner de Natal` | A pergunta `Pasta onde guardar a cópia (Enter para C:\Users\...\Downloads)` |
| Enter | `Cópia guardada em C:\Users\...\Downloads\banner-natal.svg` |
| Enter | A lista |

Abre a pasta Transferências no explorador de ficheiros: lá está o `banner-natal.svg`. Podes apagá-lo.

Sai com `0`, `0` e `0`.

O ficheiro anexado foi copiado para a pasta `dados/ficheiros`, dentro de uma pasta com o número do criativo. Confirma que o Git não o vê:

```bash
git status
```

**Deves ver** `nothing to commit, working tree clean`. A pasta `dados` está no `.gitignore`.

Confirma também:

- Entra como marketeer, escolhe `2` e a campanha `Natal 2026`. Escolhe `6` e o número de um criativo `Aprovado` ou `Publicado` (o `Banner de Natal`, se fizeste a unidade 4.4). Escreve `exemplos/banner-natal.svg`: aparece `Só se pode mudar o ficheiro de um criativo em preparação ou rejeitado. Este criativo está ...`
- Escolhe `6` e o número de um criativo `Em preparação` ou `Rejeitado`. Escreve `"exemplos/nao-existe.png"`, com as aspas: aparece `Não existe nenhum ficheiro em exemplos\nao-existe.png. O ficheiro não foi anexado.` (as aspas foram tiradas).
- Anexa agora `exemplos/banner-natal.svg` a esse criativo. Escolhe `6` outra vez, com o mesmo criativo: antes do caminho aparece `O criativo ... já tem o ficheiro banner-natal.svg, que vai ser substituído.` Carrega em Enter para cancelar.
- Entra como `cliente@empresa.pt` / `cliente12345`, escolhe `3` e descarrega esse ficheiro duas vezes (`5`, o número e Enter). Da segunda, a cópia chama-se `banner-natal (1).svg`. Apaga as duas cópias da pasta Transferências.
- Ainda como cliente, escolhe `5` e o número de um criativo sem ficheiro: aparece `O criativo ... ainda não tem ficheiro.`

### Passo 31 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

### Passo 32 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move os cards das stories M13 e C12 para **Ready**.

### Passo 33 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/4.5-ficheiros-dos-criativos
python ../ctesp-ADC/verificar.py 4.5
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/4.5-ficheiros-dos-criativos` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 4.5` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 4.5 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.5.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 34 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Ricardo](ricardo.md)).

Diz também a Fabio que já pode avançar ([página de Fabio](fabio.md), passos 25 a 34).

---

## Outras tarefas desta fase

### Passo 35 — Atualiza a página "Guia de utilização" da wiki

A página passa a explicar os criativos, com o que o Marketeer e o Cliente podem fazer, e a despesa das campanhas.

Faz este passo depois de a unidade 4.6 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Guia-de-utilizacao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Guia de utilização** na lista de páginas, à direita, e depois em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar o Guia de utilização para a versão 0.4.0` e clica em **Save page**.

**Deves ver** a página a começar por `Como usar a aplicação, na versão 0.4.0.` e com as secções novas `Criativos (Marketeer)`, `Estados de um criativo`, `Criativos (Cliente)` e `Ficheiros dos criativos`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 4.1 — Criar, editar e eliminar criativos

- **`gestor_campanhas/bd.py`** ganha a tabela `criativos`. A coluna `campanha_id` é uma chave estrangeira para a tabela `campanhas`, sem `ON DELETE CASCADE`: o SQLite recusa apagar uma campanha que ainda tenha criativos. A coluna `estado` tem um `CHECK`, que só aceita os cinco estados. A tabela já tem as colunas do custo, do prazo, do público-alvo, da plataforma, do motivo de rejeição e do ficheiro, que só vão ser usadas nas unidades seguintes: assim não é preciso alterar a tabela a meio da fase (o `CREATE TABLE IF NOT EXISTS` não acrescenta colunas a uma tabela que já existe).
- **`gestor_campanhas/modelos.py`** ganha as constantes dos estados (`EM_PREPARACAO`, `EM_REVISAO`, `PUBLICADO`; `APROVADO` e `REJEITADO` já existiam, dos pedidos de campanha), o dicionário `NOMES_ESTADOS_CRIATIVO`, com o nome de cada estado como aparece no ecrã, e a classe `Criativo`. Tal como a `Campanha`, tem um campo que não está na tabela: `campanha_nome`, que vem da tabela `campanhas`.
- **`gestor_campanhas/repositorios/criativos.py`** é novo. A consulta `_SELECIONAR` junta cada criativo à sua campanha com um `JOIN`, para trazer o nome da campanha de uma vez. `contar_por_campanha` diz quantos criativos uma campanha tem.
- **`gestor_campanhas/servicos/criativos.py`** é novo e tem as regras. Um criativo não tem marketeer: pertence a uma campanha, e a campanha é que tem o marketeer. Por isso `obter_do_marketeer` lê o criativo e confirma que a campanha dele é do marketeer que o pede. Como nas campanhas, a mensagem é a mesma quando o criativo não existe e quando é de outro.
- **`gestor_campanhas/servicos/campanhas.py`**: `eliminar` conta os criativos da campanha antes de apagar e, se houver algum, lança um `ErroValidacao` com a mensagem a dizer quantos são. Assim, o utilizador vê uma frase clara em vez de um erro do SQLite.
- **`gestor_campanhas/cli/criativos.py`** é novo. `do_marketeer` mostra as campanhas e pede uma; `da_campanha` é o ciclo do menu de criativos dessa campanha. As opções estão na lista `ACOES`, com o texto e a função de cada uma: para acrescentar uma opção, nas unidades seguintes, basta acrescentar uma linha à lista.
- **`gestor_campanhas/cli/campanhas.py`**: "Eliminar campanha" passa a apanhar o `ErroValidacao` e a mostrar a mensagem.
- **`gestor_campanhas/cli/perfis.py`**: o menu do Marketeer ganha a opção "Criativos", a seguir a "Campanhas".
- **`tests/test_criativos.py`** é novo. Testa as regras (nome obrigatório, só nas campanhas do próprio, eliminar) e o ecrã, com a fixture `teclado`. Os testes de `test_campanhas.py` e de `test_bd.py` ganham os casos da campanha com criativos e da tabela nova.
- **`docs/`**: o guia de utilização ganha a secção dos criativos do Marketeer, a arquitetura a tabela `criativos`, e a referência os módulos novos.

### Unidade 4.4 — Estados do criativo e aprovação pelo cliente

- **`gestor_campanhas/servicos/criativos.py`** tem as regras dos estados:
  - O dicionário `PROXIMOS_ESTADOS` diz, para cada estado, para onde o marketeer o pode mudar. Aprovado e Rejeitado não aparecem como destino, porque essa decisão é do cliente; Publicado não tem destinos, porque é o fim do caminho. Assim, as regras estão todas num só sítio, e o menu só tem de as ler.
  - `mudar_estado` confirma que o criativo é do marketeer e que a passagem está no dicionário; se não estiver, a mensagem diz de onde para onde não se pode passar.
  - `EDITAVEIS` são os estados em que o criativo ainda pode mudar (em preparação e rejeitado). `editar` usa-o; `eliminar` passa a recusar os criativos publicados, para não se perder o registo do que já saiu.
  - `aprovar` e `rejeitar` usam `_em_revisao_do_cliente`, que confirma que o criativo é de uma campanha do cliente e que está em revisão. `rejeitar` exige o motivo e guarda-o com o estado.
  - `contar_por_estado` devolve um dicionário, por exemplo `{"rejeitado": 1, "publicado": 1}`, pela ordem de `NOMES_ESTADOS_CRIATIVO` e sem os estados que não têm criativos.
- **`gestor_campanhas/repositorios/criativos.py`** ganha `definir_estado`, que muda o estado e o motivo de uma vez. Quando não se indica o motivo, ele fica vazio: assim, um criativo que sai de "Rejeitado" não fica com um motivo antigo à vista.
- **`gestor_campanhas/modelos.py`**: a classe `Criativo` ganha `motivo_rejeicao`.
- **`gestor_campanhas/cli/criativos.py`**:
  - `atualizar_estado` mostra o estado atual e monta o menu só com os destinos de `PROXIMOS_ESTADOS`, com os textos de `DESCRICOES_ESTADOS` ("Enviar ao cliente para revisão" em vez de "Em revisão", que diz o que acontece).
  - `decidir` é a opção do cliente. Mostra os dados antes de pedir a decisão, para o cliente saber o que está a aprovar.
  - `do_cliente` passa a contar os criativos em revisão e a mostrar a frase "Há ... à espera da sua aprovação."
- **`gestor_campanhas/cli/campanhas.py`**: `resumo_criativos` escreve a linha "Criativos: 2 (Rejeitado: 1, Publicado: 1)", e "Ver campanha" mostra-a. Uma campanha sem criativos mostra "Criativos: 0".
- **`tests/`**: `test_criativos.py` testa cada passagem permitida e proibida, a aprovação, a rejeição sem motivo e os menus; `test_campanhas.py` testa o resumo dos estados.
- **`docs/`**: o guia de utilização explica as duas opções novas, e a arquitetura ganha a secção "Estados de um criativo", com o desenho das passagens.
