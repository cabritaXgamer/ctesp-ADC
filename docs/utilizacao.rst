Utilização
==========

Contas de demonstração
----------------------

Uma instalação nova não tem contas. Para experimentar a aplicação, cria-se
as contas de demonstração com:

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
email, o telefone e o estado da conta. As contas desativadas também aparecem.

Por baixo da lista aparecem as opções de gestão. Depois de cada uma, a lista
volta a ser mostrada, já com as alterações.

**Pesquisar por nome** mostra só os clientes cujo nome contém o texto
escrito, em qualquer posição. A pesquisa não distingue maiúsculas nem acentos:
``jose`` encontra ``José Padeiro``. Com Enter, voltam a aparecer todos.

.. code-block:: text

   N.º  Nome           Empresa                  Email                  Telefone   Estado
   ---  -------------  -----------------------  ---------------------  ---------  ------
   5    Beatriz Lopes  Bicicletas do Sul, Lda.  beatriz@bicicletas.pt  910000005  Ativa
   3    Carla Cliente  Empresa Exemplo, Lda.    cliente@empresa.pt     910000003  Ativa
   4    José Padeiro   Padaria Central, Lda.    jose@padaria.pt        910000004  Ativa

   3 clientes.

O número da primeira coluna identifica o cliente nas outras opções de gestão.

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

Marketeers
~~~~~~~~~~

Funciona como a opção **Clientes**: mostra a lista dos marketeers, por ordem
alfabética do nome, e por baixo as opções de gestão.

.. code-block:: text

   N.º  Nome              Email                 Telefone   Estado
   ---  ----------------  --------------------  ---------  ------
   6    Marta Marques     marta@agencia.pt      910000006  Ativa
   2    Miguel Marketeer  marketeer@agencia.pt  910000002  Ativa

   2 marketeers.

**Pesquisar por nome**, **Adicionar marketeer** e **Editar marketeer** seguem
as regras descritas para os clientes, com uma diferença: um marketeer não tem
empresa nem NIF, por isso esses dados não são pedidos nem aparecem na lista.

O marketeer novo recebe por email as credenciais de acesso, tal como um
cliente novo.

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

