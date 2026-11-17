Utilização
==========

Contas de demonstração
----------------------

Uma instalação nova não tem contas. Para experimentar a aplicação, cria-se
as contas e as campanhas de demonstração com:

.. code-block:: console

   python -m gestor_campanhas.dados_demo

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Perfil
     - Email
     - Password
   * - Administrador
     - ``admin@agencia.pt``
     - ``admin12345``
   * - Marketeer
     - ``marketeer@agencia.pt``
     - ``marketeer12345``
   * - Marketeer
     - ``marta@agencia.pt``
     - ``marta12345``
   * - Cliente
     - ``cliente@empresa.pt``
     - ``cliente12345``
   * - Cliente
     - ``jose@padaria.pt``
     - ``jose12345``
   * - Cliente
     - ``beatriz@bicicletas.pt``
     - ``beatriz12345``

Estas passwords são públicas e servem só para demonstração.

São também criadas três campanhas: ``Natal 2026`` e ``Regresso às aulas``, do
marketeer ``marketeer@agencia.pt``, e ``Bicicletas de primavera``, da
marketeer ``marta@agencia.pt``. Ficam também dois pedidos de campanha
pendentes, um do cliente ``jose@padaria.pt`` e outro da cliente
``beatriz@bicicletas.pt``, e quatro criativos: dois na campanha
``Natal 2026``, um em ``Regresso às aulas`` e um em ``Bicicletas de
primavera``. O comando pode ser repetido: só acrescenta o que faltar.

Entrar e sair
-------------

.. code-block:: console

   python -m gestor_campanhas

No menu inicial, a opção **1. Entrar** pede o email e a password. A password
não aparece no ecrã enquanto é escrita. Se as credenciais estiverem certas,
abre-se o menu do perfil da conta; se não, aparece a mensagem
``Email ou password incorretos.`` e volta-se ao menu inicial.

A mensagem é a mesma quando o email não existe e quando a password está
errada, para não revelar que emails têm conta.

Em qualquer menu de perfil, a opção **0. Terminar sessão** volta ao menu
inicial.

Recuperar a password
--------------------

No menu inicial, a opção **2. Recuperar a password** serve para quem se
esqueceu da password.

1. A aplicação pede o email da conta e envia para lá um código de seis
   algarismos.
2. Com o código, define-se a password nova, escrita duas vezes.

O código vale durante 15 minutos e só pode ser usado uma vez. Um pedido novo
anula o código anterior. A resposta da aplicação é a mesma quer o email tenha
conta quer não.

.. note::

   Os emails são simulados: cada mensagem é um ficheiro de texto na pasta
   ``dados/caixa_saida``. Para ver o código, abre-se o ficheiro mais recente
   dessa pasta.

Sessões e inatividade
---------------------

Cada entrada e cada saída ficam registadas, com data e hora.

Se o utilizador estiver mais de 15 minutos sem responder a um menu, a sessão
termina sozinha: ao responder, aparece o aviso de que a sessão terminou por
inatividade e é preciso entrar de novo. A saída fica registada à hora em que
os 15 minutos se completaram.

.. note::

   No terminal Git Bash a password aparece no ecrã enquanto é escrita, porque
   esse terminal não permite escondê-la. No PowerShell, na Linha de Comandos
   e no terminal do VS Code fica escondida.

A minha conta
-------------

Estas duas opções aparecem no menu de todos os perfis.

Editar os meus dados
~~~~~~~~~~~~~~~~~~~~

Mostra os dados da conta e pede cada um, com o valor atual entre parênteses
retos. Com Enter, o valor mantém-se.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Dado
     - Regras
   * - Email
     - Não pode ser alterado.
   * - Nome
     - Não pode ficar vazio.
   * - Telefone
     - Vazio, ou 9 a 15 algarismos, com ou sem ``+`` no início.
   * - Empresa
     - Só é pedida aos clientes.
   * - NIF
     - Só é pedido aos clientes. Vazio ou 9 algarismos.

Se algum valor não respeitar as regras, nenhum dado é alterado.

Alterar a password
~~~~~~~~~~~~~~~~~~

Pede a password atual e a nova, duas vezes. A password nova tem de ter pelo
menos 8 caracteres e ser diferente da atual.

Administrador
-------------

Clientes
~~~~~~~~

Mostra todos os clientes, por ordem alfabética do nome, com a empresa, o
email, o telefone, o estado da conta e o número de campanhas ativas. As
contas desativadas também aparecem.

Por baixo da lista aparecem as opções de gestão. Depois de cada uma, a lista
volta a ser mostrada, já com as alterações.

**Pesquisar por nome** mostra só os clientes cujo nome contém o texto
escrito, em qualquer posição. A pesquisa não distingue maiúsculas nem acentos:
``jose`` encontra ``José Padeiro``. Com Enter, voltam a aparecer todos.

.. code-block:: text

   N.º  Nome           Empresa                  Email                  Telefone   Estado  Campanhas ativas
   ---  -------------  -----------------------  ---------------------  ---------  ------  ----------------
   5    Beatriz Lopes  Bicicletas do Sul, Lda.  beatriz@bicicletas.pt  910000005  Ativa   1
   3    Carla Cliente  Empresa Exemplo, Lda.    cliente@empresa.pt     910000003  Ativa   1
   4    José Padeiro   Padaria Central, Lda.    jose@padaria.pt        910000004  Ativa   0

   3 clientes.

O número da primeira coluna identifica o cliente nas outras opções de gestão.

Uma campanha conta como ativa enquanto não terminar: conta se estiver em
curso ou por começar.

Adicionar cliente
^^^^^^^^^^^^^^^^^

Pede os dados do cliente e cria a conta.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Dado
     - Regras
   * - Nome
     - Obrigatório.
   * - Email
     - Obrigatório, na forma ``nome@empresa.pt``. Não pode ser igual ao de
       outra conta, de qualquer perfil.
   * - Telefone
     - Opcional. 9 a 15 algarismos, com ou sem ``+`` no início.
   * - Empresa
     - Opcional.
   * - NIF
     - Opcional. 9 algarismos.

A conta começa com uma password aleatória. O email e a password são enviados
para o email do cliente, com o pedido de trocar a password na primeira vez
que entrar. O Administrador não chega a ver a password.

.. note::

   Como os emails são simulados, a mensagem com as credenciais fica na pasta
   ``dados/caixa_saida``.

Editar cliente
^^^^^^^^^^^^^^

Pede o número do cliente e mostra cada dado, com o valor atual entre
parênteses retos. Com Enter, o valor mantém-se. As regras são as mesmas de
quando se adiciona um cliente.

A password do cliente não é alterada. Se o email mudar, o cliente passa a
entrar com o email novo. Se algum valor não respeitar as regras, nenhum dado
é alterado.

Desativar ou reativar cliente
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pede o número do cliente, mostra o estado atual da conta e pede confirmação
antes de o alterar.

Um cliente com a conta desativada deixa de poder entrar e de poder recuperar
a password. A conta não é apagada: continua na lista, com o estado
``Desativada``, e os seus dados e o seu histórico mantêm-se. A mesma opção
reativa a conta, e o cliente volta a entrar com a password que tinha.

Nos dois casos, o cliente recebe um email a avisar da alteração.

Marketeers
~~~~~~~~~~

Funciona como a opção **Clientes**: mostra a lista dos marketeers, por ordem
alfabética do nome, e por baixo as opções de gestão.

.. code-block:: text

   N.º  Nome              Email                 Telefone   Estado  Campanhas ativas
   ---  ----------------  --------------------  ---------  ------  ----------------
   6    Marta Marques     marta@agencia.pt      910000006  Ativa   1
   2    Miguel Marketeer  marketeer@agencia.pt  910000002  Ativa   1

   2 marketeers.

**Pesquisar por nome**, **Adicionar marketeer** e **Editar marketeer** seguem
as regras descritas para os clientes, com uma diferença: um marketeer não tem
empresa nem NIF, por isso esses dados não são pedidos nem aparecem na lista.

O marketeer novo recebe por email as credenciais de acesso, tal como um
cliente novo.

**Desativar ou reativar marketeer** também funciona como nos clientes: pede
confirmação, a conta desativada deixa de poder entrar e o marketeer é avisado
por email. As sessões que o marketeer já fez continuam a aparecer nos
horários de entrada e saída.

Um marketeer que seja responsável por campanhas ativas não pode ser
desativado. A aplicação diz quantas campanhas são; primeiro atribui-se cada
uma a outro marketeer, na opção **Campanhas**, e só depois se desativa a
conta.

Pedidos de campanha
~~~~~~~~~~~~~~~~~~~

Mostra os pedidos de nova campanha de todos os clientes. Os que estão por
decidir (``Pendente`` e ``Em análise``) aparecem primeiro, do mais antigo
para o mais recente.

.. code-block:: text

   N.º  Feito em    Cliente        Objetivo                            Orçamento   Prazo       Estado
   ---  ----------  -------------  ----------------------------------  ----------  ----------  --------
   1    2026-11-16  José Padeiro   Divulgar o bolo-rei no Natal        600,00 €    2026-12-15  Pendente
   2    2026-11-16  Beatriz Lopes  Dar a conhecer a loja nova de Faro  1 200,00 €  2027-02-28  Pendente

   2 pedidos, 2 por decidir.

Analisar pedido
^^^^^^^^^^^^^^^

Pede o número do pedido e mostra todos os dados dele. Um pedido ``Pendente``
passa a ``Em análise`` assim que é aberto, e o cliente deixa de o poder
cancelar. Depois, a aplicação pergunta a decisão:

**Aprovar e criar a campanha** pede o nome da campanha, o budget inicial e o
marketeer responsável. O budget proposto é o orçamento do pedido; com Enter,
mantém-se. O marketeer escolhe-se pelo número, na lista dos marketeers com a
conta ativa. A campanha é criada com o objetivo do pedido e com o prazo do
pedido como data de fim. O cliente e o marketeer são avisados por email.

**Rejeitar** pede o motivo, que é obrigatório, e uma confirmação. O cliente é
avisado por email, com o motivo, e passa a vê-lo na opção **Ver pedido**.

**Decidir mais tarde** deixa o pedido ``Em análise``.

Um pedido aprovado, rejeitado ou cancelado já não pode ser decidido.

Campanhas
~~~~~~~~~

Mostra as campanhas de todos os marketeers, com o cliente, o marketeer
responsável, as datas, o budget e o estado.

.. code-block:: text

   N.º  Nome                     Cliente        Marketeer         Início      Fim         Budget       Estado
   ---  -----------------------  -------------  ----------------  ----------  ----------  -----------  -----------
   1    Natal 2026               Carla Cliente  Miguel Marketeer  2026-12-01  2026-12-24  1 500,00 €   Por começar
   2    Regresso às aulas        José Padeiro   Miguel Marketeer  2026-09-01  2026-09-30  800,00 €     Terminada
   3    Bicicletas de primavera  Beatriz Lopes  Marta Marques     -           -           Por definir  Em curso

   3 campanhas.

**Definir budget** pede o número da campanha e o valor em euros, que tem de
ser maior do que zero. Serve para as campanhas criadas pelos marketeers, que
começam sem budget, e para corrigir um budget já atribuído.

**Atribuir marketeer** pede o número da campanha e o do marketeer que passa
a ser responsável, escolhido na lista dos marketeers com a conta ativa. O
marketeer anterior deixa de ver a campanha e o novo é avisado por email.

Horários de entrada e saída dos marketeers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mostra as sessões dos marketeers, da mais recente para a mais antiga, com a
hora de entrada, a hora de saída, a duração e o motivo da saída.

A aplicação pergunta primeiro o período. As duas datas são opcionais e
escrevem-se no formato ``AAAA-MM-DD``; com Enter, esse limite não é aplicado.
O último dia do período é incluído por inteiro.

.. code-block:: text

   Marketeer         Entrada           Saída             Duração  Motivo
   ----------------  ----------------  ----------------  -------  -----------------
   Miguel Marketeer  2026-11-11 14:00  2026-11-11 14:15  0h15     Inatividade
   Miguel Marketeer  2026-11-10 09:00  2026-11-10 12:30  3h30     Terminou a sessão

Uma sessão que ainda não terminou aparece com ``(em curso)`` na coluna da
saída.


Marketeer
---------

Campanhas
~~~~~~~~~

Mostra as campanhas de que o marketeer é responsável (as que criou e as que
o Administrador lhe atribuiu) e, por baixo, as opções para as gerir. Depois de cada opção, a lista volta a ser mostrada, já com as
alterações. Um marketeer só vê e só altera as suas campanhas.

.. code-block:: text

   N.º  Nome               Cliente        Início      Fim         Budget      Estado
   ---  -----------------  -------------  ----------  ----------  ----------  -----------
   1    Natal 2026         Carla Cliente  2026-12-01  2026-12-24  1 500,00 €  Por começar
   2    Regresso às aulas  José Padeiro   2026-09-01  2026-09-30  800,00 €    Terminada

   2 campanhas.

O número da primeira coluna identifica a campanha nas outras opções.

O budget aparece como ``Por definir`` enquanto o Administrador não o
atribuir. O estado é calculado a partir das datas:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Estado
     - Quando
   * - ``Por começar``
     - A data de início ainda não chegou.
   * - ``Em curso``
     - Já começou e ainda não terminou. É também o estado de uma campanha
       sem datas.
   * - ``Terminada``
     - A data de fim já passou.

Criar campanha
^^^^^^^^^^^^^^

Mostra os clientes com a conta ativa e pede os dados da campanha. Quem cria a
campanha fica responsável por ela.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Dado
     - Regras
   * - Cliente
     - Obrigatório. Escreve-se o número do cliente, que está na lista
       mostrada. Tem de ser um cliente com a conta ativa.
   * - Nome
     - Obrigatório.
   * - Objetivo
     - Opcional.
   * - Data de início
     - Opcional, no formato ``AAAA-MM-DD``.
   * - Data de fim
     - Opcional, no formato ``AAAA-MM-DD``. Não pode ser anterior à data de
       início.

A campanha começa sem budget, porque o budget é definido pelo Administrador.
Se algum valor não respeitar as regras, a campanha não é criada.

Editar campanha
^^^^^^^^^^^^^^^

Pede o número da campanha e mostra o nome, o objetivo e as datas, com o valor
atual entre parênteses retos. Com Enter, o valor mantém-se. Para apagar uma
data, escreve-se ``-``.

O cliente e o budget não são alterados aqui. Se algum valor não respeitar as
regras, nenhum dado é alterado.

Ver campanha
^^^^^^^^^^^^

Pede o número da campanha e mostra todos os dados dela, incluindo o objetivo,
que não cabe na lista, e quantos criativos a campanha tem em cada estado:

.. code-block:: text

     Criativos: 3 (Em preparação: 2, Em revisão: 1)

Eliminar campanha
^^^^^^^^^^^^^^^^^

Pede o número da campanha, mostra os dados dela e pede confirmação. Uma
campanha eliminada não pode ser recuperada. Um marketeer só pode eliminar as
suas campanhas.

Uma campanha com criativos não pode ser eliminada: aparece uma mensagem com
o número de criativos que ela tem. Primeiro eliminam-se os criativos, na
opção **Criativos**, e depois a campanha.

Criativos
~~~~~~~~~

Um criativo é uma peça de uma campanha: uma imagem, um vídeo ou um texto que
vai ser publicado. A opção mostra as campanhas do marketeer e pede o número
de uma delas. Depois mostra os criativos dessa campanha e, por baixo, as
opções para os gerir.

.. code-block:: text

   ============================================================
   Criativos da campanha Natal 2026 (Carla Cliente)
   ============================================================
   N.º  Nome             Custo     Prazo       Público-alvo               Plataforma  Estado
   ---  ---------------  --------  ----------  -------------------------  ----------  -------------
   1    Banner de Natal  400,00 €  2026-11-25  Famílias da região de...   Facebook    Em preparação
   2    Vídeo da montra  900,00 €  2026-11-28  Jovens adultos, 18 a 3...  Instagram   Em preparação

   2 criativos.

O custo aparece como ``Por definir`` e os outros dados como ``-`` enquanto
não forem indicados. Um público-alvo comprido aparece cortado e terminado em
``...``; o texto completo está em **Ver criativo**.

Um criativo novo fica no estado ``Em preparação``. O número da primeira
coluna identifica o criativo nas outras opções. Com **0. Voltar** volta-se à
escolha da campanha, e com Enter nessa pergunta volta-se ao menu do perfil.

Criar criativo
^^^^^^^^^^^^^^

Pede os dados do criativo, que fica na campanha escolhida. Só o nome é
obrigatório: os outros dados podem ser indicados mais tarde, em **Editar
criativo**.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Dado
     - Regras
   * - Nome
     - Obrigatório.
   * - Descrição
     - Opcional.
   * - Custo estimado
     - Opcional. Valor em euros, por exemplo ``400`` ou ``399,90``.
   * - Prazo
     - Opcional, no formato ``AAAA-MM-DD``. Não pode ser depois da data de
       fim da campanha.
   * - Público-alvo
     - Opcional. Texto livre, por exemplo ``Pais de alunos do básico``.
   * - Plataforma
     - Opcional. Escolhe-se pelo número, numa lista com Facebook, Instagram,
       Google Ads, LinkedIn, TikTok e YouTube.

Se algum valor não respeitar as regras, o criativo não é criado.

Editar criativo
^^^^^^^^^^^^^^^

Só se pode editar um criativo ``Em preparação`` ou ``Rejeitado``. Um
criativo em revisão está a ser visto pelo cliente, e um aprovado ou publicado
já foi aceite tal como está.

Pede o número do criativo e mostra cada dado, com o valor atual entre
parênteses retos. Com Enter, o valor mantém-se; para apagar um valor,
escreve-se ``-``. As regras são as mesmas de quando se cria o criativo, e se
algum valor não as respeitar nenhum dado é alterado. Só se podem escolher
criativos da campanha que está a ser vista.

Ver criativo
^^^^^^^^^^^^

Pede o número do criativo e mostra todos os dados dele, um por linha,
incluindo a descrição e o público-alvo completo.

Eliminar criativo
^^^^^^^^^^^^^^^^^

Pede o número do criativo, mostra os dados dele e pede confirmação. Um
criativo eliminado não pode ser recuperado. Um criativo ``Publicado`` não
pode ser eliminado.

Atualizar estado
^^^^^^^^^^^^^^^^

Pede o número do criativo, mostra o estado atual e as mudanças permitidas a
partir dele. O caminho normal de um criativo é este:

.. code-block:: text

   Em preparação --> Em revisão --> Aprovado --> Publicado
                          |
                          +-------> Rejeitado --> Em preparação ou Em revisão

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Estado atual
     - O que o marketeer pode fazer
   * - ``Em preparação``
     - Enviar ao cliente para revisão.
   * - ``Em revisão``
     - Voltar a pôr em preparação. A aprovação e a rejeição são do cliente.
   * - ``Rejeitado``
     - Voltar a pôr em preparação, ou enviar outra vez para revisão. O motivo
       da rejeição aparece no ecrã.
   * - ``Aprovado``
     - Marcar como publicado.
   * - ``Publicado``
     - Nada: é o estado final.

Com **0. Deixar como está**, o estado não muda.

Anexar ficheiro
^^^^^^^^^^^^^^^

Pede o número do criativo e o caminho de um ficheiro no computador, por
exemplo ``C:\Users\ana\Imagens\banner.png``. No Windows, o caminho pode
ser copiado no Explorador de Ficheiros: botão direito no ficheiro,
**Copiar como caminho**. As aspas à volta do caminho são ignoradas.

O ficheiro é copiado para a pasta ``ficheiros`` da pasta de dados, por isso
o original pode depois ser apagado ou mudado de sítio. Cada criativo tem um
só ficheiro: anexar outro substitui o anterior. Tal como os outros dados, o
ficheiro só pode ser mudado enquanto o criativo está ``Em preparação`` ou
``Rejeitado``.

Para experimentar, o projeto tem o ficheiro ``exemplos/banner-natal.svg``.

Pré-visualizar ficheiro
^^^^^^^^^^^^^^^^^^^^^^^

Pede o número do criativo e mostra o nome, o tipo e o tamanho do ficheiro:

.. code-block:: text

   Ficheiro do criativo Banner de Natal
     Nome:     banner-natal.svg
     Tipo:     Imagem (image/svg+xml)
     Tamanho:  639 bytes

   Abrir o ficheiro no programa predefinido? (s/n)

Com ``s``, o ficheiro abre-se no programa que o sistema usa para esse tipo
de ficheiro (por exemplo, o browser para um ``.svg``).

Cliente
-------

Pedidos de campanha
~~~~~~~~~~~~~~~~~~~

Mostra os pedidos de nova campanha feitos pelo cliente, do mais recente para
o mais antigo, e por baixo as opções para os gerir. Um cliente só vê os seus
pedidos.

.. code-block:: text

   N.º  Feito em    Objetivo                      Orçamento  Prazo       Estado
   ---  ----------  ----------------------------  ---------  ----------  --------
   1    2026-11-16  Divulgar o bolo-rei no Natal  600,00 €   2026-12-15  Pendente

   1 pedido.

Um objetivo com mais de 40 caracteres aparece cortado na lista; a opção
**Ver pedido** mostra-o completo.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Estado
     - Significado
   * - ``Pendente``
     - Ainda ninguém analisou o pedido. É o único estado em que o cliente o
       pode cancelar.
   * - ``Em análise``
     - O Administrador já abriu o pedido, mas ainda não decidiu.
   * - ``Aprovado``
     - O pedido foi aceite e deu origem a uma campanha.
   * - ``Rejeitado``
     - O pedido foi recusado. O motivo aparece em **Ver pedido**.
   * - ``Cancelado``
     - O cliente desistiu do pedido.

Novo pedido
^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Dado
     - Regras
   * - Objetivo
     - Obrigatório.
   * - Orçamento
     - Obrigatório, em euros e maior do que zero. Aceita ``1500``,
       ``1500,50`` e ``1500.50``.
   * - Prazo pretendido
     - Obrigatório, no formato ``AAAA-MM-DD``. Não pode ser um dia que já
       passou.
   * - Plataformas
     - Pelo menos uma. A aplicação mostra as plataformas numeradas e
       escreve-se os números das escolhidas, separados por vírgulas
       (por exemplo ``1,2``).

O pedido fica no estado ``Pendente``. Se algum valor não respeitar as regras,
o pedido não é registado.

Ver pedido
^^^^^^^^^^

Pede o número do pedido e mostra todos os dados dele. Num pedido rejeitado
aparece o motivo; num pedido aprovado aparece o número da campanha criada.

Cancelar pedido
^^^^^^^^^^^^^^^

Pede o número do pedido, mostra os dados dele e pede confirmação. Só um
pedido ``Pendente`` pode ser cancelado. O pedido cancelado não é apagado:
continua na lista, com o estado ``Cancelado``.

Campanhas
~~~~~~~~~

Mostra as campanhas do cliente, com as datas, o budget, o estado e o
marketeer responsável. Um cliente só vê as suas campanhas.

.. code-block:: text

   N.º  Nome        Início      Fim         Budget      Estado       Marketeer
   ---  ----------  ----------  ----------  ----------  -----------  ----------------
   1    Natal 2026  2026-12-01  2026-12-24  1 500,00 €  Por começar  Miguel Marketeer

   1 campanha.
   O budget de cada campanha é definido pelo administrador.

Uma campanha que ainda não tem budget atribuído aparece na lista com
``Por definir`` na coluna do budget. O cliente não altera o budget.

**Ver campanha e marketeer responsável** pede o número da campanha e mostra
todos os dados dela, incluindo o objetivo, e os contactos do marketeer
responsável:

.. code-block:: text

   Marketeer responsável
     Nome:      Miguel Marketeer
     Email:     marketeer@agencia.pt
     Telefone:  910000002

Criativos
~~~~~~~~~

Mostra os criativos de todas as campanhas do cliente, numa só lista, com a
campanha, o custo, o prazo, o público-alvo, a plataforma e o estado de cada
um. Um cliente só vê os criativos das suas campanhas.

.. code-block:: text

   N.º  Nome             Campanha    Custo     Prazo       Público-alvo               Plataforma  Estado
   ---  ---------------  ----------  --------  ----------  -------------------------  ----------  -------------
   1    Banner de Natal  Natal 2026  400,00 €  2026-11-25  Famílias da região de...   Facebook    Em preparação
   2    Vídeo da montra  Natal 2026  900,00 €  2026-11-28  Jovens adultos, 18 a 3...  Instagram   Em preparação

   2 criativos.

Os criativos aparecem agrupados por campanha. O cliente não altera nada
nesta lista: os criativos são criados e alterados pelo marketeer.

**Filtrar e pesquisar** faz quatro perguntas, por esta ordem. Com Enter, a
pergunta não filtra nada:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Pergunta
     - O que filtra
   * - Texto a procurar
     - Criativos com esse texto no nome, na descrição ou no público-alvo, em
       qualquer posição. Não distingue maiúsculas nem acentos: ``familias``
       encontra ``Famílias``.
   * - Campanha
     - Escolhe-se pelo número, numa lista com as campanhas do cliente.
   * - Plataforma
     - Escolhe-se pelo número, numa lista com as seis plataformas.
   * - Estado
     - Escolhe-se pelo número, numa lista com os estados de um criativo.

Os criativos que respeitam todos os filtros aparecem com o título
``Criativos encontrados``. Se nenhum respeitar, aparece
``Nenhum criativo corresponde aos filtros.`` Depois de Enter, volta a lista
completa.

**Ver criativo** pede o número do criativo e mostra todos os dados dele,
incluindo a descrição e o público-alvo completo.

Por baixo da lista aparece quantos criativos estão à espera de aprovação,
por exemplo ``Há 1 criativo à espera da sua aprovação.``

**Aprovar ou rejeitar criativo** pede o número de um criativo
``Em revisão``, mostra os dados dele e pergunta a decisão:

.. code-block:: text

   ============================================================
   Decisão
   ============================================================
     1. Aprovar
     2. Rejeitar
     0. Decidir mais tarde

Um criativo aprovado pode ser publicado pelo marketeer. Para rejeitar, é
obrigatório escrever o motivo, que o marketeer vê quando atualiza o estado.
Com **0. Decidir mais tarde**, o criativo continua em revisão. Os criativos
noutros estados não podem ser aprovados nem rejeitados.

**Pré-visualizar ficheiro** funciona como no menu do Marketeer: mostra o
nome, o tipo e o tamanho do ficheiro e pergunta se o deve abrir.

**Descarregar ficheiro** guarda uma cópia do ficheiro numa pasta à escolha.
Com Enter, a cópia vai para a pasta ``Downloads`` (Transferências) da pasta
pessoal. Se já houver um ficheiro com o mesmo nome, a cópia fica com um
número entre parênteses, por exemplo ``banner-natal (1).svg``: nenhum
ficheiro é apagado.
