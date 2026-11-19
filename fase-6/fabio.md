# Fase 6 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 6 (Comentários, notificações, painel e relatório), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 6.1 (de Ricardo) | Quando Ricardo avisar |
| 8 a 17 | Fazer a unidade 6.2 — Notificações na aplicação e por email | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 6.4 (de Ricardo) | Quando Ricardo avisar |
| 25 a 32 | Rever a release v0.6.0 e juntá-la ao main | Quando Ricardo avisar |
| 33 a 36 | Juntar a release v0.6.0 ao develop | Quando Ricardo avisar |
| 37 | Atualiza a página "Guia de utilização" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 6.1 — Comentários dos criativos e respostas

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 6.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Comentários dos criativos e respostas**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 2 linhas `Closes #` seguida de um número, uma por issue (C18, M17), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Ricardo para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/6.1-comentarios-dos-criativos
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/6.1-comentarios-dos-criativos` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/6.1-comentarios-dos-criativos'`.

Agora experimenta:

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

Confirma também:

- Entra como `cliente@empresa.pt` / `cliente12345`, `3` e `2` e o número do `Vídeo da montra`: por baixo do comentário aparece a resposta do Miguel, com `Resposta de Miguel Marketeer, em`.
- Ainda como Carla, `6`, o número do `Vídeo da montra` e, no comentário, só Enter: volta a lista, e o `Vídeo da montra` continua só com um comentário. Depois, `6` e `999`: aparece `Não tem nenhum criativo com o número 999.`
- Entra como `marketeer@agencia.pt` / `marketeer12345`, `2`, a campanha `Natal 2026`, `8` e o número do `Vídeo da montra`, e escreve `999` no número do comentário: aparece `Este criativo não tem nenhum comentário do cliente com o número 999.`
- Ainda como Miguel, `8` e o número do `Banner de Natal`, o número do comentário da Carla e a resposta `Vou aumentar o logótipo`: a linha dos comentários por responder desaparece da lista.
- Entra como `marta@agencia.pt` / `marta12345`, `2`, a campanha `Bicicletas de primavera` e `8` com o número do `Anúncio da bicicleta elétrica`: aparece `O criativo Anúncio da bicicleta elétrica ainda não tem comentários do cliente.`

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

**f)** No Trello, move os cards das stories C18 e M17 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/6.1-comentarios-dos-criativos
python ../ctesp-ADC/verificar.py 6.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/6.1-comentarios-dos-criativos` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 6.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 6.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 6.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Ricardo](ricardo.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 6.2 — Notificações na aplicação e por email

O Marketeer e o Cliente passam a receber notificações do que lhes diz respeito: uma campanha nova, um pedido de budget, a decisão de um pedido, um criativo novo ou alterado, um comentário ou uma resposta. Cada notificação fica na opção nova "Notificações", de onde se abre diretamente o item, e é também enviada por email. Enquanto houver notificações por ler, o menu diz quantas são.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Comentários dos criativos e respostas** (unidade 6.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 6.2

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 3 issues: C17, C19, M18. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue C17** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC17%5D%22

```markdown
- [ ] Quando o Administrador aprova um pedido de alteração de budget, o cliente recebe uma notificação com o número do pedido, a campanha e o budget novo
- [ ] Quando o rejeita, a notificação tem o motivo da rejeição
- [ ] Abrir a notificação mostra o pedido de budget, com o estado final
```

**Issue C19** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BC19%5D%22

```markdown
- [ ] O cliente recebe uma notificação quando o marketeer cria, edita ou elimina um criativo de uma campanha dele, muda o estado de um criativo, lhe anexa um ficheiro ou responde a um comentário
- [ ] Quando um criativo passa a "Em revisão", a notificação diz que está à espera da aprovação do cliente
- [ ] Abrir a notificação mostra o criativo, com os comentários; a de um criativo eliminado mostra a campanha
- [ ] Uma alteração recusada por uma regra (por exemplo, um nome vazio) não notifica ninguém
```

**Issue M18** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BM18%5D%22

```markdown
- [ ] O marketeer recebe uma notificação quando passa a ser responsável por uma campanha (criada a partir de um pedido aprovado, ou atribuída pelo Administrador)
- [ ] Recebe uma notificação quando um cliente pede a alteração do budget de uma campanha dele, com o valor atual e o pedido
- [ ] Recebe uma notificação quando um cliente comenta um criativo de uma campanha dele, com o texto do comentário
- [ ] O menu do Marketeer e o do Cliente têm a opção nova "4. Notificações"; as opções da conta passam para 5 e 6
- [ ] A lista mostra o número, a data, se está lida ou por ler, o item ("Criativo n.º 2") e o texto, da mais recente para a mais antiga
- [ ] "Abrir notificação" marca-a como lida e mostra o item; "Marcar todas como lidas" marca as que faltam
- [ ] Por cima do menu do perfil aparece quantas notificações estão por ler
- [ ] Cada notificação é também enviada por email (pasta `dados/caixa_saida`); o Administrador não recebe notificações
```

Por fim, no quadro Trello, move os cards das stories C17, C19 e M18 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/6.2-notificacoes
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/6.2-notificacoes` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/6.2-notificacoes'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/6.2-notificacoes' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/6.2-notificacoes
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/6.2-notificacoes
git switch -c feature/6.2-notificacoes
```

  **Deves ver** `Deleted branch feature/6.2-notificacoes (was ...)` e depois `Switched to a new branch 'feature/6.2-notificacoes'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/6.2-notificacoes` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 6 commits

São 6 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 6.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 6.2. Eles estão na pasta `ctesp-ADC/fase-6/ficheiros/6.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.2 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/bd.py`, `tests/test_bd.py`.

```bash
git add -A
git commit -m "feat(bd): criar a tabela das notificações"
```

**Deves ver** uma linha a terminar em `2 files changed, 37 insertions(+)`.

**Commit 2 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.2 2
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/modelos.py`, `gestor_campanhas/repositorios/notificacoes.py`, `tests/test_notificacoes.py`.

```bash
git add -A
git commit -m "feat(repositorios): guardar e ler as notificações"
```

**Deves ver** uma linha a terminar em `3 files changed, 259 insertions(+)`.

**Commit 3 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.2 3
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/servicos/notificacoes.py`, `tests/test_notificacoes.py`.

```bash
git add -A
git commit -m "feat(notificacoes): notificar na plataforma e por email"
```

**Deves ver** uma linha a terminar em `2 files changed, 176 insertions(+)`.

**Commit 4 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.2 4
```

**Deves ver** `Copiados 6 ficheiros`: `gestor_campanhas/servicos/budget.py`, `gestor_campanhas/servicos/campanhas.py`, `gestor_campanhas/servicos/comentarios.py`, `gestor_campanhas/servicos/criativos.py`, `gestor_campanhas/servicos/pedidos.py`, `tests/test_notificacoes.py`.

```bash
git add -A
git commit -m "feat(notificacoes): avisar o marketeer e o cliente do que lhes diz respeito"
```

**Deves ver** uma linha a terminar em `6 files changed, 343 insertions(+), 30 deletions(-)`.

**Commit 5 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.2 5
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/cli/notificacoes.py`, `gestor_campanhas/cli/perfis.py`, `tests/test_notificacoes.py`.

```bash
git add -A
git commit -m "feat(cli): opção Notificações e aviso das notificações por ler"
```

**Deves ver** uma linha a terminar em `3 files changed, 359 insertions(+), 2 deletions(-)`.

**Commit 6 de 6**

```bash
python ../ctesp-ADC/copiar.py 6.2 6
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/referencia.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar as notificações"
```

**Deves ver** uma linha a terminar em `3 files changed, 111 insertions(+), 1 deletion(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 6.2
git log --oneline -6
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 6.2` | `Tudo certo: o ramo 'feature/6.2-notificacoes' está igual ao original no fim da unidade 6.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -6` | Os teus 6 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar as notificações
xxxxxxx feat(cli): opção Notificações e aviso das notificações por ler
xxxxxxx feat(notificacoes): avisar o marketeer e o cliente do que lhes diz respeito
xxxxxxx feat(notificacoes): notificar na plataforma e por email
xxxxxxx feat(repositorios): guardar e ler as notificações
xxxxxxx feat(bd): criar a tabela das notificações
```

### Passo 13 — Experimenta o que gravaste

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

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/6.2-notificacoes
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/6.2-notificacoes -> feature/6.2-notificacoes`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/6.2-notificacoes?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/6.2-notificacoes**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Notificações na aplicação e por email
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Marketeer e o Cliente passam a ser notificados do que lhes diz respeito, na aplicação e por email.

- Tabela `notificacoes`, classe `Notificacao` e repositório das notificações
- `notificar`, que guarda a notificação e envia o mesmo aviso por email
- Notificações nos eventos: campanha atribuída, pedido de budget novo, decisão do pedido, criativo criado, alterado, eliminado, com o estado mudado ou com um ficheiro novo, comentário e resposta
- Opção "Notificações" nos menus do Marketeer e do Cliente, para abrir cada item, e aviso das notificações por ler

Closes #(número da issue C17)
Closes #(número da issue C19)
Closes #(número da issue M18)

## Como testar

1. `python -m pytest` (795 testes)
2. `python -m gestor_campanhas.dados_demo` e depois `python -m gestor_campanhas`
3. Como `cliente@empresa.pt`, comentar o Vídeo da montra; como `marketeer@agencia.pt`, abrir a notificação, responder e criar e eliminar um criativo; como `cliente@empresa.pt`, ver as três notificações
4. Como `beatriz@bicicletas.pt`, pedir 900 € para a campanha Bicicletas de primavera; a Marta é notificada e dá parecer, o administrador rejeita e a Beatriz é notificada
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 6 — Comentários, notificações e relatórios`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move os cards das stories C17, C19 e M18 para **Ready to Verify**.

### Passo 16 — Avisa Tomas

Diz a Tomas que o pull request da unidade 6.2 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 1 a 7.

### Passo 17 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/6.2-notificacoes
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/6.2-notificacoes` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 6.4 — Relatório das campanhas em CSV

Quem fez: Ricardo. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 6.4 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Relatório das campanhas em CSV**.

Antes de mais, confirma que o pull request está ligado às issues. Na descrição tem de haver 1 linha `Closes #` seguida de um número, uma por issue (C20), e na coluna da direita, em **Development**, têm de aparecer essas issues.

Se faltar, **não juntes ainda**. Pede a Ricardo para clicar nos três pontos **…** da descrição, em **Edit**, e trocar cada `#(número da issue ...)` pelo número verdadeiro. Sem isto, as issues não fecham sozinhas quando juntares o pull request.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/6.4-exportar-relatorio
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch feature/6.4-exportar-relatorio` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/6.4-exportar-relatorio'`.

Agora experimenta:

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

Confirma também:

- Entra como `jose@padaria.pt` / `jose12345`, `2`, `3` e, na pasta, `C:\pasta\que\nao\existe`: aparece `A pasta C:\pasta\que\nao\existe não existe. O relatório não foi gravado.`
- Ainda como José, `2`, `3` e Enter: o relatório tem a campanha `Regresso às aulas`, `Terminada`, com o `Cartaz dos lanches`, e nenhuma campanha de outro cliente.
- Como Carla, `3` (Criativos) e `5` (Descarregar ficheiro) com um criativo que tenha ficheiro, se houver: a cópia continua a ir para a pasta `Downloads` com Enter, como antes.

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

**f)** No Trello, move o card da story C20 para **Ready**.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/6.4-exportar-relatorio
python ../ctesp-ADC/verificar.py 6.4
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/6.4-exportar-relatorio` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 6.4` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 6.4 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 6.4.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Ricardo que o pull request está junto e que já pode arrumar o computador (passo 27 da [página de Ricardo](ricardo.md)).

Diz também a Ricardo que já pode avançar ([página de Ricardo](ricardo.md), passos 28 a 36).

---

## Rever a release v0.6.0 e juntá-la ao main

Quem fez: Ricardo. Tu confirmas que a versão está pronta e juntas o ramo da release ao `main`.

### Passo 25 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 6.5 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Release v0.6.0**.

### Passo 26 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 27 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch release/v0.6.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch release/v0.6.0` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'release/v0.6.0'`.

Agora experimenta:

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

Confirma também:

- No separador **Files changed** do pull request aparecem só três ficheiros: `gestor_campanhas/__init__.py`, `CHANGELOG.md` e `README.md`.
- O `CHANGELOG.md` tem a secção `v0.6.0` por cima da `v0.5.0`.
- O README tem as secções novas `Comentários e notificações`, `Painel de marketeers` e `Relatório`.

### Passo 28 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

### Passo 29 — Confirma que o pull request vai para o main

Este é o único pull request da fase que não vai para o `develop`. Se for junto ao ramo errado, o `main` fica sem a versão e a tag fica no sítio errado.

Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.6.0`.

Se disser `into develop`, **não juntes**. Avisa Ricardo, que corrige o destino no botão **Edit**, à direita do título. Depois de corrigido, atualiza a página e confirma outra vez.

### Passo 30 — Junta o pull request ao main (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `main`.

**Deves ver** o símbolo roxo **Merged** no topo da página.

### Passo 31 — Arruma o teu computador

```bash
git switch develop
git branch -D release/v0.6.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git branch -D release/v0.6.0` | Apaga a cópia do ramo que criaste para experimentar. O `-D` maiúsculo é preciso porque o `develop` ainda não tem estes commits: chegam lá no pull request seguinte |

### Passo 32 — Avisa Ricardo

Diz a Ricardo que a release v0.6.0 já está no `main`. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 37 a 42.

---

## Juntar a release v0.6.0 ao develop

É o último pull request da fase.

### Passo 33 — Aprova o pull request que leva a release para o develop

Faz este passo quando Ricardo te avisar.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Juntar a release v0.6.0 ao develop**.

**b)** Confirma que na descrição está `Closes #` seguido do número da issue da release, e não `#N`. Se estiver `#N`, pede a Ricardo para editar a descrição antes de juntares.

**c)** No separador **Files changed**, confirma que as alterações são as da release: o número da versão, o `CHANGELOG.md` e o `README.md`.

**d)** Clica em **Review changes**, escolhe **Approve** e clica em **Submit review**.

### Passo 34 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** **Não cliques em Delete branch.** O ramo deste pull request é o `main`, que tem de continuar a existir.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da release fica fechada sozinha.

### Passo 35 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 6.5
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `python ../ctesp-ADC/verificar.py 6.5` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 6.5 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 6.5.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 36 — Avisa o grupo

Diz a Ricardo que a release está no `develop` e que já pode arrumar o computador (passo 42 da [página de Ricardo](ricardo.md)).

Esta era a última vez da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 37 — Atualiza a página "Guia de utilização" da wiki

A página passa a explicar os comentários, as notificações, o painel de marketeers e o relatório.

Faz este passo depois de a unidade 6.4 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/b494328/wiki/Guia-de-utilizacao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Guia de utilização** na lista de páginas, à direita, e depois em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar o Guia de utilização para a versão 0.6.0` e clica em **Save page**.

**Deves ver** a página a começar por `Como usar a aplicação, na versão 0.6.0.` e com as secções novas `Notificações`, `Comentários dos criativos`, `Painel de marketeers (Administrador)` e `Relatório das campanhas (Cliente)`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 6.2 — Notificações na aplicação e por email

- **`gestor_campanhas/bd.py`** ganha a tabela `notificacoes`. A coluna `sobre` diz de que tipo é o item (`campanha`, `pedido_budget` ou `criativo`) e `item_id` o número dele. `item_id` não é uma chave estrangeira, porque aponta para tabelas diferentes conforme o tipo; por isso, se o item for apagado, a notificação fica.
- **`gestor_campanhas/modelos.py`** ganha as constantes `SOBRE_...`, o dicionário `NOMES_SOBRE` e a classe `Notificacao`, cuja propriedade `nome_item` escreve o item como aparece na lista (`Criativo n.º 2`).
- **`gestor_campanhas/repositorios/notificacoes.py`** é novo: criar, ler, listar da mais recente para a mais antiga, contar as por ler e marcar como lidas (uma ou todas).
- **`gestor_campanhas/servicos/notificacoes.py`** é novo. `notificar` é o único sítio por onde passam as notificações: guarda-a e envia o mesmo texto por email, com uma última linha a dizer onde está o item no menu de quem o recebe (dicionário `ONDE`). `abrir` confirma que a notificação é do utilizador e marca-a como lida.
- **`gestor_campanhas/servicos/campanhas.py`**: `avisar_marketeer` passa a usar `notificar`, por isso o marketeer recebe a notificação e o email de sempre (com o mesmo assunto e o mesmo texto). A função passa a receber a ligação à base de dados, e as duas chamadas (`atribuir_marketeer` e `pedidos.aprovar`, em `servicos/pedidos.py`) foram atualizadas.
- **`gestor_campanhas/servicos/budget.py`**: `pedir` notifica o marketeer da campanha, e `aprovar` e `rejeitar` notificam o cliente, com o budget novo ou com o motivo. A notificação é a última coisa a acontecer: se uma regra recusar a operação, ninguém é notificado.
- **`gestor_campanhas/servicos/criativos.py`**: `avisar_cliente` notifica o cliente da campanha de um criativo, e é chamada em `criar`, `editar`, `eliminar`, `mudar_estado` e `anexar`. Num criativo eliminado, a notificação aponta para a campanha, porque o criativo já não existe.
- **`gestor_campanhas/servicos/comentarios.py`**: `comentar` notifica o marketeer e `responder` notifica quem escreveu o comentário.
- **`gestor_campanhas/cli/notificacoes.py`** é novo: a lista, "Abrir notificação" e "Marcar todas como lidas". `mostrar_item` procura o item com as funções de sempre (`obter_do_cliente`, `obter_do_marketeer`), por isso um utilizador não vê, por uma notificação antiga, um item a que já não tem acesso.
- **`gestor_campanhas/cli/perfis.py`**: o Marketeer e o Cliente ganham "Notificações", e o ciclo do menu chama `avisar_se_houver_por_ler` antes de cada menu.
- **`tests/test_notificacoes.py`** é novo: base de dados, `notificar`, quem é notificado de quê, e os ecrãs. `tests/test_bd.py` testa a tabela nova.
- **`docs/`**: o guia de utilização ganha a secção "Notificações", a arquitetura a tabela nova e a secção "Notificações", e a referência os três módulos novos.
