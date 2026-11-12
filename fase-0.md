# Fase 0 — Arranque: guia de replicação

Este guia diz, passo a passo, como levar a Fase 0 do Repo A (trabalho) para o Repo B (oficial).

| | |
|---|---|
| Entregue em | 12 de novembro de 2026 |
| Repo A | https://github.com/cabritaXgamer/ctesp-ADC, ramo `develop`, commit `49397f6` |
| Conteúdo esperado no fim | `e90209e7d8085e3d7d2be163df305ec58f9cdf82` (ver "Fecho da fase") |
| Estado | 20 testes a passar, documentação gerada sem avisos, aplicação a arrancar |
| Release | A Fase 0 não tem release. A primeira é a `v0.1.0`, no fim da Fase 1 |

## O que a Fase 0 entrega

A base do projeto, ainda sem user stories: a aplicação arranca, cria a base de dados e mostra o menu inicial; há testes automáticos, documentação Sphinx e as regras de trabalho escritas.

```
python -m gestor_campanhas

============================================================
Gestor de Campanhas v0.0.0
============================================================
  1. Entrar
  0. Sair
Opção:
```

## Ordem de trabalho

As unidades dependem umas das outras, por isso são replicadas **por esta ordem**. Só se começa uma unidade depois de o pull request da anterior estar fundido.

| Ordem | O quê | Quem faz | Quem revê |
|---|---|---|---|
| 1 | Preparação individual | Os três | — |
| 2 | Passo 0: preparar o Repo B | Quem criou o Repo B | — |
| 3 | Unidade 0.1 — Estrutura do pacote | Fabio | Tomas |
| 4 | Unidade 0.2 — Base de dados e menu inicial | Tomas | Ricardo |
| 5 | Unidade 0.3 — Testes e integração contínua | Ricardo | Fabio |
| 6 | Unidade 0.4 — Documentação base | Fabio | Tomas |
| 7 | Issues das user stories | Os três, um perfil cada | — |
| 8 | Wiki | Ricardo e Tomas | — |
| 9 | Fecho da fase | Qualquer um | — |

As issues das user stories (passo 7) e a wiki (passo 8) não dependem do código. Podem ser feitas enquanto se espera por uma revisão.

## 1. Preparação individual (cada membro, uma só vez)

### Identidade Git

Para o GitHub associar os commits à conta de cada um, o email configurado no Git tem de ser um dos emails dessa conta (GitHub → Settings → Emails).

```bash
git config --global user.name "O Teu Nome"
```

```bash
git config --global user.email "o-email-da-tua-conta-github"
```

### Clonar o Repo B e ligar o Repo A

O Fabio deve clonar o Repo B numa pasta diferente de `ADC-TrabalhoGrupo`, que é a cópia do Repo A.

```bash
git clone <URL-do-Repo-B>
```

Dentro da pasta clonada:

```bash
git remote add trabalho https://github.com/cabritaXgamer/ctesp-ADC
```

```bash
git fetch trabalho
```

O remote `trabalho` é uma configuração local de cada clone. Serve só para ir buscar commits ao Repo A.

## 2. Passo 0 — Preparar o Repo B

Feito uma vez, por quem criou o Repo B.

### 2.1 Commit inicial

O ponto de partida tem de ser igual ao do Repo A: um `main` só com o `README.md` inicial.

**Se o Repo B estiver vazio (sem commits):**

```bash
git checkout 77fe5f5 -- README.md
git commit -m "chore: commit inicial"
git branch -M main
git push -u origin main
```

**Se o Repo B já tiver um README criado pelo GitHub:**

```bash
git switch main
git pull
git checkout 77fe5f5 -- README.md
git commit -m "docs: definir o README inicial"
git push
```

Se o Repo B tiver outros ficheiros além do `README.md`, avisem-me antes de continuar: o conteúdo final deixaria de coincidir com o do Repo A.

### 2.2 Ramo develop

```bash
git switch -c develop
git push -u origin develop
```

### 2.3 Definições no GitHub

Em **Settings** do Repo B:

1. **Collaborators:** adicionar os outros dois membros com o papel *Write*.
2. **General → Default branch:** mudar para `develop`. Assim, os pull requests ficam logo com o destino certo.
3. **General → Pull Requests:** deixar ativo só *Allow merge commits*. Desligar *squash merging* e *rebase merging*, porque juntam ou reescrevem os commits e o histórico deixaria de mostrar o trabalho de cada um.
4. **General → Features:** ativar *Wikis* e *Issues*.
5. **Branches → Add branch ruleset** (ou *Add rule*), uma regra para `main` e outra para `develop`:
   - *Require a pull request before merging*
   - *Required approvals: 1*

   Se o repositório for privado numa conta gratuita, o GitHub não deixa ativar estas regras. Nesse caso cumprem-se por disciplina: nunca fazer commit direto em `main` nem em `develop`.

### 2.4 Labels

Em **Issues → Labels**. A label `bug` já existe.

| Nome | Cor | Descrição |
|---|---|---|
| `user story` | `#1D76DB` | Funcionalidade descrita do ponto de vista de um utilizador |
| `tarefa` | `#FBCA04` | Trabalho técnico que não corresponde a uma user story |
| `Administrador` | `#8E44AD` | User story do perfil Administrador |
| `Marketeer` | `#2ECC71` | User story do perfil Marketeer |
| `Cliente` | `#3498DB` | User story do perfil Cliente |

### 2.5 Milestones

Em **Issues → Milestones**.

| Título | Data limite |
|---|---|
| `Fase 0 — Arranque` | 13/11/2026 |
| `Fase 1 — Autenticação e sessões` | 14/11/2026 |
| `Fase 2 — Clientes e marketeers` | 15/11/2026 |
| `Fase 3 — Campanhas e pedidos` | 16/11/2026 |
| `Fase 4 — Criativos` | 18/11/2026 |
| `Fase 5 — Budget` | 19/11/2026 |
| `Fase 6 — Comentários, notificações e relatórios` | 20/11/2026 |
| `Fase 7 — Fecho e entrega` | 21/11/2026 |

Os títulos têm de ficar exatamente assim, porque as issues referem-nos.

---

## 3. Unidade 0.1 — Estrutura do pacote

**Quem faz:** Fabio · **Quem revê:** Tomas · **Ramo:** `feature/0.1-estrutura-pacote`

### Issue

- **Título:** `[0.1] Estrutura do pacote Python`
- **Labels:** `tarefa` · **Milestone:** `Fase 0 — Arranque` · **Assignee:** Fabio

```markdown
## Objetivo

Criar a estrutura base do projeto, para que a aplicação possa ser arrancada com `python -m gestor_campanhas`.

## O que inclui

- [ ] `.gitignore` e `.gitattributes`
- [ ] Pacote `gestor_campanhas` com a versão e o ponto de entrada
- [ ] Módulo `config` com os caminhos da pasta de dados e da base de dados
- [ ] `pyproject.toml` com a descrição do projeto
```

### Commits

| # | SHA | Mensagem | Ficheiros |
|---|---|---|---|
| 1 | `32635df` | `chore: adicionar .gitignore e .gitattributes` | `.gitattributes`<br>`.gitignore` |
| 2 | `39511bf` | `feat(nucleo): criar pacote gestor_campanhas com ponto de entrada` | `gestor_campanhas/__init__.py`<br>`gestor_campanhas/__main__.py` |
| 3 | `30fb481` | `feat(config): adicionar configuração dos caminhos de dados` | `gestor_campanhas/config.py` |
| 4 | `eb954a1` | `chore: adicionar pyproject.toml` | `pyproject.toml` |

### Comandos

```bash
git fetch trabalho
git switch develop
git pull
git switch -c feature/0.1-estrutura-pacote

git cherry-pick -n 32635df
git commit -m "chore: adicionar .gitignore e .gitattributes"

git cherry-pick -n 39511bf
git commit -m "feat(nucleo): criar pacote gestor_campanhas com ponto de entrada"

git cherry-pick -n 30fb481
git commit -m "feat(config): adicionar configuração dos caminhos de dados"

git cherry-pick -n eb954a1
git commit -m "chore: adicionar pyproject.toml"

git push -u origin feature/0.1-estrutura-pacote
```

### Pull request

- **Título:** `Estrutura do pacote Python`
- **Destino:** `develop`

```markdown
## O que muda

Cria a estrutura base do projeto: o pacote `gestor_campanhas`, o ponto de entrada, a configuração dos caminhos de dados e o `pyproject.toml`. Acrescenta também o `.gitignore` e o `.gitattributes`.

Closes #<número da issue 0.1>

## Como testar

1. `python -m gestor_campanhas`
2. Deve aparecer `Gestor de Campanhas v0.0.0` e o programa termina.
```

### O que o revisor verifica

- `python -m gestor_campanhas` mostra a versão e termina sem erro.
- O `.gitignore` cobre `dados/`, `.venv/`, `__pycache__/` e `docs/_build/`.
- Todas as funções de `config.py` têm docstring.

### Para perceber este código

- **`.gitattributes`** obriga a que os ficheiros fiquem com fins de linha LF em qualquer sistema. Sem isto, o mesmo ficheiro podia ficar diferente em Windows e em Linux. O `make.bat` é a exceção: os scripts do Windows precisam de CRLF.
- **`__init__.py`** é o que faz de `gestor_campanhas` um pacote Python. Guarda a versão em `__version__`, o único sítio onde ela está escrita.
- **`__main__.py`** é o ficheiro que o Python executa com `python -m gestor_campanhas`. A função `main()` devolve o código de saída (`0` quer dizer "sem erros") e `raise SystemExit(main())` entrega esse código ao sistema operativo.
- **`config.py`** calcula a pasta do projeto a partir da localização do próprio ficheiro (`Path(__file__).resolve().parent.parent`). `pasta_dados()` é uma função, e não uma constante, para que a variável de ambiente `GESTOR_CAMPANHAS_DADOS` seja lida no momento em que é precisa. É isso que permite aos testes apontar para uma pasta temporária.
- **`pyproject.toml`** descreve o projeto. `dynamic = ["version"]` diz que a versão é lida de `gestor_campanhas.__version__`. `dependencies = []` deixa explícito que a aplicação não usa bibliotecas externas.

### Depois do merge

```bash
git switch develop
git pull
git diff --stat 5b1e556 develop
```

O último comando não deve mostrar nada. Se mostrar ficheiros, o Repo B ficou diferente do Repo A: parem e avisem-me.

---

## 4. Unidade 0.2 — Base de dados e menu inicial

**Quem faz:** Tomas · **Quem revê:** Ricardo · **Ramo:** `feature/0.2-base-dados-menu` · **Depende de:** 0.1 fundida

### Issue

- **Título:** `[0.2] Base de dados e menu inicial`
- **Labels:** `tarefa` · **Milestone:** `Fase 0 — Arranque` · **Assignee:** Tomas

```markdown
## Objetivo

Ter a base de dados SQLite criada no arranque e um menu inicial a funcionar, como base para os menus de cada perfil.

## O que inclui

- [ ] Módulo `bd` com a ligação SQLite e a criação das tabelas
- [ ] Funções comuns dos menus: títulos, leitura de texto, confirmações, escolha de opções
- [ ] Menu inicial com as opções Entrar e Sair
- [ ] Ponto de entrada ligado à base de dados e ao menu
- [ ] Acentos corretos em qualquer terminal
```

### Commits

| # | SHA | Mensagem | Ficheiros |
|---|---|---|---|
| 1 | `af2b298` | `feat(bd): adicionar ligação SQLite e criação de tabelas` | `gestor_campanhas/bd.py` |
| 2 | `95790ad` | `feat(cli): adicionar funções comuns dos menus` | `gestor_campanhas/cli/__init__.py`<br>`gestor_campanhas/cli/comum.py` |
| 3 | `006bc94` | `feat(cli): adicionar menu inicial` | `gestor_campanhas/cli/principal.py` |
| 4 | `050fff7` | `feat(nucleo): ligar o ponto de entrada à base de dados e ao menu inicial` | `gestor_campanhas/__main__.py` |
| 5 | `eea2b74` | `fix(cli): ler e escrever acentos em UTF-8 em qualquer terminal` | `gestor_campanhas/__main__.py`<br>`gestor_campanhas/cli/comum.py` |

### Comandos

```bash
git fetch trabalho
git switch develop
git pull
git switch -c feature/0.2-base-dados-menu

git cherry-pick -n af2b298
git commit -m "feat(bd): adicionar ligação SQLite e criação de tabelas"

git cherry-pick -n 95790ad
git commit -m "feat(cli): adicionar funções comuns dos menus"

git cherry-pick -n 006bc94
git commit -m "feat(cli): adicionar menu inicial"

git cherry-pick -n 050fff7
git commit -m "feat(nucleo): ligar o ponto de entrada à base de dados e ao menu inicial"

git cherry-pick -n eea2b74
git commit -m "fix(cli): ler e escrever acentos em UTF-8 em qualquer terminal"

git push -u origin feature/0.2-base-dados-menu
```

### Pull request

- **Título:** `Base de dados e menu inicial`
- **Destino:** `develop`

```markdown
## O que muda

A aplicação passa a criar a base de dados SQLite no arranque e a mostrar um menu inicial. As funções comuns dos menus ficam em `cli/comum.py`, para serem reutilizadas pelos menus de cada perfil.

Inclui uma correção para os acentos aparecerem bem quando a aplicação corre no Git Bash.

Closes #<número da issue 0.2>

## Como testar

1. `python -m gestor_campanhas`
2. Escolher `1`: aparece o aviso de que a autenticação ainda não está disponível.
3. Escrever uma opção que não existe: aparece `Opção inválida.`
4. Escolher `0`: aparece `Até breve!` e o programa termina.
5. Confirmar que foi criada a pasta `dados` com o ficheiro `app.db`.
```

### O que o revisor verifica

- Os cinco passos de "Como testar".
- Ctrl+C a meio do menu termina com `A sair...`, sem mostrar um erro.
- `git status` não mostra a pasta `dados/` (está no `.gitignore`).

### Para perceber este código

- **`bd.ligar()`** abre a ligação e configura duas coisas. `row_factory = sqlite3.Row` permite ler as colunas pelo nome (`linha["chave"]`) em vez da posição. `PRAGMA foreign_keys = ON` liga a verificação das chaves estrangeiras, que o SQLite traz desligada. O SQLite cria o ficheiro mas não a pasta, por isso a função cria a pasta primeiro.
- **`bd.ESQUEMA`** tem as instruções `CREATE TABLE IF NOT EXISTS`. Por causa do `IF NOT EXISTS`, podem ser executadas em todos os arranques sem apagar dados. Para já existe só a tabela `configuracoes`; cada fase acrescenta as suas.
- **`bd.EM_MEMORIA`** (`":memory:"`) é um caminho especial do SQLite: a base de dados vive na memória e desaparece quando a ligação fecha. É usada nos testes.
- **`cli/comum.py`** junta o que todos os menus precisam. `escolher_opcao` recebe uma lista de pares `(chave, descrição)` e repete a pergunta até a resposta ser uma das chaves. `confirmar` e `ler_texto` seguem a mesma ideia: um ciclo `while True` que só termina com uma resposta válida.
- **`cli/principal.py`** é o ciclo do menu inicial. Sai do ciclo com `return` quando a opção é `0`.
- **`__main__.py`** usa `try / except / finally`: o `finally` garante que a ligação é fechada mesmo que o utilizador interrompa com Ctrl+C (`KeyboardInterrupt`) ou que a entrada acabe (`EOFError`).
- **O último commit é uma correção.** No Git Bash os acentos apareciam trocados, porque o Python usava a codificação antiga do Windows. `configurar_terminal()` força o UTF-8 no teclado, na saída e nos erros.

### Depois do merge

```bash
git switch develop
git pull
git diff --stat 7234d9a develop
```

---

## 5. Unidade 0.3 — Testes e integração contínua

**Quem faz:** Ricardo · **Quem revê:** Fabio · **Ramo:** `feature/0.3-testes-ci` · **Depende de:** 0.2 fundida

### Issue

- **Título:** `[0.3] Testes automáticos e integração contínua`
- **Labels:** `tarefa` · **Milestone:** `Fase 0 — Arranque` · **Assignee:** Ricardo

```markdown
## Objetivo

Ter testes automáticos a correr localmente e em cada pull request, para apanhar erros antes do merge.

## O que inclui

- [ ] Configuração do pytest e `requirements-dev.txt`
- [ ] Fixtures comuns: base de dados em memória e teclado simulado
- [ ] Testes da base de dados e dos caminhos de dados
- [ ] Testes dos menus e do ponto de entrada
- [ ] Workflow do GitHub Actions que corre os testes
```

### Commits

| # | SHA | Mensagem | Ficheiros |
|---|---|---|---|
| 1 | `14b647b` | `test: configurar o pytest e as fixtures comuns` | `pyproject.toml`<br>`requirements-dev.txt`<br>`tests/conftest.py` |
| 2 | `f87a6b4` | `test(bd): testar a ligação, as tabelas e os caminhos de dados` | `tests/test_bd.py` |
| 3 | `f72785a` | `test(cli): testar os menus e o ponto de entrada` | `tests/test_cli.py` |
| 4 | `9af8886` | `ci: correr os testes no GitHub Actions` | `.github/workflows/testes.yml` |

### Comandos

Antes de começar, instalar o pytest (num ambiente virtual, de preferência):

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install pytest
```

```bash
git fetch trabalho
git switch develop
git pull
git switch -c feature/0.3-testes-ci

git cherry-pick -n 14b647b
git commit -m "test: configurar o pytest e as fixtures comuns"

git cherry-pick -n f87a6b4
git commit -m "test(bd): testar a ligação, as tabelas e os caminhos de dados"

git cherry-pick -n f72785a
git commit -m "test(cli): testar os menus e o ponto de entrada"

git cherry-pick -n 9af8886
git commit -m "ci: correr os testes no GitHub Actions"

git push -u origin feature/0.3-testes-ci
```

### Pull request

- **Título:** `Testes automáticos e integração contínua`
- **Destino:** `develop`

```markdown
## O que muda

Acrescenta 20 testes com o pytest, que cobrem a base de dados, os caminhos de dados, as funções comuns dos menus, o menu inicial e o ponto de entrada. Um workflow do GitHub Actions passa a correr os testes em cada push e em cada pull request para `main` e `develop`.

Closes #<número da issue 0.3>

## Como testar

1. `python -m pip install -r requirements-dev.txt`
2. `python -m pytest`
3. Devem passar os 20 testes.
```

### O que o revisor verifica

- `python -m pytest` termina com `20 passed`.
- No pull request aparece a verificação **Testes**, a verde, para o Python 3.10 e 3.13. É a primeira vez que o workflow corre.
- Os nomes dos testes dizem o que está a ser testado.

Depois deste merge, pode acrescentar-se a verificação **Testes** às regras dos ramos (*Require status checks to pass*).

### Para perceber este código

- **`pyproject.toml`** ganha a secção `[tool.pytest.ini_options]`. `testpaths` diz onde estão os testes. `pythonpath = ["."]` deixa os testes importar `gestor_campanhas` sem instalar o pacote.
- **`tests/conftest.py`** define as *fixtures*, que são peças que o pytest prepara e entrega aos testes que as pedem pelo nome do parâmetro.
  - `ligacao` cria uma base de dados em memória com as tabelas. O `yield` entrega-a ao teste; o que vem depois do `yield` corre no fim, para a fechar.
  - `teclado` substitui a função `input` por outra que devolve respostas preparadas. Quando as respostas acabam, lança `EOFError`, tal como o `input` verdadeiro quando a entrada termina.
- **Fixtures do próprio pytest** usadas nos testes: `monkeypatch` (altera variáveis de ambiente e funções só durante o teste), `tmp_path` (pasta temporária), `capsys` (lê o que foi escrito no ecrã).
- **Estrutura de cada teste:** preparar, executar, verificar com `assert`. `pytest.raises(sqlite3.IntegrityError)` verifica que uma instrução falha como esperado.
- **`.github/workflows/testes.yml`**: `on` define quando corre; `matrix` repete o trabalho para duas versões do Python; os `steps` obtêm o código, instalam o Python, instalam o pytest e correm os testes.

### Depois do merge

```bash
git switch develop
git pull
git diff --stat 200a279 develop
```

---

## 6. Unidade 0.4 — Documentação base

**Quem faz:** Fabio · **Quem revê:** Tomas · **Ramo:** `feature/0.4-documentacao-base` · **Depende de:** 0.3 fundida

### Issue

- **Título:** `[0.4] Documentação base`
- **Labels:** `tarefa` · **Milestone:** `Fase 0 — Arranque` · **Assignee:** Fabio

```markdown
## Objetivo

Ter a documentação do código gerada com o Sphinx e as regras de trabalho do repositório escritas.

## O que inclui

- [ ] Configuração do Sphinx (`docs/conf.py`)
- [ ] Páginas de instalação, arquitetura e testes
- [ ] Referência do código gerada a partir dos docstrings
- [ ] Workflow do GitHub Actions que gera a documentação
- [ ] README completo
- [ ] Guia de contribuição (`CONTRIBUTING.md`)
- [ ] Modelos de issue e de pull request
```

### Commits

| # | SHA | Mensagem | Ficheiros |
|---|---|---|---|
| 1 | `67b6bb0` | `docs: configurar o Sphinx e documentar a instalação` | `docs/Makefile`<br>`docs/conf.py`<br>`docs/index.rst`<br>`docs/instalacao.rst`<br>`docs/make.bat`<br>`requirements-dev.txt` |
| 2 | `b5dd4ad` | `docs: descrever a arquitetura e os testes` | `docs/arquitetura.rst`<br>`docs/index.rst`<br>`docs/testes.rst` |
| 3 | `08e1cc0` | `docs: gerar a referência do código a partir dos docstrings` | `docs/index.rst`<br>`docs/referencia.rst` |
| 4 | `6d2e427` | `ci: gerar a documentação no GitHub Actions` | `.github/workflows/docs.yml` |
| 5 | `64458cc` | `docs: escrever o README` | `README.md` |
| 6 | `ad311fd` | `docs: adicionar o guia de contribuição` | `CONTRIBUTING.md` |
| 7 | `50f15da` | `chore: adicionar modelos de issue e de pull request` | `.github/ISSUE_TEMPLATE/bug.md`<br>`.github/ISSUE_TEMPLATE/tarefa.md`<br>`.github/ISSUE_TEMPLATE/user_story.md`<br>`.github/pull_request_template.md` |

### Comandos

Antes de começar, instalar o Sphinx no ambiente virtual:

```bash
python -m pip install sphinx
```

```bash
git fetch trabalho
git switch develop
git pull
git switch -c feature/0.4-documentacao-base

git cherry-pick -n 67b6bb0
git commit -m "docs: configurar o Sphinx e documentar a instalação"

git cherry-pick -n b5dd4ad
git commit -m "docs: descrever a arquitetura e os testes"

git cherry-pick -n 08e1cc0
git commit -m "docs: gerar a referência do código a partir dos docstrings"

git cherry-pick -n 6d2e427
git commit -m "ci: gerar a documentação no GitHub Actions"

git cherry-pick -n 64458cc
git commit -m "docs: escrever o README"

git cherry-pick -n ad311fd
git commit -m "docs: adicionar o guia de contribuição"

git cherry-pick -n 50f15da
git commit -m "chore: adicionar modelos de issue e de pull request"

git push -u origin feature/0.4-documentacao-base
```

### Pull request

- **Título:** `Documentação base`
- **Destino:** `develop`

```markdown
## O que muda

Configura o Sphinx e escreve as primeiras páginas da documentação: instalação, arquitetura, testes e a referência do código, gerada a partir dos docstrings. Um workflow do GitHub Actions gera a documentação em cada pull request e falha se houver avisos.

Acrescenta também o README completo, o guia de contribuição e os modelos de issue e de pull request.

Closes #<número da issue 0.4>

## Como testar

1. `python -m pip install -r requirements-dev.txt`
2. `python -m sphinx -W -b html docs docs/_build/html`
3. Abrir `docs/_build/html/index.html` e percorrer as quatro páginas.
```

### O que o revisor verifica

- A documentação é gerada sem avisos.
- A página "Referência do código" mostra todas as funções de `config`, `bd`, `cli.comum` e `cli.principal`.
- No pull request aparecem as verificações **Testes** e **Documentação**, a verde.
- Ao criar uma issue nova, o GitHub oferece os três modelos (User story, Erro, Tarefa).

### Para perceber este código

- **`docs/conf.py`** é a configuração do Sphinx.
  - `sys.path.insert(0, os.path.abspath(".."))` acrescenta a pasta do projeto ao caminho do Python. É preciso porque o autodoc importa os módulos para ler os docstrings, e o `conf.py` está dentro de `docs`.
  - `extensions`: `autodoc` gera a referência a partir dos docstrings; `viewcode` acrescenta a ligação para o código-fonte.
  - `release` é lida de `gestor_campanhas.__version__`, para a versão da documentação acompanhar a do código.
  - `autodoc_default_options` aplica `members` e `undoc-members` a todos os módulos, por isso em `referencia.rst` basta escrever `.. automodule:: nome_do_modulo`.
  - `autodoc_typehints = "description"` mostra os tipos na descrição dos parâmetros.
- **`docs/referencia.rst`** tem uma diretiva `automodule` por módulo. Um módulo novo só aparece na documentação depois de ser acrescentado aqui.
- **`docs/Makefile` e `docs/make.bat`** são os atalhos habituais do Sphinx (`make html`). Fazem o mesmo que `python -m sphinx -b html docs docs/_build/html`.
- **`.github/workflows/docs.yml`** gera a documentação com `-W`, que transforma avisos em erros. Um docstring mal formatado faz falhar a verificação do pull request.
- **Docstrings** seguem o formato do Sphinx: `:param nome:`, `:return:`, `:raises Erro:`. Os comentários `#:` por cima de uma constante são o docstring dessa constante.
- **`.github/ISSUE_TEMPLATE/`** tem os modelos que o GitHub oferece ao criar uma issue. O cabeçalho entre `---` define o nome, o título sugerido e a label.

### Depois do merge

```bash
git switch develop
git pull
git diff --stat 49397f6 develop
```

---

## 7. Issues das user stories

As 57 user stories do Trello passam a issues. Os textos estão em [`issues/issues.md`](issues/issues.md).

| Perfil | Issues | Quem cria |
|---|---|---|
| Administrador | A01 a A19 | Fabio |
| Marketeer | M01 a M18 | Tomas |
| Cliente | C01 a C20 | Ricardo |

**À mão:** para cada issue, *New issue*, copiar o título e o corpo de `issues.md` e escolher as labels e a milestone indicadas.

**Com script (opcional):** o [`issues/criar_issues.py`](issues/criar_issues.py) cria as issues de um perfil de uma vez, com o GitHub CLI. Cada membro corre-o com a sua conta, para ficar como autor das suas issues. Só testei o modo `--simular`, porque não tenho o GitHub CLI neste computador; experimentem primeiro com `--simular`.

```bash
winget install GitHub.cli
```

```bash
gh auth login
```

```bash
python criar_issues.py --repo DONO/REPO --perfil Administrador --simular
```

```bash
python criar_issues.py --repo DONO/REPO --perfil Administrador
```

Os critérios de aceitação ficam por detalhar de propósito. O guia de cada fase traz os critérios das stories dessa fase, para acrescentarem à issue quando a story entra no Sprint Backlog.

## 8. Wiki

Os textos estão na pasta [`wiki/`](wiki/). No Repo B, separador **Wiki**: criar a página, colar o texto e guardar.

| Página | Ficheiro | Quem cria |
|---|---|---|
| Home | `wiki/Home.md` | Ricardo |
| Fluxo Git | `wiki/Fluxo-Git.md` | Tomas |

A página Home tem de ser a primeira a ser criada.

## 9. Fecho da fase

Com os quatro pull requests fundidos, num clone atualizado do Repo B:

```bash
git switch develop
git pull
git fetch trabalho
git diff --stat trabalho/develop develop
```

O `git diff` não deve mostrar nada. Confirmação adicional:

```bash
git rev-parse "develop^{tree}"
```

O resultado tem de ser `e90209e7d8085e3d7d2be163df305ec58f9cdf82`.

Depois, com as ferramentas de desenvolvimento instaladas:

```bash
python -m pytest
```

```bash
python -m sphinx -W -b html docs docs/_build/html
```

```bash
python -m gestor_campanhas
```

Lista de verificação:

- [ ] Quatro issues `[0.1]` a `[0.4]` fechadas pelos respetivos pull requests
- [ ] Quatro pull requests fundidos em `develop`, cada um com uma revisão aprovada
- [ ] 57 issues de user stories criadas, com labels e milestone
- [ ] Wiki com as páginas Home e Fluxo Git
- [ ] `git diff --stat trabalho/develop develop` vazio
- [ ] 20 testes a passar e documentação gerada sem avisos

Quando estiver tudo, digam-me **"avança para a Fase 1"**, juntamente com qualquer problema que tenham encontrado.

## Trello

A Fase 0 não tem cards de user stories. No fim desta fase, mover para **Sprint Backlog** os oito cards da Fase 1: os três de login (Administrador, Marketeer, Cliente), registo de logins e logouts, horários de entrada e saída, recuperar password, alterar password e editar a minha informação.

## Se algo correr mal

| Problema | O que fazer |
|---|---|
| `git cherry-pick -n` dá conflito | Os repositórios divergiram. `git reset --hard` desfaz a tentativa. Parem e avisem-me |
| O commit ficou com o autor errado (ainda sem push) | `git commit --amend --reset-author --no-edit`, depois de corrigir `user.name` e `user.email` |
| Trocaram a ordem dos commits ou saltaram um (ainda sem push) | No ramo da unidade: `git reset --hard develop` e recomeçar os comandos da unidade a partir do primeiro `cherry-pick` |
| `git fetch trabalho` falha | O Repo A é público, não precisa de login. Confirmem o URL com `git remote -v` |
| O `git diff --stat` depois do merge mostra ficheiros | Não avancem para a unidade seguinte. Digam-me que ficheiros aparecem |
| A verificação **Testes** falha no pull request | Abrir o separador *Checks* do pull request, copiar o erro e enviar-mo |
