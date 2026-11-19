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
ficheiro ``app.db`` com a base de dados. A pasta ``dados`` não vai para o
Git.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Dentro da pasta de dados
     - O que é
   * - ``app.db``
     - A base de dados (ver :doc:`modelo_dados`).
   * - ``caixa_saida/``
     - Os emails que a aplicação "envia", um ficheiro de texto por email.
       É criada quando é enviado o primeiro.
   * - ``ficheiros/``
     - Os ficheiros anexados aos criativos, uma pasta por criativo. É
       criada quando é anexado o primeiro.

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
     - Pasta onde a aplicação guarda a base de dados, os emails simulados e
       os ficheiros dos criativos.

Exemplo, para usar uma pasta separada numa demonstração:

.. code-block:: console

   # PowerShell
   $env:GESTOR_CAMPANHAS_DADOS = "C:\demo\dados"
   python -m gestor_campanhas

   # Git Bash, Linux ou macOS
   GESTOR_CAMPANHAS_DADOS=/tmp/demo python -m gestor_campanhas

Para recomeçar com uma base de dados vazia, basta apagar a pasta de dados.

Algumas definições ficam guardadas na própria base de dados, na tabela
``configuracoes``. Enquanto não houver um valor guardado, a aplicação usa o
de :mod:`gestor_campanhas.config`:

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Definição
     - Por omissão
     - Onde se muda
   * - Minutos sem atividade ao fim dos quais a sessão termina
     - 15
     - Na tabela ``configuracoes``, com a chave ``minutos_inatividade``
       (:data:`~gestor_campanhas.config.MINUTOS_INATIVIDADE`).
   * - Dias sem mexer nos criativos ao fim dos quais um marketeer aparece
       como parado
     - 7
     - No menu do Administrador, em "Painel de marketeers", "Mudar os dias
       sem atividade" (:data:`~gestor_campanhas.config.DIAS_SEM_ATIVIDADE`).
   * - Minutos de validade do código de recuperação da password
     - 15
     - Só no código (:data:`~gestor_campanhas.config.MINUTOS_VALIDADE_CODIGO`).

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
