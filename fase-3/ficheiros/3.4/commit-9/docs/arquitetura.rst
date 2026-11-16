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
     modelos.py           classes de dados (Utilizador, Campanha, PedidoCampanha), perfis e estados
     erros.py             erros que os menus mostram ao utilizador
     relogio.py           data e hora atuais
     seguranca.py         hash das passwords
     dinheiro.py          conversão de valores em euros para cêntimos e vice-versa
     dados_demo.py        cria as contas, as campanhas e os pedidos de demonstração
     repositorios/        leitura e escrita na base de dados, uma tabela por módulo
     servicos/            regras de negócio, um assunto por módulo
     cli/                 menus da linha de comandos
       comum.py           funções partilhadas por todos os menus
       principal.py       menu inicial e entrada na aplicação
       perfis.py          menu de cada perfil
       admin.py           opções do menu do Administrador
       gestao.py          gestão de clientes e marketeers, pelo Administrador
       campanhas.py       campanhas, nos menus do Marketeer e do Administrador
       pedidos.py         pedidos de campanha, nos menus do Cliente e do Administrador
       conta.py           opções da conta, comuns a todos os perfis
       recuperacao.py     recuperação da password
   tests/                 testes automáticos (pytest)
   docs/                  esta documentação (Sphinx)
   dados/                 criada no primeiro arranque; não vai para o Git

Camadas
-------

O código está separado por responsabilidades. Cada camada só conhece as que
estão abaixo dela:

.. code-block:: text

   __main__        arranca a aplicação
      |
      v
   cli             mostra menus, lê respostas, apresenta resultados
      |
      v
   servicos        regras de negócio: decide o que é permitido
      |
      v
   repositorios    lê e escreve na base de dados (único sítio com SQL)
      |
      v
   bd              abre a ligação e cria as tabelas
      |
      v
   SQLite          ficheiro dados/app.db

Três regras orientam esta separação:

* **Os menus não tomam decisões.** O pacote ``cli`` limita-se a perguntar e a
  mostrar. As regras ficam em ``servicos``, que não lê do teclado nem escreve
  no ecrã, e por isso pode ser testado diretamente.
* **Os erros esperados são exceções próprias.** Quando uma regra não é
  cumprida, o serviço lança um erro de :mod:`gestor_campanhas.erros`. O menu
  apanha-o e mostra a mensagem.
* **A ligação à base de dados é passada como argumento.** Só o ponto de
  entrada abre a ligação; os outros módulos recebem-na já aberta. Assim, os
  testes podem entregar uma base de dados em memória em vez da verdadeira.

Exemplo: entrar na aplicação
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. :func:`gestor_campanhas.cli.principal.entrar` pede o email e a password.
2. :func:`gestor_campanhas.servicos.autenticacao.autenticar` procura o
   utilizador, confirma a password e verifica se a conta está ativa.
3. :mod:`gestor_campanhas.repositorios.utilizadores` faz as consultas SQL.
4. :func:`gestor_campanhas.seguranca.verificar_password` compara a password
   com o hash guardado.
5. Se tudo estiver certo, :func:`gestor_campanhas.cli.perfis.executar` mostra
   o menu do perfil. Se não, é lançado
   :class:`~gestor_campanhas.erros.ErroAutenticacao` e o menu mostra a
   mensagem.

Exemplo: adicionar um cliente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. :func:`gestor_campanhas.cli.gestao.adicionar` pede os dados no ecrã.
2. :func:`gestor_campanhas.servicos.gestao.criar` valida-os com
   :mod:`gestor_campanhas.servicos.validacao`, confirma que o email ainda não
   tem conta e gera a password inicial.
3. :func:`gestor_campanhas.repositorios.utilizadores.criar` guarda a conta,
   com o hash da password.
4. :func:`gestor_campanhas.servicos.correio.enviar` envia as credenciais.
5. Se algum dado não for válido, o serviço lança
   :class:`~gestor_campanhas.erros.ErroValidacao` antes de guardar seja o que
   for, e o menu mostra a mensagem.

Os mesmos ecrãs e as mesmas funções servem para os marketeers: o perfil é
passado como argumento. O que muda de um perfil para o outro está em
:data:`gestor_campanhas.cli.gestao.NOMES` e
:data:`gestor_campanhas.cli.gestao.ACOES`.

Exemplo: aprovar um pedido de campanha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. :func:`gestor_campanhas.cli.pedidos.decidir` pede o número do pedido e
   mostra-o. :func:`gestor_campanhas.servicos.pedidos.analisar` passa-o de
   pendente para em análise.
2. :func:`gestor_campanhas.cli.pedidos.aprovar` pede o nome da campanha, o
   budget inicial e o marketeer responsável.
3. :func:`gestor_campanhas.servicos.pedidos.aprovar` confirma que o pedido
   ainda está por decidir, valida os dados, cria a campanha com
   :func:`gestor_campanhas.repositorios.campanhas.criar` e marca o pedido
   como aprovado, com o número da campanha.
4. :func:`gestor_campanhas.servicos.correio.enviar` avisa o cliente e o
   marketeer.

Se algum dado não for válido, o serviço lança
:class:`~gestor_campanhas.erros.ErroValidacao` antes de criar a campanha, e o
pedido continua em análise.

Contas desativadas
------------------

Remover um cliente ou um marketeer não apaga a linha da tabela
``utilizadores``: põe a coluna ``ativo`` a zero. Assim, as sessões já
registadas (e, nas fases seguintes, as campanhas) continuam ligadas a uma
conta que existe. Uma conta desativada não pode entrar nem recuperar a
password, e pode ser reativada.

Um marketeer só pode ser desativado quando já não for responsável por
campanhas por terminar. A verificação está em
:func:`gestor_campanhas.servicos.gestao.definir_estado`.

Dinheiro
--------

Os valores em euros (o budget de uma campanha e o orçamento de um pedido)
são guardados em cêntimos, como números inteiros. O módulo
:mod:`gestor_campanhas.dinheiro` converte o que o utilizador escreve em
cêntimos e os cêntimos no texto que é mostrado.

Passwords
---------

A aplicação nunca guarda passwords. Guarda um hash calculado com PBKDF2
(SHA-256), com um *salt* aleatório por conta, no formato
``algoritmo$iterações$salt$hash``. Ver :mod:`gestor_campanhas.seguranca`.

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

Sessões e inatividade
---------------------

Quando alguém entra, :func:`gestor_campanhas.servicos.sessoes.iniciar` regista
uma linha na tabela ``sessoes`` com a hora de entrada. A saída é registada por
:func:`gestor_campanhas.servicos.sessoes.terminar`, com o motivo.

O limite de inatividade é de 15 minutos por omissão
(:data:`gestor_campanhas.config.MINUTOS_INATIVIDADE`) e pode ser alterado na
tabela ``configuracoes``, com a chave ``minutos_inatividade``.

Uma aplicação de linha de comandos fica parada enquanto espera pelo teclado,
por isso a inatividade é verificada quando o utilizador responde a um menu.
Se nesse momento o limite já tiver passado, a sessão é dada como terminada à
hora em que o limite foi atingido, e é preciso entrar de novo.

Emails
------

A aplicação não envia emails verdadeiros.
:func:`gestor_campanhas.servicos.correio.enviar` escreve cada mensagem num
ficheiro de texto da pasta ``caixa_saida``, dentro da pasta de dados. O resto
da aplicação chama essa função como se o email fosse mesmo enviado, por isso
trocar a simulação por um envio a sério só obriga a alterar esse módulo.

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
   * - ``utilizadores``
     - Uma linha por conta: nome, email (único), hash da password, perfil
       (``administrador``, ``marketeer`` ou ``cliente``), se está ativa,
       telefone e, para os clientes, empresa e NIF.
   * - ``sessoes``
     - Uma linha por entrada na aplicação: utilizador, hora de entrada, hora
       de saída e motivo da saída (``logout`` ou ``inatividade``).
   * - ``recuperacoes``
     - Uma linha por pedido de recuperação de password: utilizador, hash do
       código, prazo de validade e se já foi usado.
   * - ``campanhas``
     - Uma linha por campanha: nome, objetivo, cliente a quem pertence,
       marketeer responsável, budget em cêntimos (vazio enquanto não for
       definido) e datas de início e de fim.
   * - ``pedidos_campanha``
     - Uma linha por pedido de nova campanha: cliente, objetivo, orçamento em
       cêntimos, prazo, plataformas, estado (``pendente``, ``em_analise``,
       ``aprovado``, ``rejeitado`` ou ``cancelado``), motivo da rejeição e
       campanha a que deu origem.
