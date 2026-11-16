# Fase 3 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 3 (Campanhas e pedidos), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 10 | Fazer a unidade 3.1 — Criar e editar campanhas | No início da fase |
| 11 a 17 | Rever e juntar a unidade 3.3 (de Tomas) | Quando Tomas avisar |
| 18 a 27 | Fazer a unidade 3.4 — Decidir pedidos, budget e marketeer responsável | A seguir ao teu passo anterior |
| 28 a 34 | Rever e juntar a unidade 3.5 (de Fabio) | Quando Fabio avisar |
| 35 a 43 | Preparar a release v0.3.0 | A seguir ao teu passo anterior |
| 44 a 49 | Publicar a release v0.3.0 e pedir o regresso ao develop | Quando Fabio avisar |
| 50 a 51 | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | Em qualquer altura durante a fase |

---

## Fazer a unidade 3.1 — Criar e editar campanhas

Aparecem as campanhas. O Marketeer ganha a opção "Campanhas", onde cria campanhas para um cliente e edita o nome, o objetivo e as datas das suas campanhas.

### Passo 1 — Confirma que podes começar

A fase anterior tem de estar fechada: todos os pull requests juntos e o `develop` do teu computador atualizado. Se for a primeira fase, tens de ter feito a [Preparação](../preparacao.md).

### Passo 2 — Fica com as issues da unidade 3.1

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 2 issues: M02, M03. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue M02** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM02%5D%22

```markdown
- [ ] O menu do Marketeer tem a opção "Campanhas", que mostra as campanhas dele e as opções "Criar campanha" e "Editar campanha"
- [ ] Ao criar, é mostrada a lista dos clientes com a conta ativa, e o cliente é escolhido pelo número
- [ ] São pedidos o nome (obrigatório), o objetivo e as datas de início e de fim (opcionais), no formato `AAAA-MM-DD`
- [ ] A data de fim não pode ser anterior à data de início
- [ ] Quem cria a campanha fica responsável por ela
- [ ] A campanha começa sem budget, porque o budget é definido pelo Administrador (issue A12)
- [ ] Com dados inválidos, ou com um número que não é de um cliente ativo, aparece a mensagem do erro e nada é criado
```

**Issue M03** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM03%5D%22

```markdown
- [ ] A opção "Editar campanha" pede o número da campanha
- [ ] Cada dado é mostrado com o valor atual; com Enter, o valor mantém-se
- [ ] É possível alterar o nome, o objetivo e as datas; para apagar uma data escreve-se `-`
- [ ] O cliente e o budget não são alterados
- [ ] Um marketeer só edita as suas campanhas: com o número de uma campanha de outro aparece "Não tem nenhuma campanha com o número ..."
- [ ] Com dados inválidos aparece a mensagem do erro e nenhum dado é alterado
```

Por fim, no quadro Trello, move os cards das stories M02 e M03 de **Sprint Backlog** para **Work In Progress**.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/3.1-criar-editar-campanha
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/3.1-criar-editar-campanha` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/3.1-criar-editar-campanha'`.

### Passo 4 — Copia e grava os 8 commits

São 8 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 3.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 3.1. Eles estão na pasta `ctesp-ADC/fase-3/ficheiros/3.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela das campanhas"
```

**Deves ver** uma linha a terminar em `2 files changed, 20 insertions(+)`.

**Commit 2 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/modelos.py`.

```bash
git add -A
git commit -m "feat(modelos): acrescentar a classe Campanha"
```

**Deves ver** uma linha a terminar em `1 file changed, 33 insertions(+), 1 deletion(-)`.

**Commit 3 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/repositorios/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar e ler campanhas"
```

**Deves ver** uma linha a terminar em `2 files changed, 232 insertions(+)`.

**Commit 4 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 4
```

**Deves ver** `Copiados 3 ficheiros`: `docs/referencia.rst`, `gestor_campanhas/servicos/validacao.py`, `tests/test_validacao.py`.

```bash
git add -A
git commit -m "feat(validacao): validar datas e períodos"
```

**Deves ver** uma linha a terminar em `3 files changed, 62 insertions(+), 5 deletions(-)`.

**Commit 5 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 5
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(campanhas): criar campanhas para um cliente"
```

**Deves ver** uma linha a terminar em `2 files changed, 147 insertions(+)`.

**Commit 6 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 6
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/campanhas.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(campanhas): editar o nome, o objetivo e as datas"
```

**Deves ver** uma linha a terminar em `2 files changed, 93 insertions(+)`.

**Commit 7 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 7
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_campanhas.py`.

```bash
git add -A
git commit -m "feat(cli): menu de campanhas do marketeer"
```

**Deves ver** uma linha a terminar em `3 files changed, 286 insertions(+), 2 deletions(-)`.

**Commit 8 de 8**

```bash
python ../ctesp-ADC/copiar.py 3.1 8
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar a criação e a edição de campanhas"
```

**Deves ver** uma linha a terminar em `3 files changed, 79 insertions(+), 1 deletion(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 3.1
git log --oneline -8
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 3.1` | `Tudo certo: o ramo 'feature/3.1-criar-editar-campanha' está igual ao original no fim da unidade 3.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -8` | Os teus 8 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar a criação e a edição de campanhas
xxxxxxx feat(cli): menu de campanhas do marketeer
xxxxxxx feat(campanhas): editar o nome, o objetivo e as datas
xxxxxxx feat(campanhas): criar campanhas para um cliente
xxxxxxx feat(validacao): validar datas e períodos
xxxxxxx feat(repositorios): guardar e ler campanhas
xxxxxxx feat(modelos): acrescentar a classe Campanha
xxxxxxx feat(bd): criar a tabela das campanhas
```

### Passo 6 — Experimenta o que gravaste

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

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/3.1-criar-editar-campanha
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/3.1-criar-editar-campanha -> feature/3.1-criar-editar-campanha`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/3.1-criar-editar-campanha?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/3.1-criar-editar-campanha**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Criar e editar campanhas
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Marketeer passa a poder criar campanhas para os clientes e editar as suas campanhas.

- Tabela `campanhas` na base de dados e classe `Campanha`
- Repositório das campanhas, que lê cada campanha já com o nome do cliente e do marketeer
- Validação de datas e de períodos
- Regras para criar e editar: cliente ativo, nome obrigatório, datas coerentes, só as campanhas do próprio
- Opção "Campanhas" no menu do Marketeer

Closes #(número da issue M02)
Closes #(número da issue M03)

## Como testar

1. `python -m pytest` (234 testes)
2. `python -m gestor_campanhas`, entrar como marketeer e escolher "Campanhas"
3. Criar uma campanha e editá-la
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories M02 e M03 para **Ready to Verify**.

### Passo 9 — Avisa Fabio

Diz a Fabio que o pull request da unidade 3.1 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 1 a 7.

### Passo 10 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/3.1-criar-editar-campanha
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/3.1-criar-editar-campanha` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 3.3 — Pedidos de nova campanha

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 11 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 3.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Pedidos de nova campanha**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 3 linhas `Closes #` seguida de um número, uma por issue (C05, C06, C07), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Tomas para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/3.3-pedidos-de-campanha
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/3.3-pedidos-de-campanha` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/3.3-pedidos-de-campanha'`.

Agora experimenta:

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

Confirma também:

- Entra como `cliente@empresa.pt` / `cliente12345`, escolhe `1` e depois `1` (Novo pedido). Escreve um objetivo, o orçamento `0`, um prazo e uma plataforma: aparece `O orçamento tem de ser maior do que zero. O pedido não foi registado.`
- Faz um pedido com o prazo `2026-01-01`: aparece `O prazo não pode ser um dia que já passou. O pedido não foi registado.`
- Na pergunta das plataformas, escreve `9`: aparece `Escreva números entre 1 e 6, separados por vírgulas.` e a pergunta repete-se.
- Na opção `3`, escreve o número do pedido que já está cancelado: aparece `Só é possível cancelar um pedido pendente. Este pedido está no estado Cancelado.`
- Sai e entra como `jose@padaria.pt` / `jose12345`. Em "Pedidos de campanha" aparece só o pedido `Divulgar o bolo-rei no Natal`, e não os pedidos do outro cliente.

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

**f)** No Trello, move os cards das stories C05, C06 e C07 para **Ready**.

### Passo 16 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/3.3-pedidos-de-campanha
python ../ctesp-ADC/verificar.py 3.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/3.3-pedidos-de-campanha` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 3.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 3.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 3.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 17 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 18.

---

## Fazer a unidade 3.4 — Decidir pedidos, budget e marketeer responsável

O Administrador ganha duas opções. Em "Pedidos de campanha" analisa os pedidos dos clientes e aprova-os ou rejeita-os. Em "Campanhas" vê todas as campanhas, define o budget e escolhe o marketeer responsável. Fecham-se também as duas partes que tinham ficado da Fase 2.

### Passo 18 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Pedidos de nova campanha** (unidade 3.3) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 19 — Fica com as issues da unidade 3.4

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 3 issues: A11, A12, A13. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A11** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA11%5D%22

```markdown
- [ ] O menu do Administrador tem a opção "Pedidos de campanha", com os pedidos de todos os clientes; os que estão por decidir aparecem primeiro
- [ ] A opção "Analisar pedido" mostra todos os dados do pedido; um pedido pendente passa a "Em análise"
- [ ] Ao aprovar, é criada uma campanha para o cliente, com o objetivo do pedido e o prazo do pedido como data de fim
- [ ] Ao rejeitar, é obrigatório indicar o motivo, e é pedida uma confirmação
- [ ] O cliente é avisado por email da decisão; na rejeição, o email tem o motivo
- [ ] Um pedido já aprovado, rejeitado ou cancelado não pode ser decidido outra vez
- [ ] É possível deixar a decisão para mais tarde; o pedido fica "Em análise"
```

**Issue A12** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA12%5D%22

```markdown
- [ ] Ao aprovar um pedido, é pedido o budget inicial da campanha; o valor proposto é o orçamento do pedido
- [ ] O menu do Administrador tem a opção "Campanhas", com as campanhas de todos os marketeers
- [ ] A opção "Definir budget" atribui ou corrige o budget de uma campanha
- [ ] O budget é um valor em euros maior do que zero
- [ ] As alterações de budget pedidas pelo cliente entram na Fase 5
```

**Issue A13** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA13%5D%22

```markdown
- [ ] Ao aprovar um pedido, é escolhido o marketeer responsável, na lista dos marketeers com a conta ativa
- [ ] A opção "Atribuir marketeer" muda o responsável de uma campanha
- [ ] Só pode ser escolhido um marketeer com a conta ativa
- [ ] O marketeer que passa a ser responsável é avisado por email
- [ ] O marketeer anterior deixa de ver a campanha
```

Por fim, no quadro Trello, move os cards das stories A11, A12 e A13 de **Sprint Backlog** para **Work In Progress**.

### Passo 20 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/3.4-decisao-budget-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/3.4-decisao-budget-marketeer` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/3.4-decisao-budget-marketeer'`.

### Passo 21 — Copia e grava os 9 commits

São 9 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 3.4 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 3.4. Eles estão na pasta `ctesp-ADC/fase-3/ficheiros/3.4/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 1
```

**Deves ver** `Copiados 4 ficheiros`: `gestor_campanhas/repositorios/campanhas.py`, `gestor_campanhas/repositorios/pedidos.py`, `tests/conftest.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(repositorios): ler todos os pedidos e alterar o budget e o marketeer"
```

**Deves ver** uma linha a terminar em `4 files changed, 145 insertions(+), 1 deletion(-)`.

**Commit 2 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 2
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/campanhas.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(campanhas): definir o budget de uma campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 87 insertions(+), 1 deletion(-)`.

**Commit 3 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/campanhas.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(campanhas): atribuir um marketeer a uma campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 111 insertions(+), 1 deletion(-)`.

**Commit 4 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 4
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/pedidos.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(pedidos): analisar, aprovar e rejeitar pedidos de campanha"
```

**Deves ver** uma linha a terminar em `2 files changed, 243 insertions(+), 3 deletions(-)`.

**Commit 5 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 5
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/pedidos.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(cli): pedidos de campanha no menu do administrador"
```

**Deves ver** uma linha a terminar em `3 files changed, 275 insertions(+), 3 deletions(-)`.

**Commit 6 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 6
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(cli): campanhas no menu do administrador"
```

**Deves ver** uma linha a terminar em `3 files changed, 217 insertions(+), 1 deletion(-)`.

**Commit 7 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 7
```

**Deves ver** `Copiados 4 ficheiros`: `gestor_campanhas/cli/gestao.py`, `gestor_campanhas/modelos.py`, `gestor_campanhas/servicos/campanhas.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(gestao): mostrar as campanhas ativas de cada cliente e marketeer"
```

**Deves ver** uma linha a terminar em `4 files changed, 98 insertions(+), 6 deletions(-)`.

**Commit 8 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 8
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/gestao.py`, `gestor_campanhas/servicos/gestao.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "feat(gestao): impedir desativar um marketeer com campanhas por terminar"
```

**Deves ver** uma linha a terminar em `3 files changed, 83 insertions(+), 9 deletions(-)`.

**Commit 9 de 9**

```bash
python ../ctesp-ADC/copiar.py 3.4 9
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar as decisões do administrador sobre pedidos e campanhas"
```

**Deves ver** uma linha a terminar em `3 files changed, 118 insertions(+), 18 deletions(-)`.


### Passo 22 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 3.4
git log --oneline -9
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 3.4` | `Tudo certo: o ramo 'feature/3.4-decisao-budget-marketeer' está igual ao original no fim da unidade 3.4.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -9` | Os teus 9 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar as decisões do administrador sobre pedidos e campanhas
xxxxxxx feat(gestao): impedir desativar um marketeer com campanhas por terminar
xxxxxxx feat(gestao): mostrar as campanhas ativas de cada cliente e marketeer
xxxxxxx feat(cli): campanhas no menu do administrador
xxxxxxx feat(cli): pedidos de campanha no menu do administrador
xxxxxxx feat(pedidos): analisar, aprovar e rejeitar pedidos de campanha
xxxxxxx feat(campanhas): atribuir um marketeer a uma campanha
xxxxxxx feat(campanhas): definir o budget de uma campanha
xxxxxxx feat(repositorios): ler todos os pedidos e alterar o budget e o marketeer
```

### Passo 23 — Experimenta o que gravaste

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

### Passo 24 — Envia o ramo para o GitHub

```bash
git push -u origin feature/3.4-decisao-budget-marketeer
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/3.4-decisao-budget-marketeer -> feature/3.4-decisao-budget-marketeer`.

### Passo 25 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/3.4-decisao-budget-marketeer?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/3.4-decisao-budget-marketeer**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Decidir pedidos, budget e marketeer responsável
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a decidir os pedidos de campanha, a definir o budget das campanhas e a escolher o marketeer responsável.

- Aprovar um pedido cria a campanha, com o budget inicial e o marketeer escolhido; rejeitar exige um motivo
- Emails ao cliente (decisão do pedido) e ao marketeer (campanha atribuída)
- Opções "Pedidos de campanha" e "Campanhas" no menu do Administrador
- Coluna "Campanhas ativas" nas listas de clientes e de marketeers (fecha a parte da A04 adiada na Fase 2)
- Um marketeer com campanhas por terminar não pode ser desativado (fecha a parte da A10 adiada na Fase 2)

Closes #(número da issue A11)
Closes #(número da issue A12)
Closes #(número da issue A13)

## Como testar

1. `python -m pytest` (370 testes)
2. `python -m gestor_campanhas.dados_demo`
3. `python -m gestor_campanhas`, entrar como administrador
4. Em "Pedidos de campanha", aprovar um pedido e rejeitar outro
5. Em "Campanhas", definir um budget e mudar um marketeer
6. Em "Marketeers", tentar desativar um marketeer com campanhas
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories A11, A12 e A13 para **Ready to Verify**.

### Passo 26 — Avisa Tomas

Diz a Tomas que o pull request da unidade 3.4 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 18 a 24.

### Passo 27 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/3.4-decisao-budget-marketeer
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/3.4-decisao-budget-marketeer` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 3.5 — Campanhas do cliente e marketeer responsável

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 28 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 3.5 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Campanhas do cliente e marketeer responsável**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (C08, C09), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Fabio para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 29 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 30 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/3.5-campanhas-do-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/3.5-campanhas-do-cliente` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/3.5-campanhas-do-cliente'`.

Agora experimenta:

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

Confirma também:

- Entra como `jose@padaria.pt` / `jose12345`, escolhe `2` e depois `1`. Escreve o número de uma campanha que não está na tabela (por exemplo o da campanha `Natal 2026`, que é de outro cliente): aparece `Não tem nenhuma campanha com o número ...`
- Sai e entra como `beatriz@bicicletas.pt` / `beatriz12345`. Em "Campanhas" aparece `Bicicletas de primavera`. Se o budget ainda não foi definido nesse computador, a coluna do budget diz `Por definir`.
- Entra como marketeer (`marketeer@agencia.pt` / `marketeer12345`): a opção "Campanhas" continua a mostrar o menu do marketeer, com as opções de criar, editar, ver e eliminar.

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

**f)** No Trello, move os cards das stories C08 e C09 para **Ready**.

### Passo 33 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/3.5-campanhas-do-cliente
python ../ctesp-ADC/verificar.py 3.5
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/3.5-campanhas-do-cliente` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 3.5` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 3.5 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 3.5.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 34 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 35.

---

## Preparar a release v0.3.0

Fecha a fase com a versão 0.3.0: corrige uma mensagem, sobe o número da versão, acrescenta a secção desta versão ao registo de alterações e atualiza o README. Esta unidade vai para o `main`, e não para o `develop`.

### Passo 35 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Campanhas do cliente e marketeer responsável** (unidade 3.5) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 36 — Cria a issue da unidade 3.6

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[3.6] Release v0.3.0
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Publicar a versão 0.3.0, com as user stories da Fase 3 (campanhas e pedidos de campanha).

## O que inclui

- [ ] Correção da mensagem de atribuição de marketeer
- [ ] Versão 0.3.0 em `gestor_campanhas/__init__.py`
- [ ] Registo de alterações (`CHANGELOG.md`)
- [ ] README atualizado
- [ ] Pull request para `main`
- [ ] Tag e release `v0.3.0` no GitHub
- [ ] `main` de volta ao `develop`
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 37 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c release/v0.3.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c release/v0.3.0` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'release/v0.3.0'`.

### Passo 38 — Copia e grava os 4 commits

São 4 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 3.6 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 3.6. Eles estão na pasta `ctesp-ADC/fase-3/ficheiros/3.6/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 4**

```bash
python ../ctesp-ADC/copiar.py 3.6 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/campanhas.py`, `tests/test_administracao.py`.

```bash
git add -A
git commit -m "fix(cli): corrigir a mensagem de atribuição de marketeer"
```

**Deves ver** uma linha a terminar em `2 files changed, 2 insertions(+), 2 deletions(-)`.

**Commit 2 de 4**

```bash
python ../ctesp-ADC/copiar.py 3.6 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/__init__.py`.

```bash
git add -A
git commit -m "chore(release): passar a versão para 0.3.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 1 insertion(+), 1 deletion(-)`.

**Commit 3 de 4**

```bash
python ../ctesp-ADC/copiar.py 3.6 3
```

**Deves ver** `Copiados 1 ficheiro`: `CHANGELOG.md`.

```bash
git add -A
git commit -m "docs(release): registar as alterações da versão 0.3.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 27 insertions(+)`.

**Commit 4 de 4**

```bash
python ../ctesp-ADC/copiar.py 3.6 4
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(release): atualizar o README para a versão 0.3.0"
```

**Deves ver** uma linha a terminar em `1 file changed, 21 insertions(+), 3 deletions(-)`.


### Passo 39 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 3.6
git log --oneline -4
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 3.6` | `Tudo certo: o ramo 'release/v0.3.0' está igual ao original no fim da unidade 3.6.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -4` | Os teus 4 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(release): atualizar o README para a versão 0.3.0
xxxxxxx docs(release): registar as alterações da versão 0.3.0
xxxxxxx chore(release): passar a versão para 0.3.0
xxxxxxx fix(cli): corrigir a mensagem de atribuição de marketeer
```

### Passo 40 — Experimenta o que gravaste

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

### Passo 41 — Envia o ramo para o GitHub

```bash
git push -u origin release/v0.3.0
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      release/v0.3.0 -> release/v0.3.0`.

### Passo 42 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `main`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/main...release/v0.3.0?expand=1

**b)** Confirma, no topo, que está **base: main** e **compare: release/v0.3.0**. O link do ponto a) já abre com o `main` escolhido. Se estiver **base: develop**, clica aí e escolhe `main`. Uma release vai para o `main`, que é o ramo das versões entregues.

**c)** No título, cola:

```text
Release v0.3.0
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Não é preciso trocar nada:

```markdown
## O que muda

Prepara a versão 0.3.0.

- Corrige a mensagem mostrada quando uma campanha muda de marketeer
- Versão passa de 0.2.0 para 0.3.0
- `CHANGELOG.md` com a secção da versão 0.3.0
- README atualizado: tabela de versões, dados de demonstração e secção sobre campanhas e pedidos

Este pull request vai para o `main`. A issue da release é fechada pelo pull request que leva a release de volta ao `develop`.

## Como testar

1. `python -m pytest` (382 testes)
2. `python -m sphinx -W -b html docs docs/_build/html`
3. `python -m gestor_campanhas`: o título mostra `v0.3.0`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** Confirma o destino. Por baixo do título do pull request tem de estar escrito `... wants to merge 4 commits into main from release/v0.3.0`. Se disser `into develop`, **não avises ninguém ainda**: clica em **Edit**, à direita do título, clica em **base: develop**, escolhe `main`, confirma em **Change base** e clica em **Save**.

### Passo 43 — Avisa Fabio

Diz a Fabio que o pull request da release v0.3.0 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 28 a 35.

---

## Publicar a release v0.3.0 e pedir o regresso ao develop

Com a release no `main`, falta marcá-la com uma tag e levar os commits dela de volta ao `develop`.

### Passo 44 — Confirma que o main já tem a versão 0.3.0

Faz este passo quando Fabio te avisar que a release está no `main`.

A tag vai ser criada no `main`. Se o `main` ainda não tiver a versão nova, a tag fica a marcar o código da versão anterior. Foi o que aconteceu nas duas primeiras fases.

Abre https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py

**Deves ver** a linha `__version__ = "0.3.0"`.

Se vires outra versão, **não publiques a release**. O pull request foi junto ao `develop` em vez do `main`. Avisa Fabio e corrijam assim: abre https://github.com/Blive77/ADC-TrabGrupo/compare/main...develop?expand=1, cria um pull request com o título `Release v0.3.0`, Fabio aprova e junta, e só depois voltas a este passo.

### Passo 45 — Publica a release v0.3.0 no GitHub

Publicar a release cria a **tag**, uma etiqueta que marca para sempre o commit desta versão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/releases/new

**b)** Clica em **Choose a tag**, escreve `v0.3.0` e clica em **Create new tag: v0.3.0 on publish**.

**c)** Em **Target**, escolhe `main`.

**d)** Em **Release title**, cola:

```text
v0.3.0 — Campanhas e pedidos
```

**e)** Na caixa de texto, cola:

````markdown
## Campanhas e pedidos de campanha

A aplicação passa a ter campanhas. O Marketeer cria-as e gere-as, o Cliente pede-as e acompanha-as, e o Administrador decide os pedidos, define o budget e escolhe o marketeer responsável.

### Acrescentado

- Campanhas: o Marketeer cria, edita, consulta e elimina as campanhas que lhe estão atribuídas
- Lista de campanhas com o cliente, as datas, o budget e o estado (por começar, em curso ou terminada)
- Pedidos de nova campanha: o Cliente indica o objetivo, o orçamento, o prazo e as plataformas, acompanha o estado e cancela os pedidos pendentes
- Decisão dos pedidos pelo Administrador: aprovar cria a campanha; rejeitar exige um motivo. O cliente é avisado por email
- Budget de cada campanha e marketeer responsável, definidos pelo Administrador. O marketeer é avisado por email
- O Cliente vê as suas campanhas, o budget de cada uma e os contactos do marketeer responsável
- Número de campanhas ativas nas listas de clientes e de marketeers
- Campanhas e pedidos de demonstração

### Alterado

- Um marketeer só pode ser desativado depois de as suas campanhas por terminar serem atribuídas a outro marketeer

### User stories

M02, M03, M04, M05, C05, C06, C07, C08, C09, A11, A12 e A13.

Ficam também concluídas as partes de A04 e de A10 adiadas na versão 0.2.0. O budget restante e os criativos por estado (M04) e a verificação "sem criativos" (M05) entram na versão 0.4.0; os pedidos de alteração de budget (C06) entram na versão 0.5.0.

### Como experimentar

```
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

Entrar com `admin@agencia.pt` / `admin12345` e escolher "Pedidos de campanha" ou "Campanhas". As outras contas de demonstração estão no README.
````

**f)** Clica em **Publish release**.

**Deves ver** a página da release, e a tag `v0.3.0` em https://github.com/Blive77/ADC-TrabGrupo/tags. Na linha da tag aparece o commit `Merge pull request ... from .../release/v0.3.0`. Se aparecer outro commit, o **Target** ficou errado: avisa o grupo antes de continuar.

### Passo 46 — Abre o pull request que leva a release para o develop

A release está no `main`, mas o `develop` ainda não tem os commits dela (a versão nova e o registo de alterações). Este pull request leva-os para lá, para os dois ramos ficarem alinhados.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/compare/develop...main

**b)** Confirma, no topo, que está **base: develop** e **compare: main**, e clica em **Create pull request**.

**c)** No título, cola:

```text
Juntar a release v0.3.0 ao develop
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue da release, que apontaste no início:

```markdown
## O que muda

Traz para o `develop` os commits da release v0.3.0, que já estão no `main`: a versão nova, o registo de alterações e o README.

Closes #N
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 3 — Campanhas e pedidos`

**f)** Clica em **Create pull request**.

### Passo 47 — Avisa Fabio

Diz a Fabio que o pull request que leva a release v0.3.0 para o `develop` está aberto. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 36 a 39.

### Passo 48 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d release/v0.3.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d release/v0.3.0` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

### Passo 49 — Fecha a milestone da fase

Faz este passo depois de Fabio juntar o último pull request. Nessa altura a issue da release já está fechada, e a milestone fica com todas as issues fechadas.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/milestones

**b)** Na linha `Fase 3 — Campanhas e pedidos`, confirma que a barra está a 100% e clica em **Close**.

Se a barra não estiver a 100%, clica no nome da milestone para ver que issues estão abertas. Uma issue fica aberta quando o pull request dela foi junto sem `Closes #número`. Para a fechar à mão, abre a issue, escreve na caixa de comentário `Resolvida pelo pull request #N` (com o número do pull request) e clica em **Close with comment**. Depois volta a este passo.

---

## Outras tarefas desta fase

### Passo 50 — Atualiza a página inicial da wiki

A página inicial passa a indicar a versão 0.3.0.

Faz este passo no fim da fase, depois de publicares a release.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 0.3.0` e clica em **Save page**.

**Deves ver** a linha `Versão atual: v0.3.0 (Fase 3 — Campanhas e pedidos).`

### Passo 51 — Atualiza a página "Registo das fases" da wiki

A página ganha a secção da Fase 3: quem fez e quem reviu cada unidade, as decisões tomadas e o que correu mal na Fase 2.

Faz este passo no fim da fase, depois de a release v0.3.0 estar publicada.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Registo das fases** na lista de páginas, à direita, e depois em **Edit**.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Registar a Fase 3` e clica em **Save page**.

**Deves ver** a secção `Fase 3 — Campanhas e pedidos`, com a tabela das seis unidades.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 3.1 — Criar e editar campanhas

- **`gestor_campanhas/bd.py`** ganha a tabela `campanhas`. Duas colunas são chaves estrangeiras para a tabela `utilizadores`: `cliente_id` (a quem pertence a campanha) e `marketeer_id` (quem é responsável). O SQLite recusa uma campanha cujo cliente ou marketeer não exista. A tabela já tem a coluna `budget_centimos`, que só vai ser usada na unidade 3.4: assim não é preciso alterar a tabela a meio da fase.
- **`gestor_campanhas/modelos.py`** ganha a classe `Campanha`. Além das colunas da tabela, tem `cliente_nome` e `marketeer_nome`, que não estão na tabela `campanhas`: vêm da tabela `utilizadores`.
- **`gestor_campanhas/repositorios/campanhas.py`** é novo. A constante `_SELECIONAR` é uma consulta com dois `JOIN`: junta cada campanha à linha do cliente e à linha do marketeer, para trazer os nomes de uma só vez. Como a tabela `utilizadores` entra duas vezes, cada entrada leva um nome diferente (`AS clientes`, `AS marketeers`). As datas são guardadas como texto `AAAA-MM-DD` e convertidas para `date` ao ler.
- **`gestor_campanhas/servicos/validacao.py`** ganha `data`, que converte o texto escrito numa data (ou em `None`, se ficar vazio), e `periodo`, que recusa um fim anterior ao início. O módulo deixou de ser só para os dados de uma conta, por isso o texto de apresentação dele foi atualizado.
- **`gestor_campanhas/servicos/campanhas.py`** é novo e tem as regras.
  - `criar` confirma que o número indicado é de um cliente com a conta ativa e valida os dados antes de guardar. O marketeer que cria fica como responsável.
  - `obter_do_marketeer` devolve uma campanha só se for do marketeer que a pede. A mensagem é a mesma quando a campanha não existe e quando é de outro marketeer, para não revelar que campanhas existem.
  - `editar` usa `obter_do_marketeer` e as mesmas validações de `criar`. Se um valor estiver errado, o erro é lançado antes do `UPDATE`.
- **`gestor_campanhas/cli/campanhas.py`** é novo. `do_marketeer` é um ciclo igual ao da gestão de clientes: mostra a lista, mostra o menu e volta ao início depois de cada opção. Na edição, `_ler_data_com_valor` trata o `-` como "apagar a data".
- **`gestor_campanhas/cli/perfis.py`**: o menu do Marketeer ganha a opção "Campanhas", antes das opções da conta.
- **`tests/test_campanhas.py`** é novo. As fixtures `marta` e `jose` criam um segundo marketeer e um segundo cliente, para testar que cada um só vê o que é seu. Os testes do ecrã usam a fixture `teclado`: em `teclado("1", str(cliente.id), "Natal", "Vender mais", "2026-12-01", "", "", "0")`, as respostas são a opção 1, o número do cliente, o nome, o objetivo, a data de início, a data de fim vazia, o Enter da pausa e o `0` para voltar.

### Unidade 3.4 — Decidir pedidos, budget e marketeer responsável

- **Os repositórios** ganham as funções que faltavam ao Administrador: `listar_todas`, `definir_budget` e `definir_marketeer` nas campanhas, e `listar_todos` nos pedidos.
- **`tests/conftest.py`** ganha a fixture `emails`. Põe a pasta de dados numa pasta temporária e devolve uma função que lê os emails enviados. O ficheiro `tests/test_administracao.py` usa-a em todos os testes, para nenhum escrever na pasta `dados` verdadeira.
- **`gestor_campanhas/servicos/campanhas.py`** ganha as regras do budget e do marketeer.
  - `budget_validado` converte o valor e exige que seja maior do que zero. É usada em dois sítios: em "Definir budget" e na aprovação de um pedido.
  - `marketeer_ativo` confirma que o número é de um marketeer com a conta ativa. Também é usada nos dois sítios.
  - `atribuir_marketeer` recusa atribuir ao marketeer que já é o responsável, para não enviar um aviso sem ter mudado nada.
- **`gestor_campanhas/servicos/pedidos.py`** ganha a parte do Administrador.
  - `analisar` passa um pedido pendente a "Em análise". É por isso que o cliente deixa de o poder cancelar: a regra da unidade 3.3 só aceita pedidos pendentes.
  - `aprovar` valida tudo primeiro e só depois cria a campanha, marca o pedido como aprovado e envia os dois emails. Se o nome, o budget ou o marketeer não servirem, o erro é lançado antes de qualquer alteração.
  - `rejeitar` exige o motivo, que fica guardado no pedido e vai no email.
  - A constante `POR_DECIDIR` junta os dois estados em que um pedido ainda espera pela decisão. `listar_todos` usa-a para pôr esses pedidos em primeiro lugar.
- **O prazo do pedido passa a ser a data de fim da campanha.** O cliente pede a campanha "até" um dia; a campanha criada fica com esse dia como data de fim, e o marketeer pode ajustar as datas na opção "Editar campanha".
- **`gestor_campanhas/cli/pedidos.py`** e **`gestor_campanhas/cli/campanhas.py`** ganham as funções `do_administrador`. O ecrã de analisar tem um segundo menu (`Decisão`), feito com a mesma função `escolher_opcao` de todos os menus.
- **Campanhas ativas (A04).** `Campanha.terminada` diz se a data de fim já passou. `contar_ativas` conta as campanhas não terminadas de cada cliente ou de cada marketeer, e a tabela da gestão de contas ganha a coluna `Campanhas ativas`. Os testes antigos da tabela continuam a passar, porque a coluna nova ficou à direita.
- **Desativar um marketeer (A10).** `gestao.definir_estado` passa a recusar a desativação de um marketeer que ainda seja responsável por campanhas por terminar, e diz quantas são. O ecrã `alterar_estado` não apanhava erros, porque até aqui a desativação não podia falhar depois da confirmação; ganhou um `try`/`except`.
- **Porque é que a verificação usa o repositório e não o serviço das campanhas.** O serviço das campanhas já usa o serviço da gestão (para listar clientes e marketeers). Se a gestão usasse o serviço das campanhas, os dois módulos ficavam a depender um do outro, e o Python não consegue carregar dois módulos que se importam mutuamente. Por isso a regra "terminada" está na classe `Campanha`, que os dois podem usar.

### Unidade 3.6 — Release v0.3.0

- **Um `fix` num ramo de release.** O primeiro commit corrige uma mensagem da unidade 3.4. Quando o Administrador atribuía uma campanha à Marta, aparecia "A campanha passou para Marta Marques, que foi avisado por email". A frase nova não depende de ser um marketeer ou uma marketeer: "A campanha passou para Marta Marques. Foi enviado um aviso por email." É para isto que serve o ramo de release: antes de publicar a versão, faz-se uma última revisão e corrigem-se os pormenores que aparecerem. O tipo do commit é `fix`, e não `feat`, porque corrige uma coisa que já existia.
- **`tests/test_administracao.py`** muda no mesmo commit: o teste que confirmava a mensagem antiga passa a confirmar a nova. Código e teste mudam sempre juntos, para os testes passarem em todos os commits.
- **`gestor_campanhas/__init__.py`**: `__version__` passa para `"0.3.0"`. O menu inicial, o `pyproject.toml` e a documentação leem a versão daqui.
- **`CHANGELOG.md`** ganha a secção `v0.3.0`, por cima das anteriores. A parte "User stories concluídas" diz também o que ficou das fases anteriores e o que passa para as seguintes, para quem lê saber exatamente o que a versão tem.
- **`README.md`**: a tabela de versões ganha uma linha, o exemplo do menu passa a mostrar `v0.3.0` e há uma secção nova que explica as duas maneiras de uma campanha nascer e o que cada perfil faz.
- **O caminho de uma release.** São quatro momentos, sempre pela mesma ordem: o pull request do ramo `release/v0.3.0` para o `main`; a publicação da release, que cria a tag no `main`; o pull request do `main` para o `develop`; e o fecho da milestone.
- **O que correu mal nas Fases 1 e 2.** Nas duas, o pull request da release foi junto ao `develop` em vez do `main`, e a tag ficou no código da versão anterior. Corrigiu-se das duas vezes com um pull request do `develop` para o `main` e refazendo a tag. Nesta fase mudam duas coisas: o link para abrir o pull request já traz o `main` escolhido, e há um passo novo, antes de publicar a release, para confirmar que o `main` já tem a versão 0.3.0.
- **Porque é que a tag tem de estar no `main`.** A tag é o que diz "a versão 0.3.0 é exatamente este commit". Quem descarregar a versão pela página das releases recebe o código desse commit. Se a tag estiver no sítio errado, recebe outra coisa.
