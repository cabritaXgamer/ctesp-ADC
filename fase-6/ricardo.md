# Fase 6 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 6 (Comentários, notificações, painel e relatório), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 10 | Fazer a unidade 6.1 — Comentários dos criativos e respostas | No início da fase |
| 11 a 17 | Rever e juntar a unidade 6.3 (de Tomas) | Quando Tomas avisar |
| 18 a 27 | Fazer a unidade 6.4 — Relatório das campanhas em CSV | A seguir ao teu passo anterior |
| 28 a 36 | Preparar a release v0.6.0 | Quando Fabio avisar |
| 37 a 42 | Publicar a release v0.6.0 e pedir o regresso ao develop | Quando Fabio avisar |
| 43 a 44 | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | Em qualquer altura durante a fase |

---

## Fazer a unidade 6.1 — Comentários dos criativos e respostas

O Cliente passa a poder comentar os criativos das suas campanhas, para dizer ao marketeer o que quer que mude. O Marketeer vê os comentários no detalhe de cada criativo, com a data e o autor, e responde a cada um. A lista dos criativos do Marketeer diz quantos comentários estão por responder.

### Passo 1 — Confirma que podes começar

A fase anterior tem de estar fechada: todos os pull requests juntos e o `develop` do teu computador atualizado. Se for a primeira fase, tens de ter feito a [Preparação](../preparacao.md).

### Passo 2 — Fica com as issues da unidade 6.1

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: C18, M17. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C18** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC18%5D%22

```markdown
- [ ] O menu de criativos do Cliente tem a opção nova "6. Comentar criativo", no fim
- [ ] "Comentar criativo" pede o número de um criativo do cliente, mostra os comentários que ele já tem e pede o comentário ou a sugestão
- [ ] O comentário fica com a data, a hora e o nome de quem o escreveu; um comentário vazio não é guardado (Enter cancela)
- [ ] Pode comentar-se um criativo em qualquer estado
- [ ] Um cliente só comenta os criativos das suas campanhas
- [ ] "Ver criativo" do Cliente mostra também os comentários, com as respostas do marketeer
```

**Issue M17** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM17%5D%22

```markdown
- [ ] "Ver criativo" do Marketeer mostra os comentários do criativo por ordem, cada um com o número, o autor, a data e as respostas; os que não têm resposta dizem `(ainda sem resposta)`
- [ ] O menu de criativos do Marketeer tem a opção nova "8. Responder a comentário", no fim, que pede o criativo, o número do comentário e a resposta
- [ ] Um comentário pode ter mais do que uma resposta; não se responde a uma resposta
- [ ] Um marketeer só responde aos comentários dos criativos das suas campanhas
- [ ] Por baixo da lista dos criativos aparece quantos comentários do cliente estão por responder, e em que criativos
- [ ] Os dados de demonstração têm um comentário da Carla ao criativo `Vídeo da montra`
```

Por fim, no quadro Trello, move os cards das stories C18 e M17 de **Sprint Backlog** para **Work In Progress**.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/6.1-comentarios-dos-criativos
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/6.1-comentarios-dos-criativos` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/6.1-comentarios-dos-criativos'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/6.1-comentarios-dos-criativos' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/6.1-comentarios-dos-criativos
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/6.1-comentarios-dos-criativos
git switch -c feature/6.1-comentarios-dos-criativos
```

  **Deves ver** `Deleted branch feature/6.1-comentarios-dos-criativos (was ...)` e depois `Switched to a new branch 'feature/6.1-comentarios-dos-criativos'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/6.1-comentarios-dos-criativos` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 4 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 6.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 6.1. Eles estão na pasta `ctesp-ADC/fase-6/ficheiros/6.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.1 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela dos comentários dos criativos"
```

**Deves ver** uma linha a terminar em `2 files changed, 50 insertions(+)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.1 2
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/comentarios.py`, `tests/test_comentarios.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar e ler os comentários dos criativos"
```

**Deves ver** uma linha a terminar em `3 files changed, 211 insertions(+)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.1 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/comentarios.py`, `tests/test_comentarios.py`.

```bash
git add -A
git commit -m "feat(comentarios): comentar um criativo e responder aos comentários"
```

**Deves ver** uma linha a terminar em `2 files changed, 219 insertions(+)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.1 4
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/criativos.py`, `tests/test_comentarios.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): comentários nos menus de criativos do cliente e do marketeer"
```

**Deves ver** uma linha a terminar em `3 files changed, 270 insertions(+), 6 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.1 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dados_demo.py`, `tests/test_comentarios.py`.

```bash
git add -A
git commit -m "feat(demo): acrescentar um comentário de demonstração"
```

**Deves ver** uma linha a terminar em `2 files changed, 95 insertions(+), 4 deletions(-)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.1 6
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os comentários dos criativos"
```

**Deves ver** uma linha a terminar em `3 files changed, 73 insertions(+), 5 deletions(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 6.1
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 6.1` | `Tudo certo: o ramo 'feature/6.1-comentarios-dos-criativos' está igual ao original no fim da unidade 6.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os comentários dos criativos
xxxxxxx feat(demo): acrescentar um comentário de demonstração
xxxxxxx feat(cli): comentários nos menus de criativos do cliente e do marketeer
xxxxxxx feat(comentarios): comentar um criativo e responder aos comentários
xxxxxxx feat(repositorios): guardar e ler os comentários dos criativos
xxxxxxx feat(bd): criar a tabela dos comentários dos criativos
```

### Passo 6 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `747 passed`.

Cria o comentário de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

**Deves ver**, entre as outras linhas, `Comentários criados: 1 (os restantes já existiam).` Se aparecer `0`, já tinhas corrido este comando com o código desta unidade, e o comentário já existe.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como cliente (`1`, depois `cliente@empresa.pt` e `cliente12345`) e escolhe `3` (Criativos). O menu tem agora `6. Comentar criativo`, no fim.

| Escreves | Deves ver |
|---|---|
| `2` e o número do `Vídeo da montra` (primeira coluna) | Os dados do criativo e, por baixo, os comentários (ver a seguir) |
| Enter | A lista dos criativos outra vez |
| `6` e o número do `Banner de Natal` | `Criativo Banner de Natal, da campanha Natal 2026. Estado: ...` (o estado depende do que fizeste na Fase 4), `Comentários: nenhum.` e a pergunta `Comentário ou sugestão (Enter para cancelar)` |
| `O logótipo da loja devia aparecer maior` | `Comentário guardado. O marketeer vai vê-lo no detalhe do criativo.` |

Os comentários do `Vídeo da montra` são assim (a data e a hora são as do momento em que correste o `dados_demo`, e o número pode ser outro):

```text
Comentários
  N.º 1, de Carla Cliente, em 2026-11-19 11:03:
    Gostava que o vídeo mostrasse a montra à noite, com as luzes acesas.
    (ainda sem resposta)
```

Sai com Enter, `0` e `0`. Entra como marketeer (`1`, `marketeer@agencia.pt` e `marketeer12345`), escolhe `2` (Criativos) e o número da campanha `Natal 2026`.

**Deves ver**, por baixo da tabela, a linha nova `Há 2 comentários do cliente por responder (criativos n.º 1, 2).`, com os números do `Banner de Natal` e do `Vídeo da montra`. O menu tem agora `8. Responder a comentário`.

| Escreves | Deves ver |
|---|---|
| `8` e o número do `Vídeo da montra` | `Criativo Vídeo da montra`, o comentário da Carla e a pergunta `Número do comentário a que responde (Enter para cancelar)` |
| O número do comentário da Carla (o que aparece em `N.º ...`) | A pergunta `Resposta (Enter para cancelar)` |
| `Vou gravar o vídeo ao fim da tarde, com as luzes acesas` | `Resposta guardada. O cliente vai vê-la no detalhe do criativo.` |
| Enter | A tabela e `Há 1 comentário do cliente por responder (criativo n.º ...)`, com o número do `Banner de Natal` |
| `3` e o número do `Vídeo da montra` | Os dados do criativo e, por baixo do comentário da Carla, `Resposta de Miguel Marketeer, em ...:` e a resposta |

Sai com Enter, `0`, Enter e `0`. Os comentários não se apagam: ficam nos teus dados, e nas unidades seguintes vais vê-los outra vez.

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/6.1-comentarios-dos-criativos
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/6.1-comentarios-dos-criativos -> feature/6.1-comentarios-dos-criativos`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/6.1-comentarios-dos-criativos?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/6.1-comentarios-dos-criativos**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Comentários dos criativos e respostas
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Cliente passa a comentar os criativos e o Marketeer a responder aos comentários.

- Tabela `comentarios`, com os comentários e as respostas, classe `Comentario` e repositório dos comentários
- Regras: comentar só os criativos do cliente, responder só nos criativos do marketeer, texto obrigatório, sem respostas a respostas
- Opção "Comentar criativo" no menu de criativos do Cliente e "Responder a comentário" no do Marketeer; os comentários aparecem em "Ver criativo" dos dois
- Aviso dos comentários por responder na lista dos criativos do Marketeer
- Um comentário de demonstração

Closes #(número da issue C18)
Closes #(número da issue M17)

## Como testar

1. `python -m pytest` (747 testes)
2. `python -m gestor_campanhas.dados_demo` e depois `python -m gestor_campanhas`
3. Como `cliente@empresa.pt`, comentar o criativo Banner de Natal; como `marketeer@agencia.pt`, responder ao comentário do Vídeo da montra
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 6 — Comentários, notificações e relatórios`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories C18 e M17 para **Ready to Verify**.

### Passo 9 — Avisa Fabio

Diz a Fabio que o pull request da unidade 6.1 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 1 a 7.

### Passo 10 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/6.1-comentarios-dos-criativos
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/6.1-comentarios-dos-criativos` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 6.3 — Painel de marketeers

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 11 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 6.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Painel de marketeers**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 3 linhas `Closes #` seguida de um número, uma por issue (A17, A18, A19), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Tomas para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/6.3-painel-de-marketeers
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/6.3-painel-de-marketeers` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/6.3-painel-de-marketeers'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `845 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, `admin@agencia.pt` e `admin12345`). O menu tem agora `8. Painel de marketeers`, e as opções da conta passaram para `9` e `10`. Escolhe `8`.

**Deves ver** uma linha por marketeer. Os números dependem do que fizeste nas fases anteriores; se fizeste os passos da unidade 4.4 (banner publicado, vídeo rejeitado), é assim:

```text
N.º  Marketeer         Campanhas ativas  Ativos  Em atraso  Concluídos  Última atividade  Situação
---  ----------------  ----------------  ------  ---------  ----------  ----------------  --------
3    Marta Marques     1                 1       0          0           2026-11-17
2    Miguel Marketeer  1                 2       1          1           2026-11-17
```

A `Última atividade` é o dia em que criaste os criativos de demonstração, porque até agora a atividade não era registada. O Miguel tem 1 criativo em atraso: o `Cartaz dos lanches`, com o prazo `2026-08-25`. Por baixo aparecem as explicações das colunas e `Nenhum marketeer está sem atividade.`

| Escreves | Deves ver |
|---|---|
| `1` e o número do Miguel (primeira coluna) | O título `Trabalho de Miguel Marketeer`, a campanha `Natal 2026` (`Por começar`) com o banner e o vídeo, a campanha `Regresso às aulas` (`Terminada`) com o cartaz e `Em atraso` na coluna `Situação`, e por fim `Últimas atividades: nenhuma registada.` |
| Enter, `2`, `2026-11-01` e `2026-11-30` | O título `Carga de trabalho de 2026-11-01 a 2026-11-30` e a tabela: a Marta com `0` (o criativo dela não tem prazo) e o Miguel com `2` criativos, os de novembro |
| Enter, `3` | `Um marketeer fica sem atividade ao fim de 7 dias sem mexer nos criativos.` e a pergunta `Número de dias novo (Enter para manter)` |
| `1` | `Guardado. Um marketeer fica sem atividade ao fim de 1 dia.` |
| Enter | Na coluna `Situação`, `Parado há N dias` nos marketeers cuja última atividade não é de hoje, e por baixo `Marketeers sem atividade: ...`, com os nomes |

Agora a Marta vai mexer num criativo. Sai com `0` e `0` e entra como `marta@agencia.pt` / `marta12345`:

| Escreves | Deves ver |
|---|---|
| `2` e o número da campanha `Bicicletas de primavera` | O criativo `Anúncio da bicicleta elétrica` |
| `2`, o número do anúncio, Enter no nome, `Bicicleta elétrica em fundo branco` na descrição e Enter nas outras perguntas | `Criativo guardado.` |

Sai com Enter, `0`, Enter e `0`. Entra outra vez como administrador e escolhe `8`:

| Escreves | Deves ver |
|---|---|
| (o painel) | A `Última atividade` da Marta passou a hoje, e ela já não aparece como parada |
| `1` e o número da Marta | A campanha `Bicicletas de primavera` e, em `Últimas atividades`, `Editou o criativo Anúncio da bicicleta elétrica (campanha Bicicletas de primavera)` |
| Enter, `3` e `7` | `Guardado. Um marketeer fica sem atividade ao fim de 7 dias.` |

Sai com Enter, `0` e `0`. Põe sempre os dias outra vez em 7, para o painel das unidades seguintes bater certo.

Confirma também:

- No painel, `2`, `2026-11-30` em `Desde` e `2026-11-01` em `Até`: aparece `A data inicial não pode ser posterior à data final.`
- `2`, Enter em `Desde` e `2026-11-30` em `Até`: o título é `Carga de trabalho até 2026-11-30`.
- `3` e `0`: aparece `O número de dias tem de ser pelo menos 1. Nada foi alterado.`, e o painel continua a dizer `há 7 dias ou mais`.
- `1` e o número de um cliente (por exemplo o da Carla, que vês na opção `1. Clientes`): aparece `Não existe nenhum marketeer com o número ...`.
- Como Miguel, `2`, a campanha `Natal 2026`, `1` (Criar criativo) com o nome `Teste do painel` e Enter no resto; depois `4`, o número dele e `s`. No painel, em `1` e o número do Miguel, as duas primeiras `Últimas atividades` são `Eliminou o criativo Teste do painel (campanha Natal 2026)` e `Criou o criativo Teste do painel (campanha Natal 2026)`.

### Passo 14 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 15 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move os cards das stories A17, A18 e A19 para **Ready**.

### Passo 16 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/6.3-painel-de-marketeers
python ../ctesp-ADC/verificar.py 6.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/6.3-painel-de-marketeers` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 6.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 6.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 6.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 17 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 18.

---

## Fazer a unidade 6.4 — Relatório das campanhas em CSV

O Cliente passa a poder exportar um relatório das suas campanhas, com os criativos, os custos e o budget, para um ficheiro CSV que se abre diretamente no Excel. A opção fica em "Campanhas".

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Painel de marketeers** (unidade 6.3) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 6.4

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: C20. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C20** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC20%5D%22

```markdown
- [ ] A opção "Campanhas" do Cliente tem a opção nova "3. Exportar relatório"
- [ ] O relatório tem uma linha por criativo, com a campanha (nome, estado, início, fim, marketeer, budget, despesa e restante) e o criativo (nome, estado, plataforma, prazo e custo)
- [ ] Uma campanha sem criativos tem uma linha só com os dados da campanha; um valor que não existe (um budget por definir, um prazo por indicar) fica vazio
- [ ] Um cliente só vê as suas campanhas no relatório
- [ ] O ficheiro chama-se `relatorio-campanhas-AAAA-MM-DD.csv`, com a data do dia, e vai para a pasta indicada ou, com Enter, para a pasta `Downloads`
- [ ] Nenhum ficheiro é apagado: se já houver um relatório com o mesmo nome, o novo fica com um número entre parênteses
- [ ] O ficheiro abre no Excel com cada valor na sua coluna, os acentos certos e os valores em euros reconhecidos como números (separador `;`, vírgula nas casas decimais, UTF-8 com BOM)
- [ ] Um cliente sem campanhas, ou uma pasta que não existe, dão uma mensagem e nenhum ficheiro é gravado
- [ ] O relatório é só em CSV (a story fala em PDF ou CSV)
```

Por fim, no quadro Trello, move o card da story C20 de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/6.4-exportar-relatorio
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/6.4-exportar-relatorio` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/6.4-exportar-relatorio'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/6.4-exportar-relatorio' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/6.4-exportar-relatorio
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/6.4-exportar-relatorio
git switch -c feature/6.4-exportar-relatorio
```

  **Deves ver** `Deleted branch feature/6.4-exportar-relatorio (was ...)` e depois `Switched to a new branch 'feature/6.4-exportar-relatorio'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/6.4-exportar-relatorio` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 21 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 6.4 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 6.4. Eles estão na pasta `ctesp-ADC/fase-6/ficheiros/6.4/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 6.4 1
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/servicos/ficheiros.py`, `gestor_campanhas/servicos/relatorios.py`, `tests/test_relatorios.py`.

```bash
git add -A
git commit -m "feat(relatorios): gravar o relatório das campanhas de um cliente em CSV"
```

**Deves ver** uma linha a terminar em `3 files changed, 295 insertions(+), 8 deletions(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 6.4 2
```

**Deves ver** `Copiados 5 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/cli/comum.py`, `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`, `tests/test_relatorios.py`.

```bash
git add -A
git commit -m "feat(cli): exportar o relatório nas campanhas do cliente"
```

**Deves ver** uma linha a terminar em `5 files changed, 107 insertions(+), 20 deletions(-)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 6.4 3
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar o relatório das campanhas"
```

**Deves ver** uma linha a terminar em `3 files changed, 46 insertions(+)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 6.4
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 6.4` | `Tudo certo: o ramo 'feature/6.4-exportar-relatorio' está igual ao original no fim da unidade 6.4.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar o relatório das campanhas
xxxxxxx feat(cli): exportar o relatório nas campanhas do cliente
xxxxxxx feat(relatorios): gravar o relatório das campanhas de um cliente em CSV
```

### Passo 23 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `863 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`) e escolhe `2` (Campanhas). O menu tem agora `3. Exportar relatório`.

| Escreves | Deves ver |
|---|---|
| `3` | O título `Exportar relatório`, a explicação do que o relatório tem e a pergunta `Pasta onde guardar o relatório (Enter para C:\Users\...\Downloads)` |
| Enter | `Relatório gravado em C:\Users\...\Downloads\relatorio-campanhas-AAAA-MM-DD.csv`, com a data de hoje |
| Enter, `3` e Enter outra vez | `Relatório gravado em ...\relatorio-campanhas-AAAA-MM-DD (1).csv`: o primeiro não foi apagado |

Sai com Enter, `0` e `0`. Abre a pasta `Downloads` e abre o ficheiro `relatorio-campanhas-...csv` com o Bloco de Notas (botão direito, **Abrir com**). As duas primeiras linhas são assim (os estados dos criativos dependem do que fizeste na Fase 4):

```text
Campanha;Estado da campanha;Início;Fim;Marketeer;Budget (€);Despesa (€);Restante (€);Criativo;Estado do criativo;Plataforma;Prazo;Custo (€)
Natal 2026;Por começar;2026-12-01;2026-12-24;Miguel Marketeer;1500,00;1300,00;200,00;Banner de Natal;Em preparação;Facebook;2026-11-25;400,00
```

A linha seguinte é a do `Vídeo da montra`, com os mesmos dados da campanha. Se tiveres o Excel, abre o ficheiro com ele: cada valor fica na sua coluna, e os valores em euros ficam alinhados à direita, como números.

Agora uma campanha sem budget. Entra como `beatriz@bicicletas.pt` / `beatriz12345`, escolhe `2`, `3` e Enter. Abre o ficheiro novo na pasta `Downloads` (o que tem o número mais alto entre parênteses):

```text
Campanha;Estado da campanha;Início;Fim;Marketeer;Budget (€);Despesa (€);Restante (€);Criativo;Estado do criativo;Plataforma;Prazo;Custo (€)
Bicicletas de primavera;Em curso;;;Marta Marques;;0,00;;Anúncio da bicicleta elétrica;Em preparação;;;
```

As datas, o budget, o restante, a plataforma, o prazo e o custo estão vazios, porque não foram definidos. Se o budget da campanha já tiver sido aprovado nalguma unidade anterior, aparece o valor. Sai com Enter, `0` e `0`.

Os ficheiros de teste podem ser apagados da pasta `Downloads`: não vão para o Git.

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/6.4-exportar-relatorio
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/6.4-exportar-relatorio -> feature/6.4-exportar-relatorio`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/6.4-exportar-relatorio?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/6.4-exportar-relatorio**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Relatório das campanhas em CSV
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Cliente passa a exportar um relatório das suas campanhas em CSV.

- Montagem e gravação do relatório, com o módulo `csv` da biblioteca padrão, num formato que o Excel em português abre diretamente
- `caminho_livre`, que escolhe o nome do ficheiro sem apagar nenhum que já exista, agora partilhado com "Descarregar ficheiro"
- Opção "Exportar relatório" nas campanhas do Cliente; a pasta `Downloads` passa a ser dada por `comum.pasta_transferencias`, usada pelos dois menus

Closes #(número da issue C20)

## Como testar

1. `python -m pytest` (863 testes)
2. `python -m gestor_campanhas`
3. Como `cliente@empresa.pt`, exportar o relatório para a pasta `Downloads` e abri-lo no Excel; como `beatriz@bicicletas.pt`, exportar e confirmar as colunas vazias da campanha sem budget
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 6 — Comentários, notificações e relatórios`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move o card da story C20 para **Ready to Verify**.

### Passo 26 — Avisa Fabio

Diz a Fabio que o pull request da unidade 6.4 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 18 a 24.

### Passo 27 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/6.4-exportar-relatorio
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/6.4-exportar-relatorio` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Preparar a release v0.6.0

Fecha a fase com a versão 0.6.0: sobe o número da versão, acrescenta a secção desta versão ao registo de alterações e atualiza o README. Esta unidade vai para o `main`, e não para o `develop`.

### Passo 28 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Relatório das campanhas em CSV** (unidade 6.4) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 29 — Cria a issue da unidade 6.5

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[6.5] Release v0.6.0
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Publicar a versão 0.6.0, com as user stories da Fase 6 (comentários, notificações, painel de marketeers e relatório).

## O que inclui

- [ ] Versão 0.6.0 em `gestor_campanhas/__init__.py`
- [ ] Registo de alterações (`CHANGELOG.md`)
- [ ] README atualizado
- [ ] Pull request para `main`
- [ ] Tag e release `v0.6.0` no GitHub
- [ ] `main` de volta ao `develop`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 6 — Comentários, notificações e relatórios`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 30 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c release/v0.6.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c release/v0.6.0` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'release/v0.6.0'`.

**Se em vez disso aparecer** `fatal: a branch named 'release/v0.6.0' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..release/v0.6.0
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D release/v0.6.0
git switch -c release/v0.6.0
```

  **Deves ver** `Deleted branch release/v0.6.0 (was ...)` e depois `Switched to a new branch 'release/v0.6.0'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch release/v0.6.0` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 31 — Copia e grava os 3 commits

São 3 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 6.5 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 6.5. Eles estão na pasta `ctesp-ADC/fase-6/ficheiros/6.5/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 3**

```bash
python ../ctesp-ADC/copiar.py 6.5 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__init__.py`.

```bash
git add -A
git commit -m "chore(release): passar a versão para 0.6.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Commit 2 de 3**

```bash
python ../ctesp-ADC/copiar.py 6.5 2
```

**Deves ver** `Copiados 1 ficheiro`: `CHANGELOG.md`.

```bash
git add -A
git commit -m "docs(release): registar as alterações da versão 0.6.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 25 insertions(+)`.

**Commit 3 de 3**

```bash
python ../ctesp-ADC/copiar.py 6.5 3
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(release): atualizar o README para a versão 0.6.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 29 insertions(+), 7 deletions(-)`.


### Passo 32 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 6.5
git log --oneline -3
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 6.5` | `Tudo certo: o ramo 'release/v0.6.0' está igual ao original no fim da unidade 6.5.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -3` | Os teus 3 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(release): atualizar o README para a versão 0.6.0
xxxxxxx docs(release): registar as alterações da versão 0.6.0
xxxxxxx chore(release): passar a versão para 0.6.0
```

### Passo 33 — Experimenta o que gravaste

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `863 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v0.6.0`. Sai com `0`.

### Passo 34 — Envia o ramo para o GitHub

```bash
git push -u origin release/v0.6.0
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      release/v0.6.0 -> release/v0.6.0`.

### Passo 35 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `main`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/main...release/v0.6.0?expand=1

**b)** Confirma, no topo, que está **base: main** e **compare: release/v0.6.0**. O link do ponto a) já abre com o `main` escolhido. Se estiver **base: develop**, clica aí e escolhe `main`. Uma release vai para o `main`, que é o ramo das versões entregues.

**c)** No título, cola:

```text
Release v0.6.0
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Não é preciso trocar nada:

```markdown
## O que muda

Prepara a versão 0.6.0.

- Versão passa de 0.5.0 para 0.6.0
- `CHANGELOG.md` com a secção da versão 0.6.0
- README atualizado: perfis, tabela de versões, dados de demonstração e secções novas sobre os comentários e as notificações, o painel de marketeers e o relatório

Este pull request vai para o `main`. A issue da release é fechada pelo pull request que leva a release de volta ao `develop`.

## Como testar

1. `python -m pytest` (863 testes)
2. `python -m sphinx -W -b html docs docs/_build/html`
3. `python -m gestor_campanhas`: o título mostra `v0.6.0`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 6 — Comentários, notificações e relatórios`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** Confirma o destino. Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.6.0`. Se disser `into develop`, **não avises ninguém ainda**: clica em **Edit**, à direita do título, clica em **base: develop**, escolhe `main`, confirma em **Change base** e clica em **Save**.

### Passo 36 — Avisa Fabio

Diz a Fabio que o pull request da release v0.6.0 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 25 a 32.

---

## Publicar a release v0.6.0 e pedir o regresso ao develop

Com a release no `main`, falta marcá-la com uma tag e levar os commits dela de volta ao `develop`.

### Passo 37 — Confirma que o main já tem a versão 0.6.0

Faz este passo quando Fabio te avisar que a release está no `main`.

A tag vai ser criada no `main`. Se o `main` ainda não tiver a versão nova, a tag fica a marcar o código da versão anterior. Foi o que aconteceu nas duas primeiras fases.

Abre https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py

**Deves ver** a linha `__version__ = "0.6.0"`.

Se vires outra versão, **não publiques a release**. O pull request foi junto ao `develop` em vez do `main`. Avisa Fabio e corrijam assim: abre https://github.com/Blive77/ADC-TrabGrupo/compare/main...develop?expand=1, cria um pull request com o título `Release v0.6.0`, Fabio aprova e junta, e só depois voltas a este passo.

### Passo 38 — Publica a release v0.6.0 no GitHub

Publicar a release cria a **tag**, uma etiqueta que marca para sempre o commit desta versão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/releases/new

**b)** Clica em **Choose a tag**, escreve `v0.6.0` e clica em **Create new tag: v0.6.0 on publish**.

**c)** Em **Target**, escolhe `main`.

**d)** Em **Release title**, cola:

```text
v0.6.0 — Comentários, notificações, painel e relatório
```

**e)** Na caixa de texto, cola:

````markdown
## Comentários, notificações, painel e relatório

O Cliente passa a comentar os criativos e o Marketeer a responder. Os dois recebem notificações do que lhes diz respeito, na aplicação e por email. O Administrador tem um painel para comparar o trabalho dos marketeers, e o Cliente exporta um relatório das suas campanhas em CSV. Com esta versão ficam feitas as 57 user stories do projeto.

### Acrescentado

- Comentários dos criativos: o Cliente comenta ou sugere alterações; o Marketeer vê os comentários no detalhe do criativo e responde a cada um
- Notificações para o Marketeer (campanha atribuída, pedido de budget, comentário) e para o Cliente (decisão de um pedido de budget, criativos criados, alterados ou eliminados, respostas), na opção nova "Notificações", de onde se abre o item; cada notificação é também enviada por email
- Aviso das notificações por ler, por cima do menu
- Painel de marketeers, na opção nova "Painel de marketeers" do Administrador: campanhas ativas, criativos ativos, em atraso e concluídos, última atividade, marketeers sem atividade, trabalho de cada marketeer e comparação num período
- Relatório das campanhas do Cliente em CSV, em "Campanhas", "Exportar relatório"
- Um comentário de demonstração

### Alterado

- O aviso de campanha atribuída passa a ser também uma notificação
- Os menus do Marketeer e do Cliente ganharam "Notificações", e o do Administrador "Painel de marketeers"; as opções da conta mudaram de número
- Os menus de criativos e as campanhas do Cliente ganharam uma opção no fim

### User stories

C17, C18, C19, C20, M17, M18, A17, A18 e A19.

Ficam também concluídos os avisos sobre os pedidos de budget (C17 e M18), adiados na versão 0.5.0.

### Como experimentar

```
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

Entrar com `cliente@empresa.pt` / `cliente12345` e escolher "Criativos" e depois "Comentar criativo"; com `marketeer@agencia.pt` / `marketeer12345` e escolher "Notificações"; ou com `admin@agencia.pt` / `admin12345` e escolher "Painel de marketeers". As outras contas de demonstração estão no README.
````

**f)** Clica em **Publish release**.

**Deves ver** a página da release, e a tag `v0.6.0` em https://github.com/Blive77/ADC-TrabGrupo/tags. Na linha da tag aparece o commit `Merge pull request ... from .../release/v0.6.0`. Se aparecer outro commit, o **Target** ficou errado: avisa o grupo antes de continuar.

### Passo 39 — Abre o pull request que leva a release para o develop

A release está no `main`, mas o `develop` ainda não tem os commits dela (a versão nova e o registo de alterações). Este pull request leva-os para lá, para os dois ramos ficarem alinhados.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/compare/develop...main

**b)** Confirma, no topo, que está **base: develop** e **compare: main**, e clica em **Create pull request**.

**c)** No título, cola:

```text
Juntar a release v0.6.0 ao develop
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue da release, que apontaste no início:

```markdown
## O que muda

Traz para o `develop` os commits da release v0.6.0, que já estão no `main`: a versão nova, o registo de alterações e o README.

Closes #N
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 6 — Comentários, notificações e relatórios`

**f)** Clica em **Create pull request**.

### Passo 40 — Avisa Fabio

Diz a Fabio que o pull request que leva a release v0.6.0 para o `develop` está aberto. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 33 a 36.

### Passo 41 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d release/v0.6.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d release/v0.6.0` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

### Passo 42 — Fecha a milestone da fase

Faz este passo depois de Fabio juntar o último pull request. Nessa altura a issue da release já está fechada, e a milestone fica com todas as issues fechadas.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/milestones

**b)** Na linha `Fase 6 — Comentários, notificações e relatórios`, confirma que a barra está a 100% e clica em **Close**.

Se a barra não estiver a 100%, clica no nome da milestone para ver que issues estão abertas. Uma issue fica aberta quando o pull request dela foi junto sem `Closes #número`. Para a fechar à mão, abre a issue, escreve na caixa de comentário `Resolvida pelo pull request #N` (com o número do pull request) e clica em **Close with comment**. Depois volta a este passo.

---

## Outras tarefas desta fase

### Passo 43 — Atualiza a página inicial da wiki

A página inicial passa a indicar a versão 0.6.0, e os perfis e as páginas dizem o que há de novo.

Faz este passo no fim da fase, depois de publicares a release.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 0.6.0` e clica em **Save page**.

**Deves ver** a linha `Versão atual: v0.6.0 (Fase 6 — Comentários, notificações, painel e relatório).`

### Passo 44 — Atualiza a página "Registo das fases" da wiki

A página ganha a secção da Fase 6: quem fez e quem reviu cada unidade, e as decisões tomadas. A secção da Fase 5 ganha o que correu mal.

Faz este passo no fim da fase, depois de a release v0.6.0 estar publicada.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Registo das fases** na lista de páginas, à direita, e depois em **Edit**.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Registar a Fase 6` e clica em **Save page**.

**Deves ver** a secção `Fase 6 — Comentários, notificações, painel e relatório`, com a tabela das cinco unidades.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 6.1 — Comentários dos criativos e respostas

- **`gestor_campanhas/bd.py`** ganha a tabela `comentarios`. Os comentários e as respostas ficam na mesma tabela: uma resposta é um comentário com a coluna `resposta_a` preenchida, com o número do comentário a que responde. A coluna `criativo_id` tem `ON DELETE CASCADE`: quando um criativo é eliminado, os comentários dele vão com ele (sem isto, o SQLite recusava eliminar um criativo com comentários).
- **`gestor_campanhas/modelos.py`** ganha a classe `Comentario`, com o nome e o perfil de quem escreveu, para os mostrar sem outra consulta.
- **`gestor_campanhas/repositorios/comentarios.py`** é novo, com `criar`, `obter_por_id` e `listar_por_criativo`. A consulta junta cada comentário ao seu autor, na tabela `utilizadores`. Não há funções para alterar nem apagar comentários.
- **`gestor_campanhas/servicos/comentarios.py`** é novo e tem as regras. `comentar` usa `criativos.obter_do_cliente`, que já confirmava que o criativo é do cliente, e `responder` usa `obter_do_marketeer` e recusa responder a uma resposta. `conversa` arruma a lista em pares (comentário, respostas), que é a forma como os menus a mostram, e `por_responder` conta, em cada criativo de uma campanha, os comentários sem nenhuma resposta.
- **`gestor_campanhas/cli/criativos.py`**: `mostrar_comentarios` escreve a conversa de um criativo e é usada no "Ver criativo" dos dois perfis. `comentar` (Cliente) e `responder` (Marketeer) são as opções novas, acrescentadas no fim das listas `ACOES_DO_CLIENTE` e `ACOES`, para as opções que já existiam não mudarem de número. `avisar_comentarios_por_responder` escreve a linha por baixo da lista do Marketeer.
- **`gestor_campanhas/dados_demo.py`** ganha `COMENTARIOS` e `criar_comentarios`. Se o criativo `Vídeo da montra` tiver sido eliminado, o comentário não é criado.
- **`tests/test_comentarios.py`** é novo: base de dados, regras, ecrãs e dados de demonstração. Em `tests/test_criativos.py`, os dois testes que confirmam as opções dos menus de criativos ganham as opções novas. `tests/test_bd.py` testa a tabela nova, incluindo o `ON DELETE CASCADE`.
- **`docs/`**: o guia de utilização explica as duas opções novas e os comentários em "Ver criativo", a arquitetura ganha a tabela nova e a secção "Comentários dos criativos", e a referência os dois módulos novos.

### Unidade 6.4 — Relatório das campanhas em CSV

- **`gestor_campanhas/servicos/relatorios.py`** é novo. `linhas` monta as linhas a partir das mesmas funções que mostram as campanhas e a despesa no ecrã (`campanhas.listar_do_cliente`, `criativos.despesas`, `criativos.restante`), por isso o relatório dá sempre os mesmos números que a aplicação. `valor` escreve os euros sem `€` e sem o espaço dos milhares, para o Excel os ler como números. `exportar` grava o ficheiro com o módulo `csv`, separador `;` e codificação `utf-8-sig` (UTF-8 com a marca inicial, sem a qual o Excel troca os acentos).
- **`gestor_campanhas/servicos/ficheiros.py`** ganha `caminho_livre`, tirado de `copiar_para`: escolhe o nome de um ficheiro novo numa pasta, com um número entre parênteses se o nome já existir. Assim, o relatório e os ficheiros descarregados seguem a mesma regra, escrita uma só vez.
- **`gestor_campanhas/cli/comum.py`** ganha `pasta_transferencias`, que estava em `cli/criativos.py`. O menu das campanhas não pode importar o dos criativos, porque o dos criativos já importa o das campanhas, e os dois ficariam a depender um do outro; por isso a função passou para o módulo comum, de que os dois dependem.
- **`gestor_campanhas/cli/criativos.py`** passa a usar `comum.pasta_transferencias`.
- **`gestor_campanhas/cli/campanhas.py`** ganha `exportar_relatorio` e a opção 3 no menu das campanhas do Cliente.
- **`tests/test_relatorios.py`** é novo: os valores, as linhas, o ficheiro gravado, os nomes repetidos e o ecrã. Em `tests/test_criativos.py`, os dois testes da pasta `Downloads` passam a usar `comum`.
- **`docs/`**: o guia de utilização explica o relatório, com um exemplo, a arquitetura ganha a secção "Relatório das campanhas", e a referência o módulo novo.

### Unidade 6.5 — Release v0.6.0

- **`gestor_campanhas/__init__.py`**: `__version__` passa para `"0.6.0"`. O menu inicial, o `pyproject.toml` e a documentação leem a versão daqui.
- **`CHANGELOG.md`** ganha a secção `v0.6.0`, por cima das anteriores. A parte "Alterado" regista o que pode surpreender quem já usava a versão 0.5.0: os números novos das opções dos menus, e o aviso de campanha atribuída, que passa a ser também uma notificação.
- **`README.md`**: os perfis dizem o que cada um ganhou, a tabela de versões ganha uma linha, o exemplo do menu passa a mostrar `v0.6.0`, os dados de demonstração incluem o comentário, e há três secções novas: `Comentários e notificações`, `Painel de marketeers` e `Relatório`.
- **O caminho de uma release** é o mesmo das fases anteriores: o pull request do ramo `release/v0.6.0` para o `main`; a confirmação de que o `main` já tem a versão 0.6.0; a publicação da release, que cria a tag no `main`; o pull request do `main` para o `develop`; e o fecho da milestone.
