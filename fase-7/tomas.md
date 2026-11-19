# Fase 7 — Passo a passo de Tomas

Esta página tem tudo o que **Tomas** faz na Fase 7 (Fecho e entrega), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

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
| 1 a 7 | Rever e juntar a unidade 7.1 (de Fabio) | Quando Fabio avisar |
| 8 a 17 | Fazer a unidade 7.2 — Revisão dos docstrings, Sphinx e README final | A seguir ao teu passo anterior |
| 18 a 20 | Cria a página "Instalação e configuração" da wiki; Cria a página "Modelo de dados" da wiki; Atualiza a página "Arquitetura" da wiki | Depois de a unidade 7.2 estar junta ao develop |

---

## Rever e juntar a unidade 7.1 — Testes dos fluxos completos e dados de demonstração finais

Quem fez: Fabio. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Fabio

Faz este passo quando Fabio te avisar que o pull request da unidade 7.1 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Testes dos fluxos completos e dados de demonstração finais**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Fabio:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/7.1-testes-dos-fluxos
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Fabio. Não mexe nos teus ficheiros |
| `git switch feature/7.1-testes-dos-fluxos` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/7.1-testes-dos-fluxos'`.

Agora experimenta:

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

Confirma também:

- No separador **Files changed** aparecem oito ficheiros: os novos `tests/test_fluxos.py` e `tests/test_dados_demo.py`, e `gestor_campanhas/dados_demo.py`, `gestor_campanhas/servicos/budget.py`, `tests/test_comentarios.py`, `README.md`, `docs/testes.rst` e `docs/utilizacao.rst`.
- Em `gestor_campanhas/servicos/budget.py`, a função `pedir` continua a fazer o mesmo: só o aviso ao marketeer passou para a função nova `avisar_marketeer`.
- Na descrição está `Closes #` seguido do número da issue da unidade, e não `#N`.

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

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/7.1-testes-dos-fluxos
python ../ctesp-ADC/verificar.py 7.1
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/7.1-testes-dos-fluxos` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 7.1` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 7.1 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 7.1.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Fabio que o pull request está junto e que já pode arrumar o computador (passo 10 da [página de Fabio](fabio.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 7.2 — Revisão dos docstrings, Sphinx e README final

Fecha a documentação: completa os últimos docstrings e acrescenta um teste que confirma que nenhum fica a faltar, junta ao Sphinx a página do modelo de dados, revê a arquitetura e a configuração, e deixa o README na sua forma final.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Testes dos fluxos completos e dados de demonstração finais** (unidade 7.1) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Cria a issue da unidade 7.2

A issue é o registo, no GitHub, do trabalho que vai ser feito. Um pull request fecha-a sozinho mais à frente.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/issues e clica no botão verde **New issue**. Se aparecer uma lista de modelos, escolhe **Tarefa**.

**b)** No campo do título, apaga o que lá estiver e cola:

```text
[7.2] Revisão dos docstrings, Sphinx e README final
```

**c)** Na caixa grande de texto, apaga o que lá estiver e cola:

```markdown
## Objetivo

Deixar a documentação do código completa e confirmada por testes, e o README pronto para a entrega.

## O que inclui

- [ ] Revisão dos docstrings de todos os módulos, classes e funções
- [ ] Teste que confirma que o código tem docstrings e que a referência do Sphinx inclui todos os módulos
- [ ] Página "Modelo de dados" no Sphinx
- [ ] Páginas de arquitetura e de configuração revistas
- [ ] README final
- [ ] Documentação gerada sem avisos (`sphinx -W`)
```

**d)** Na coluna da direita, escolhe:

- **Assignees:** tu (clica em *assign yourself*)
- **Labels:** `tarefa`
- **Milestone:** `Fase 7 — Fecho e entrega`

**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).

**f)** Repara no número que aparece a seguir ao título, por exemplo `#40`. Aponta-o: vais precisar dele mais à frente.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/7.2-documentacao-final
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/7.2-documentacao-final` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/7.2-documentacao-final'`.

**Se em vez disso aparecer** `fatal: a branch named 'feature/7.2-documentacao-final' already exists`, já tinhas criado este ramo noutra altura (por exemplo, antes de a unidade anterior estar junta). Continuas no `develop`, já atualizado. Vê se o ramo antigo tem commits:

```bash
git log --oneline develop..feature/7.2-documentacao-final
```

- **Se não aparecer nenhuma linha**, o ramo antigo está vazio. Apaga-o e cria-o outra vez, a partir do `develop` atualizado:

```bash
git branch -D feature/7.2-documentacao-final
git switch -c feature/7.2-documentacao-final
```

  **Deves ver** `Deleted branch feature/7.2-documentacao-final (was ...)` e depois `Switched to a new branch 'feature/7.2-documentacao-final'`.
- **Se aparecerem linhas**, são commits que já gravaste. Não apagues nada: muda para o ramo com `git switch feature/7.2-documentacao-final` e continua no passo seguinte. Se o `copiar.py` responder com `ERRO`, avisa o grupo antes de mexer em mais alguma coisa.

### Passo 11 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 7.2 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 7.2. Eles estão na pasta `ctesp-ADC/fase-7/ficheiros/7.2/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.2 1
```

**Deves ver** `Copiados 2 ficheiros`: `gestor_campanhas/cli/comum.py`, `gestor_campanhas/servicos/sessoes.py`.

```bash
git add -A
git commit -m "docs(código): completar os docstrings que faltavam"
```

**Deves ver** uma linha a terminar em `2 files changed, 5 insertions(+), 1 deletion(-)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.2 2
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_documentacao.py`.

```bash
git add -A
git commit -m "test(docs): confirmar que o código e a referência ficam documentados"
```

**Deves ver** uma linha a terminar em `1 file changed, 96 insertions(+)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.2 3
```

**Deves ver** `Copiados 3 ficheiros`: `docs/arquitetura.rst`, `docs/index.rst`, `docs/modelo_dados.rst`.

```bash
git add -A
git commit -m "docs(sphinx): página do modelo de dados"
```

**Deves ver** uma linha a terminar em `3 files changed, 225 insertions(+), 75 deletions(-)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.2 4
```

**Deves ver** `Copiados 2 ficheiros`: `docs/arquitetura.rst`, `docs/instalacao.rst`.

```bash
git add -A
git commit -m "docs(sphinx): atualizar a arquitetura e a configuração"
```

**Deves ver** uma linha a terminar em `2 files changed, 49 insertions(+), 7 deletions(-)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 7.2 5
```

**Deves ver** `Copiados 1 ficheiro`: `README.md`.

```bash
git add -A
git commit -m "docs(readme): README final"
```

**Deves ver** uma linha a terminar em `1 file changed, 27 insertions(+), 10 deletions(-)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 7.2
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 7.2` | `Tudo certo: o ramo 'feature/7.2-documentacao-final' está igual ao original no fim da unidade 7.2.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(readme): README final
xxxxxxx docs(sphinx): atualizar a arquitetura e a configuração
xxxxxxx docs(sphinx): página do modelo de dados
xxxxxxx test(docs): confirmar que o código e a referência ficam documentados
xxxxxxx docs(código): completar os docstrings que faltavam
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `987 passed`. São mais 109 do que no fim da unidade 7.1: os testes da documentação, um por ficheiro de código.

Corre só os testes da documentação:

```bash
python -m pytest tests/test_documentacao.py
```

**Deves ver** `109 passed`.

Gera a documentação:

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Abre a documentação gerada: no Explorador de Ficheiros, entra na pasta `ADC-TrabGrupo`, depois em `docs`, `_build` e `html`, e faz duplo clique em `index.html`.

**Deves ver**, na lista "Conteúdo", a página nova **Modelo de dados**, entre **Arquitetura** e **Testes**. Abre-a: tem as secções `Relações entre as tabelas`, `Tabelas`, `Como os valores são guardados`, `O que acontece quando se apaga` e `Tabelas novas numa base de dados que já existe`.

Abre também a página **Arquitetura** e desce até `Base de dados`.

**Deves ver** só um parágrafo, com uma ligação para o **Modelo de dados**.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/7.2-documentacao-final
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/7.2-documentacao-final -> feature/7.2-documentacao-final`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Ricardo vai rever o teu trabalho.

**a)** Abre este link, que já traz o destino e o ramo escolhidos: https://github.com/Blive77/ADC-TrabGrupo/compare/develop...feature/7.2-documentacao-final?expand=1

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/7.2-documentacao-final**. Se a base for `main`, clica aí e escolhe `develop`.

**c)** No título, cola:

```text
Revisão dos docstrings, Sphinx e README final
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca `#N` pelo número da issue que apontaste:

```markdown
## O que muda

Revisão final da documentação.

- Os dois docstrings que faltavam: a função interna `formatar` de `cli/comum.py` e o resultado de `SessaoAtiva.expirou`
- `tests/test_documentacao.py`: todos os módulos, classes e funções têm docstring, as funções públicas descrevem os parâmetros (`:param:`) e o resultado (`:return:`), e a referência do Sphinx inclui todos os módulos
- Página nova "Modelo de dados" (`docs/modelo_dados.rst`): relações entre as tabelas, todas as referências e o que acontece quando se apaga, como cada valor é guardado. A secção das tabelas sai da arquitetura para esta página
- Arquitetura com os módulos que faltavam na estrutura de pastas; configuração com as subpastas da pasta de dados e as definições guardadas na base de dados
- README final: estado do projeto, definições, os três tipos de testes, estrutura completa e documentação

Closes #N

## Como testar

1. `python -m pytest` (987 testes)
2. `python -m pytest tests/test_documentacao.py` (109 testes)
3. `python -m sphinx -W -b html docs docs/_build/html` e abrir `docs/_build/html/modelo_dados.html`
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Ricardo (no GitHub, `CabritaXgamer`)
- **Assignees:** tu
- **Labels:** `tarefa`
- **Milestone:** `Fase 7 — Fecho e entrega`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

### Passo 16 — Avisa Ricardo

Diz a Ricardo que o pull request da unidade 7.2 está pronto para rever. A partir daqui é a vez de Ricardo: [página de Ricardo](ricardo.md), passos 1 a 7.

### Passo 17 — Quando Ricardo disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/7.2-documentacao-final
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/7.2-documentacao-final` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Outras tarefas desta fase

### Passo 18 — Cria a página "Instalação e configuração" da wiki

Uma página nova, com o que é preciso para instalar e arrancar a aplicação, os dados de demonstração, a pasta de dados, as definições e o ambiente de desenvolvimento.

Faz os teus passos da wiki depois de a unidade 7.2 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Instalacao-e-configuracao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New Page**, no canto superior direito.

**c)** Em **Title**, escreve exatamente (com os acentos):

```text
Instalação e configuração
```

As outras páginas ligam para esta pelo título. Se o título ficar diferente, essas ligações não abrem.

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Instalação e configuração` e clica em **Save page**.

**Deves ver** a página com as secções `Requisitos`, `Obter o código e arrancar`, `Dados de demonstração`, `Configuração` e `Ambiente de desenvolvimento`. As ligações para `Modelo de dados` e `Testes` só abrem depois de essas páginas serem criadas.

### Passo 19 — Cria a página "Modelo de dados" da wiki

Uma página nova, com as tabelas da base de dados, as relações entre elas, os estados, a forma como cada valor é guardado e o que acontece quando se apaga.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Modelo-de-dados.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **New Page**, no canto superior direito.

**c)** Em **Title**, escreve exatamente:

```text
Modelo de dados
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Modelo de dados` e clica em **Save page**.

**Deves ver** a página com as secções `Relações`, `Tabelas`, `Estados`, `Como os valores são guardados` e `O que acontece quando se apaga`.

### Passo 20 — Atualiza a página "Arquitetura" da wiki

A página passa a falar da versão 1.0.0, ganha ligações para as páginas "Modelo de dados" e "Testes", e uma secção nova, `Dados de demonstração`.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Arquitetura.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki/Arquitetura e clica em **Edit**, no canto superior direito.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a Arquitetura para a versão 1.0.0` e clica em **Save page**.

**Deves ver** a página a começar por `Como o código está organizado, na versão 1.0.0.` e, no fim, a secção `Dados de demonstração`.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 7.2 — Revisão dos docstrings, Sphinx e README final

**Commit 1 — os docstrings que faltavam.** Uma revisão de todos os ficheiros encontrou só dois: a função `formatar`, definida dentro de `comum.mostrar_tabela` para juntar as células de uma linha, não tinha docstring; e o método `expirou` de `SessaoAtiva` não dizia o que devolve (`:return:`). Nenhuma linha de código mudou.

**Commit 2 — `tests/test_documentacao.py`.** Em vez de se confiar numa revisão à mão, a documentação passa a ser confirmada pelos testes, como o resto do código.

- O módulo `ast` da biblioteca padrão lê um ficheiro Python e devolve a sua árvore sintática: os módulos, as classes e as funções, com os seus docstrings, sem executar o código. `ast.get_docstring` devolve o docstring de cada um, ou `None`.
- `FICHEIROS` são todos os `.py` de `gestor_campanhas`, e `nome_do_modulo` transforma o caminho no nome do módulo (`gestor_campanhas/cli/comum.py` passa a `gestor_campanhas.cli.comum`).
- `@pytest.mark.parametrize` corre o mesmo teste uma vez por ficheiro, cada uma com o seu nome. É por isso que os testes passam de 878 para 987: dois testes por cada um dos 54 ficheiros, mais o da referência.
- `test_modulo_classes_e_funcoes_tem_docstring` confirma que o módulo, as classes e todas as funções (mesmo as internas) têm docstring.
- `test_funcoes_publicas_descrevem_os_parametros_e_o_resultado` olha só para as funções públicas (sem `_` no início) e para os métodos das classes, e confirma que cada parâmetro tem `:param nome:` e que, se a função devolve alguma coisa, há `:return:`. As propriedades (`@property`) ficam de fora: descrevem-se com uma frase.
- `test_referencia_inclui_todos_os_modulos` lê `docs/referencia.rst` e confirma que há um `.. automodule::` por cada módulo, nem mais nem menos. Quem acrescentar um módulo e se esquecer da referência vê este teste falhar.

**Commit 3 — `docs/modelo_dados.rst`.** O plano da documentação pedia uma página do modelo de dados. Tem um esquema das relações principais ("um para muitos"), a tabela de todas as referências entre tabelas com o que acontece quando a linha referida é apagada (`ON DELETE CASCADE`, `ON DELETE SET NULL`, ou a recusa do SQLite), a tabela das tabelas (que veio da arquitetura), a forma como se guardam o dinheiro, as datas, os sim/não e os estados, e porque é que as tabelas foram criadas logo com todas as colunas. Em `docs/index.rst`, a página entra na lista entre a arquitetura e os testes; em `docs/arquitetura.rst`, a secção "Base de dados" fica só com a ligação.

**Commit 4 — arquitetura e configuração.** Na estrutura de pastas de `docs/arquitetura.rst` faltavam `cli/notificacoes.py` e `cli/painel.py`, e as descrições de `config.py`, `modelos.py` e `dados_demo.py` estavam desatualizadas. Em `docs/instalacao.rst`, a configuração passa a dizer o que há dentro da pasta de dados e a explicar as definições guardadas na tabela `configuracoes`, com os valores por omissão de `config.py`.

**Commit 5 — README final.** O estado do projeto diz que as 57 user stories estão feitas (19, 18 e 20 por perfil), a configuração fala das duas definições guardadas na base de dados, a secção "Testes e documentação" explica os três tipos de testes e o `-W` do Sphinx, a estrutura do projeto lista todos os módulos, e a secção da documentação diz que páginas há no Sphinx e na wiki.
