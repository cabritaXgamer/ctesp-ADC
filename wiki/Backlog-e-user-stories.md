# Backlog e user stories

As 57 user stories do projeto, tiradas do quadro Trello `TP1_v2`. Cada uma é uma issue do repositório, com a label `user story`, a label do perfil e a milestone da fase. Os critérios de aceitação foram escritos na issue por quem implementou a story, no início da unidade, e a issue foi fechada pelo pull request que a implementou.

Estado: **todas implementadas** na versão 1.0.0.

| Perfil | User stories |
|---|---|
| Administrador | 19 (A01 a A19) |
| Marketeer | 18 (M01 a M18) |
| Cliente | 20 (C01 a C20) |

## Por fase

| Fase | Tema | User stories | Release |
|---|---|---|---|
| 1 | Autenticação e sessões | 8: A01, A02, A03, M01, C01, C02, C03, C04 | v0.1.0 |
| 2 | Clientes e marketeers | 7: A04, A05, A06, A07, A08, A09, A10 | v0.2.0 |
| 3 | Campanhas e pedidos | 12: A11, A12, A13, M02, M03, M04, M05, C05, C06, C07, C08, C09 | v0.3.0 |
| 4 | Criativos | 15: M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, C10, C11, C12, C13, C14 | v0.4.0 |
| 5 | Budget | 6: A14, A15, A16, M16, C15, C16 | v0.5.0 |
| 6 | Comentários, notificações, painel e relatório | 9: A17, A18, A19, M17, M18, C17, C18, C19, C20 | v0.6.0 |

A Fase 0 (arranque) e a Fase 7 (fecho e entrega, v1.0.0) não têm user stories.

## Administrador

| ID | User story | Fase | Unidade | Quem fez |
|---|---|---|---|---|
| A01 | Como Administrador, quero fazer login na plataforma, para que possa aceder às funcionalidades de gestão. | 1 | 1.1 Login e logout dos três perfis | Tomas |
| A02 | Como Administrador, quero que os logins e logouts dos marketeers fiquem registados, para que haja histórico de acessos. | 1 | 1.2 Registo de sessões e saída por inatividade | Ricardo |
| A03 | Como Administrador, quero consultar os horários de entrada e saída de cada marketeer, para que possa controlar a assiduidade. | 1 | 1.3 Horários de entrada e saída dos marketeers | Fabio |
| A04 | Como Administrador, quero ver a lista de todos os clientes, para que possa consultar rapidamente quem usa a plataforma. | 2 | 2.1 Lista de clientes com pesquisa | Fabio |
| A05 | Como Administrador, quero adicionar clientes, para que tenham acesso à plataforma. | 2 | 2.2 Adicionar e editar clientes | Tomas |
| A06 | Como Administrador, quero editar os dados de um cliente, para que a informação se mantenha correta. | 2 | 2.2 Adicionar e editar clientes | Tomas |
| A07 | Como Administrador, quero remover clientes, para que deixem de ter acesso à plataforma. | 2 | 2.3 Desativar e reativar clientes | Ricardo |
| A08 | Como Administrador, quero adicionar marketeers, para que possam aceder à plataforma. | 2 | 2.4 Adicionar e editar marketeers | Fabio |
| A09 | Como Administrador, quero editar os dados de um marketeer, para que a informação se mantenha correta. | 2 | 2.4 Adicionar e editar marketeers | Fabio |
| A10 | Como Administrador, quero remover marketeers, para que deixem de ter acesso à plataforma. | 2 | 2.5 Desativar e reativar marketeers | Tomas |
| A11 | Como Administrador, quero aprovar ou rejeitar pedidos de nova campanha, para que só avancem os pedidos viáveis. | 3 | 3.4 Decidir pedidos, budget e marketeer responsável | Ricardo |
| A12 | Como Administrador, quero definir o budget inicial de uma campanha, para que a equipa saiba o limite de investimento. | 3 | 3.4 Decidir pedidos, budget e marketeer responsável | Ricardo |
| A13 | Como Administrador, quero atribuir um marketeer a uma campanha, para que fique definido quem é o responsável. | 3 | 3.4 Decidir pedidos, budget e marketeer responsável | Ricardo |
| A14 | Como Administrador, quero ver a lista de pedidos de alteração de budget pendentes, com o parecer do marketeer, para que possa decidir. | 5 | 5.3 Decisão dos pedidos de budget e histórico do budget | Fabio |
| A15 | Como Administrador, quero alterar o budget das campanhas, para que fique ajustado aos pedidos aprovados dos clientes. | 5 | 5.3 Decisão dos pedidos de budget e histórico do budget | Fabio |
| A16 | Como Administrador, quero ver um resumo global do budget atribuído face ao gasto, por cliente, para que tenha visão financeira. | 5 | 5.4 Resumo global do budget | Tomas |
| A17 | Como Administrador, quero ver a lista de marketeers e as tarefas/criativos atribuídos a cada um, para que saiba em que estão a trabalhar. | 6 | 6.3 Painel de marketeers | Tomas |
| A18 | Como Administrador, quero comparar a carga de trabalho entre marketeers, para que possa distribuir melhor as tarefas. | 6 | 6.3 Painel de marketeers | Tomas |
| A19 | Como Administrador, quero identificar marketeers sem atividade, para que possa agir quando alguém não tem trabalho atribuído ou está parado. | 6 | 6.3 Painel de marketeers | Tomas |

## Marketeer

| ID | User story | Fase | Unidade | Quem fez |
|---|---|---|---|---|
| M01 | Como Marketeer, quero fazer login na plataforma, para que possa aceder ao meu trabalho. | 1 | 1.1 Login e logout dos três perfis | Tomas |
| M02 | Como Marketeer, quero criar campanhas, para que possa organizar os criativos de cada cliente. | 3 | 3.1 Criar e editar campanhas | Ricardo |
| M03 | Como Marketeer, quero editar uma campanha, para que a informação se mantenha atualizada. | 3 | 3.1 Criar e editar campanhas | Ricardo |
| M04 | Como Marketeer, quero ver as campanhas que me estão atribuídas, para que saiba em que tenho de trabalhar. | 3 | 3.2 Campanhas atribuídas e eliminar campanha | Fabio |
| M05 | Como Marketeer, quero eliminar uma campanha sem criativos, para que não fiquem registos desnecessários. | 3 | 3.2 Campanhas atribuídas e eliminar campanha | Fabio |
| M06 | Como Marketeer, quero criar um novo criativo, para que fique registado no projeto do cliente. | 4 | 4.1 Criar, editar e eliminar criativos | Tomas |
| M07 | Como Marketeer, quero editar um criativo existente, para que a informação se mantenha atualizada. | 4 | 4.1 Criar, editar e eliminar criativos | Tomas |
| M08 | Como Marketeer, quero eliminar um criativo, para que não fiquem registos desnecessários. | 4 | 4.1 Criar, editar e eliminar criativos | Tomas |
| M09 | Como Marketeer, quero indicar o custo estimado de cada criativo, para que o cliente saiba quanto vai investir. | 4 | 4.2 Custo, prazo, público-alvo e plataforma | Ricardo |
| M10 | Como Marketeer, quero definir prazos para cada criativo, para que o cliente saiba quando estará pronto. | 4 | 4.2 Custo, prazo, público-alvo e plataforma | Ricardo |
| M11 | Como Marketeer, quero definir o público-alvo de cada criativo, para que o cliente perceba a quem se destina. | 4 | 4.2 Custo, prazo, público-alvo e plataforma | Ricardo |
| M12 | Como Marketeer, quero escolher a plataforma alvo, para que o cliente saiba onde o criativo vai ser publicado. | 4 | 4.2 Custo, prazo, público-alvo e plataforma | Ricardo |
| M13 | Como Marketeer, quero anexar o ficheiro ou a pré-visualização do criativo, para que o cliente veja o conteúdo. | 4 | 4.3 Criativos do cliente, com pesquisa e filtros | Fabio |
| M14 | Como Marketeer, quero atualizar o estado do criativo, para que o cliente acompanhe o progresso. | 4 | 4.4 Estados do criativo e aprovação pelo cliente | Tomas |
| M15 | Como Marketeer, quero ser avisado quando o custo dos criativos ultrapassa o budget da campanha, para que não exceda o investimento aprovado. | 4 | 4.6 Despesa face ao budget e aviso de budget ultrapassado | Fabio |
| M16 | Como Marketeer, quero dar parecer sobre os pedidos de alteração de budget, para que o Administrador saiba se são viáveis. | 5 | 5.2 Parecer do marketeer sobre os pedidos de budget | Ricardo |
| M17 | Como Marketeer, quero ver os comentários do cliente sobre um criativo, para que saiba o que ajustar. | 6 | 6.1 Comentários dos criativos e respostas | Ricardo |
| M18 | Como Marketeer, quero ser notificado quando recebo uma nova campanha, um pedido de budget ou um comentário, para que possa responder a tempo. | 6 | 6.2 Notificações na aplicação e por email | Fabio |

## Cliente

| ID | User story | Fase | Unidade | Quem fez |
|---|---|---|---|---|
| C01 | Como Cliente, quero fazer login na plataforma, para que possa aceder às minhas campanhas de forma segura. | 1 | 1.1 Login e logout dos três perfis | Tomas |
| C02 | Como Cliente, quero recuperar a minha password, para que possa voltar a aceder à conta se a esquecer. | 1 | 1.5 Recuperar a password | Ricardo |
| C03 | Como Cliente, quero alterar a minha password, para que possa manter a conta segura. | 1 | 1.4 Alterar a password e editar os meus dados | Tomas |
| C04 | Como Cliente, quero editar a minha informação, para que os meus dados estejam sempre atualizados. | 1 | 1.4 Alterar a password e editar os meus dados | Tomas |
| C05 | Como Cliente, quero pedir novas campanhas de marketing, para que a equipa comece a trabalhar nelas. | 3 | 3.3 Pedidos de nova campanha | Tomas |
| C06 | Como Cliente, quero acompanhar o estado dos meus pedidos, para que saiba em que fase estão. | 3 | 3.3 Pedidos de nova campanha | Tomas |
| C07 | Como Cliente, quero cancelar um pedido ainda pendente, para que possa desistir antes de ser analisado. | 3 | 3.3 Pedidos de nova campanha | Tomas |
| C08 | Como Cliente, quero ver as minhas campanhas e o budget atribuído a cada uma, para que saiba o estado do meu investimento. | 3 | 3.5 Campanhas do cliente e marketeer responsável | Fabio |
| C09 | Como Cliente, quero saber qual o marketeer responsável por cada campanha, para que saiba a quem me dirigir. | 3 | 3.5 Campanhas do cliente e marketeer responsável | Fabio |
| C10 | Como Cliente, quero ver a lista dos meus criativos com custo, prazo, público e plataforma, para que possa acompanhar o trabalho. | 4 | 4.5 Ficheiros dos criativos | Ricardo |
| C11 | Como Cliente, quero filtrar e pesquisar os meus criativos, para que encontre rapidamente o que procuro. | 4 | 4.5 Ficheiros dos criativos | Ricardo |
| C12 | Como Cliente, quero pré-visualizar e descarregar os ficheiros dos criativos, para que possa rever o conteúdo e usá-lo internamente. | 4 | 4.3 Criativos do cliente, com pesquisa e filtros | Fabio |
| C13 | Como Cliente, quero aprovar ou rejeitar um criativo em revisão, para que o marketeer saiba se pode avançar com a publicação. | 4 | 4.4 Estados do criativo e aprovação pelo cliente | Tomas |
| C14 | Como Cliente, quero ver a despesa total de cada campanha face ao budget, para que possa controlar o investimento. | 4 | 4.6 Despesa face ao budget e aviso de budget ultrapassado | Fabio |
| C15 | Como Cliente, quero pedir a alteração do budget de uma campanha, para que possa ajustar o investimento. | 5 | 5.1 Pedido de alteração de budget | Tomas |
| C16 | Como Cliente, quero ver o histórico de alterações de budget de cada campanha, para que tenha registo das mudanças feitas. | 5 | 5.3 Decisão dos pedidos de budget e histórico do budget | Fabio |
| C17 | Como Cliente, quero ser informado da decisão sobre o meu pedido de budget, para que saiba se foi aceite. | 6 | 6.2 Notificações na aplicação e por email | Fabio |
| C18 | Como Cliente, quero comentar ou sugerir alterações a um criativo, para que o marketeer saiba o que ajustar. | 6 | 6.1 Comentários dos criativos e respostas | Ricardo |
| C19 | Como Cliente, quero ser notificado quando um criativo é criado ou alterado, para que esteja sempre a par das mudanças. | 6 | 6.2 Notificações na aplicação e por email | Fabio |
| C20 | Como Cliente, quero exportar um relatório das minhas campanhas, para que possa partilhá-lo internamente. | 6 | 6.4 Relatório das campanhas em CSV | Ricardo |

## Como ler uma issue

Cada issue de user story tem quatro partes:

- **User story**: a frase do Trello, no formato "Como ..., quero ..., para que ...".
- **Descrição**: o que a story inclui na aplicação de linha de comandos.
- **Critérios de aceitação**: o que tem de funcionar para a story estar feita, escrito no início da unidade. As decisões do grupo sobre o que a story quer dizer ficaram aqui.
- **Planeamento**: o perfil, a fase e a unidade de trabalho.

Para ver as issues: [todas as user stories](https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+label%3A%22user+story%22).
