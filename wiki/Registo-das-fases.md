# Registo das fases

O que foi feito em cada fase do projeto, e por quem. Cada fase corresponde a uma milestone do repositório.

## Fase 0 — Arranque

Base do projeto, ainda sem user stories.

| Unidade | Quem fez | Quem reviu |
|---|---|---|
| 0.1 Estrutura do pacote Python | Fabio | Tomas |
| 0.2 Base de dados e menu inicial | Tomas | Ricardo |
| 0.3 Testes automáticos e integração contínua | Ricardo | Fabio |
| 0.4 Documentação base | Fabio | Tomas |

Resultado: a aplicação arranca, cria a base de dados e mostra o menu inicial; 20 testes automáticos; documentação Sphinx; 57 issues criadas a partir das user stories.

## Fase 1 — Autenticação e sessões

Release: **v0.1.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 1.1 Login e logout dos três perfis | A01, M01, C01 | Tomas | Ricardo |
| 1.2 Registo de sessões e saída por inatividade | A02 | Ricardo | Fabio |
| 1.3 Horários de entrada e saída dos marketeers | A03 | Fabio | Tomas |
| 1.4 Alterar a password e editar os meus dados | C03, C04 | Tomas | Ricardo |
| 1.5 Recuperar a password | C02 | Ricardo | Fabio |
| 1.6 Release v0.1.0 | — | Fabio | Tomas |

Resultado: 8 user stories concluídas; 104 testes automáticos; primeira versão publicada.

Decisões tomadas nesta fase:

- **Código em vez de link na recuperação da password.** A user story fala num link enviado por email. Na linha de comandos não há onde clicar, por isso é enviado um código de 6 algarismos, com validade de 15 minutos.
- **Emails simulados.** A aplicação escreve cada email num ficheiro de texto, em vez de o enviar.
- **Inatividade verificada ao responder.** A aplicação fica parada à espera do teclado, por isso a inatividade é detetada quando o utilizador responde a um menu.
- **Opções da conta em todos os perfis.** As user stories de alterar a password e editar os dados são do Cliente, mas as opções ficaram disponíveis para os três perfis.

## Fase 2 — Clientes e marketeers

Release: **v0.2.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 2.1 Lista de clientes com pesquisa | A04 | Fabio | Tomas |
| 2.2 Adicionar e editar clientes | A05, A06 | Tomas | Ricardo |
| 2.3 Desativar e reativar clientes | A07 | Ricardo | Fabio |
| 2.4 Adicionar e editar marketeers | A08, A09 | Fabio | Tomas |
| 2.5 Desativar e reativar marketeers | A10 | Tomas | Ricardo |
| 2.6 Release v0.2.0 | — | Tomas | Ricardo |

Resultado: 7 user stories concluídas (15 no total); 194 testes automáticos; segunda versão publicada.

Decisões tomadas nesta fase:

- **Remover é desativar.** As user stories falam em remover clientes e marketeers, mas pedem que o histórico se mantenha. A conta fica desativada, com os dados guardados, e pode ser reativada.
- **Password inicial aleatória.** Quem é adicionado recebe por email uma password gerada pela aplicação. O Administrador não a vê.
- **Os mesmos ecrãs para os dois perfis.** A gestão de marketeers reutiliza os ecrãs da gestão de clientes, que passaram a receber o perfil.
- **Pesquisa e ordenação sem acentos.** A pesquisa por nome e a ordem alfabética são feitas em Python, porque o SQLite põe as letras com acento depois do "z".
- **Duas partes adiadas para a Fase 3.** O número de campanhas ativas por cliente (A04) e a reatribuição das campanhas antes de desativar um marketeer (A10) dependem das campanhas, que ainda não existem.

O que correu mal e como se resolveu:

- **Release da Fase 1 junta ao ramo errado.** O pull request da release v0.1.0 foi junto ao `develop` em vez do `main`, e a tag ficou num commit sem código. Corrigiu-se com um pull request do `develop` para o `main` e refazendo a tag. O guia de trabalho passou a ter dois passos de confirmação do destino.

## Fase 3 — Campanhas e pedidos

Release: **v0.3.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 3.1 Criar e editar campanhas | M02, M03 | Ricardo | Fabio |
| 3.2 Campanhas atribuídas e eliminar campanha | M04, M05 | Fabio | Tomas |
| 3.3 Pedidos de nova campanha | C05, C06, C07 | Tomas | Ricardo |
| 3.4 Decidir pedidos, budget e marketeer responsável | A11, A12, A13 | Ricardo | Tomas |
| 3.5 Campanhas do cliente e marketeer responsável | C08, C09 | Fabio | Ricardo |
| 3.6 Release v0.3.0 | — | Ricardo | Fabio |

Resultado: 12 user stories concluídas (27 no total); 382 testes automáticos; terceira versão publicada.

Decisões tomadas nesta fase:

- **Duas maneiras de criar uma campanha.** O Marketeer cria-a diretamente, ou o Cliente pede-a e o Administrador aprova o pedido. Nos dois casos o budget é definido pelo Administrador.
- **Dinheiro em cêntimos.** O budget e o orçamento são guardados como números inteiros de cêntimos, para evitar os erros de arredondamento dos números decimais.
- **O estado da campanha é calculado.** Por começar, em curso e terminada resultam das datas, e não de uma coluna que alguém tivesse de atualizar.
- **O prazo do pedido passa a data de fim.** A campanha criada a partir de um pedido fica com o prazo como data de fim; o marketeer pode ajustar as datas.
- **Um pedido aberto deixa de poder ser cancelado.** Quando o Administrador abre um pedido, ele passa a "Em análise", e o cliente só pode cancelar pedidos pendentes.
- **Cada um só vê o que é seu.** O marketeer só vê as campanhas que lhe estão atribuídas; o cliente só vê as suas campanhas e os seus pedidos.
- **Partes da Fase 2 fechadas.** A lista de clientes ganhou o número de campanhas ativas (A04), e um marketeer com campanhas por terminar deixou de poder ser desativado (A10).
- **Partes adiadas.** O budget restante e os criativos por estado (M04) e a verificação "sem criativos" antes de eliminar (M05) ficam para a Fase 4; os pedidos de alteração de budget (C06, C08) ficam para a Fase 5.

O que correu mal e como se resolveu:

- **Release da Fase 2 junta outra vez ao ramo errado.** Apesar dos passos de confirmação, o pull request da release v0.2.0 foi junto ao `develop`, e a tag ficou no código da v0.1.0. Corrigiu-se como na Fase 1. O guia passou a dar um link que já abre o pull request com o `main` como destino, e a ter um passo, antes de criar a tag, para confirmar que o `main` já tem a versão nova.
- **Issues que ficaram abertas.** Dois pull requests foram abertos sem `Closes #número`, e as issues não fecharam sozinhas. Foram fechadas à mão, com um comentário a indicar o pull request.
- **Mensagem com o género errado.** A mensagem de atribuição de marketeer dizia "foi avisado" também para uma marketeer. Foi corrigida no ramo da release, com um commit do tipo `fix`.

## Fase 4 — Criativos

Release: **v0.4.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 4.1 Criar, editar e eliminar criativos | M06, M07, M08 | Tomas | Ricardo |
| 4.2 Custo, prazo, público-alvo e plataforma | M09, M10, M11, M12 | Ricardo | Fabio |
| 4.3 Criativos do cliente, com pesquisa e filtros | C10, C11 | Fabio | Tomas |
| 4.4 Estados do criativo e aprovação pelo cliente | M14, C13 | Tomas | Fabio |
| 4.5 Ficheiros dos criativos | M13, C12 | Ricardo | Tomas |
| 4.6 Despesa face ao budget e aviso de budget ultrapassado | C14, M15 | Fabio | Ricardo |
| 4.7 Release v0.4.0 | — | Fabio | Ricardo |

Resultado: 15 user stories concluídas (42 no total); 566 testes automáticos; quarta versão publicada.

Decisões tomadas nesta fase:

- **A ordem das unidades mudou.** A lista dos criativos do cliente passou para a unidade 4.3 e os ficheiros para a 4.5, porque a aprovação e o descarregar acontecem no menu de criativos do cliente, que tinha de existir primeiro.
- **A tabela dos criativos nasceu completa.** Foi criada na unidade 4.1 já com todas as colunas da fase, porque o `CREATE TABLE IF NOT EXISTS` não acrescenta colunas a uma tabela que já existe nos computadores de cada um.
- **Uma plataforma por criativo** (M12). O mesmo anúncio em duas plataformas tem formatos diferentes, por isso são dois criativos.
- **Um só prazo** (M10): a data de entrega, que não pode passar o fim da campanha. A publicação fica registada no estado "Publicado".
- **A rejeição tem um estado próprio** (C13). O criativo fica "Rejeitado", com o motivo à vista, e o marketeer decide quando o volta a preparar.
- **Sem filtro por intervalo de datas** (C11) e **sem data da última alteração** (M07), para manter a fase dentro do tempo.
- **A despesa é calculada.** A soma do custo dos criativos não é guardada, para nunca ficar desatualizada. O aviso de budget ultrapassado não impede guardar o criativo: o custo é uma estimativa.
- **Ficheiros fora da base de dados.** São copiados para `dados/ficheiros`, e a base de dados guarda só o nome. Os testes usam sempre uma pasta de dados temporária.
- **Partes da Fase 3 fechadas.** O budget restante e os criativos por estado (M04) e a regra "só se eliminam campanhas sem criativos" (M05).

O que correu mal e como se resolveu:

- **Issues que ficaram abertas.** O pull request da unidade 3.3 não fechou as issues C05, C06 e C07, e a milestone da Fase 3 não chegou aos 100%. Foram fechadas à mão.
- **Um ramo criado antes do tempo.** O ramo da unidade 3.5 tinha sido criado num `develop` antigo, e o `copiar.py` recusou continuar; ao criar o ramo outra vez, apareceu `a branch named ... already exists`. Apagou-se o ramo antigo e criou-se de novo. O passo "Atualiza as duas pastas e cria o ramo" passou a explicar este caso.

## Fase 5 — Budget

Release: **v0.5.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 5.1 Pedido de alteração de budget | C15 | Tomas | Ricardo |
| 5.2 Parecer do marketeer | M16 | Ricardo | Fabio |
| 5.3 Decisão dos pedidos e histórico do budget | A14, A15, C16 | Fabio | Tomas |
| 5.4 Resumo global do budget | A16 | Tomas | Ricardo |
| 5.5 Release v0.5.0 | — | Tomas | Fabio |

Resultado: 6 user stories concluídas (48 no total); 707 testes automáticos; quinta versão publicada.

Decisões tomadas nesta fase:

- **Os pedidos de budget ficam ao lado dos pedidos de campanha.** O cliente vê e gere os dois tipos na mesma opção, "Pedidos de campanha", em duas listas. Como têm numerações próprias, cada tipo tem as suas opções de ver e de cancelar. Assim fica concluída a parte de C06 que faltava.
- **Primeiro o parecer, depois a decisão.** O Administrador só decide um pedido que já tenha o parecer do marketeer (A15). O parecer ajuda, mas não obriga: um pedido "Não viável" pode ser aprovado.
- **Aprovar é alterar.** Aprovar um pedido muda logo o budget da campanha para o valor pedido. Para outro valor, o Administrador usa "Definir budget", que passou a pedir o motivo.
- **Um pedido por decidir de cada vez, por campanha**, para não haver dois valores pedidos ao mesmo tempo para o mesmo budget. Uma campanha terminada já não aceita pedidos.
- **Todo o budget tem histórico** (C16). Não só os pedidos aprovados: também o budget inicial e as alterações diretas do Administrador. Todas passam pela mesma função, para o histórico nunca falhar uma.
- **O resumo é calculado** (A16), como a despesa. O budget de cada cliente soma só as campanhas que já têm budget; a despesa soma todas.
- **Notificações ficam para a Fase 6.** O aviso ao cliente sobre a decisão (C17) e ao marketeer sobre um pedido novo (M18) entram com as notificações. Até lá, o cliente vê a decisão na lista dos seus pedidos.

O que correu mal e como se resolveu:

- **Issues que ficaram abertas.** Os pull requests das unidades 5.1 e 5.4 foram juntos sem a linha `Closes #` com o número verdadeiro, e as issues C15 e A16 não fecharam sozinhas. Foram fechadas à mão, com um comentário a indicar o pull request. A página da Fase 6 lembra que quem revê tem de confirmar esta linha antes de juntar.
- **`No module named pytest` depois de reinstalar o Python.** Um Python novo vem sem as ferramentas de desenvolvimento. Resolveu-se com `python -m pip install -r requirements-dev.txt`, como no passo de preparação.

## Fase 6 — Comentários, notificações, painel e relatório

Release: **v0.6.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 6.1 Comentários dos criativos e respostas | C18, M17 | Ricardo | Fabio |
| 6.2 Notificações na aplicação e por email | C17, C19, M18 | Fabio | Tomas |
| 6.3 Painel de marketeers | A17, A18, A19 | Tomas | Ricardo |
| 6.4 Relatório das campanhas em CSV | C20 | Ricardo | Fabio |
| 6.5 Release v0.6.0 | — | Ricardo | Fabio |

Resultado: 9 user stories concluídas (as 57 do projeto); 863 testes automáticos; sexta versão publicada.

Decisões tomadas nesta fase:

- **Só o cliente comenta; o marketeer responde** (C18, M17). Os comentários e as respostas ficam na mesma tabela; não se responde a uma resposta, e os comentários não se editam nem se apagam.
- **Notificações na aplicação e por email** (C17, C19, M18). As duas, e não uma ou outra. Abrir uma notificação mostra logo o item a que se refere.
- **O cliente sabe tudo o que acontece aos seus criativos** (C19), incluindo as respostas aos comentários. O Administrador não recebe notificações.
- **A carga de trabalho conta os criativos pelo prazo** (A18). Concluídos são os aprovados e os publicados; em atraso, os que ainda têm trabalho por fazer com o prazo já passado.
- **"Sem atividade" tem duas causas** (A19): não ter criativos ativos, ou não mexer nos criativos há 7 dias ou mais (o número muda-se no painel). A atividade só começou a ser registada nesta fase, numa tabela própria; os criativos anteriores contam pela data de criação.
- **O relatório é em CSV** (C20), preparado para abrir no Excel em português.
- **Partes da Fase 5 fechadas.** Os avisos sobre os pedidos de budget (C17 e M18).

## Fases seguintes

| Fase | Tema | User stories | Release |
|---|---|---|---|
| 7 | Fecho e entrega | — | v1.0.0 |
