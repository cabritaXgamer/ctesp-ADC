# Fase 6 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 6 (Comentários, notificações, painel e relatório), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 6.2 (de Fabio) | Quando Fabio avisar |
| 8 a 17 | Fazer a unidade 6.3 — Painel de marketeers | A seguir ao teu passo anterior |
| 18 | Atualiza a página "Arquitetura" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 6.2 — Notificações na aplicação e por email

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 6.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Notificações na aplicação e por email**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 3 linhas `Closes #` seguida de um número, uma por issue (C17, C19, M18), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Fabio para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/6.2-notificacoes
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/6.2-notificacoes` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/6.2-notificacoes'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `795 passed`.

Garante que tens os dados de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Primeiro, um comentário. Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`). O menu tem agora `4. Notificações`, e as opções da conta passaram para `5` e `6`.

| Escreves | Deves ver |
|---|---|
| `3`, `6` e o número do `Vídeo da montra` | Os comentários do criativo e a pergunta `Comentário ou sugestão (Enter para cancelar)` |
| `O vídeo devia ter música de Natal` | `Comentário guardado. O marketeer vai vê-lo no detalhe do criativo.` |

Sai com Enter, `0` e `0`. Entra como marketeer (`1`, `marketeer@agencia.pt` e `marketeer12345`).

**Deves ver**, logo por baixo de `Bem-vindo, Miguel Marketeer.`, a linha `Tem 1 notificação por ler, na opção "Notificações".`

| Escreves | Deves ver |
|---|---|
| `4` | O título `As minhas notificações` e uma linha `Por ler`, sobre o `Criativo n.º ...`, com a mensagem `Carla Cliente comentou o criativo Vídeo da montra, da cam...`; por baixo, `1 notificação, 1 por ler.` |
| `1` e o número da notificação (primeira coluna) | `Notificação n.º ..., de ...`, a mensagem completa e, logo a seguir, os dados do `Vídeo da montra`, com os comentários; o último é `O vídeo devia ter música de Natal`, `(ainda sem resposta)` |
| Enter | A notificação passou a `Lida`, e por baixo `1 notificação, 0 por ler.` |
| `0` | O menu, já sem a linha das notificações por ler |

Agora responde ao comentário e cria e elimina um criativo de teste, para a Carla receber notificações:

| Escreves | Deves ver |
|---|---|
| `2` e o número da campanha `Natal 2026` | Os criativos da campanha |
| `8`, o número do `Vídeo da montra`, o número do comentário `O vídeo devia ter música de Natal` e `Vou pôr música de Natal no vídeo` | `Resposta guardada. O cliente vai vê-la no detalhe do criativo.` |
| Enter, `1`, `Teste das notificações` e Enter nas outras cinco perguntas | `Criativo criado com o número ...`. Aponta o número |
| Enter, `4`, o número do `Teste das notificações` e `s` | `O criativo Teste das notificações foi eliminado.` |

Sai com Enter, `0`, Enter e `0`. Entra outra vez como cliente (`1`, `cliente@empresa.pt` e `cliente12345`).

**Deves ver** `Tem 3 notificações por ler, na opção "Notificações".` Escolhe `4`. Os números das notificações e dos itens podem ser outros:

```text
N.º  Data              Estado   Sobre           Mensagem
---  ----------------  -------  --------------  ------------------------------------------------------------
4    2026-11-19 11:06  Por ler  Campanha n.º 1  O criativo Teste das notificações, da campanha Natal 2026...
3    2026-11-19 11:06  Por ler  Criativo n.º 5  Foi criado o criativo Teste das notificações, da campanha...
2    2026-11-19 11:06  Por ler  Criativo n.º 2  Miguel Marketeer respondeu ao seu comentário sobre o cria...

3 notificações, 3 por ler.
```

| Escreves | Deves ver |
|---|---|
| `1` e o número da notificação da resposta (a de baixo) | A mensagem completa, os dados do `Vídeo da montra` e, por baixo do comentário, `Resposta de Miguel Marketeer` |
| Enter, `1` e o número da notificação do criativo criado (a do meio) | A mensagem e `Não tem nenhum criativo com o número .... O item desta notificação já não está disponível.`, porque o criativo foi eliminado |
| Enter e `2` | `1 notificação marcada como lida.` |
| Enter | As três notificações `Lida` e `3 notificações, 0 por ler.` |

Sai com `0` e `0`. Por fim, um pedido de budget, que passa pelos três perfis. Entra como `beatriz@bicicletas.pt` / `beatriz12345`:

| Escreves | Deves ver |
|---|---|
| `1`, `4`, o número da campanha `Bicicletas de primavera`, `900` e `Começar a campanha` | `Pedido registado com o número ...`. Aponta o número. Se aparecer que a campanha já tem um pedido por decidir, cancela esse pedido primeiro (`6`, o número dele e `s`) |

Sai com Enter, `0` e `0`. Entra como `marta@agencia.pt` / `marta12345`: aparece `Tem 1 notificação por ler`.

| Escreves | Deves ver |
|---|---|
| `4`, `1` e o número da notificação | `Beatriz Lopes pediu para alterar o budget da campanha Bicicletas de primavera de Por definir para 900,00 € (pedido n.º ...).` e os dados do pedido, com `Parecer:      Por dar` |
| Enter, `0`, `3`, `1`, o número do pedido, `n` e `Ainda não há criativos com custo` | `Parecer guardado. O pedido fica em análise, à espera da decisão do administrador.` |

Sai com Enter, `0` e `0`. Entra como administrador (`admin@agencia.pt` / `admin12345`). O menu do Administrador não tem `Notificações`.

| Escreves | Deves ver |
|---|---|
| `4`, `1`, o número do pedido da Beatriz, `2`, `Sem orçamento este mês` e `s` | `Pedido rejeitado. O budget da campanha não mudou.` |

Sai com Enter, `0` e `0`. Entra outra vez como Beatriz: aparece `Tem 1 notificação por ler`.

| Escreves | Deves ver |
|---|---|
| `4`, `1` e o número da notificação | `O seu pedido de budget n.º ..., para a campanha Bicicletas de primavera, foi rejeitado. Motivo: Sem orçamento este mês` e os dados do pedido, com `Estado:       Rejeitado` |

Sai com Enter, `0` e `0`. Abre a pasta `dados\caixa_saida`: o ficheiro mais recente é o email para a Beatriz, com `Assunto: O seu pedido de budget foi rejeitado` e o mesmo texto.

Confirma também:

- Entra como `beatriz@bicicletas.pt`, faz outro pedido para a `Bicicletas de primavera` (`1`, `4`, a campanha, `700` e `Segunda tentativa`); como `marta@agencia.pt`, dá parecer `s` com a justificação `Já há criativos`; como administrador, `4`, `1`, o número do pedido e `1` (Aprovar). Entra como Beatriz e abre a notificação nova: `O seu pedido de budget n.º ... foi aprovado. O budget da campanha Bicicletas de primavera passou a 700,00 €.`
- Como administrador, `5` (Campanhas), `2` (Atribuir marketeer), o número da `Bicicletas de primavera` e o número do Miguel. Entra como Miguel: há uma notificação `Passou a ser responsável pela campanha Bicicletas de primavera, do cliente Beatriz Lopes.`, e abri-la mostra os dados da campanha. Depois, como administrador, devolve a campanha à Marta da mesma maneira.
- Como Miguel, `2`, a campanha `Natal 2026`, `5` (Atualizar estado), o número do `Banner de Natal`: se o banner estiver `Em preparação`, envia-o para revisão (`1`). Entra como Carla: há uma notificação `O criativo Banner de Natal, da campanha Natal 2026, passou a Em revisão e está à espera da sua aprovação.` (Se o banner estiver noutro estado, salta este ponto.)
- Ainda como Carla, `4` e `2` (Marcar todas como lidas) duas vezes: a segunda responde `Não havia notificações por ler.`

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

**f)** No Trello, move os cards das stories C17, C19 e M18 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/6.2-notificacoes
python ../ctesp-ADC/verificar.py 6.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/6.2-notificacoes` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 6.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 6.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 6.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 6.3 — Painel de marketeers

O Administrador ganha a opção "Painel de marketeers", que compara o trabalho de cada marketeer: campanhas ativas, criativos ativos, em atraso e concluídos, e a última atividade. Os marketeers sem atividade aparecem em destaque. Do painel vê-se o trabalho de cada marketeer, compara-se a carga num período e muda-se o número de dias sem atividade.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Notificações na aplicação e por email** (unidade 6.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 6.3

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 3 issues: A17, A18, A19. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A17** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA17%5D%22

```markdown
- [ ] O menu do Administrador tem a opção nova "8. Painel de marketeers", a seguir a "Horários de entrada e saída dos marketeers"; as opções da conta passam para 9 e 10
- [ ] O painel mostra uma linha por marketeer com a conta ativa, por ordem alfabética
- [ ] "Ver o trabalho de um marketeer" mostra cada campanha dele, com o cliente e o estado, e os criativos de cada uma, com o estado, o prazo e `Em atraso` quando é o caso
- [ ] Mostra também as cinco últimas atividades do marketeer, com a data e a hora
```

**Issue A18** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA18%5D%22

```markdown
- [ ] O painel mostra, de cada marketeer, as campanhas ativas e os criativos ativos (em preparação, em revisão ou rejeitados), em atraso (ativos com o prazo já passado) e concluídos (aprovados ou publicados)
- [ ] "Comparar num período" pede as datas `Desde` e `Até` (cada uma pode ficar vazia) e conta só os criativos com o prazo dentro do período
- [ ] Uma data inicial depois da data final é recusada
```

**Issue A19** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA19%5D%22

```markdown
- [ ] O painel mostra a data da última atividade de cada marketeer: a última vez que criou, editou ou eliminou um criativo, lhe mudou o estado, lhe anexou um ficheiro ou respondeu a um comentário
- [ ] Os criativos que já existiam antes desta unidade contam pelo dia em que foram criados
- [ ] A coluna `Situação` diz `Sem criativos ativos` ou `Parado há N dias` (sem atividade há 7 dias ou mais); por baixo aparece quantos marketeers estão sem atividade, e quais
- [ ] "Mudar os dias sem atividade" muda o número de dias (pelo menos 1); o valor fica guardado
```

Por fim, no quadro Trello, move os cards das stories A17, A18 e A19 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/6.3-painel-de-marketeers
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/6.3-painel-de-marketeers` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/6.3-painel-de-marketeers'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/6.3-painel-de-marketeers' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/6.3-painel-de-marketeers
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/6.3-painel-de-marketeers
git switch -c feature/6.3-painel-de-marketeers
```

  **Deves ver** `Deleted branch feature/6.3-painel-de-marketeers (was ...)` e depois `Switched to a new branch 'feature/6.3-painel-de-marketeers'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/6.3-painel-de-marketeers` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 6.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 6.3. Eles estão na pasta `ctesp-ADC/fase-6/ficheiros/6.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.3 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela da atividade dos marketeers"
```

**Deves ver** uma linha a terminar em `2 files changed, 26 insertions(+)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.3 2
```

**Deves ver** `Copiados 4 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/atividades.py`, `gestor_campanhas/repositorios/criativos.py`, `tests/test_painel.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar a atividade e ler os criativos de cada marketeer"
```

**Deves ver** uma linha a terminar em `4 files changed, 233 insertions(+), 1 deletion(-)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.3 3
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/servicos/comentarios.py`, `gestor_campanhas/servicos/criativos.py`, `tests/test_painel.py`.

```bash
git add -A
git commit -m "feat(painel): registar a atividade dos marketeers nos criativos"
```

**Deves ver** uma linha a terminar em `3 files changed, 67 insertions(+), 4 deletions(-)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.3 4
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/config.py`, `gestor_campanhas/servicos/painel.py`, `tests/test_painel.py`.

```bash
git add -A
git commit -m "feat(painel): carga de trabalho e inatividade dos marketeers"
```

**Deves ver** uma linha a terminar em `3 files changed, 358 insertions(+)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.3 5
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/painel.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_painel.py`.

```bash
git add -A
git commit -m "feat(cli): painel de marketeers no menu do administrador"
```

**Deves ver** uma linha a terminar em `3 files changed, 409 insertions(+), 1 deletion(-)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.3 6
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar o painel de marketeers"
```

**Deves ver** uma linha a terminar em `3 files changed, 97 insertions(+)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 6.3
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 6.3` | `Tudo certo: o ramo 'feature/6.3-painel-de-marketeers' está igual ao original no fim da unidade 6.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar o painel de marketeers
xxxxxxx feat(cli): painel de marketeers no menu do administrador
xxxxxxx feat(painel): carga de trabalho e inatividade dos marketeers
xxxxxxx feat(painel): registar a atividade dos marketeers nos criativos
xxxxxxx feat(repositorios): guardar a atividade e ler os criativos de cada marketeer
xxxxxxx feat(bd): criar a tabela da atividade dos marketeers
```

### Passo 13 — Experimenta o que gravaste

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

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/6.3-painel-de-marketeers
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/6.3-painel-de-marketeers -> feature/6.3-painel-de-marketeers`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/6.3-painel-de-marketeers?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/6.3-painel-de-marketeers**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Painel de marketeers
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a ter um painel para acompanhar o trabalho dos marketeers.

- Tabela `atividades`, classe `Atividade` e repositório, com a atividade dos marketeers
- As alterações aos criativos e as respostas a comentários ficam registadas na atividade do marketeer
- Indicadores de cada marketeer (campanhas ativas, criativos ativos, em atraso e concluídos, última atividade) e a regra "sem atividade", com o número de dias guardado nas configurações
- Opção "Painel de marketeers" no menu do Administrador, com o trabalho de cada marketeer, a comparação num período e os dias sem atividade

Closes #(número da issue A17)
Closes #(número da issue A18)
Closes #(número da issue A19)

## Como testar

1. `python -m pytest` (845 testes)
2. `python -m gestor_campanhas`
3. Como administrador, abrir o painel, ver o trabalho do Miguel, comparar novembro, mudar os dias para 1 e depois outra vez para 7; como `marta@agencia.pt`, editar um criativo e confirmar que a última atividade dela passa a hoje
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 6 — Comentários, notificações e relatórios`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories A17, A18 e A19 para **Ready to Verify**.

### Passo 16 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 6.3 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 11 a 17.

### Passo 17 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/6.3-painel-de-marketeers
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/6.3-painel-de-marketeers` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Outras tarefas desta fase

### Passo 18 — Atualiza a página "Arquitetura" da wiki

A página ganha as secções `Comentários`, `Notificações`, `Painel de marketeers` e `Relatório`. A tabela das tabelas ganha as linhas `comentarios`, `notificacoes` e `atividades`.

Faz este passo depois de a unidade 6.4 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Arquitetura.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki/Arquitetura e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a Arquitetura para a versão 0.6.0` e clica em **Save page**.

**Deves ver** a página com as secções novas `Comentários`, `Notificações`, `Painel de marketeers` e `Relatório`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 6.3 — Painel de marketeers

- **`gestor_campanhas/bd.py`** ganha a tabela `atividades`: uma linha por alteração feita por um marketeer, com a descrição e a data. A tabela `criativos` não guarda a data da última alteração (ficou de fora na Fase 4), e o `CREATE TABLE IF NOT EXISTS` não acrescenta colunas a uma tabela que já existe; por isso a atividade tem uma tabela própria.
- **`gestor_campanhas/modelos.py`** ganha a classe `Atividade`.
- **`gestor_campanhas/repositorios/atividades.py`** é novo: `registar`, `listar_por_utilizador` (as mais recentes primeiro) e `ultima_por_utilizador`, que devolve a data da última atividade de cada marketeer numa só consulta (`MAX` com `GROUP BY`).
- **`gestor_campanhas/repositorios/criativos.py`** ganha `listar_por_marketeer` (os criativos de todas as campanhas de um marketeer) e `ultima_criacao_por_marketeer`, a data do criativo mais recente de cada marketeer, que serve de atividade para os criativos que já existiam.
- **`gestor_campanhas/servicos/criativos.py`** e **`servicos/comentarios.py`**: cada alteração bem-sucedida fica na atividade do marketeer (função `_registar` nos criativos), ao lado da notificação ao cliente.
- **`gestor_campanhas/config.py`** ganha `DIAS_SEM_ATIVIDADE = 7`, o valor usado enquanto o Administrador não guardar outro.
- **`gestor_campanhas/servicos/painel.py`** é novo. As constantes `ATIVOS` e `CONCLUIDOS` dizem que estados contam em cada grupo, e `em_atraso` a regra do atraso. `carga` calcula os indicadores de cada marketeer com a conta ativa, com ou sem período; `situacao` diz se está sem atividade; `dias_sem_atividade` e `definir_dias_sem_atividade` guardam o número de dias na tabela `configuracoes`, como o limite de inatividade das sessões. `trabalho` junta as campanhas de um marketeer aos criativos de cada uma.
- **`gestor_campanhas/cli/painel.py`** é novo: a tabela principal (`mostrar_carga`), as explicações das colunas e as três opções. `em_dias` escreve "1 dia" ou "N dias".
- **`gestor_campanhas/cli/perfis.py`**: o menu do Administrador ganha "Painel de marketeers", a seguir aos horários.
- **`tests/test_painel.py`** é novo: base de dados, registo da atividade, indicadores, situação e ecrãs. `tests/test_bd.py` testa a tabela nova.
- **`docs/`**: o guia de utilização ganha a secção "Painel de marketeers", a arquitetura a tabela nova e a secção com o mesmo nome, e a referência os três módulos novos.
