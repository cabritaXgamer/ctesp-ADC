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
| Administrador | Gere clientes e marketeers, aprova pedidos de campanha, define e altera budgets, acompanha a carga de trabalho dos marketeers | 19 |
| Marketeer | Cria campanhas e criativos, define custos e prazos, dá parecer sobre pedidos de budget, responde aos comentários do cliente | 18 |
| Cliente | Pede campanhas e alterações de budget, acompanha, comenta e aprova os criativos, exporta um relatório das campanhas | 20 |

## Páginas desta wiki

| Página | Conteúdo |
|---|---|
| [Instalação e configuração](Instalação-e-configuração) | Requisitos, arrancar a aplicação, dados de demonstração, pasta de dados, definições e ambiente de desenvolvimento |
| [Guia de utilização](Guia-de-utilização) | Como usar a aplicação: entrar, menus de cada perfil, gestão de clientes e marketeers, campanhas, pedidos de campanha, pedidos de alteração de budget, histórico e resumo do budget, criativos e comentários, notificações, painel de marketeers, relatório das campanhas, recuperar a password |
| [Arquitetura](Arquitetura) | Camadas do código, tabelas, campanhas e pedidos, budget e histórico, criativos e ficheiros, comentários, notificações, painel de marketeers, relatório, dinheiro, passwords, sessões, emails e contas desativadas |
| [Modelo de dados](Modelo-de-dados) | Tabelas, relações, estados, como cada valor é guardado e o que acontece quando se apaga |
| [Testes](Testes) | Como correr os testes, os fluxos completos, os ficheiros de testes e a integração contínua |
| [Backlog e user stories](Backlog-e-user-stories) | As 57 user stories, por perfil e por fase, com a unidade e quem a fez |
| [Fluxo Git](Fluxo-Git) | Ramos, commits, pull requests e releases |
| [Registo das fases](Registo-das-fases) | O que foi feito em cada fase, por quem, as decisões tomadas e o que correu mal |
| [Changelog](Changelog) | As alterações de cada versão, da v0.1.0 à v1.0.0 |

Versão atual: **v1.0.0** (Fase 7 — Fecho e entrega). As 57 user stories estão implementadas.

## Plano de desenvolvimento

O trabalho foi dividido em fases. Cada fase corresponde a uma milestone do repositório e terminou com uma release. Estão todas concluídas.

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

O detalhe de cada fase (quem fez e quem reviu cada unidade, e as decisões) está no [Registo das fases](Registo-das-fases).

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
python -m gestor_campanhas.dados_demo
python -m gestor_campanhas
```

O segundo comando cria as contas de demonstração e mostra as passwords. A página [Instalação e configuração](Instalação-e-configuração) explica o resto.
