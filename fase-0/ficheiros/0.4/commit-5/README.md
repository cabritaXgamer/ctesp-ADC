# Gestor de Campanhas

Trabalho de Grupo UAlg 2026.

Aplicação de linha de comandos para gestão de campanhas de marketing, escrita em Python.

Uma agência usa-a para organizar o trabalho com os seus clientes: os clientes pedem campanhas, o administrador aprova-as e define o budget, e os marketeers produzem os criativos (anúncios) que o cliente acompanha e aprova.

## Perfis

| Perfil | O que faz |
|---|---|
| Administrador | Gere clientes e marketeers, aprova pedidos de campanha, define e altera budgets |
| Marketeer | Cria campanhas e criativos, define custos e prazos, dá parecer sobre pedidos de budget |
| Cliente | Pede campanhas e alterações de budget, acompanha, comenta e aprova os criativos |

## Estado do projeto

O desenvolvimento é feito por fases, cada uma fechada com uma *release*. As funcionalidades previstas estão registadas nas [issues](https://github.com/Blive77/ADC-TrabGrupo/issues) do repositório, uma por *user story*.

| Versão | Conteúdo |
|---|---|
| em desenvolvimento | Estrutura base: menu inicial, base de dados, testes e documentação |

## Requisitos

- Python 3.10 ou superior
- Git

A aplicação usa apenas a biblioteca padrão do Python. Para a correr não é preciso instalar mais nada.

## Instalação

```bash
git clone https://github.com/Blive77/ADC-TrabGrupo
cd ADC-TrabGrupo
```

## Utilização

A partir da pasta do projeto:

```bash
python -m gestor_campanhas
```

A aplicação mostra um menu numerado. Escreve-se o número da opção e prime-se Enter.

```
============================================================
Gestor de Campanhas v0.0.0
============================================================
  1. Entrar
  0. Sair
Opção:
```

No primeiro arranque é criada a pasta `dados`, com a base de dados `app.db`. Essa pasta não vai para o Git.

## Configuração

| Variável de ambiente | Valor por omissão | Para que serve |
|---|---|---|
| `GESTOR_CAMPANHAS_DADOS` | `dados` (na pasta do projeto) | Pasta onde a aplicação guarda a base de dados |

Exemplo em PowerShell:

```powershell
$env:GESTOR_CAMPANHAS_DADOS = "C:\demo\dados"
python -m gestor_campanhas
```

Para recomeçar com uma base de dados vazia, basta apagar a pasta de dados.

## Desenvolvimento

Os testes e a documentação precisam do pytest e do Sphinx. Recomenda-se um ambiente virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate      # Git Bash; em PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Correr os testes:

```bash
python -m pytest
```

Gerar a documentação do código (fica em `docs/_build/html/index.html`):

```bash
python -m sphinx -b html docs docs/_build/html
```

## Estrutura do projeto

```
gestor_campanhas/      código da aplicação
  __main__.py          ponto de entrada
  config.py            caminhos da pasta de dados e da base de dados
  bd.py                ligação SQLite e criação das tabelas
  cli/                 menus da linha de comandos
tests/                 testes automáticos (pytest)
docs/                  documentação do código (Sphinx)
.github/               integração contínua e modelos de issue e de pull request
pyproject.toml         descrição do projeto e configuração do pytest
requirements-dev.txt   ferramentas de desenvolvimento
```

## Documentação

- **Documentação do código:** pasta [`docs/`](docs/), gerada com o Sphinx a partir dos docstrings.
- **Wiki do repositório:** [wiki](https://github.com/Blive77/ADC-TrabGrupo/wiki), com a apresentação do projeto, o fluxo de trabalho e o registo das fases.
- **Como contribuir:** [CONTRIBUTING.md](CONTRIBUTING.md) descreve os ramos, as mensagens de commit e os pull requests.

## Equipa

| Nome | GitHub |
|---|---|
| Fabio Felgueiras | [blive77](https://github.com/blive77) |
| Tomas Paulo | [GLKIIRA](https://github.com/GLKIIRA) |
| Ricardo Cabrita | [CabritaXgamer](https://github.com/CabritaXgamer) |
