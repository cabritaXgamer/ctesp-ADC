# Plano de execução — TP2 (Desenvolver a aplicação)

Aplicação de linha de comandos, em Python, para gerir campanhas de marketing com três perfis (Administrador, Marketeer, Cliente). Implementa as 57 user stories do quadro Trello `TP1_v2`.

- **Grupo:** Fabio Felgueiras (@blive77), Tomas Paulo (@GLKIIRA), Ricardo Cabrita (@CabritaXgamer)
- **Entrega:** domingo, 22 de novembro de 2026
- **Repo A (trabalho):** https://github.com/cabritaXgamer/ctesp-ADC. O projeto está no ramo `develop`. O ramo `main` guarda um exercício antigo e não é usado.
- **Documentação do código:** Sphinx

## 1. Como funciona o trabalho com dois repositórios

| | Repo A — trabalho | Repo B — oficial |
|---|---|---|
| Quem escreve | Claude | Os três membros do grupo |
| Para que serve | Desenvolver e testar cada fase | É o que é entregue e avaliado |
| Ramos | Os mesmos nomes que o Repo B, mais o ramo `guias` | `main`, `develop`, `feature/*`, `fix/*`, `release/*` |
| Issues, PR, wiki | Não usa | Tudo aqui |

Regras fixas:

- **Só começo uma fase quando derem o aviso** ("avança para a Fase N"). No fim de cada fase paro e entrego.
- **Nunca faço push para o Repo B.** No máximo leio-o para confirmar que está sincronizado.
- **O Repo A é a fonte do código.** Se alterarem algo diretamente no Repo B (por exemplo, corrigirem um bug), avisam-me para eu trazer essa alteração para o Repo A antes da fase seguinte.
- No Repo A os commits já têm a granularidade final (pequenos, um propósito cada), para que replicar seja mecânico.

### O que recebem no fim de cada fase

No ramo `guias` do Repo A, um ficheiro `fase-N.md` com, para cada unidade de trabalho:

1. A issue a criar (título, descrição, critérios de aceitação, labels, milestone).
2. O nome do ramo.
3. A lista ordenada de commits: mensagem, ficheiros tocados e o SHA no Repo A.
4. O texto do pull request (com `Closes #n`) e quem deve rever.
5. As páginas da wiki a criar ou atualizar (texto pronto a colar).
6. Como testar à mão e uma explicação curta do código, para quem faz o commit o conseguir defender.

### Como copiar um commit do Repo A para o Repo B

Cada membro, uma única vez, no seu clone do Repo B:

```bash
git remote add trabalho https://github.com/cabritaXgamer/ctesp-ADC
```

Depois, para cada unidade:

```bash
git fetch trabalho
git switch develop
git pull
git switch -c feature/A01-login
git cherry-pick -n <sha>          # aplica as alterações, sem criar commit
git diff --staged                 # ler o que entrou
git commit -m "feat(auth): ..."   # commit do próprio membro
git push -u origin feature/A01-login
```

Repete-se `cherry-pick -n` + `commit` para cada commit da unidade, pela ordem do guia. Depois abre-se o PR para `develop` no GitHub, outro membro revê e faz o merge. Se um `cherry-pick` der conflito, é sinal de que os repositórios divergiram: param e avisam-me.

Alternativa sem remote: copiar à mão os ficheiros indicados no guia. Funciona, mas é mais lento e mais sujeito a erros.

## 2. Ciclo de cada fase

| Passo | Quem | O que acontece |
|---|---|---|
| 1. Aviso | Grupo | "Avança para a Fase N", com o feedback da fase anterior |
| 2. Desenvolvimento | Claude | Implemento as unidades no Repo A, com testes e docstrings |
| 3. Entrega | Claude | Publico `guias/fase-N.md` e paro |
| 4. Replicação | Grupo | Issue → ramo → commits → PR → revisão → merge, unidade a unidade |
| 5. Verificação | Grupo | Correr a aplicação e os testes no Repo B; bugs viram issues com label `bug` |
| 6. Correções | Claude + grupo | Corrijo no Repo A, replicam num ramo `fix/*` |
| 7. Release | Grupo | `release/v0.N.0` → PR para `main` → tag → merge de volta para `develop` |
| 8. Sincronização | Ambos | Confirmar que o `develop` dos dois repositórios tem o mesmo conteúdo |

Dentro de cada fase, as unidades são replicadas pela ordem do guia: só se começa uma unidade depois de o pull request da anterior estar fundido. As unidades partilham ficheiros (o esquema da base de dados, os menus, a referência da documentação), por isso fora de ordem os commits não encaixam.

Verificação do passo 8: `git rev-parse develop^{tree}` tem de dar o mesmo valor nos dois repositórios. O guia de cada fase traz o valor esperado.

Correspondência com as listas do Trello: no início da fase os cards vão para *Sprint Backlog*; ao começar a replicar uma unidade, *Work In Progress*; PR aberto, *Ready to Verify*; bug encontrado, *Debug in Progress*; PR fundido, *Ready*.

## 3. Calendário

Hoje é quinta, 12 de novembro. Há dez dias até à entrega.

| Fase | Aviso até | Replicada no Repo B até |
|---|---|---|
| 0 — Arranque | qui 12 | sex 13 |
| 1 — Autenticação e sessões | sex 13 | sáb 14 |
| 2 — Clientes e marketeers | sáb 14 | dom 15 |
| 3 — Campanhas e pedidos | dom 15 | seg 16 |
| 4 — Criativos | seg 16 | qua 18 |
| 5 — Budget | qua 18 | qui 19 |
| 6 — Comentários, notificações, monitorização, relatórios | qui 19 | sex 20 |
| 7 — Fecho e entrega | sex 20 | sáb 21 |
| Margem e entrega | | dom 22 |

O meu lado de cada fase demora horas, não dias. O ritmo depende da replicação, por isso podem dar o aviso seguinte assim que uma fase estiver replicada, sem esperar pela data.

**Ponto de controlo:** se na quarta, dia 18, a Fase 4 ainda não estiver replicada, cortamos na Fase 6 (ver "Se for preciso cortar").

## 4. Fluxo Git no Repo B (o que é avaliado)

- **Ramos:** `main` (só releases), `develop` (integração), `feature/<ID>-<slug>`, `fix/<slug>`, `release/vX.Y.0`.
- **Issues:** uma por user story, com o ID no título (`[A01] Como Administrador, quero fazer login…`), label do perfil e milestone da fase.
- **Commits:** 2 a 5 por unidade, na ordem dados → regras de negócio → menu → testes → documentação. Mensagens no formato `tipo(área): descrição` (`feat`, `fix`, `test`, `docs`, `chore`).
- **Pull requests:** um por unidade, para `develop`, com revisão de outro membro e merge com *merge commit* (para os merges ficarem visíveis no histórico).
- **Releases:** uma tag por fase, de `v0.1.0` (Fase 1) a `v1.0.0` (Fase 7).
- **Wiki:** cresce em todas as fases (ver secção 8).

Volume esperado no fim: cerca de 60 issues, 43 pull requests, 150 a 180 commits, 7 releases. Por membro: 12 unidades, cerca de 14 pull requests e 50 a 60 commits.

## 5. Distribuição pelos membros

A avaliação é individual, por isso as 36 unidades são repartidas em rotação: 12 para cada um. Quem revê o PR é o membro seguinte na rotação (Fabio → revê Tomas, Tomas → revê Ricardo, Ricardo → revê Fabio).

| Fase | Fabio | Tomas | Ricardo | Release |
|---|---|---|---|---|
| 0 | 0.1, 0.4 | 0.2 | 0.3 | — |
| 1 | 1.3 | 1.1, 1.4 | 1.2, 1.5 | v0.1.0 — Fabio |
| 2 | 2.1, 2.4 | 2.2, 2.5 | 2.3 | v0.2.0 — Tomas |
| 3 | 3.2, 3.5 | 3.3 | 3.1, 3.4 | v0.3.0 — Ricardo |
| 4 | 4.3, 4.6 | 4.1, 4.4 | 4.2, 4.5 | v0.4.0 — Fabio |
| 5 | 5.3 | 5.1, 5.4 | 5.2 | v0.5.0 — Tomas |
| 6 | 6.2 | 6.3 | 6.1, 6.4 | v0.6.0 — Ricardo |
| 7 | 7.1 | 7.2 | 7.3 | v1.0.0 — os três |

Com esta rotação, cada membro tem trabalho em todas as fases e passa pelos três perfis. A wiki segue a mesma lógica: quem faz a release da fase atualiza as páginas dessa fase.

## 6. Aplicação: linha de comandos

A aplicação arranca com `python -m gestor_campanhas`, pede email e password e mostra o menu do perfil. Toda a interação é por menus numerados e perguntas no terminal.

| Parte | Escolha | Porquê |
|---|---|---|
| Interface | Menus em texto com `input` e `getpass` | Só linha de comandos, sem bibliotecas externas |
| Dados | `sqlite3` (biblioteca padrão), ficheiro `dados/app.db` | Sem instalação; as relações entre campanhas, criativos e pedidos ficam simples |
| Passwords | `hashlib` com *salt* | Nunca se guarda a password em claro |
| Testes | pytest | Corre também no GitHub Actions a cada PR |
| Documentação | Docstrings + Sphinx (autodoc) | A ferramenta que usam na cadeira |

Para correr a aplicação não é preciso instalar nada além do Python. O pytest e o Sphinx só são necessários para desenvolver.

Estrutura de pastas:

```
gestor_campanhas/
  __main__.py      ponto de entrada
  config.py        caminhos e tempo de inatividade
  bd.py            ligação SQLite e criação das tabelas
  modelos.py       classes de dados (Utilizador, Campanha, Criativo, ...)
  repositorios/    leitura e escrita na base de dados, por entidade
  servicos/        regras de negócio: autenticação, campanhas, criativos, budget, notificações, relatórios
  cli/             menus: comum, admin, marketeer, cliente
tests/
docs/              Sphinx
scripts/           dados de demonstração
README.md  pyproject.toml  requirements-dev.txt
```

As regras de negócio ficam em `servicos/`, separadas dos menus. É isso que permite testá-las com pytest sem simular o teclado.

### Como as stories se traduzem para a linha de comandos

Várias stories foram escritas a pensar num ecrã. Proposta de adaptação:

| Na story | Na linha de comandos |
|---|---|
| Formulário | Sequência de perguntas, com validação de cada resposta |
| Tabela ou lista com filtros | Tabela em texto; os filtros são pedidos antes de listar |
| Pedido de confirmação | Pergunta "Tem a certeza? (s/n)" |
| Envio de email (credenciais, notificações) | Ficheiro de texto na pasta `dados/caixa_saida/`, que simula o envio |
| Link de reposição de password | Código temporário com validade, "enviado" para a `dados/caixa_saida/` e introduzido no menu |
| Sessão com expiração por inatividade | Conta o tempo desde a última ação; ao expirar faz logout automático e regista-o |
| Notificação na plataforma | Contador ao entrar ("3 notificações por ler") e menu de notificações |
| Upload de ficheiro | Indica-se o caminho; o ficheiro é copiado para `dados/ficheiros/` |
| Pré-visualização | Mostra nome, tipo e tamanho, e abre o ficheiro no programa predefinido do sistema |
| Download | Copia o ficheiro para uma pasta à escolha |
| Exportar em PDF ou CSV | CSV, com a biblioteca padrão |

## 7. Fases e unidades

| Fase | Tema | Stories | Unidades | Release |
|---|---|---|---|---|
| 0 | Arranque do projeto | — | 4 | — |
| 1 | Autenticação e sessões | 8 | 5 | v0.1.0 |
| 2 | Gestão de clientes e marketeers | 7 | 5 | v0.2.0 |
| 3 | Campanhas e pedidos de campanha | 12 | 5 | v0.3.0 |
| 4 | Criativos | 15 | 6 | v0.4.0 |
| 5 | Budget | 6 | 4 | v0.5.0 |
| 6 | Comentários, notificações, monitorização, relatórios | 9 | 4 | v0.6.0 |
| 7 | Fecho e entrega | — | 3 | v1.0.0 |

No fim de cada fase a aplicação corre e os testes passam, por isso qualquer fase pode ser a última se o tempo apertar.

### Fase 0 — Arranque

| Unidade | Membro |
|---|---|
| 0.1 Estrutura do pacote: `__main__.py`, `config.py`, `pyproject.toml`, `.gitignore`, `.gitattributes` | Fabio |
| 0.2 Base de dados (`bd.py`), funções comuns dos menus e menu inicial | Tomas |
| 0.3 pytest com um primeiro teste e workflow do GitHub Actions | Ricardo |
| 0.4 README, esqueleto do Sphinx, `CONTRIBUTING.md` com o fluxo Git, modelos de issue e de PR | Fabio |

Tarefas só do Repo B, com textos preparados por mim:

- Criar `develop` e proteger `main` e `develop` (merge só por PR).
- Criar labels (perfis e tipos) e milestones (uma por fase).
- Criar as 57 issues a partir dos cards do Trello: Fabio as de Administrador (19), Tomas as de Marketeer (18), Ricardo as de Cliente (20).
- Criar as páginas Home e Fluxo Git da wiki.

O script de dados de demonstração entra na Fase 1, quando passam a existir utilizadores.

### Fase 1 — Autenticação e sessões

| Unidade | Stories | Membro |
|---|---|---|
| 1.1 Login e logout dos três perfis | A01, M01, C01 | Tomas |
| 1.2 Expiração por inatividade e registo de sessões | A02 | Ricardo |
| 1.3 Consulta de horários de entrada e saída | A03 | Fabio |
| 1.4 Alterar password e editar perfil | C03, C04 | Tomas |
| 1.5 Recuperar password | C02 | Ricardo |

### Fase 2 — Gestão de clientes e marketeers

| Unidade | Stories | Membro |
|---|---|---|
| 2.1 Lista de clientes com pesquisa | A04 | Fabio |
| 2.2 Adicionar e editar cliente | A05, A06 | Tomas |
| 2.3 Desativar cliente | A07 | Ricardo |
| 2.4 Adicionar e editar marketeer | A08, A09 | Fabio |
| 2.5 Desativar marketeer | A10 | Tomas |

### Fase 3 — Campanhas e pedidos de campanha

| Unidade | Stories | Membro |
|---|---|---|
| 3.1 Criar e editar campanha | M02, M03 | Ricardo |
| 3.2 Campanhas atribuídas e eliminar campanha vazia | M04, M05 | Fabio |
| 3.3 Pedido de nova campanha: criar, acompanhar, cancelar | C05, C06, C07 | Tomas |
| 3.4 Decisão do pedido, budget inicial, atribuir marketeer | A11, A12, A13 | Ricardo |
| 3.5 Cliente vê campanhas, budget e marketeer responsável | C08, C09 | Fabio |

Fecha também a regra de A10: um marketeer só é desativado depois de as suas campanhas serem reatribuídas.

### Fase 4 — Criativos

| Unidade | Stories | Membro |
|---|---|---|
| 4.1 Criar, editar e eliminar criativo | M06, M07, M08 | Tomas |
| 4.2 Custo, prazos, público-alvo e plataformas | M09, M10, M11, M12 | Ricardo |
| 4.3 Ficheiros: anexar, pré-visualizar, descarregar | M13, C12 | Fabio |
| 4.4 Estados do criativo e aprovação pelo cliente | M14, C13 | Tomas |
| 4.5 Lista e filtros de criativos do cliente | C10, C11 | Ricardo |
| 4.6 Despesa face ao budget e aviso de ultrapassagem | C14, M15 | Fabio |

### Fase 5 — Budget

| Unidade | Stories | Membro |
|---|---|---|
| 5.1 Pedido de alteração de budget | C15 | Tomas |
| 5.2 Parecer do marketeer | M16 | Ricardo |
| 5.3 Pedidos pendentes, decisão e histórico | A14, A15, C16 | Fabio |
| 5.4 Resumo global do budget | A16 | Tomas |

Completa C06: a lista de pedidos do cliente passa a incluir os pedidos de budget.

### Fase 6 — Comentários, notificações, monitorização, relatórios

| Unidade | Stories | Membro |
|---|---|---|
| 6.1 Comentários e respostas | C18, M17 | Ricardo |
| 6.2 Notificações na aplicação e na `dados/caixa_saida/` | C17, C19, M18 | Fabio |
| 6.3 Painel de marketeers: tarefas, carga, inatividade | A17, A18, A19 | Tomas |
| 6.4 Exportar relatório em CSV | C20 | Ricardo |

### Fase 7 — Fecho e entrega

| Unidade | Membro |
|---|---|
| 7.1 Testes dos fluxos completos (pedido → campanha → criativo → aprovação → budget) e dados de demonstração finais | Fabio |
| 7.2 Revisão de todos os docstrings, build final do Sphinx, README final | Tomas |
| 7.3 Wiki completa, `CHANGELOG.md`, release `v1.0.0` | Ricardo |

### Se for preciso cortar

Assumo que implementam as 57 stories. A especificação admite implementar só parte delas, a combinar com o professor. As Fases 1 a 5 são o núcleo (48 stories). Os primeiros candidatos a sair, todos da Fase 6, são: comparação de carga e inatividade (A18, A19), exportação de relatório (C20) e notificações (C17, C19, M18).

## 8. Documentação

- **Código:** docstring em todos os módulos, classes e funções (parâmetros, retorno, exceções), no formato nativo do Sphinx (`:param:`, `:return:`, `:raises:`). Cada unidade inclui um commit `docs`, para a documentação crescer com o código.
- **Sphinx (`docs/`):** introdução, instalação, configuração, arquitetura, modelo de dados, referência dos módulos gerada do código, testes. O `conf.py` fica comentado, porque a configuração também é avaliada.
- **README:** descrição, requisitos, instalação, configuração, como correr, como testar, estrutura, equipa.
- **Wiki:** Home, Instalação e configuração, Arquitetura, Modelo de dados, Fluxo Git, Backlog e user stories, Guia de utilização por perfil, Testes, Registo de sprints, Changelog.

## 9. Riscos

| Risco | Como se controla |
|---|---|
| Dez dias para oito fases | Calendário da secção 3, ponto de controlo no dia 18, um dia de margem |
| Os dois repositórios divergem | Regra da fonte única e verificação do `tree` no fim de cada fase |
| Um membro não consegue explicar o que fez commit | Explicação por unidade no guia; ler o `diff` antes de cada commit; tirar dúvidas comigo |
| Histórico concentrado no fim | Replicar a fase N antes de pedir a N+1 |
| Adaptações à linha de comandos diferentes do que o professor espera | Validar com ele a tabela da secção 6 |
| Regras da cadeira sobre uso de IA | Confirmar com o professor que este método de trabalho é aceite |

## Anexo — IDs das user stories

IDs criados para este plano; os títulos completos são os dos cards do Trello.

### Administrador

| ID | Story | Fase |
|---|---|---|
| A01 | Login na plataforma | 1 |
| A02 | Registo de logins e logouts dos marketeers | 1 |
| A03 | Consultar horários de entrada e saída | 1 |
| A04 | Ver lista de clientes | 2 |
| A05 | Adicionar clientes | 2 |
| A06 | Editar dados de um cliente | 2 |
| A07 | Remover clientes | 2 |
| A08 | Adicionar marketeers | 2 |
| A09 | Editar dados de um marketeer | 2 |
| A10 | Remover marketeers | 2 |
| A11 | Aprovar ou rejeitar pedidos de nova campanha | 3 |
| A12 | Definir budget inicial de uma campanha | 3 |
| A13 | Atribuir marketeer a uma campanha | 3 |
| A14 | Ver pedidos de alteração de budget pendentes, com parecer | 5 |
| A15 | Alterar o budget das campanhas | 5 |
| A16 | Resumo global do budget atribuído face ao gasto | 5 |
| A17 | Ver marketeers e tarefas/criativos atribuídos | 6 |
| A18 | Comparar carga de trabalho entre marketeers | 6 |
| A19 | Identificar marketeers sem atividade | 6 |

### Marketeer

| ID | Story | Fase |
|---|---|---|
| M01 | Login na plataforma | 1 |
| M02 | Criar campanhas | 3 |
| M03 | Editar uma campanha | 3 |
| M04 | Ver campanhas atribuídas | 3 |
| M05 | Eliminar campanha sem criativos | 3 |
| M06 | Criar um novo criativo | 4 |
| M07 | Editar um criativo | 4 |
| M08 | Eliminar um criativo | 4 |
| M09 | Indicar o custo estimado | 4 |
| M10 | Definir prazos | 4 |
| M11 | Definir o público-alvo | 4 |
| M12 | Escolher a plataforma alvo | 4 |
| M13 | Anexar ficheiro ou pré-visualização | 4 |
| M14 | Atualizar o estado do criativo | 4 |
| M15 | Aviso quando o custo ultrapassa o budget | 4 |
| M16 | Dar parecer sobre pedidos de alteração de budget | 5 |
| M17 | Ver e responder a comentários do cliente | 6 |
| M18 | Notificações de nova campanha, pedido de budget e comentário | 6 |

### Cliente

| ID | Story | Fase |
|---|---|---|
| C01 | Login na plataforma | 1 |
| C02 | Recuperar a password | 1 |
| C03 | Alterar a password | 1 |
| C04 | Editar a minha informação | 1 |
| C05 | Pedir novas campanhas | 3 |
| C06 | Acompanhar o estado dos pedidos | 3 |
| C07 | Cancelar um pedido pendente | 3 |
| C08 | Ver campanhas e budget atribuído | 3 |
| C09 | Saber o marketeer responsável | 3 |
| C10 | Ver lista de criativos com custo, prazo, público e plataforma | 4 |
| C11 | Filtrar e pesquisar criativos | 4 |
| C12 | Pré-visualizar e descarregar ficheiros | 4 |
| C13 | Aprovar ou rejeitar criativo em revisão | 4 |
| C14 | Ver despesa total face ao budget | 4 |
| C15 | Pedir alteração do budget | 5 |
| C16 | Ver histórico de alterações de budget | 5 |
| C17 | Ser informado da decisão do pedido de budget | 6 |
| C18 | Comentar ou sugerir alterações a um criativo | 6 |
| C19 | Ser notificado quando um criativo é criado ou alterado | 6 |
| C20 | Exportar relatório das campanhas | 6 |
