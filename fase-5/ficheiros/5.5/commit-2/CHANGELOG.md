# Registo de alterações

Todas as alterações relevantes da aplicação, por versão. Cada versão corresponde a uma fase do projeto.

## v0.5.0 — Budget (2026-11-19)

### Acrescentado

- Pedidos de alteração de budget: o Cliente pede um budget diferente para uma campanha que ainda não terminou, indicando o valor e o motivo. Cada campanha só pode ter um pedido por decidir de cada vez.
- A opção "Pedidos de campanha" do Cliente mostra os pedidos de nova campanha e, por baixo, os pedidos de alteração de budget, com as opções para pedir, ver e cancelar cada tipo.
- Parecer do Marketeer: na opção nova "Pedidos de budget", o marketeer responsável vê os pedidos das suas campanhas, com a despesa atual, e diz se cada um é viável, com uma justificação. Com o parecer, o pedido passa a "Em análise".
- Decisão do Administrador: na opção nova "Pedidos de budget", vê os pedidos de todas as campanhas, com o parecer do marketeer, e aprova-os ou rejeita-os. Aprovar altera logo o budget da campanha para o valor pedido; rejeitar obriga a indicar o motivo.
- Histórico do budget de cada campanha, com o valor anterior, o valor novo, a data e o motivo de cada alteração, na opção "Campanhas" do Cliente e do Administrador.
- Resumo global do budget, na opção nova "Resumo do budget" do Administrador: budget atribuído, despesa e restante de cada cliente, com os totais, as campanhas acima do budget em destaque e o detalhe das campanhas de cada cliente.
- Um pedido de alteração de budget de demonstração e o budget inicial das campanhas de demonstração no histórico.

### Alterado

- "Definir budget", no menu do Administrador, pede o motivo quando a campanha já tem budget, e recusa um valor igual ao atual. Todas as alterações do budget ficam no histórico, incluindo o budget inicial de uma campanha criada a partir de um pedido de campanha.
- As opções de ver e de cancelar pedidos do Cliente passam a chamar-se "Ver pedido de campanha" e "Cancelar pedido de campanha", porque os pedidos de budget têm as suas próprias opções.
- Os menus do Marketeer e do Administrador ganharam as opções "Pedidos de budget" e, no Administrador, "Resumo do budget". As opções que vinham a seguir mudaram de número.
- Uma campanha apagada leva consigo os pedidos de alteração de budget e o histórico do budget dela.

### User stories concluídas

C15, M16, A14, A15, C16 e A16.

Fica também concluída a parte de C06 (os pedidos de alteração de budget na lista de pedidos do cliente) que tinha sido adiada na versão 0.3.0.

O aviso ao cliente quando o pedido de budget é decidido (C17) e o aviso ao marketeer quando chega um pedido de budget (M18) entram na versão 0.6.0, com as notificações. Até lá, o cliente vê a decisão na lista dos seus pedidos.

## v0.4.0 — Criativos (2026-11-18)

### Acrescentado

- Criativos: o Marketeer cria, edita, consulta e elimina os criativos de cada uma das suas campanhas, na opção "Criativos" do seu menu.
- Custo estimado, prazo, público-alvo e plataforma de cada criativo. O prazo não pode passar a data de fim da campanha.
- Estados de um criativo: em preparação, em revisão, aprovado, rejeitado e publicado. O Marketeer envia o criativo ao cliente para revisão e marca-o como publicado depois de aprovado.
- Aprovação pelo Cliente: aprova ou rejeita os criativos em revisão; a rejeição tem de ter um motivo, que o marketeer vê.
- Ficheiros: o Marketeer anexa um ficheiro a cada criativo, que é copiado para a pasta `dados/ficheiros`. O Marketeer e o Cliente pré-visualizam o ficheiro (nome, tipo e tamanho) e abrem-no no programa predefinido; o Cliente descarrega uma cópia para uma pasta à escolha.
- Opção "Criativos" no menu do Cliente, com os criativos de todas as suas campanhas e a pesquisa e os filtros por campanha, plataforma e estado.
- Despesa de cada campanha (a soma do custo dos criativos) e budget restante, nas listas e nos detalhes das campanhas do Marketeer e do Cliente.
- Aviso ao Marketeer quando o custo dos criativos ultrapassa o budget da campanha.
- Número de criativos de cada campanha em cada estado, em "Ver campanha".
- Criativos de demonstração e o ficheiro de exemplo `exemplos/banner-natal.svg`.

### Alterado

- Uma campanha com criativos já não pode ser eliminada: primeiro eliminam-se os criativos.
- Um criativo só pode ser editado em preparação ou depois de rejeitado, e um criativo publicado não pode ser eliminado.
- Os valores negativos em euros são escritos com o sinal à frente, por exemplo `-200,00 €`.
- Os testes usam sempre uma pasta de dados temporária, para nunca mexerem na pasta `dados` do projeto.

### User stories concluídas

M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, C10, C11, C12, C13 e C14.

Ficam também concluídas as partes de M04 (budget restante e criativos por estado) e de M05 (só eliminar campanhas sem criativos) que tinham sido adiadas na versão 0.3.0.

## v0.3.0 — Campanhas e pedidos de campanha (2026-11-17)

### Acrescentado

- Campanhas: o Marketeer cria campanhas para um cliente, edita o nome, o objetivo e as datas, vê os detalhes e elimina as suas campanhas, com pedido de confirmação.
- Lista das campanhas atribuídas a cada marketeer, com o cliente, as datas, o budget e o estado (por começar, em curso ou terminada), calculado a partir das datas.
- Pedidos de nova campanha: o Cliente indica o objetivo, o orçamento, o prazo e as plataformas, acompanha o estado de cada pedido e pode cancelar os que ainda estão pendentes.
- Decisão dos pedidos pelo Administrador: ao aprovar, é criada a campanha, com o budget inicial e o marketeer responsável; ao rejeitar, é indicado o motivo. O cliente é avisado por email nos dois casos.
- Opção "Campanhas" no menu do Administrador, com as campanhas de todos os marketeers, para definir o budget e atribuir o marketeer responsável. O marketeer é avisado por email.
- Opção "Campanhas" no menu do Cliente, com o budget de cada campanha e os contactos do marketeer responsável.
- Número de campanhas ativas de cada conta, nas listas de clientes e de marketeers.
- Campanhas e pedidos de demonstração, criados com `python -m gestor_campanhas.dados_demo`.

### Alterado

- Um marketeer só pode ser desativado depois de as suas campanhas por terminar serem atribuídas a outro marketeer.
- Os valores em euros são guardados em cêntimos, como números inteiros.
- O menu do Administrador ganhou as opções "Pedidos de campanha" e "Campanhas", a seguir a "Marketeers".

### User stories concluídas

M02, M03, M04, M05, C05, C06, C07, C08, C09, A11, A12 e A13.

Ficam também concluídas as partes de A04 (campanhas ativas de cada cliente) e de A10 (reatribuição das campanhas antes de desativar um marketeer) que tinham sido adiadas na versão 0.2.0.

Três pontos dependem dos criativos e entram na versão 0.4.0: o budget restante e o número de criativos por estado, na lista do marketeer (M04), e a verificação de que uma campanha não tem criativos antes de ser eliminada (M05). Os pedidos de alteração de budget, referidos em C06, entram na versão 0.5.0.

## v0.2.0 — Clientes e marketeers (2026-11-16)

### Acrescentado

- Lista de clientes no menu do Administrador, por ordem alfabética, com pesquisa por nome que não distingue maiúsculas nem acentos.
- Adicionar clientes: a conta é criada com uma password aleatória e as credenciais são enviadas por email.
- Editar os dados de um cliente: nome, email, telefone, empresa e NIF.
- Desativar e reativar clientes, com pedido de confirmação. A conta desativada deixa de poder entrar, mas os dados mantêm-se.
- Lista de marketeers, com as mesmas opções: pesquisar, adicionar, editar, desativar e reativar.
- Aviso por email a quem tem a conta desativada ou reativada.
- Mais contas de demonstração: três clientes e dois marketeers.

### Alterado

- As regras de validação do nome, do email, do telefone e do NIF passaram para um módulo próprio, usado tanto pelo próprio utilizador como pelo Administrador.
- O menu do Administrador passa a começar pelas opções "Clientes" e "Marketeers".

### User stories concluídas

A04, A05, A06, A07, A08, A09 e A10.

O número de campanhas ativas na lista de clientes (A04) e a reatribuição das campanhas antes de desativar um marketeer (A10) entram na versão 0.3.0, com as campanhas.

## v0.1.0 — Autenticação e sessões (2026-11-14)

### Acrescentado

- Entrada na aplicação com email e password, para os três perfis: Administrador, Marketeer e Cliente.
- Menu próprio de cada perfil, com a opção de terminar a sessão.
- Passwords guardadas com hash e salt (PBKDF2), nunca em texto.
- Registo de todas as entradas e saídas, com data, hora e motivo da saída.
- Saída automática ao fim de 15 minutos sem atividade.
- Consulta, pelo Administrador, dos horários de entrada e saída dos marketeers, com filtro por datas.
- Edição dos próprios dados (nome, telefone e, nos clientes, empresa e NIF).
- Alteração da própria password.
- Recuperação da password com um código enviado por email, válido durante 15 minutos.
- Envio de emails simulado: cada mensagem é um ficheiro de texto na pasta `dados/caixa_saida`.
- Contas de demonstração, criadas com `python -m gestor_campanhas.dados_demo`.

### User stories concluídas

A01, A02, A03, M01, C01, C02, C03 e C04.

## v0.0.0 — Arranque

### Acrescentado

- Estrutura do projeto e ponto de entrada (`python -m gestor_campanhas`).
- Base de dados SQLite criada no arranque e menu inicial.
- Testes automáticos com o pytest e integração contínua no GitHub Actions.
- Documentação do código com o Sphinx, README e guia de contribuição.
