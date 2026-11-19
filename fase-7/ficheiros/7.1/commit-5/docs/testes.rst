Testes
======

Os testes automáticos estão na pasta ``tests`` e usam o pytest.

Correr os testes
----------------

Com as ferramentas de desenvolvimento instaladas (ver :doc:`instalacao`), a
partir da pasta do projeto:

.. code-block:: console

   python -m pytest

Para ver o nome de cada teste, acrescentar ``-v``. Para correr só um ficheiro,
indicar o caminho:

.. code-block:: console

   python -m pytest -v tests/test_bd.py

Organização
-----------

Há um ficheiro de testes por parte da aplicação, e dois que olham para a
aplicação no seu conjunto: ``test_fluxos.py`` e ``test_dados_demo.py``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Ficheiro
     - O que testa
   * - ``tests/conftest.py``
     - Não tem testes: define as peças partilhadas (*fixtures*).
   * - ``tests/test_bd.py``
     - Ligação à base de dados, criação das tabelas e caminhos de dados.
   * - ``tests/test_cli.py``
     - Funções comuns dos menus, menu inicial e ponto de entrada.
   * - ``tests/test_validacao.py``
     - Validação dos dados escritos pelo utilizador (nomes, emails, datas).
   * - ``tests/test_dinheiro.py``
     - Conversão de valores em euros para cêntimos e de volta.
   * - ``tests/test_autenticacao.py``
     - Passwords, entrada na aplicação e menus de cada perfil.
   * - ``tests/test_sessoes.py``
     - Registo das entradas e saídas e fim da sessão por inatividade.
   * - ``tests/test_horarios.py``
     - Horários de entrada e saída dos marketeers.
   * - ``tests/test_recuperacao.py``
     - Recuperação da password e envio simulado de emails.
   * - ``tests/test_contas.py``
     - Alteração da própria password e dos próprios dados.
   * - ``tests/test_gestao.py``
     - Gestão de clientes e de marketeers pelo Administrador.
   * - ``tests/test_campanhas.py``
     - Campanhas do Marketeer: criar, editar, consultar e eliminar.
   * - ``tests/test_pedidos.py``
     - Pedidos de campanha do Cliente.
   * - ``tests/test_administracao.py``
     - Decisões do Administrador sobre pedidos de campanha, budget e marketeer.
   * - ``tests/test_campanhas_cliente.py``
     - Campanhas vistas pelo Cliente.
   * - ``tests/test_criativos.py``
     - Criativos: dados, estados, aprovação pelo cliente, filtros e despesa.
   * - ``tests/test_ficheiros.py``
     - Ficheiros anexados aos criativos.
   * - ``tests/test_budget.py``
     - Pedidos de alteração de budget e parecer do marketeer.
   * - ``tests/test_decisao_budget.py``
     - Decisão dos pedidos de alteração de budget e histórico do budget.
   * - ``tests/test_resumo_budget.py``
     - Resumo global do budget.
   * - ``tests/test_comentarios.py``
     - Comentários dos criativos e respostas.
   * - ``tests/test_notificacoes.py``
     - Notificações na aplicação e por email.
   * - ``tests/test_painel.py``
     - Painel de marketeers: trabalho, carga e inatividade.
   * - ``tests/test_relatorios.py``
     - Relatório das campanhas em CSV.
   * - ``tests/test_fluxos.py``
     - Fluxos completos, com os três perfis (ver abaixo).
   * - ``tests/test_dados_demo.py``
     - Resultado final dos dados de demonstração.

Fluxos completos
----------------

Os testes de ``tests/test_fluxos.py`` seguem o caminho que as pessoas fazem
na aplicação, de uma ponta à outra, e confirmam que o que um perfil faz
chega aos outros:

* **da conta nova à entrada**: o Administrador cria a conta, a password
  chega por email, a pessoa entra e troca a password; uma conta desativada
  deixa de entrar;
* **do pedido de campanha ao criativo publicado**: o Cliente pede a
  campanha, o Administrador aprova-a com o budget e o marketeer, o Marketeer
  cria o criativo, anexa o ficheiro e envia-o para revisão, o Cliente
  comenta e o Marketeer responde, o Cliente aprova e o Marketeer publica. No
  fim confirmam-se as notificações e os emails de cada perfil, o painel de
  marketeers e o relatório do cliente;
* **o criativo rejeitado**: o Cliente rejeita, o Marketeer corrige e volta
  a enviar, o Cliente aprova;
* **o pedido de budget**: a despesa passa o budget, o Cliente pede mais, o
  Marketeer dá parecer e o Administrador aprova ou rejeita; confirma-se o
  budget, o histórico e o resumo global.

Os passos usam as funções das regras de negócio (``servicos``), pela ordem
em que os menus as chamam. O relógio da aplicação avança um minuto entre
passos, para as notificações e os emails ficarem pela ordem certa.

Fixtures
--------

Uma *fixture* é uma peça que o pytest prepara antes de cada teste e entrega
ao teste que a pede pelo nome.

``ligacao``
   Base de dados em memória, já com as tabelas criadas. Cada teste recebe uma
   base de dados nova, por isso os testes não interferem uns com os outros nem
   tocam nos dados reais.

``teclado``
   Simula o que o utilizador escreve. Por exemplo, ``teclado("9", "0")``
   responde ``9`` à primeira pergunta e ``0`` à segunda.

``contas``
   Uma conta de cada perfil (Administrador, Marketeer e Cliente), todas com
   a mesma password.

``emails``
   Dá acesso aos emails que a aplicação escreveu na caixa de saída.

Há ainda duas que se aplicam a todos os testes sem ser preciso pedi-las:
uma põe a pasta de dados numa pasta temporária, para nenhum teste mexer nos
ficheiros da pasta ``dados`` do projeto, e outra torna o cálculo das
passwords mais rápido.

O pytest fornece outras, usadas em alguns testes: ``capsys`` (lê o que foi
escrito no ecrã), ``tmp_path`` (pasta temporária) e ``monkeypatch`` (altera
temporariamente variáveis de ambiente e funções). Os testes que dependem do
dia ou da hora usam o ``monkeypatch`` para substituir o relógio da aplicação
(:func:`gestor_campanhas.relogio.agora`).

Integração contínua
-------------------

O ficheiro ``.github/workflows/testes.yml`` corre os testes no GitHub Actions
em cada *push* e em cada *pull request* para os ramos ``main`` e ``develop``,
com a versão mínima suportada do Python e com uma versão recente. O resultado
aparece no próprio *pull request*.
