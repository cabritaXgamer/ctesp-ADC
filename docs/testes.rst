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

O pytest fornece outras, usadas em alguns testes: ``capsys`` (lê o que foi
escrito no ecrã), ``tmp_path`` (pasta temporária) e ``monkeypatch`` (altera
temporariamente variáveis de ambiente e funções).

Integração contínua
-------------------

O ficheiro ``.github/workflows/testes.yml`` corre os testes no GitHub Actions
em cada *push* e em cada *pull request* para os ramos ``main`` e ``develop``,
com a versão mínima suportada do Python e com uma versão recente. O resultado
aparece no próprio *pull request*.
