"""Regras das campanhas.

Uma campanha pertence a um cliente e tem um marketeer responsável. O
marketeer que cria a campanha fica responsável por ela e só pode mexer nas
suas campanhas.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import dinheiro, modelos, relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import AlteracaoBudget, Campanha, Utilizador
from gestor_campanhas.repositorios import alteracoes_budget, campanhas, criativos, utilizadores
from gestor_campanhas.servicos import correio, gestao, validacao

#: Motivo registado no histórico quando uma campanha recebe o primeiro budget.
MOTIVO_BUDGET_INICIAL = "Budget inicial"


def clientes_disponiveis(ligacao: sqlite3.Connection) -> list[Utilizador]:
    """Lista os clientes para quem se pode criar uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :return: Clientes com a conta ativa, por ordem alfabética do nome.
    """
    return [cliente for cliente in gestao.listar(ligacao, modelos.CLIENTE) if cliente.ativo]


def listar_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador) -> list[Campanha]:
    """Lista as campanhas de que um marketeer é responsável.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :return: Campanhas desse marketeer, pela ordem em que foram criadas.
    """
    return campanhas.listar_por_marketeer(ligacao, marketeer.id)


def _dados_validados(nome: str, objetivo: str, data_inicio: str, data_fim: str) -> tuple:
    """Valida o nome, o objetivo e as datas e devolve-os arrumados, pela mesma ordem."""
    nome = validacao.nome(nome)
    inicio = validacao.data(data_inicio, "data de início")
    fim = validacao.data(data_fim, "data de fim")
    validacao.periodo(inicio, fim)
    return nome, objetivo.strip(), inicio, fim


def criar(
    ligacao: sqlite3.Connection,
    marketeer: Utilizador,
    nome: str,
    objetivo: str,
    cliente_id: int,
    data_inicio: str = "",
    data_fim: str = "",
) -> Campanha:
    """Cria uma campanha para um cliente. Quem a cria fica responsável por ela.

    A campanha começa sem budget: é o Administrador que o define.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a criar a campanha.
    :param nome: Nome da campanha. Obrigatório.
    :param objetivo: O que se pretende com a campanha. Pode ficar vazio.
    :param cliente_id: Número do cliente a quem a campanha pertence.
    :param data_inicio: Primeiro dia, no formato ``AAAA-MM-DD``, ou vazio.
    :param data_fim: Último dia, no formato ``AAAA-MM-DD``, ou vazio.
    :return: A campanha criada.
    :raises ErroValidacao: Se o cliente não existir ou tiver a conta
        desativada, ou se algum dos valores não respeitar as regras.
    """
    cliente = utilizadores.obter_por_id(ligacao, cliente_id)
    if cliente is None or cliente.perfil != modelos.CLIENTE:
        raise ErroValidacao(f"Não existe nenhum cliente com o número {cliente_id}.")
    if not cliente.ativo:
        raise ErroValidacao("Este cliente tem a conta desativada.")
    nome, objetivo, inicio, fim = _dados_validados(nome, objetivo, data_inicio, data_fim)
    return campanhas.criar(ligacao, nome, objetivo, cliente.id, marketeer.id, inicio, fim)


def obter_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> Campanha:
    """Procura uma campanha pelo número, confirmando que é do marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :param identificador: Número da campanha, mostrado na primeira coluna da lista.
    :return: A campanha.
    :raises ErroValidacao: Se o marketeer não for responsável por nenhuma
        campanha com esse número.
    """
    campanha = campanhas.obter_por_id(ligacao, identificador)
    if campanha is None or campanha.marketeer_id != marketeer.id:
        raise ErroValidacao(f"Não tem nenhuma campanha com o número {identificador}.")
    return campanha


def editar(
    ligacao: sqlite3.Connection,
    marketeer: Utilizador,
    identificador: int,
    nome: str,
    objetivo: str,
    data_inicio: str = "",
    data_fim: str = "",
) -> Campanha:
    """Altera o nome, o objetivo e as datas de uma campanha do marketeer.

    O cliente e o budget não são alterados: o budget é definido pelo
    Administrador. Nada é guardado se algum dos valores não for válido.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a editar.
    :param identificador: Número da campanha.
    :param nome: Nome novo. Obrigatório.
    :param objetivo: Objetivo novo. Pode ficar vazio.
    :param data_inicio: Primeiro dia novo (``AAAA-MM-DD``), ou vazio para ficar sem data.
    :param data_fim: Último dia novo (``AAAA-MM-DD``), ou vazio para ficar sem data.
    :return: A campanha, já com os dados novos.
    :raises ErroValidacao: Se a campanha não for do marketeer ou se algum dos
        valores não respeitar as regras.
    """
    campanha = obter_do_marketeer(ligacao, marketeer, identificador)
    nome, objetivo, inicio, fim = _dados_validados(nome, objetivo, data_inicio, data_fim)
    return campanhas.atualizar(ligacao, campanha.id, nome, objetivo, inicio, fim)


def estado(campanha: Campanha, hoje: date | None = None) -> str:
    """Diz em que estado está uma campanha, a partir das datas dela.

    :param campanha: Campanha a avaliar.
    :param hoje: Dia de referência. Se for ``None``, usa-se o dia atual.
    :return: :data:`~gestor_campanhas.modelos.POR_COMECAR` se a data de início
        ainda não chegou, :data:`~gestor_campanhas.modelos.TERMINADA` se a
        data de fim já passou, e :data:`~gestor_campanhas.modelos.EM_CURSO`
        nos outros casos (incluindo quando não tem datas).
    """
    hoje = hoje or relogio.hoje()
    if campanha.data_inicio and campanha.data_inicio > hoje:
        return modelos.POR_COMECAR
    if campanha.terminada(hoje):
        return modelos.TERMINADA
    return modelos.EM_CURSO


def eliminar(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> Campanha:
    """Elimina uma campanha do marketeer. Não pode ser desfeito.

    Só se pode eliminar uma campanha sem criativos, para não se perder
    trabalho por engano: os criativos têm de ser eliminados primeiro.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a eliminar.
    :param identificador: Número da campanha.
    :return: A campanha que foi eliminada, para se poder mostrar o nome.
    :raises ErroValidacao: Se a campanha não for do marketeer ou se ainda
        tiver criativos.
    """
    campanha = obter_do_marketeer(ligacao, marketeer, identificador)
    total = criativos.contar_por_campanha(ligacao, campanha.id)
    if total:
        palavra = "criativo" if total == 1 else "criativos"
        raise ErroValidacao(
            f"A campanha {campanha.nome} tem {total} {palavra}. Elimine primeiro os criativos, na opção \"Criativos\"."
        )
    campanhas.eliminar(ligacao, campanha.id)
    return campanha


def listar_todas(ligacao: sqlite3.Connection) -> list[Campanha]:
    """Lista todas as campanhas, para o Administrador.

    :param ligacao: Ligação aberta à base de dados.
    :return: Campanhas de todos os clientes, pela ordem em que foram criadas.
    """
    return campanhas.listar_todas(ligacao)


def obter(ligacao: sqlite3.Connection, identificador: int) -> Campanha:
    """Procura uma campanha pelo número, seja de quem for.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número da campanha.
    :return: A campanha.
    :raises ErroValidacao: Se não existir nenhuma campanha com esse número.
    """
    campanha = campanhas.obter_por_id(ligacao, identificador)
    if campanha is None:
        raise ErroValidacao(f"Não existe nenhuma campanha com o número {identificador}.")
    return campanha


def budget_validado(valor: str) -> int:
    """Converte um budget escrito em euros e confirma que é maior do que zero.

    :param valor: Budget tal como foi escrito, por exemplo ``"1500"`` ou ``"1500,50"``.
    :return: O budget em cêntimos.
    :raises ErroValidacao: Se não for um valor em euros ou não for maior do que zero.
    """
    centimos = dinheiro.para_centimos(valor)
    if centimos <= 0:
        raise ErroValidacao("O budget tem de ser maior do que zero.")
    return centimos


def alterar_budget(
    ligacao: sqlite3.Connection,
    campanha: Campanha,
    centimos: int,
    motivo: str,
    pedido_budget_id: int | None = None,
) -> Campanha:
    """Muda o budget de uma campanha e regista a alteração no histórico.

    É o único sítio onde o budget de uma campanha existente muda, para que
    nenhuma alteração fique fora do histórico. Não valida nada: quem a chama
    já validou o valor e o motivo.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha: Campanha, ainda com o budget anterior.
    :param centimos: Budget novo, em cêntimos.
    :param motivo: Porque é que o budget muda.
    :param pedido_budget_id: Número do pedido de alteração de budget que deu
        origem à alteração, se houver.
    :return: A campanha, já com o budget novo.
    """
    alterada = campanhas.definir_budget(ligacao, campanha.id, centimos)
    alteracoes_budget.registar(ligacao, campanha.id, campanha.budget_centimos, centimos, motivo, pedido_budget_id)
    return alterada


def definir_budget(ligacao: sqlite3.Connection, identificador: int, valor: str, motivo: str = "") -> Campanha:
    """Define ou altera o budget de uma campanha. Só o Administrador o faz.

    A alteração fica registada no histórico do budget da campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número da campanha.
    :param valor: Budget em euros, tal como foi escrito. Tem de ser diferente
        do budget atual.
    :param motivo: Porque é que o budget muda. Obrigatório quando a campanha
        já tem budget; quando é o primeiro, pode ficar vazio e fica registado
        :data:`MOTIVO_BUDGET_INICIAL`.
    :return: A campanha, já com o budget novo.
    :raises ErroValidacao: Se a campanha não existir, se o valor não for
        válido ou for igual ao atual, ou se faltar o motivo.
    """
    campanha = obter(ligacao, identificador)
    centimos = budget_validado(valor)
    if centimos == campanha.budget_centimos:
        raise ErroValidacao("O budget novo é igual ao budget atual.")
    motivo = motivo.strip()
    if not motivo:
        if campanha.budget_centimos is not None:
            raise ErroValidacao("Indique o motivo da alteração do budget.")
        motivo = MOTIVO_BUDGET_INICIAL
    return alterar_budget(ligacao, campanha, centimos, motivo)


def historico_budget(ligacao: sqlite3.Connection, campanha: Campanha) -> list[AlteracaoBudget]:
    """Lista as alterações do budget de uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha: Campanha a consultar.
    :return: Alterações, da mais antiga para a mais recente.
    """
    return alteracoes_budget.listar_por_campanha(ligacao, campanha.id)


def marketeers_disponiveis(ligacao: sqlite3.Connection) -> list[Utilizador]:
    """Lista os marketeers a quem se pode atribuir uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :return: Marketeers com a conta ativa, por ordem alfabética do nome.
    """
    return [marketeer for marketeer in gestao.listar(ligacao, modelos.MARKETEER) if marketeer.ativo]


def marketeer_ativo(ligacao: sqlite3.Connection, identificador: int) -> Utilizador:
    """Procura um marketeer pelo número, confirmando que tem a conta ativa.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do marketeer.
    :return: O marketeer.
    :raises ErroValidacao: Se não existir um marketeer com esse número ou se
        tiver a conta desativada.
    """
    marketeer = utilizadores.obter_por_id(ligacao, identificador)
    if marketeer is None or marketeer.perfil != modelos.MARKETEER:
        raise ErroValidacao(f"Não existe nenhum marketeer com o número {identificador}.")
    if not marketeer.ativo:
        raise ErroValidacao("Este marketeer tem a conta desativada.")
    return marketeer


def avisar_marketeer(marketeer: Utilizador, campanha: Campanha) -> None:
    """Envia um email ao marketeer a dizer que passou a ser responsável por uma campanha.

    :param marketeer: Marketeer que recebe o aviso.
    :param campanha: Campanha que lhe foi atribuída.
    """
    correio.enviar(
        marketeer.email,
        "Foi-lhe atribuída uma campanha",
        f"Olá, {marketeer.nome}.\n\n"
        f"Passou a ser responsável pela campanha {campanha.nome}, do cliente {campanha.cliente_nome}.\n"
        'Pode consultá-la na opção "Campanhas" do seu menu.',
    )


def atribuir_marketeer(ligacao: sqlite3.Connection, identificador: int, marketeer_id: int) -> Campanha:
    """Atribui uma campanha a um marketeer, que passa a ser o responsável.

    O marketeer anterior deixa de ver a campanha. O marketeer novo é avisado
    por email.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número da campanha.
    :param marketeer_id: Número do marketeer que passa a ser responsável.
    :return: A campanha, já com o marketeer novo.
    :raises ErroValidacao: Se a campanha não existir, se o marketeer não
        existir ou tiver a conta desativada, ou se já for o responsável.
    """
    campanha = obter(ligacao, identificador)
    marketeer = marketeer_ativo(ligacao, marketeer_id)
    if campanha.marketeer_id == marketeer.id:
        raise ErroValidacao(f"{marketeer.nome} já é responsável por esta campanha.")
    campanha = campanhas.definir_marketeer(ligacao, campanha.id, marketeer.id)
    avisar_marketeer(marketeer, campanha)
    return campanha


def contar_ativas(ligacao: sqlite3.Connection, perfil: str) -> dict[int, int]:
    """Conta as campanhas ativas de cada cliente ou de cada marketeer.

    Uma campanha está ativa enquanto não terminar: conta se estiver em curso
    ou por começar.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: :data:`~gestor_campanhas.modelos.CLIENTE` para contar por
        cliente, :data:`~gestor_campanhas.modelos.MARKETEER` para contar por
        marketeer responsável.
    :return: Dicionário do número da conta para o número de campanhas ativas.
        As contas sem campanhas ativas não aparecem.
    """
    hoje = relogio.hoje()
    totais: dict[int, int] = {}
    for campanha in campanhas.listar_todas(ligacao):
        if campanha.terminada(hoje):
            continue
        conta = campanha.cliente_id if perfil == modelos.CLIENTE else campanha.marketeer_id
        totais[conta] = totais.get(conta, 0) + 1
    return totais


def listar_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> list[Campanha]:
    """Lista as campanhas de um cliente, incluindo as que ainda não têm budget.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :return: Campanhas desse cliente, pela ordem em que foram criadas.
    """
    return campanhas.listar_por_cliente(ligacao, cliente.id)


def obter_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> Campanha:
    """Procura uma campanha pelo número, confirmando que é do cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :param identificador: Número da campanha, mostrado na primeira coluna da lista.
    :return: A campanha.
    :raises ErroValidacao: Se o cliente não tiver nenhuma campanha com esse número.
    """
    campanha = campanhas.obter_por_id(ligacao, identificador)
    if campanha is None or campanha.cliente_id != cliente.id:
        raise ErroValidacao(f"Não tem nenhuma campanha com o número {identificador}.")
    return campanha


def responsavel(ligacao: sqlite3.Connection, campanha: Campanha) -> Utilizador:
    """Devolve o marketeer responsável por uma campanha, com os contactos.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha: Campanha a consultar.
    :return: A conta do marketeer, com o email e o telefone.
    """
    return utilizadores.obter_por_id(ligacao, campanha.marketeer_id)
