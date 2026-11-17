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
| v0.1.0 | Autenticação e sessões: entrar e sair, registo de sessões, inatividade, horários dos marketeers, dados da conta, recuperação da password |
| v0.2.0 | Clientes e marketeers: o Administrador lista, pesquisa, adiciona, edita, desativa e reativa as contas de clientes e de marketeers |
| v0.3.0 | Campanhas e pedidos de campanha: o Marketeer cria e gere campanhas, o Cliente pede campanhas e acompanha-as, o Administrador decide os pedidos, define o budget e atribui o marketeer |
| v0.4.0 | Criativos: o Marketeer cria os criativos de cada campanha, com custo, prazo, público-alvo, plataforma e ficheiro; o Cliente vê-os, filtra-os, aprova-os ou rejeita-os e descarrega os ficheiros; a despesa é comparada com o budget |

O detalhe de cada versão está no [registo de alterações](CHANGELOG.md).

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
Gestor de Campanhas v0.4.0
============================================================
  1. Entrar
  2. Recuperar a password
  0. Sair
Opção:
```

No primeiro arranque é criada a pasta `dados`, com a base de dados `app.db`. Essa pasta não vai para o Git.

### Contas de demonstração

Uma instalação nova não tem contas. Para criar as contas, as campanhas, os pedidos e os criativos de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

| Perfil | Email | Password |
|---|---|---|
| Administrador | `admin@agencia.pt` | `admin12345` |
| Marketeer | `marketeer@agencia.pt` | `marketeer12345` |
| Marketeer | `marta@agencia.pt` | `marta12345` |
| Cliente | `cliente@empresa.pt` | `cliente12345` |
| Cliente | `jose@padaria.pt` | `jose12345` |
| Cliente | `beatriz@bicicletas.pt` | `beatriz12345` |

Estas passwords são públicas e servem só para demonstração.

O mesmo comando cria três campanhas, dois pedidos de campanha pendentes e quatro criativos. Pode ser repetido: só acrescenta o que faltar.

### Clientes e marketeers

O Administrador gere as contas dos clientes e dos marketeers nas opções **Clientes** e **Marketeers** do seu menu. Cada uma mostra a lista das contas e, por baixo, as opções para pesquisar por nome, adicionar, editar e desativar ou reativar.

Uma conta nova começa com uma password aleatória, enviada por email para a pessoa. Uma conta desativada deixa de poder entrar, mas não é apagada e pode ser reativada.

### Campanhas e pedidos de campanha

Uma campanha pertence a um cliente e tem um marketeer responsável. Nasce de duas maneiras:

- o **Marketeer** cria-a na opção **Campanhas** do seu menu, onde também a edita, consulta e elimina;
- o **Cliente** pede-a na opção **Pedidos de campanha**, indicando o objetivo, o orçamento, o prazo e as plataformas. O **Administrador** analisa o pedido e, se o aprovar, a campanha é criada com o budget inicial e o marketeer que escolher. Se o rejeitar, indica o motivo.

| Perfil | O que faz |
|---|---|
| Administrador | Decide os pedidos, define o budget de cada campanha e atribui o marketeer responsável |
| Marketeer | Cria, edita, consulta e elimina as campanhas que lhe estão atribuídas |
| Cliente | Faz pedidos, acompanha o estado deles, cancela os pendentes e vê as suas campanhas, com o budget e os contactos do marketeer |

O budget é sempre definido pelo Administrador. Um marketeer só pode ser desativado depois de as suas campanhas por terminar serem atribuídas a outro.

### Criativos

Um criativo é uma peça de uma campanha: uma imagem, um vídeo ou um texto a publicar. O **Marketeer** cria-os na opção **Criativos** do seu menu, com o custo estimado, o prazo, o público-alvo, a plataforma e um ficheiro anexado. Quando um criativo está pronto, envia-o ao cliente para revisão.

```
Em preparação --> Em revisão --> Aprovado --> Publicado
                       |
                       +-------> Rejeitado --> Em preparação ou Em revisão
```

| Perfil | O que faz |
|---|---|
| Marketeer | Cria, edita, consulta e elimina os criativos das suas campanhas, muda o estado, anexa o ficheiro e pré-visualiza-o |
| Cliente | Vê os criativos de todas as suas campanhas, pesquisa e filtra, aprova ou rejeita os que estão em revisão, pré-visualiza e descarrega os ficheiros |

A **despesa** de uma campanha é a soma do custo dos seus criativos. As listas de campanhas mostram a despesa e o budget restante, e o Marketeer é avisado quando a despesa passa o budget.

Os ficheiros anexados são copiados para a pasta `dados/ficheiros`. Para experimentar, o projeto tem o ficheiro `exemplos/banner-natal.svg`.

### Emails

A aplicação não envia emails verdadeiros. Cada mensagem (por exemplo, o código para recuperar a password, as credenciais de uma conta nova ou o aviso de que um pedido foi aprovado) é escrita num ficheiro de texto na pasta `dados/caixa_saida`.

### Sessões

Todas as entradas e saídas ficam registadas. Ao fim de 15 minutos sem atividade, a sessão termina sozinha e é preciso entrar de novo.

## Configuração

| Variável de ambiente | Valor por omissão | Para que serve |
|---|---|---|
| `GESTOR_CAMPANHAS_DADOS` | `dados` (na pasta do projeto) | Pasta onde a aplicação guarda a base de dados, os emails simulados e os ficheiros dos criativos |

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
  modelos.py           classes de dados
  seguranca.py         hash das passwords
  repositorios/        leitura e escrita na base de dados
  servicos/            regras de negócio
  cli/                 menus da linha de comandos
tests/                 testes automáticos (pytest)
docs/                  documentação do código (Sphinx)
exemplos/              ficheiros para experimentar a aplicação
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
