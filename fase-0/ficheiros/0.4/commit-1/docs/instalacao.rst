Instalação e configuração
=========================

Requisitos
----------

* Python 3.10 ou superior.
* Git, para obter o código.

A aplicação usa apenas a biblioteca padrão do Python: para a correr não é
preciso instalar mais nada.

Obter o código
--------------

.. code-block:: console

   git clone https://github.com/Blive77/ADC-TrabGrupo
   cd ADC-TrabGrupo

Correr a aplicação
------------------

A partir da pasta do projeto:

.. code-block:: console

   python -m gestor_campanhas

No primeiro arranque a aplicação cria a pasta ``dados`` e, dentro dela, o
ficheiro ``app.db`` com a base de dados.

Configuração
------------

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Variável de ambiente
     - Valor por omissão
     - Para que serve
   * - ``GESTOR_CAMPANHAS_DADOS``
     - ``dados`` (na pasta do projeto)
     - Pasta onde a aplicação guarda a base de dados.

Exemplo, para usar uma pasta separada numa demonstração:

.. code-block:: console

   # PowerShell
   $env:GESTOR_CAMPANHAS_DADOS = "C:\demo\dados"
   python -m gestor_campanhas

   # Git Bash, Linux ou macOS
   GESTOR_CAMPANHAS_DADOS=/tmp/demo python -m gestor_campanhas

Para recomeçar com uma base de dados vazia, basta apagar a pasta de dados.

Ambiente de desenvolvimento
---------------------------

Os testes e a documentação precisam de duas ferramentas, o pytest e o Sphinx.
Recomenda-se instalá-las num ambiente virtual:

.. code-block:: console

   python -m venv .venv

   # PowerShell
   .venv\Scripts\Activate.ps1
   # Git Bash
   source .venv/Scripts/activate
   # Linux ou macOS
   source .venv/bin/activate

   python -m pip install -r requirements-dev.txt

Gerar esta documentação
-----------------------

.. code-block:: console

   python -m sphinx -b html docs docs/_build/html

O resultado fica em ``docs/_build/html/index.html``.

Em alternativa, dentro da pasta ``docs``, pode usar-se ``make html`` (Linux,
macOS e Git Bash) ou ``make.bat html`` (Windows).
