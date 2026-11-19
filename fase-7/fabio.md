# Fase 7 — Passo a passo de Fabio

Esta página tem tudo o que **Fabio** faz na Fase 7 (Fecho e entrega), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 10 | Fazer a unidade 7.1 — Testes dos fluxos completos e dados de demonstração finais | No início da fase |
| 11 a 18 | Rever a release v1.0.0 e juntá-la ao main | Quando Ricardo avisar |
| 19 a 22 | Juntar a release v1.0.0 ao develop | Quando Ricardo avisar |
| 23 a 24 | Cria a página "Testes" da wiki; Atualiza a página "Guia de utilização" da wiki | Depois de a unidade 7.2 estar junta ao develop |

---

## Fazer a unidade 7.1 — Testes dos fluxos completos e dados de demonstração finais

Acrescenta os testes dos fluxos completos, que seguem o caminho das pessoas na aplicação com os três perfis, de uma ponta à outra, e completa os dados de demonstração: os criativos ficam em estados diferentes, um deles com ficheiro, e há uma conversa já respondida, com as notificações correspondentes.

### Passo 1 — Confirma que podes começar

A fase anterior tem de estar fechada: todos os pull requests juntos e o `develop` do teu computador atualizado. Se for a primeira fase, tens de ter feito a [Preparação](../preparacao.md).

### Passo 2 — Cria a issue da unidade 7.1

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[7.1] Testes dos fluxos completos e dados de demonstração finais
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Confirmar com testes automáticos que as partes da aplicação funcionam juntas, com os três perfis, e deixar os dados de demonstração prontos para experimentar cada perfil logo à primeira.

## O que inclui

- [ ] Testes do fluxo da conta nova à primeira entrada, e da conta desativada e reativada
- [ ] Testes do fluxo do pedido de campanha ao criativo publicado, com o ficheiro, os comentários, as notificações e os emails, o painel de marketeers e o relatório
- [ ] Testes do criativo rejeitado e corrigido e do pedido de campanha rejeitado
- [ ] Testes do pedido de budget, aprovado e rejeitado, com o histórico e o resumo global
- [ ] Dados de demonstração finais: criativos em estados diferentes, um ficheiro anexado, um segundo comentário já respondido e as notificações de demonstração
- [ ] Testes dos dados de demonstração no seu conjunto
- [ ] Documentação dos testes e dos dados de demonstração
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 7 — Fecho e entrega`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 3 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/7.1-testes-dos-fluxos
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/7.1-testes-dos-fluxos` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/7.1-testes-dos-fluxos'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/7.1-testes-dos-fluxos' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/7.1-testes-dos-fluxos
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/7.1-testes-dos-fluxos
git switch -c feature/7.1-testes-dos-fluxos
```

  **Deves ver** `Deleted branch feature/7.1-testes-dos-fluxos (was ...)` e depois `Switched to a new branch 'feature/7.1-testes-dos-fluxos'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/7.1-testes-dos-fluxos` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 4 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 7.1 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 7.1. Eles estão na pasta `ctesp-ADC/fase-7/ficheiros/7.1/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.1 1
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_fluxos.py`.

```bash
git add -A
git commit -m "test(fluxos): da conta nova ao criativo publicado"
```

**Deves ver** uma linha a terminar em `1 file changed, 223 insertions(+)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.1 2
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_fluxos.py`.

```bash
git add -A
git commit -m "test(fluxos): do pedido de budget à decisão do Administrador"
```

**Deves ver** uma linha a terminar em `1 file changed, 72 insertions(+)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.1 3
```

**Deves ver** `Copiados 3 ficheiros`: `gestor_campanhas/dados_demo.py`, `gestor_campanhas/servicos/budget.py`, `tests/test_comentarios.py`.

```bash
git add -A
git commit -m "feat(demo): dados de demonstração finais, com criativos em vários estados e notificações"
```

**Deves ver** uma linha a terminar em `3 files changed, 101 insertions(+), 19 deletions(-)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.1 4
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_dados_demo.py`.

```bash
git add -A
git commit -m "test(demo): testar os dados de demonstração no seu conjunto"
```

**Deves ver** uma linha a terminar em `1 file changed, 148 insertions(+)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.1 5
```

**Deves ver** `Copiados 3 ficheiros`: `README.md`, `docs/testes.rst`, `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs: documentar os testes dos fluxos e os dados de demonstração finais"
```

**Deves ver** uma linha a terminar em `3 files changed, 133 insertions(+), 12 deletions(-)`.


### Passo 5 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 7.1
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 7.1` | `Tudo certo: o ramo 'feature/7.1-testes-dos-fluxos' está igual ao original no fim da unidade 7.1.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs: documentar os testes dos fluxos e os dados de demonstração finais
xxxxxxx test(demo): testar os dados de demonstração no seu conjunto
xxxxxxx feat(demo): dados de demonstração finais, com criativos em vários estados e notificações
xxxxxxx test(fluxos): do pedido de budget à decisão do Administrador
xxxxxxx test(fluxos): da conta nova ao criativo publicado
```

### Passo 6 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `878 passed`.

Corre só os testes dos fluxos completos, com o nome de cada um:

```bash
python -m pytest -v tests/test_fluxos.py
```

**Deves ver** sete linhas com `PASSED`, uma por fluxo (no fim de cada uma aparece também uma percentagem), e no fim `7 passed`:

```text
tests/test_fluxos.py::test_conta_nova_entra_e_troca_a_password PASSED
tests/test_fluxos.py::test_conta_desativada_deixa_de_entrar_e_volta_a_entrar_depois_de_reativada PASSED
tests/test_fluxos.py::test_do_pedido_de_campanha_ao_criativo_publicado PASSED
tests/test_fluxos.py::test_criativo_rejeitado_e_corrigido_volta_a_revisao_e_e_aprovado PASSED
tests/test_fluxos.py::test_pedido_de_campanha_rejeitado_nao_cria_campanha PASSED
tests/test_fluxos.py::test_pedido_de_budget_aprovado_muda_o_budget_e_fica_no_historico PASSED
tests/test_fluxos.py::test_pedido_de_budget_rejeitado_mantem_o_budget PASSED
```

Agora experimenta os dados de demonstração novos, numa pasta de dados à parte, para não mexeres nos teus dados. A pasta `dados-demo` fica ao lado das pastas `ADC-TrabGrupo` e `ctesp-ADC`, fora do repositório.

No **PowerShell** (o terminal do VS Code, no Windows, costuma ser este):

```powershell
$env:GESTOR_CAMPANHAS_DADOS = "../dados-demo"
python -m gestor_campanhas.dados_demo
```

No **Git Bash**:

```bash
export GESTOR_CAMPANHAS_DADOS=../dados-demo
python -m gestor_campanhas.dados_demo
```

**Deves ver**, entre outras, as linhas `Criativos criados: 4 (os restantes já existiam).` e `Comentários criados: 2 (os restantes já existiam).` Se aparecer `0` em todas as linhas, a pasta `dados-demo` já existia de outra vez: não faz mal, os dados são os mesmos.

No mesmo terminal, arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como cliente (`1`, `cliente@empresa.pt` e `cliente12345`).

**Deves ver**, por cima do menu, `Tem 3 notificações por ler, na opção "Notificações".`

Escolhe `3` (Criativos).

**Deves ver** os dois criativos da Carla, com o `Banner de Natal` em revisão, e por baixo da lista `Há 1 criativo à espera da sua aprovação.`:

```text
N.º  Nome             Campanha    Custo     Prazo       Público-alvo               Plataforma  Estado
---  ---------------  ----------  --------  ----------  -------------------------  ----------  -------------
1    Banner de Natal  Natal 2026  400,00 €  2026-11-25  Famílias da região de...   Facebook    Em revisão
2    Vídeo da montra  Natal 2026  900,00 €  2026-11-28  Jovens adultos, 18 a 3...  Instagram   Em preparação
```

Escolhe `2` (Ver criativo) e escreve `1`.

**Deves ver** o `Ficheiro:    banner-natal.svg` e, em `Comentários`, o comentário da Carla com a resposta do Miguel:

```text
Comentários
  N.º 2, de Carla Cliente, em 2026-11-21 10:00:
    O vermelho do fundo podia ser o da nossa marca.
    Resposta de Miguel Marketeer, em 2026-11-21 10:00:
      Combinado: na próxima versão o fundo fica com o vermelho da marca.
```

A data e a hora são as do momento em que correste o `dados_demo`. Prime Enter, escolhe `0` (Voltar), `0` (Terminar sessão) e `0` (Sair).

Por fim, volta à pasta de dados de sempre. No **PowerShell**:

```powershell
Remove-Item Env:GESTOR_CAMPANHAS_DADOS
```

No **Git Bash**:

```bash
unset GESTOR_CAMPANHAS_DADOS
```

Não aparece nada. A partir daqui, a aplicação volta a usar a pasta `dados` do repositório. A pasta `dados-demo` pode ficar onde está: não faz parte do repositório.

### Passo 7 — Envia o ramo para o GitHub

```bash
git push -u origin feature/7.1-testes-dos-fluxos
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/7.1-testes-dos-fluxos -> feature/7.1-testes-dos-fluxos`.

### Passo 8 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Tomas vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/7.1-testes-dos-fluxos?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/7.1-testes-dos-fluxos**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Testes dos fluxos completos e dados de demonstração finais
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue que apontaste:

```markdown
## O que muda

Testes dos fluxos completos e dados de demonstração finais.

- `tests/test_fluxos.py`: sete testes que seguem o caminho das pessoas na aplicação, com os três perfis, e confirmam o que cada um vê no fim (notificações, emails, painel, relatório, histórico do budget)
- Dados de demonstração: o `Banner de Natal` fica em revisão, com o ficheiro `exemplos/banner-natal.svg`; o `Cartaz dos lanches` fica publicado; a Carla tem um segundo comentário, já respondido pelo Miguel; e cada conta encontra as notificações do que lhe diz respeito. O que acontece aos criativos depois de criados passa pelas regras de negócio, como na aplicação
- `budget.avisar_marketeer`: o aviso ao marketeer de um pedido de budget novo passa a ser uma função própria, usada pelo pedido e pelos dados de demonstração
- `tests/test_dados_demo.py`: o resultado final dos dados de demonstração numa instalação nova
- Documentação: página de testes do Sphinx com todos os ficheiros de testes e os fluxos completos; dados de demonstração no README e na utilização

Closes #N

## Como testar

1. `python -m pytest` (878 testes)
2. `python -m pytest -v tests/test_fluxos.py` (7 testes)
3. Numa pasta de dados à parte (`GESTOR_CAMPANHAS_DADOS=../dados-demo`), `python -m gestor_campanhas.dados_demo` e entrar como `cliente@empresa.pt`: 3 notificações por ler e o `Banner de Natal` à espera de aprovação, com o comentário respondido
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Tomas (no GitHub, `GLKIIRA`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 7 — Fecho e entrega`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

### Passo 9 — Avisa Tomas

Diz a Tomas que o pull request da unidade 7.1 está pronto para rever. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 1 a 7.

### Passo 10 — Quando Tomas disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/7.1-testes-dos-fluxos
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/7.1-testes-dos-fluxos` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever a release v1.0.0 e juntá-la ao main

Quem fez: Ricardo. Tu confirmas que a versão está pronta e juntas o ramo da release ao `main`.

### Passo 11 — Abre o pull request de Ricardo

Faz este passo quando Ricardo te avisar que o pull request da unidade 7.3 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Release v1.0.0**.

### Passo 12 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 13 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Ricardo:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch release/v1.0.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Ricardo. Não mexe nos teus ficheiros |
| `git switch release/v1.0.0` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'release/v1.0.0'`.

Agora experimenta:

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `987 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v1.0.0`. Sai com `0`.

Confirma também:

- No separador **Files changed** do pull request aparecem só três ficheiros: `gestor_campanhas/__init__.py`, `CHANGELOG.md` e `README.md`.
- O `CHANGELOG.md` tem a secção `v1.0.0 — Fecho e entrega` por cima da `v0.6.0`.
- A tabela de versões do README tem a linha `v1.0.0`, a negrito.

### Passo 14 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Ricardo. Não avances para o passo seguinte.

### Passo 15 — Confirma que o pull request vai para o main

Este é o único pull request da fase que não vai para o `develop`. Se for junto ao ramo errado, o `main` fica sem a versão e a tag fica no sítio errado.

Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v1.0.0`.

Se disser `into develop`, **não juntes**. Avisa Ricardo, que corrige o destino no botão **Edit**, à direita do título. Depois de corrigido, atualiza a página e confirma outra vez.

### Passo 16 — Junta o pull request ao main (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `main`.

**Deves ver** o símbolo roxo **Merged** no topo da página.

### Passo 17 — Arruma o teu computador

```bash
git switch develop
git branch -D release/v1.0.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git branch -D release/v1.0.0` | Apaga a cópia do ramo que criaste para experimentar. O `-D` maiúsculo é preciso porque o `develop` ainda não tem estes commits: chegam lá no pull request seguinte |

### Passo 18 — Avisa Ricardo

Diz a Ricardo que a release v1.0.0 já está no `main`. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 17 a 22.

---

## Juntar a release v1.0.0 ao develop

É o último pull request da fase.

### Passo 19 — Aprova o pull request que leva a release para o develop

Faz este passo quando Ricardo te avisar.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Juntar a release v1.0.0 ao develop**.

**b)** Confirma que na descrição está `Closes #` seguido do número da issue da release, e não `#N`. Se estiver `#N`, pede a Ricardo para editar a descrição antes de juntares.

**c)** No separador **Files changed**, confirma que as alterações são as da release: o número da versão, o `CHANGELOG.md` e o `README.md`.

**d)** Clica em **Review changes**, escolhe **Approve** e clica em **Submit review**.

### Passo 20 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** **Não cliques em Delete branch.** O ramo deste pull request é o `main`, que tem de continuar a existir.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da release fica fechada sozinha.

### Passo 21 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 7.3
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `python ../ctesp-ADC/verificar.py 7.3` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 7.3 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 7.3.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 22 — Avisa o grupo

Diz a Ricardo que a release está no `develop` e que já pode arrumar o computador (passo 22 da [página de Ricardo](ricardo.md)).

Esta era a última vez da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 23 — Cria a página "Testes" da wiki

Uma página nova, que explica como a aplicação é testada: como correr os testes, os três tipos de testes, os fluxos completos e o que cada ficheiro de testes testa.

Faz este passo depois de a unidade 7.2 estar junta ao `develop`: a página fala dos testes da documentação, que chegam nessa unidade.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Testes.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New Page**, no canto superior direito.

**c)** Em **Title**, escreve exatamente:

```text
Testes
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Testes` e clica em **Save page**.

**Deves ver** a página a começar por `Como a aplicação é testada. Na versão 1.0.0 há 987 testes automáticos, todos a passar.` e com as secções `Três tipos de testes`, `Fluxos completos` e `Ficheiros de testes`.

### Passo 24 — Atualiza a página "Guia de utilização" da wiki

A página passa a falar da versão 1.0.0 e a descrever os dados de demonstração finais: o estado de cada criativo, os comentários, as notificações e por onde começar com cada conta.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Guia-de-utilizacao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Guia de utilização** na lista de páginas, à direita, e depois em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar o Guia de utilização para a versão 1.0.0` e clica em **Save page**.

**Deves ver** a página a começar por `Como usar a aplicação, na versão 1.0.0.` e, em `Contas de demonstração`, a tabela dos quatro criativos, com o `Banner de Natal` em revisão.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 7.1 — Testes dos fluxos completos e dados de demonstração finais

**Commit 1 — `tests/test_fluxos.py`, da conta nova ao criativo publicado.** Os outros ficheiros de testes experimentam cada regra sozinha; este segue o caminho das pessoas, com os três perfis, chamando as funções de `servicos` pela ordem em que os menus as chamam.

- A *fixture* `relogio_falso` põe o relógio da aplicação a 20 de novembro de 2026, às 10h00, em todos os testes do ficheiro. A função `passa_um_minuto` adianta-o um minuto entre passos: as notificações e os emails ficam ordenados pela hora, e sem isto os passos do mesmo minuto não teriam uma ordem certa.
- `assuntos` e `emails_para` leem os emails da caixa de saída (a *fixture* `emails`) e tiram-lhes o assunto e o destinatário, para comparar com o que se espera.
- `test_conta_nova_entra_e_troca_a_password`: o Administrador cria a conta com `gestao.criar`; a password inicial é lida do email com uma expressão regular (`re.search`); a pessoa entra com ela, troca-a, e a antiga deixa de servir (`pytest.raises(ErroAutenticacao)`).
- `test_do_pedido_de_campanha_ao_criativo_publicado` é o fluxo principal: o pedido da Carla, a aprovação do Administrador com o budget e o Miguel, o criativo com o ficheiro, a revisão, o comentário e a resposta, a aprovação e a publicação. No fim confirma as cinco notificações da Carla (da mais recente para a mais antiga), os assuntos dos emails de cada um, o painel (`painel.carga`) e a linha do relatório (`relatorios.linhas`).
- `test_criativo_rejeitado...` e `test_pedido_de_campanha_rejeitado...` seguem os caminhos de recusa: um criativo rejeitado não pode ser aprovado até ser corrigido e reenviado; um pedido rejeitado não cria campanha.

**Commit 2 — os fluxos do budget.** A *fixture* `campanha_com_budget` cria uma campanha do Miguel para a Carla com 1000 € de budget. `test_pedido_de_budget_aprovado...` cria um criativo de 1200 € (acima do budget), segue o pedido, o parecer e a aprovação, e confirma o budget novo, as duas linhas do histórico (a mais antiga primeiro), a campanha já fora da lista das que estão acima do budget e o resumo global. `test_pedido_de_budget_rejeitado...` confirma que sem parecer não se decide, que rejeitar não muda o budget, e que depois o cliente pode pedir outra vez.

**Commit 3 — `gestor_campanhas/dados_demo.py`, dados de demonstração finais.**

- Cada entrada de `CRIATIVOS` ganha o `estado` a que o criativo é levado depois de criado e, no `Banner de Natal`, o `ficheiro` a anexar (`exemplos/banner-natal.svg`, a partir da pasta do projeto, `config.PASTA_PROJETO`).
- `preparar_criativo` faz isso com as regras de negócio, pela ordem da aplicação: `anexar`, `mudar_estado` para revisão, `aprovar` (pelo cliente) e `mudar_estado` para publicado. Os `if estado in (...)` dizem até onde ir: o `Banner de Natal` fica em revisão, o `Cartaz dos lanches` vai até publicado. Por passar pelas regras, cada passo notifica o cliente e fica na atividade do marketeer, como se tivesse sido feito no menu.
- `criar_criativos` só chama `preparar_criativo` para os criativos que acabou de criar. Os que já existiam ficam como estão: por isso, nos teus dados de sempre, nada muda.
- `COMENTARIOS` ganha a `resposta`. `criar_comentarios` passa a usar `comentarios.comentar` e `comentarios.responder` (os serviços), que notificam o marketeer e o cliente.
- Em `servicos/budget.py`, o aviso ao marketeer de um pedido novo passou para a função `avisar_marketeer`, para os dados de demonstração o poderem usar sem repetir o texto. `pedir` chama-a, e faz o mesmo que fazia.
- Em `tests/test_comentarios.py`, os testes dos dados de demonstração foram atualizados para os dois comentários.

**Commit 4 — `tests/test_dados_demo.py`.** Confirma o resultado final, como fica numa instalação nova: os estados dos quatro criativos, o ficheiro copiado igual ao original, as notificações de cada conta (três da Carla, três do Miguel, nenhuma da Marta nem do Administrador), a atividade no painel, e que correr outra vez não cria nem notifica nada de novo.

**Commit 5 — documentação.** `docs/testes.rst` passa a ter a tabela de todos os ficheiros de testes, a secção "Fluxos completos" e as *fixtures* `contas` e `emails`; `docs/utilizacao.rst` e o README descrevem os dados de demonstração novos, com a tabela dos estados dos criativos.
