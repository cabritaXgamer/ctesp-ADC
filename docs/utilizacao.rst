Utilização
==========

Contas de demonstração
----------------------

Uma instalação nova não tem contas. Para experimentar a aplicação, cria-se
uma conta de cada perfil com:

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
   * - Cliente
     - ``cliente@empresa.pt``
     - ``cliente12345``

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
