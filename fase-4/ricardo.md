# Fase 4 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 4 (Criativos), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 4.1 (de Tomas) | Quando Tomas avisar |
| 8 a 17 | Fazer a unidade 4.2 — Custo, prazo, público-alvo e plataforma | A seguir ao teu passo anterior |
| 18 a 27 | Fazer a unidade 4.5 — Ficheiros dos criativos | Quando Fabio avisar |
| 28 a 34 | Rever e juntar a unidade 4.6 (de Fabio) | Quando Fabio avisar |
| 35 a 42 | Rever a release v0.4.0 e juntá-la ao main | Quando Fabio avisar |
| 43 a 46 | Juntar a release v0.4.0 ao develop | Quando Fabio avisar |
| 47 | Atualiza a página "Arquitetura" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 4.1 — Criar, editar e eliminar criativos

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 4.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Criar, editar e eliminar criativos**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 3 linhas `Closes #` seguida de um número, uma por issue (M06, M07, M08), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Tomas para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/4.1-criar-editar-eliminar-criativo
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/4.1-criar-editar-eliminar-criativo` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/4.1-criar-editar-eliminar-criativo'`.

Agora experimenta:

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

Confirma também:

- Entra como marketeer, escolhe `2` e o número da campanha `Natal 2026`. Escolhe `1` (Criar criativo) e, no nome, carrega só em Enter: aparece `Este campo é obrigatório.` e o nome é pedido outra vez. Escreve `Teste` e carrega em Enter na descrição.
- Escolhe `3` (Eliminar criativo), escreve o número do `Teste` e responde `n`: aparece `Nada foi alterado.` e o criativo continua na tabela. Elimina-o agora a sério (`3`, o número e `s`).
- Escolhe `2` (Editar criativo) e escreve `999`: aparece `Não tem nenhum criativo com o número 999.`
- Sai e entra como `marta@agencia.pt` / `marta12345`. Em "Criativos" aparecem só as campanhas da Marta: não aparecem `Natal 2026` nem `Regresso às aulas`. Escreve `1` (nos dados de demonstração, é a campanha `Natal 2026`, do Miguel): aparece `Não tem nenhuma campanha com o número 1.`

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

**f)** No Trello, move os cards das stories M06, M07 e M08 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/4.1-criar-editar-eliminar-criativo
python ../ctesp-ADC/verificar.py 4.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/4.1-criar-editar-eliminar-criativo` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 4.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 4.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 4.2 — Custo, prazo, público-alvo e plataforma

Cada criativo ganha o custo estimado, o prazo, o público-alvo e a plataforma onde vai ser publicado. O Marketeer passa também a poder ver todos os dados de um criativo, e os dados de demonstração ganham quatro criativos.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Criar, editar e eliminar criativos** (unidade 4.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 4.2

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 4 issues: M09, M10, M11, M12. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue M09** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM09%5D%22

```markdown
- [ ] Ao criar e ao editar um criativo, é pedido o custo estimado em euros (opcional), por exemplo `400` ou `399,90`
- [ ] Um valor inválido mostra a mensagem do erro e nada é guardado
- [ ] Sem custo, o criativo mostra `Por definir`
- [ ] A lista dos criativos mostra o custo de cada um
```

**Issue M10** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM10%5D%22

```markdown
- [ ] Ao criar e ao editar, é pedido o prazo no formato `AAAA-MM-DD` (opcional)
- [ ] O prazo não pode ser depois do fim da campanha
- [ ] Decisão do grupo: há um só prazo, a data de entrega; a publicação fica registada quando o criativo é marcado como publicado (issue M14)
```

**Issue M11** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM11%5D%22

```markdown
- [ ] Ao criar e ao editar, é pedido o público-alvo (opcional), em texto livre: idade, região, interesses
- [ ] A lista mostra o início do público-alvo; "Ver criativo" mostra-o todo
```

**Issue M12** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM12%5D%22

```markdown
- [ ] Ao criar e ao editar, a plataforma é escolhida de uma lista numerada: Facebook, Instagram, Google Ads, LinkedIn, TikTok e YouTube
- [ ] Com Enter, a plataforma fica por escolher; na edição, `-` apaga-a
- [ ] Decisão do grupo: uma plataforma por criativo; o mesmo anúncio em duas plataformas são dois criativos, porque os formatos são diferentes
- [ ] A opção "Ver criativo" mostra todos os dados de um criativo
```

Por fim, no quadro Trello, move os cards das stories M09, M10, M11 e M12 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/4.2-custo-prazo-publico-plataforma
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/4.2-custo-prazo-publico-plataforma` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/4.2-custo-prazo-publico-plataforma'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/4.2-custo-prazo-publico-plataforma' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/4.2-custo-prazo-publico-plataforma
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/4.2-custo-prazo-publico-plataforma
git switch -c feature/4.2-custo-prazo-publico-plataforma
```

  **Deves ver** `Deleted branch feature/4.2-custo-prazo-publico-plataforma (was ...)` e depois `Switched to a new branch 'feature/4.2-custo-prazo-publico-plataforma'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/4.2-custo-prazo-publico-plataforma` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 4.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 4.2. Eles estão na pasta `ctesp-ADC/fase-4/ficheiros/4.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.2 1
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar o custo, o prazo, o público-alvo e a plataforma"
```

**Deves ver** uma linha a terminar em `3 files changed, 104 insertions(+), 8 deletions(-)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.2 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(criativos): validar o custo, o prazo, o público-alvo e a plataforma"
```

**Deves ver** uma linha a terminar em `2 files changed, 178 insertions(+), 8 deletions(-)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.2 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): pedir e mostrar o custo, o prazo, o público-alvo e a plataforma"
```

**Deves ver** uma linha a terminar em `2 files changed, 176 insertions(+), 13 deletions(-)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.2 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): ver os detalhes de um criativo"
```

**Deves ver** uma linha a terminar em `2 files changed, 61 insertions(+), 3 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.2 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/dados_demo.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(demo): acrescentar criativos de demonstração"
```

**Deves ver** uma linha a terminar em `2 files changed, 115 insertions(+), 6 deletions(-)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.2 6
```

**Deves ver** `Copiados 1 ficheiro`: `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar o custo, o prazo, o público-alvo e a plataforma dos criativos"
```

**Deves ver** uma linha a terminar em `1 file changed, 48 insertions(+), 10 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 4.2
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 4.2` | `Tudo certo: o ramo 'feature/4.2-custo-prazo-publico-plataforma' está igual ao original no fim da unidade 4.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar o custo, o prazo, o público-alvo e a plataforma dos criativos
xxxxxxx feat(demo): acrescentar criativos de demonstração
xxxxxxx feat(cli): ver os detalhes de um criativo
xxxxxxx feat(cli): pedir e mostrar o custo, o prazo, o público-alvo e a plataforma
xxxxxxx feat(criativos): validar o custo, o prazo, o público-alvo e a plataforma
xxxxxxx feat(repositorios): guardar o custo, o prazo, o público-alvo e a plataforma
```

### Passo 13 — Experimenta o que gravaste

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

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/4.2-custo-prazo-publico-plataforma
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/4.2-custo-prazo-publico-plataforma -> feature/4.2-custo-prazo-publico-plataforma`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/4.2-custo-prazo-publico-plataforma?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/4.2-custo-prazo-publico-plataforma**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Custo, prazo, público-alvo e plataforma
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

Os criativos ganham o custo estimado, o prazo, o público-alvo e a plataforma.

- Validação do custo (em cêntimos, como o budget), do prazo (até ao fim da campanha) e da plataforma (uma da lista)
- Perguntas novas ao criar e ao editar; na edição, `-` apaga um valor
- Lista dos criativos com as colunas novas e opção "Ver criativo"
- Quatro criativos de demonstração

Closes #(número da issue M09)
Closes #(número da issue M10)
Closes #(número da issue M11)
Closes #(número da issue M12)

## Como testar

1. `python -m pytest` (442 testes)
2. `python -m gestor_campanhas.dados_demo` e `python -m gestor_campanhas`, entrar como marketeer e escolher "Criativos"
3. Criar um criativo com todos os dados, vê-lo, editá-lo e eliminá-lo
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories M09, M10, M11 e M12 para **Ready to Verify**.

### Passo 16 — Avisa Fabio

Diz a Fabio que o pull request da unidade 4.2 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 1 a 7.

### Passo 17 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/4.2-custo-prazo-publico-plataforma
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/4.2-custo-prazo-publico-plataforma` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Fazer a unidade 4.5 — Ficheiros dos criativos

Cada criativo pode ter um ficheiro: uma imagem, um vídeo ou um documento. O Marketeer anexa-o e o Cliente descarrega uma cópia. Os dois podem pré-visualizar o ficheiro, que mostra o nome, o tipo e o tamanho e o abre no programa predefinido do computador.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Estados do criativo e aprovação pelo cliente** (unidade 4.4) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 4.5

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: M13, C12. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue M13** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM13%5D%22

```markdown
- [ ] O menu de criativos do Marketeer tem as opções "Anexar ficheiro" e "Pré-visualizar ficheiro"
- [ ] Ao anexar, é pedido o caminho de um ficheiro do computador; o ficheiro é copiado para a pasta `dados/ficheiros` da aplicação
- [ ] O caminho pode vir com aspas, como o que o Windows copia com "Copiar como caminho"
- [ ] Se o criativo já tiver ficheiro, é avisado de que vai ser substituído
- [ ] Só se muda o ficheiro de um criativo em preparação ou rejeitado
- [ ] Com um caminho que não existe aparece a mensagem do erro e nada é alterado
- [ ] A pré-visualização mostra o nome, o tipo e o tamanho do ficheiro e pergunta se o deve abrir no programa predefinido
- [ ] Ao eliminar um criativo, o ficheiro dele também é apagado
```

**Issue C12** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC12%5D%22

```markdown
- [ ] O menu de criativos do Cliente tem as opções "Pré-visualizar ficheiro" e "Descarregar ficheiro"
- [ ] "Ver criativo" mostra o nome do ficheiro, se houver
- [ ] Ao descarregar, é pedida a pasta de destino; com Enter, é a pasta Transferências (`Downloads`) do utilizador
- [ ] Se já houver um ficheiro com o mesmo nome na pasta, a cópia fica com ` (1)` no nome, e o que lá estava não é apagado
- [ ] Com um criativo sem ficheiro aparece "O criativo ... ainda não tem ficheiro."
```

Por fim, no quadro Trello, move os cards das stories M13 e C12 de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/4.5-ficheiros-dos-criativos
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/4.5-ficheiros-dos-criativos` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/4.5-ficheiros-dos-criativos'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/4.5-ficheiros-dos-criativos' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/4.5-ficheiros-dos-criativos
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/4.5-ficheiros-dos-criativos
git switch -c feature/4.5-ficheiros-dos-criativos
```

  **Deves ver** `Deleted branch feature/4.5-ficheiros-dos-criativos (was ...)` e depois `Switched to a new branch 'feature/4.5-ficheiros-dos-criativos'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/4.5-ficheiros-dos-criativos` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 21 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 4.5 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 4.5. Eles estão na pasta `ctesp-ADC/fase-4/ficheiros/4.5/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.5 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/config.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(config): pasta dos ficheiros dos criativos"
```

**Deves ver** uma linha a terminar em `2 files changed, 16 insertions(+)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.5 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/ficheiros.py`, `tests/test_ficheiros.py`.

```bash
git add -A
git commit -m "feat(ficheiros): copiar, descrever e abrir ficheiros"
```

**Deves ver** uma linha a terminar em `2 files changed, 301 insertions(+)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.5 3
```

**Deves ver** `Copiados 5 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/criativos.py`, `gestor_campanhas/servicos/criativos.py`, `tests/conftest.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(criativos): anexar um ficheiro a um criativo"
```

**Deves ver** uma linha a terminar em `5 files changed, 165 insertions(+), 3 deletions(-)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.5 4
```

**Deves ver** `Copiados 3 ficheiros`: `exemplos/banner-natal.svg`, `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): anexar e pré-visualizar ficheiros no menu do marketeer"
```

**Deves ver** uma linha a terminar em `3 files changed, 201 insertions(+), 3 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.5 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/criativos.py`, `tests/test_criativos.py`.

```bash
git add -A
git commit -m "feat(cli): pré-visualizar e descarregar ficheiros no menu do cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 134 insertions(+), 2 deletions(-)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 4.5 6
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os ficheiros dos criativos"
```

**Deves ver** uma linha a terminar em `3 files changed, 70 insertions(+)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 4.5
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 4.5` | `Tudo certo: o ramo 'feature/4.5-ficheiros-dos-criativos' está igual ao original no fim da unidade 4.5.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os ficheiros dos criativos
xxxxxxx feat(cli): pré-visualizar e descarregar ficheiros no menu do cliente
xxxxxxx feat(cli): anexar e pré-visualizar ficheiros no menu do marketeer
xxxxxxx feat(criativos): anexar um ficheiro a um criativo
xxxxxxx feat(ficheiros): copiar, descrever e abrir ficheiros
xxxxxxx feat(config): pasta dos ficheiros dos criativos
```

### Passo 23 — Experimenta o que gravaste

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

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/4.5-ficheiros-dos-criativos
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/4.5-ficheiros-dos-criativos -> feature/4.5-ficheiros-dos-criativos`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/4.5-ficheiros-dos-criativos?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/4.5-ficheiros-dos-criativos**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Ficheiros dos criativos
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

Os criativos passam a ter um ficheiro anexado.

- Pasta `dados/ficheiros`, com uma pasta por criativo
- Módulo novo `servicos/ficheiros.py`: copiar, descrever (tipo e tamanho), abrir e descarregar ficheiros
- Opções "Anexar ficheiro" e "Pré-visualizar ficheiro" no menu do Marketeer
- Opções "Pré-visualizar ficheiro" e "Descarregar ficheiro" no menu do Cliente
- Ficheiro de exemplo `exemplos/banner-natal.svg`
- Os testes passam a usar sempre uma pasta de dados temporária

Closes #(número da issue M13)
Closes #(número da issue C12)

## Como testar

1. `python -m pytest` (546 testes)
2. `python -m gestor_campanhas`: como marketeer, anexar `exemplos/banner-natal.svg` ao Banner de Natal e pré-visualizá-lo
3. Como `cliente@empresa.pt`, pré-visualizar e descarregar o ficheiro
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 4 — Criativos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories M13 e C12 para **Ready to Verify**.

### Passo 26 — Avisa Tomas

Diz a Tomas que o pull request da unidade 4.5 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 28 a 34.

### Passo 27 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/4.5-ficheiros-dos-criativos
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/4.5-ficheiros-dos-criativos` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 4.6 — Despesa face ao budget e aviso de budget ultrapassado

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 28 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 4.6 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Despesa face ao budget e aviso de budget ultrapassado**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (C14, M15), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Fabio para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 29 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 30 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/4.6-despesa-e-budget
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/4.6-despesa-e-budget` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/4.6-despesa-e-budget'`.

Agora experimenta:

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

Confirma também:

- Entra como marketeer e, em `1` (Campanhas), confirma que a linha de `Regresso às aulas` tem `300,00 €` na despesa e `500,00 €` no restante.
- Ainda em "Campanhas", cria uma campanha nova sem budget: `1`, o número da `Carla Cliente`, o nome `Teste sem budget` e Enter nas outras perguntas. Na tabela, a linha nova tem `0,00 €` na despesa e `Por definir` no budget e no restante.
- Escolhe `0`, `2` e a campanha `Teste sem budget`. Cria um criativo `Teste` com o custo `9999` (Enter nas outras perguntas): aparece `Criativo criado com o número ...` e nenhum aviso, porque a campanha não tem budget. Por baixo da tabela aparece `Custo dos criativos: 9 999,00 €. Budget da campanha: Por definir.`
- Elimina o criativo `Teste` (`4`, o número e `s`). Volta a "Campanhas" e elimina a campanha `Teste sem budget` (`4`, o número e `s`): como já não tem criativos, aparece `A campanha Teste sem budget foi eliminada.`
- Entra como `jose@padaria.pt` / `jose12345`, escolhe `2`, depois `1` e a campanha `Regresso às aulas`: aparece `Gasto:     37% do budget`.

### Passo 31 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

### Passo 32 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move os cards das stories C14 e M15 para **Ready**.

### Passo 33 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/4.6-despesa-e-budget
python ../ctesp-ADC/verificar.py 4.6
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/4.6-despesa-e-budget` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 4.6` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 4.6 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.6.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 34 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 34 da [página de Fabio](fabio.md)).

Diz também a Fabio que já pode avançar ([página de Fabio](fabio.md), passos 35 a 43).

---

## Rever a release v0.4.0 e juntá-la ao main

Quem fez: Fabio. Tu confirmas que a versão está pronta e juntas o ramo da release ao `main`.

### Passo 35 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 4.7 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Release v0.4.0**.

### Passo 36 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 37 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch release/v0.4.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch release/v0.4.0` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'release/v0.4.0'`.

Agora experimenta:

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

Confirma também:

- No separador **Files changed** do pull request aparecem só três ficheiros: `gestor_campanhas/__init__.py`, `CHANGELOG.md` e `README.md`.
- O `CHANGELOG.md` tem a secção `v0.4.0` por cima da `v0.3.0`.
- O README tem a secção nova `Criativos`, com o desenho dos estados.

### Passo 38 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Fabio. Não avances para o passo seguinte.

### Passo 39 — Confirma que o pull request vai para o main

Este é o único pull request da fase que não vai para o `develop`. Se for junto ao ramo errado, o `main` fica sem a versão e a tag fica no sítio errado.

Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.4.0`.

Se disser `into develop`, **não juntes**. Avisa Fabio, que corrige o destino no botão **Edit**, à direita do título. Depois de corrigido, atualiza a página e confirma outra vez.

### Passo 40 — Junta o pull request ao main (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `main`.

**Deves ver** o símbolo roxo **Merged** no topo da página.

### Passo 41 — Arruma o teu computador

```bash
git switch develop
git branch -D release/v0.4.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git branch -D release/v0.4.0` | Apaga a cópia do ramo que criaste para experimentar. O `-D` maiúsculo é preciso porque o `develop` ainda não tem estes commits: chegam lá no pull request seguinte |

### Passo 42 — Avisa Fabio

Diz a Fabio que a release v0.4.0 já está no `main`. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 44 a 49.

---

## Juntar a release v0.4.0 ao develop

É o último pull request da fase.

### Passo 43 — Aprova o pull request que leva a release para o develop

Faz este passo quando Fabio te avisar.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Juntar a release v0.4.0 ao develop**.

**b)** Confirma que na descrição está `Closes #` seguido do número da issue da release, e não `#N`. Se estiver `#N`, pede a Fabio para editar a descrição antes de juntares.

**c)** No separador **Files changed**, confirma que as alterações são as da release: o número da versão, o `CHANGELOG.md` e o `README.md`.

**d)** Clica em **Review changes**, escolhe **Approve** e clica em **Submit review**.

### Passo 44 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** **Não cliques em Delete branch.** O ramo deste pull request é o `main`, que tem de continuar a existir.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da release fica fechada sozinha.

### Passo 45 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 4.7
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `python ../ctesp-ADC/verificar.py 4.7` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 4.7 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.7.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 46 — Avisa o grupo

Diz a Fabio que a release está no `develop` e que já pode arrumar o computador (passo 49 da [página de Fabio](fabio.md)).

Esta era a última vez da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 47 — Atualiza a página "Arquitetura" da wiki

A página ganha duas secções, sobre os criativos e sobre os ficheiros. A tabela das tabelas ganha a linha `criativos`.

Faz este passo depois de a unidade 4.6 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Arquitetura.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki/Arquitetura e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a Arquitetura para a versão 0.4.0` e clica em **Save page**.

**Deves ver** a página com as secções novas `Criativos` e `Ficheiros`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 4.2 — Custo, prazo, público-alvo e plataforma

- **`gestor_campanhas/modelos.py`**: a classe `Criativo` ganha `custo_centimos`, `prazo`, `publico_alvo` e `plataforma`. As colunas já existiam na tabela desde a unidade 4.1.
- **`gestor_campanhas/repositorios/criativos.py`**: `criar` e `atualizar` passam a guardar os quatro dados novos. O prazo é guardado como texto `AAAA-MM-DD`, como as datas das campanhas, e convertido para `date` ao ler.
- **`gestor_campanhas/servicos/criativos.py`** ganha três validações:
  - `custo_validado` usa o `dinheiro.para_centimos` das campanhas: `150,50` passa a `15050`. Um texto vazio dá `None`, que quer dizer "por definir".
  - `prazo_validado` usa o `validacao.data` das campanhas e recusa uma data depois do fim da campanha, porque um criativo que fica pronto depois de a campanha acabar já não serve.
  - `plataforma_validada` só aceita um dos nomes da lista `modelos.PLATAFORMAS`, que já existia desde os pedidos de campanha.
  - `_dados_validados` junta as validações, para `criar` e `editar` usarem exatamente as mesmas regras. Se um valor estiver errado, o erro é lançado antes de se gravar alguma coisa.
- **`gestor_campanhas/cli/criativos.py`**:
  - `ler_plataforma` mostra a lista numerada e devolve o nome escolhido (ou vazio, com Enter).
  - Na edição, `_ler_com_valor` trata o `-` como "apagar o valor", como já acontecia com as datas das campanhas.
  - A tabela ganha as colunas novas. O público-alvo é cortado a `LARGURA_PUBLICO` (25) caracteres, com `...` no fim, para a tabela caber no ecrã; "Ver criativo" mostra-o inteiro.
- **`gestor_campanhas/dados_demo.py`** ganha a lista `CRIATIVOS` e a função `criar_criativos`. Como nas campanhas, cada criativo só é criado se ainda não existir um com o mesmo nome na mesma campanha.
- **`tests/test_criativos.py`** ganha os testes das validações (custos, prazos e plataformas certos e errados), das perguntas novas e de "Ver criativo".
- **`docs/utilizacao.rst`** explica os dados novos e a forma de apagar um valor na edição.

### Unidade 4.5 — Ficheiros dos criativos

- **`gestor_campanhas/config.py`** ganha `pasta_ficheiros`, que é a pasta `ficheiros` dentro da pasta de dados. Muda com a variável `GESTOR_CAMPANHAS_DADOS`, como a base de dados e a caixa de saída dos emails.
- **`gestor_campanhas/servicos/ficheiros.py`** é novo e trata de tudo o que mexe em ficheiros, sem saber nada de criativos nem de menus:
  - `limpar_caminho` tira os espaços e as aspas do caminho escrito. O Windows põe aspas quando se usa "Copiar como caminho".
  - `guardar` copia o ficheiro para `dados/ficheiros/<número do criativo>/`. Antes de copiar, apaga o que lá estiver, por isso um ficheiro novo substitui o antigo. Usa `shutil.copy2`, que mantém a data do ficheiro.
  - `tipo` usa o módulo `mimetypes` da biblioteca padrão, que adivinha o tipo pela extensão (`.svg` dá `image/svg+xml`), e acrescenta um nome em português: "Imagem", "Vídeo", "Áudio", "Texto" ou "PDF".
  - `tamanho` escreve o tamanho em bytes, KB ou MB, com vírgula decimal.
  - `abrir` abre o ficheiro no programa predefinido: `os.startfile` no Windows, `open` no macOS e `xdg-open` no Linux.
  - `copiar_para` copia para a pasta escolhida pelo cliente e nunca escreve por cima de um ficheiro que já lá esteja: procura o primeiro nome livre, com ` (1)`, ` (2)`, etc.
- **`gestor_campanhas/servicos/criativos.py`**: `anexar` confirma que o criativo é do marketeer e está em `EDITAVEIS`, guarda o ficheiro e grava o nome dele na base de dados. `ficheiro_de` devolve o caminho do ficheiro de um criativo, ou lança um erro se não houver. `eliminar` passa a apagar também a pasta do ficheiro.
- **`gestor_campanhas/repositorios/criativos.py`** ganha `definir_ficheiro`. Na base de dados guarda-se só o nome do ficheiro; o ficheiro fica no disco.
- **`gestor_campanhas/cli/criativos.py`**: `anexar`, `pre_visualizar` e `descarregar`. `pre_visualizar_ficheiro` é usado pelos dois menus, do marketeer e do cliente. `pasta_transferencias` devolve a pasta `Downloads` do utilizador, que é a pasta proposta para descarregar.
- **`exemplos/banner-natal.svg`** é um desenho simples, em texto, para experimentar sem ter de procurar uma imagem.
- **`tests/conftest.py`** ganha a fixture `dados_temporarios`, com `autouse=True`: corre sozinha em todos os testes e põe a pasta de dados numa pasta temporária. Sem ela, um teste que eliminasse um criativo podia apagar uma pasta da pasta `dados` verdadeira.
- **`tests/test_ficheiros.py`** é novo e testa o módulo dos ficheiros com ficheiros temporários. Em `tests/test_criativos.py`, os testes da pré-visualização não abrem janelas: a fixture `aberturas` troca `ficheiros.abrir` por uma função que só regista o ficheiro que lhe pediram para abrir.
- **`docs/`**: o guia de utilização explica as quatro opções, a arquitetura ganha a secção "Ficheiros dos criativos", e a referência o módulo novo.
