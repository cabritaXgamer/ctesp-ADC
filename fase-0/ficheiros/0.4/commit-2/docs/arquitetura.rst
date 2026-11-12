Arquitetura
===========

A aplicação é um programa de linha de comandos escrito apenas com a biblioteca
padrão do Python. Os dados ficam numa base de dados SQLite, que é um único
ficheiro e não precisa de servidor.

Estrutura de pastas
-------------------

.. code-block:: text

   gestor_campanhas/      código da aplicação
     __init__.py          versão da aplicação
     __main__.py          ponto de entrada (python -m gestor_campanhas)
     config.py            caminhos da pasta de dados e da base de dados
     bd.py                ligação SQLite e criação das tabelas
     cli/                 menus da linha de comandos
       comum.py           funções partilhadas por todos os menus
       principal.py       menu inicial
   tests/                 testes automáticos (pytest)
   docs/                  esta documentação (Sphinx)
   dados/                 criada no primeiro arranque; não vai para o Git

Camadas
-------

O código está separado por responsabilidades. Cada camada só conhece a que
está abaixo dela:

.. code-block:: text

   __main__        arranca a aplicação
      |
      v
   cli             mostra menus, lê respostas, apresenta resultados
      |
      v
   bd              abre a ligação e cria as tabelas
      |
      v
   SQLite          ficheiro dados/app.db

Duas regras orientam esta separação:

* **Os menus não tomam decisões.** O pacote ``cli`` limita-se a perguntar e a
  mostrar. As regras da aplicação ficam em módulos próprios, que podem ser
  testados sem simular o teclado.
* **A ligação à base de dados é passada como argumento.** Só o ponto de
  entrada abre a ligação; os outros módulos recebem-na já aberta. Assim, os
  testes podem entregar uma base de dados em memória em vez da verdadeira.

Arranque
--------

Quando se executa ``python -m gestor_campanhas``:

1. :func:`gestor_campanhas.cli.comum.configurar_terminal` garante que os
   acentos são lidos e escritos em UTF-8.
2. :func:`gestor_campanhas.bd.iniciar_bd` abre o ficheiro da base de dados
   (criando a pasta, se for preciso) e cria as tabelas em falta.
3. :func:`gestor_campanhas.cli.principal.executar` mostra o menu inicial até
   o utilizador escolher sair.
4. A ligação à base de dados é fechada, mesmo que o programa seja
   interrompido com Ctrl+C.

Base de dados
-------------

As tabelas são criadas a partir da constante :data:`gestor_campanhas.bd.ESQUEMA`.
Todas as instruções usam ``CREATE TABLE IF NOT EXISTS``, por isso podem ser
executadas em todos os arranques sem apagar dados.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Tabela
     - Conteúdo
   * - ``configuracoes``
     - Pares chave/valor com definições que podem ser alteradas durante a
       utilização da aplicação.
