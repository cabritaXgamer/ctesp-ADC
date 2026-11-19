# Instalação e configuração

Como instalar, configurar e arrancar a aplicação, na versão 1.0.0.

## Requisitos

| O quê | Para quê |
|---|---|
| Python 3.10 ou superior | Correr a aplicação. Usa só a biblioteca padrão: não é preciso instalar mais nada |
| Git | Obter o código |
| pytest e Sphinx (opcional) | Correr os testes e gerar a documentação do código |

## Obter o código e arrancar

```bash
git clone https://github.com/Blive77/ADC-TrabGrupo
cd ADC-TrabGrupo
python -m gestor_campanhas
```

No Windows, se o `python` não for reconhecido, experimenta `py`.

No primeiro arranque a aplicação cria a pasta `dados`, que não vai para o Git:

| Dentro da pasta `dados` | O que é |
|---|---|
| `app.db` | A base de dados SQLite (ver [Modelo de dados](Modelo-de-dados)) |
| `caixa_saida/` | Os emails que a aplicação "envia", um ficheiro de texto por email |
| `ficheiros/` | Os ficheiros anexados aos criativos, uma pasta por criativo |

## Dados de demonstração

Uma instalação nova não tem contas. Para criar as contas, as campanhas, os pedidos, os criativos e os comentários de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

O comando mostra as contas criadas e as passwords de cada uma. Pode ser repetido: só acrescenta o que faltar. O que se pode fazer com cada conta está no [Guia de utilização](Guia-de-utilização).

## Configuração

### Pasta de dados

| Variável de ambiente | Por omissão | Para que serve |
|---|---|---|
| `GESTOR_CAMPANHAS_DADOS` | `dados`, na pasta do projeto | Pasta onde ficam a base de dados, os emails e os ficheiros |

Serve, por exemplo, para fazer uma demonstração sem mexer nos dados de sempre:

```powershell
# PowerShell
$env:GESTOR_CAMPANHAS_DADOS = "C:\demo\dados"
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

```bash
# Git Bash, Linux ou macOS
export GESTOR_CAMPANHAS_DADOS=/tmp/demo
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

Para recomeçar com uma base de dados vazia, basta apagar a pasta de dados.

### Definições

| Definição | Por omissão | Onde se muda |
|---|---|---|
| Minutos sem atividade ao fim dos quais a sessão termina | 15 | Na tabela `configuracoes` da base de dados, chave `minutos_inatividade` |
| Dias sem mexer nos criativos ao fim dos quais um marketeer aparece como parado | 7 | No menu do Administrador: "Painel de marketeers", "Mudar os dias sem atividade" |
| Minutos de validade do código de recuperação da password | 15 | Só no código, em `gestor_campanhas/config.py` |

Os valores por omissão estão em `gestor_campanhas/config.py`. As duas primeiras definições, quando são mudadas, ficam guardadas na base de dados e valem para todos os utilizadores.

## Ambiente de desenvolvimento

Para correr os testes e gerar a documentação, instalam-se o pytest e o Sphinx, de preferência num ambiente virtual:

```bash
python -m venv .venv
source .venv/Scripts/activate      # Git Bash; em PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

| Comando | O que faz |
|---|---|
| `python -m pytest` | Corre os testes (ver [Testes](Testes)) |
| `python -m sphinx -W -b html docs docs/_build/html` | Gera a documentação do código em `docs/_build/html/index.html`; o `-W` faz falhar se houver avisos |

Depois de reinstalar o Python, é preciso instalar outra vez as ferramentas: se aparecer `No module named pytest`, corre-se de novo o `pip install`.

## Documentação do código

A documentação gerada pelo Sphinx tem as páginas de instalação e configuração, utilização, arquitetura, modelo de dados e testes, e a referência de todos os módulos, gerada a partir dos docstrings. O ficheiro de configuração, `docs/conf.py`, está comentado linha a linha.
