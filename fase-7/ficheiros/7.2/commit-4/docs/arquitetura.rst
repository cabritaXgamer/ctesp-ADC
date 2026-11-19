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
     config.py            caminhos da pasta de dados e valores por omissão das definições
     bd.py                ligação SQLite e criação das tabelas
     modelos.py           classes de dados (uma por tabela), perfis, estados e plataformas
     erros.py             erros que os menus mostram ao utilizador
     relogio.py           data e hora atuais
     seguranca.py         hash das passwords
     dinheiro.py          conversão de valores em euros para cêntimos e vice-versa
     dados_demo.py        cria os dados de demonstração
     repositorios/        leitura e escrita na base de dados, uma tabela por módulo
     servicos/            regras de negócio, um assunto por módulo
     cli/                 menus da linha de comandos
       comum.py           funções partilhadas por todos os menus
       principal.py       menu inicial e entrada na aplicação
       perfis.py          menu de cada perfil
       admin.py           opções do menu do Administrador
       gestao.py          gestão de clientes e marketeers, pelo Administrador
       campanhas.py       campanhas, nos menus dos três perfis
       criativos.py       criativos, nos menus do Marketeer e do Cliente
       pedidos.py         pedidos de campanha, nos menus do Cliente e do Administrador
       budget.py          pedidos de alteração de budget, histórico e resumo do budget
       notificacoes.py    notificações, nos menus do Marketeer e do Cliente
       painel.py          painel de marketeers, no menu do Administrador
       conta.py           opções da conta, comuns a todos os perfis
       recuperacao.py     recuperação da password
   exemplos/              ficheiros para experimentar a aplicação
   tests/                 testes automáticos (pytest)
   docs/                  esta documentação (Sphinx)
   dados/                 criada no primeiro arranque; não vai para o Git
     app.db               base de dados
     caixa_saida/         emails "enviados"
     ficheiros/           ficheiros dos criativos, uma pasta por criativo

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

Os valores em euros (o budget de uma campanha, o orçamento de um pedido e
o custo de um criativo) são guardados em cêntimos, como números inteiros. O módulo
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

Notificações
------------

Todas as notificações passam por
:func:`gestor_campanhas.servicos.notificacoes.notificar`, que faz duas
coisas: guarda a notificação na tabela ``notificacoes`` e envia o mesmo
texto por email. O email acaba com uma linha a dizer onde está o item no
menu de quem o recebe, tirada do dicionário
:data:`gestor_campanhas.servicos.notificacoes.ONDE`.

Quem decide quem é notificado são as regras de cada assunto, no fim de cada
operação que corre bem: :mod:`gestor_campanhas.servicos.campanhas` (campanha
atribuída), :mod:`gestor_campanhas.servicos.budget` (pedido novo e
decisão), :mod:`gestor_campanhas.servicos.criativos` (criativo criado,
alterado, eliminado, mudança de estado e ficheiro) e
:mod:`gestor_campanhas.servicos.comentarios` (comentário e resposta). Como a
notificação é a última coisa a acontecer, uma operação recusada por uma
regra não notifica ninguém.

Cada notificação guarda o tipo do item (coluna ``sobre``: ``campanha``,
``pedido_budget`` ou ``criativo``) e o número dele (``item_id``). A coluna
``item_id`` não é uma chave estrangeira, porque aponta para tabelas
diferentes conforme o tipo. Ao abrir a notificação,
:func:`gestor_campanhas.cli.notificacoes.mostrar_item` procura o item com as
mesmas funções que os menus usam (por exemplo
:func:`gestor_campanhas.servicos.criativos.obter_do_cliente`), por isso um
utilizador nunca vê, por uma notificação antiga, um item a que já não tem
acesso.

Base de dados
-------------

As tabelas, as relações entre elas, a forma como cada valor é guardado e o
que acontece quando se apaga uma campanha ou um criativo estão descritos em
:doc:`modelo_dados`.

Estados de um criativo
----------------------

As mudanças de estado que o marketeer pode fazer estão no dicionário
:data:`gestor_campanhas.servicos.criativos.PROXIMOS_ESTADOS`: a chave é o
estado atual e o valor são os estados para onde pode passar. O menu "Atualizar
estado" mostra só essas opções, e
:func:`gestor_campanhas.servicos.criativos.mudar_estado` recusa qualquer
outra. A aprovação e a rejeição são do cliente, em
:func:`gestor_campanhas.servicos.criativos.aprovar` e
:func:`gestor_campanhas.servicos.criativos.rejeitar`, e só valem para
criativos em revisão.

Ter as regras num dicionário, em vez de espalhadas por vários ``if``, faz com
que acrescentar ou retirar uma mudança seja alterar uma linha.

Ficheiros dos criativos
-----------------------

A tabela ``criativos`` guarda só o nome do ficheiro anexado. O ficheiro em si
fica em ``ficheiros/<número do criativo>/``, dentro da pasta de dados (ver
:func:`gestor_campanhas.config.pasta_ficheiros`). Guardar uma cópia, em vez
do caminho do original, faz com que o ficheiro continue disponível mesmo que
o original seja apagado ou mudado de sítio.

O módulo :mod:`gestor_campanhas.servicos.ficheiros` trata só dos ficheiros:
copia-os, descreve-os, abre-os e apaga-os. As regras sobre quem pode anexar e
quando estão em :mod:`gestor_campanhas.servicos.criativos`. Quando um
criativo é eliminado, a pasta dele também é apagada.

Os testes nunca mexem na pasta ``dados`` do projeto: a *fixture*
``dados_temporarios``, em ``tests/conftest.py``, põe a pasta de dados numa
pasta temporária em todos os testes, e a *fixture* ``aberturas`` substitui a
abertura de ficheiros, para não aparecerem janelas.

Despesa e budget restante
-------------------------

A despesa de uma campanha não é guardada: é calculada sempre que é precisa,
somando o custo dos criativos. Assim, nunca fica desatualizada quando um
criativo muda de custo ou é eliminado. Para as listas, que mostram várias
campanhas, :func:`gestor_campanhas.servicos.criativos.despesas` faz uma só
consulta com ``GROUP BY`` e devolve a despesa de todas as campanhas de uma
vez, em vez de uma consulta por campanha.

O aviso de budget ultrapassado é preparado por
:func:`gestor_campanhas.servicos.criativos.aviso_budget` e mostrado pelos
menus. Não impede guardar o criativo: o custo é uma estimativa, e cabe ao
marketeer e ao Administrador decidir o que fazer.

Pedidos de alteração de budget
------------------------------

Um pedido de alteração de budget usa os mesmos estados de um pedido de
campanha, mas quem o faz avançar é diferente:

.. code-block:: text

   Pendente --(parecer do marketeer)--> Em análise --(o Administrador aprova)--> Aprovado
      |                                     |
      |                                     +--------(o Administrador rejeita)--> Rejeitado
      |
      +--(o cliente cancela)--> Cancelado

O parecer é guardado no próprio pedido, nas colunas ``parecer_viavel`` e
``parecer_justificacao``. Enquanto o pedido estiver por decidir, o marketeer
pode dar outro parecer, que substitui o anterior:
:func:`gestor_campanhas.servicos.budget.dar_parecer` só recusa pedidos já
decididos ou cancelados.

O Administrador só decide pedidos com parecer
(:func:`gestor_campanhas.servicos.budget.aprovar` e
:func:`gestor_campanhas.servicos.budget.rejeitar`). Aprovar altera o budget
da campanha para o valor pedido.

O marketeer que vê o pedido é sempre o responsável atual pela campanha: as
consultas de :mod:`gestor_campanhas.repositorios.pedidos_budget` vão buscar o
marketeer à tabela ``campanhas``, e não guardam uma cópia no pedido. Se a
campanha mudar de marketeer, os pedidos mudam com ela.

Histórico do budget
-------------------

O budget de uma campanha está na coluna ``budget_centimos`` da tabela
``campanhas``; o histórico está na tabela ``alteracoes_budget``. Para os dois
nunca ficarem desencontrados, todas as alterações passam por
:func:`gestor_campanhas.servicos.campanhas.alterar_budget`, que muda o
budget e regista a alteração de uma só vez. Usam-na:

* :func:`gestor_campanhas.servicos.campanhas.definir_budget`, a opção
  **Definir budget** do Administrador;
* :func:`gestor_campanhas.servicos.budget.aprovar`, quando o Administrador
  aprova um pedido de alteração de budget.

O budget inicial de uma campanha criada a partir de um pedido de campanha é
registado diretamente em :func:`gestor_campanhas.servicos.pedidos.aprovar`,
porque a campanha já é criada com ele.

O histórico só cresce: as linhas nunca são alteradas. Cada linha guarda o
budget anterior e o novo, e não a diferença, para se poder ler cada linha
sozinha.

Resumo global do budget
-----------------------

O resumo do Administrador não tem tabela própria: é calculado sempre que é
mostrado, a partir das campanhas e da despesa de cada uma, como a despesa
(ver `Despesa e budget restante`_).
:func:`gestor_campanhas.servicos.budget.campanhas_com_despesa` junta cada
campanha à sua despesa, com as duas consultas de sempre (todas as campanhas e
a soma dos custos por campanha), e as restantes funções do resumo trabalham
sobre essa lista:

* :func:`gestor_campanhas.servicos.budget.resumo_por_cliente` agrupa as
  campanhas por cliente, num
  :class:`~gestor_campanhas.servicos.budget.ResumoCliente`;
* :func:`gestor_campanhas.servicos.budget.somar` faz a linha do total;
* :func:`gestor_campanhas.servicos.budget.campanhas_acima_do_budget` filtra
  as campanhas cuja despesa passa o budget.

A regra "acima do budget" está num só sítio,
:func:`gestor_campanhas.servicos.budget.acima_do_budget`: uma campanha sem
budget nunca está acima do budget.

Comentários dos criativos
-------------------------

Os comentários do cliente e as respostas do marketeer ficam na mesma tabela,
``comentarios``. Uma resposta é um comentário com a coluna ``resposta_a``
preenchida. Assim, uma só consulta traz a conversa toda de um criativo, pela
ordem em que foi escrita.

:func:`gestor_campanhas.servicos.comentarios.conversa` arruma essa lista em
pares ``(comentário, respostas)``, que é a forma como os menus a mostram.
Responde-se a um comentário do cliente, e não a uma resposta: para continuar
a conversa, o cliente escreve um comentário novo. Por isso a conversa tem só
dois níveis.

Os comentários por responder também não são guardados: são os comentários do
cliente que não têm nenhuma resposta, contados por
:func:`gestor_campanhas.servicos.comentarios.por_responder`.

Painel de marketeers
--------------------

Os indicadores do painel não são guardados: são calculados sempre que o
painel é mostrado, por :func:`gestor_campanhas.servicos.painel.carga`, a
partir dos criativos de cada marketeer. Os estados que contam como ativos e
como concluídos estão nas constantes
:data:`gestor_campanhas.servicos.painel.ATIVOS` e
:data:`gestor_campanhas.servicos.painel.CONCLUIDOS`, e a regra do atraso em
:func:`gestor_campanhas.servicos.painel.em_atraso`.

A tabela ``criativos`` não guarda a data da última alteração, e o
``CREATE TABLE IF NOT EXISTS`` não acrescentaria a coluna às bases de dados
que já existem. Por isso a atividade tem uma tabela própria, ``atividades``,
onde :mod:`gestor_campanhas.servicos.criativos` e
:mod:`gestor_campanhas.servicos.comentarios` registam cada alteração feita
por um marketeer. A última atividade de um marketeer é a mais recente dessa
tabela ou, para os criativos que já existiam antes dela, a data de criação
do criativo mais recente das campanhas dele.

O número de dias ao fim dos quais um marketeer aparece como parado é de 7 por
omissão (:data:`gestor_campanhas.config.DIAS_SEM_ATIVIDADE`) e fica guardado
na tabela ``configuracoes``, com a chave ``dias_sem_atividade``, quando o
Administrador o muda. É a mesma forma de guardar o limite de inatividade das
sessões.

Relatório das campanhas
-----------------------

O relatório do Cliente é montado por
:func:`gestor_campanhas.servicos.relatorios.linhas`, a partir das mesmas
funções que mostram as campanhas e a despesa no ecrã, e gravado por
:func:`gestor_campanhas.servicos.relatorios.exportar` com o módulo ``csv``
da biblioteca padrão. O formato pensa no Excel em português:

* as colunas são separadas por ``;``, porque a vírgula é a das casas
  decimais;
* os valores em euros vão sem ``€`` e sem o espaço dos milhares
  (:func:`gestor_campanhas.servicos.relatorios.valor`), para serem lidos
  como números;
* o ficheiro é gravado em UTF-8 com a marca inicial (``utf-8-sig``), sem a
  qual o Excel mostra os acentos trocados.

O nome do ficheiro é escolhido por
:func:`gestor_campanhas.servicos.ficheiros.caminho_livre`, a mesma função que
escolhe o nome de um ficheiro descarregado, por isso nenhum ficheiro que já
esteja na pasta é apagado.
