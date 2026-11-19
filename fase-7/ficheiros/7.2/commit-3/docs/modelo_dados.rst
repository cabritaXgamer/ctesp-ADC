Modelo de dados
===============

Os dados ficam numa base de dados SQLite, no ficheiro ``app.db`` da pasta de
dados (ver :doc:`instalacao`). As tabelas são criadas a partir da constante
:data:`gestor_campanhas.bd.ESQUEMA`. Todas as instruções usam
``CREATE TABLE IF NOT EXISTS``, por isso podem ser executadas em todos os
arranques sem apagar dados.

Cada tabela tem um módulo em :mod:`gestor_campanhas.repositorios`, o único
sítio da aplicação onde se escreve SQL, e cada linha lida é convertida numa
classe de :mod:`gestor_campanhas.modelos`.

Relações entre as tabelas
-------------------------

O centro do modelo é a campanha: pertence a um cliente, tem um marketeer
responsável e reúne os criativos, os pedidos de budget e o histórico do
budget. Cada ``1 ---< N`` lê-se "um para muitos": por exemplo, uma campanha
tem muitos criativos, e cada criativo pertence a uma só campanha.

.. code-block:: text

   cliente    1 ---< N  pedidos_campanha  1 ---  0..1  campanhas
   cliente    1 ---< N  campanhas
   marketeer  1 ---< N  campanhas

   campanhas  1 ---< N  criativos          1 ---< N  comentarios
   campanhas  1 ---< N  pedidos_budget     1 ---  0..1  alteracoes_budget
   campanhas  1 ---< N  alteracoes_budget

O cliente e o marketeer são linhas da tabela ``utilizadores``. A tabela
seguinte mostra todas as referências, e o que acontece a cada linha quando
a linha para onde aponta é apagada:

.. list-table::
   :header-rows: 1
   :widths: 22 22 20 36

   * - Tabela
     - Coluna
     - Aponta para
     - Se a linha apontada for apagada
   * - ``sessoes``, ``recuperacoes``, ``notificacoes``, ``atividades``
     - ``utilizador_id``
     - ``utilizadores``
     - Não acontece: as contas nunca são apagadas
   * - ``campanhas``
     - ``cliente_id``, ``marketeer_id``
     - ``utilizadores``
     - Não acontece: as contas nunca são apagadas
   * - ``pedidos_campanha``
     - ``cliente_id``
     - ``utilizadores``
     - Não acontece: as contas nunca são apagadas
   * - ``pedidos_campanha``
     - ``campanha_id``
     - ``campanhas``
     - Fica vazia (``ON DELETE SET NULL``)
   * - ``criativos``
     - ``campanha_id``
     - ``campanhas``
     - A campanha não pode ser apagada
   * - ``pedidos_budget``
     - ``campanha_id``
     - ``campanhas``
     - É apagada com a campanha (``ON DELETE CASCADE``)
   * - ``alteracoes_budget``
     - ``campanha_id``
     - ``campanhas``
     - É apagada com a campanha (``ON DELETE CASCADE``)
   * - ``alteracoes_budget``
     - ``pedido_budget_id``
     - ``pedidos_budget``
     - Fica vazia (``ON DELETE SET NULL``)
   * - ``comentarios``
     - ``criativo_id``
     - ``criativos``
     - É apagada com o criativo (``ON DELETE CASCADE``)
   * - ``comentarios``
     - ``autor_id``
     - ``utilizadores``
     - Não acontece: as contas nunca são apagadas
   * - ``comentarios``
     - ``resposta_a``
     - ``comentarios``
     - É apagada com o comentário (``ON DELETE CASCADE``)

A tabela ``configuracoes`` não tem referências: guarda pares chave/valor.

Tabelas
-------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Tabela
     - Conteúdo
   * - ``configuracoes``
     - Pares chave/valor com definições que podem ser alteradas durante a
       utilização da aplicação: ``minutos_inatividade`` e
       ``dias_sem_atividade``.
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
   * - ``criativos``
     - Uma linha por criativo: campanha a que pertence, nome, descrição,
       custo em cêntimos, prazo, público-alvo, plataforma, estado
       (``em_preparacao``, ``em_revisao``, ``aprovado``, ``rejeitado`` ou
       ``publicado``), motivo da rejeição e nome do ficheiro anexado.
   * - ``pedidos_budget``
     - Uma linha por pedido de alteração de budget: campanha, budget da
       campanha quando o pedido foi feito, budget pedido (ambos em
       cêntimos), motivo, estado (os mesmos de ``pedidos_campanha``), parecer
       do marketeer (``1`` viável, ``0`` não viável, vazio enquanto não for
       dado) e a justificação, motivo da rejeição e data da decisão. O
       cliente é o da campanha, por isso não tem coluna própria.
   * - ``alteracoes_budget``
     - O histórico do budget: uma linha por alteração, com a campanha, o
       budget anterior (vazio se não havia), o budget novo, o motivo, a data
       e, quando a alteração vem de um pedido aprovado, o número do pedido.
   * - ``comentarios``
     - Uma linha por comentário ou resposta: criativo, autor, texto, data e,
       numa resposta, o número do comentário a que responde
       (``resposta_a``).
   * - ``notificacoes``
     - Uma linha por notificação: quem a recebe, o texto, o tipo do item
       (``campanha``, ``pedido_budget`` ou ``criativo``), o número do item, se
       já foi lida e a data.
   * - ``atividades``
     - O registo da atividade dos marketeers: uma linha por alteração, com o
       marketeer, a descrição e a data.

Todas as tabelas, exceto ``configuracoes``, têm uma coluna ``id``, o número
de cada linha, que o SQLite atribui sozinho e nunca reutiliza
(``AUTOINCREMENT``). É esse o número que aparece nos menus, por exemplo em
"Criativo n.º 3".

Como os valores são guardados
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Valor
     - Como fica na base de dados
   * - Dinheiro
     - Em cêntimos, num número inteiro: ``150050`` são 1500,50 €. As colunas
       acabam em ``_centimos``. Ver :mod:`gestor_campanhas.dinheiro`.
   * - Datas
     - Texto no formato ``AAAA-MM-DD`` (prazos, datas de início e de fim).
   * - Datas e horas
     - Texto no formato ``AAAA-MM-DD HH:MM:SS`` (entradas, criação, decisões).
       Ver :mod:`gestor_campanhas.relogio`.
   * - Sim ou não
     - ``1`` ou ``0`` (por exemplo ``ativo``, ``lida`` e ``usado``).
   * - Estados e perfis
     - Texto sem acentos, de uma lista fechada, confirmado pelo próprio
       SQLite (``CHECK``). Os nomes que aparecem nos menus estão em
       :mod:`gestor_campanhas.modelos`.
   * - Plataformas de um pedido
     - Um só texto, com as plataformas separadas por vírgula.
   * - Passwords e códigos
     - Nunca o valor: só o hash (ver :doc:`arquitetura`).
   * - Ficheiros dos criativos
     - Só o nome. O ficheiro fica na pasta ``ficheiros`` da pasta de dados.

O que acontece quando se apaga
------------------------------

O SQLite só respeita as referências entre tabelas quando se pede, e
:func:`gestor_campanhas.bd.ligar` pede-o em todas as ligações
(``PRAGMA foreign_keys = ON``).

Uma campanha com criativos não pode ser apagada: a coluna ``campanha_id`` da
tabela ``criativos`` aponta para ela, e o SQLite recusa apagar uma linha a
que outra tabela ainda faz referência. A regra está também em
:func:`gestor_campanhas.servicos.campanhas.eliminar`, que mostra uma
mensagem a explicar o que fazer.

Os pedidos de alteração de budget e o histórico do budget, pelo contrário,
não impedem que a campanha seja apagada. A coluna ``campanha_id`` das tabelas
``pedidos_budget`` e ``alteracoes_budget`` tem ``ON DELETE CASCADE``: quando
a campanha é apagada, os pedidos e o histórico dela são apagados com ela,
porque não fazem sentido sem a campanha. O mesmo acontece aos comentários de
um criativo: a coluna ``criativo_id`` da tabela ``comentarios`` também tem
``ON DELETE CASCADE``.

Um pedido de campanha aprovado fica no histórico do cliente mesmo que a
campanha seja apagada: a coluna ``campanha_id`` da tabela
``pedidos_campanha`` tem ``ON DELETE SET NULL``, e fica só vazia.

As contas nunca são apagadas, só desativadas, por isso as referências para
a tabela ``utilizadores`` nunca ficam sem destino.

Tabelas novas numa base de dados que já existe
----------------------------------------------

O ``CREATE TABLE IF NOT EXISTS`` cria as tabelas que faltam, mas não
acrescenta colunas a uma tabela que já existe. Por isso cada tabela foi
criada logo com todas as colunas de que vai precisar, mesmo as que só
começaram a ser usadas numa versão seguinte. Assim, quem atualiza a
aplicação continua a usar a base de dados que já tinha, sem perder nada.
