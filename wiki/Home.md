# Gestor de Campanhas

Aplicação de linha de comandos, em Python, para gestão de campanhas de marketing. Trabalho de Grupo UAlg 2026.

Uma agência usa-a para organizar o trabalho com os seus clientes: os clientes pedem campanhas, o administrador aprova-as e define o budget, e os marketeers produzem os criativos (anúncios) que o cliente acompanha e aprova.

## Equipa

| Nome | GitHub |
|---|---|
| Fabio Felgueiras | [blive77](https://github.com/blive77) |
| Tomas Paulo | [GLKIIRA](https://github.com/GLKIIRA) |
| Ricardo Cabrita | [CabritaXgamer](https://github.com/CabritaXgamer) |

## Perfis da aplicação

| Perfil | O que faz | User stories |
|---|---|---|
| Administrador | Gere clientes e marketeers, aprova pedidos de campanha, define e altera budgets | 19 |
| Marketeer | Cria campanhas e criativos, define custos e prazos, dá parecer sobre pedidos de budget | 18 |
| Cliente | Pede campanhas e alterações de budget, acompanha, comenta e aprova os criativos | 20 |

## Páginas desta wiki

| Página | Conteúdo |
|---|---|
| [Fluxo Git](Fluxo-Git) | Ramos, commits, pull requests e releases |

Esta lista cresce em cada fase.

## Plano de desenvolvimento

O trabalho está dividido em fases. Cada fase corresponde a uma milestone do repositório e termina com uma release.

| Fase | Tema | User stories | Release |
|---|---|---|---|
| 0 | Arranque: estrutura, base de dados, testes, documentação | — | — |
| 1 | Autenticação e sessões | 8 | v0.1.0 |
| 2 | Gestão de clientes e marketeers | 7 | v0.2.0 |
| 3 | Campanhas e pedidos de campanha | 12 | v0.3.0 |
| 4 | Criativos | 15 | v0.4.0 |
| 5 | Budget | 6 | v0.5.0 |
| 6 | Comentários, notificações, monitorização e relatórios | 9 | v0.6.0 |
| 7 | Fecho e entrega | — | v1.0.0 |

## Tecnologias

| Para quê | O que se usa |
|---|---|
| Linguagem | Python 3.10 ou superior, só com a biblioteca padrão |
| Dados | SQLite (`sqlite3`) |
| Testes | pytest |
| Documentação do código | Sphinx |
| Integração contínua | GitHub Actions |
| Gestão do trabalho | Issues e milestones do GitHub, quadro Trello |

## Como começar

```bash
git clone https://github.com/Blive77/ADC-TrabGrupo
cd ADC-TrabGrupo
python -m gestor_campanhas
```

O README do repositório explica a configuração e o ambiente de desenvolvimento.
