"""Regras dos pedidos de nova campanha.

Um cliente pede uma campanha indicando o objetivo, o orçamento, o prazo e as
plataformas. O pedido começa no estado pendente; enquanto estiver pendente, o
cliente pode cancelá-lo.

O Administrador analisa os pedidos e decide: se aprovar, é criada a campanha;
se rejeitar, indica o motivo. Nos dois casos o cliente é avisado por email.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import dinheiro, modelos, relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import PedidoCampanha, Utilizador
from gestor_campanhas.repositorios import alteracoes_budget
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos, utilizadores
from gestor_campanhas.servicos import campanhas, correio, validacao

#: Estados em que um pedido ainda espera pela decisão do Administrador.
POR_DECIDIR = (modelos.PENDENTE, modelos.EM_ANALISE)


def _plataformas_validadas(escolhidas: list[str]) -> list[str]:
    """Confirma as plataformas escolhidas e devolve-as sem repetições, pela ordem dos menus."""
    desconhecidas = [nome for nome in escolhidas if nome not in modelos.PLATAFORMAS]
    if desconhecidas:
        raise ErroValidacao(f"A plataforma {desconhecidas[0]} não existe.")
    if not escolhidas:
        raise ErroValidacao("Escolha pelo menos uma plataforma.")
    return [nome for nome in modelos.PLATAFORMAS if nome in escolhidas]


def criar(
    ligacao: sqlite3.Connection,
    cliente: Utilizador,
    objetivo: str,
    orcamento: str,
    prazo: str,
    plataformas: list[str],
) -> PedidoCampanha:
    """Regista um pedido de nova campanha, no estado pendente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    :param objetivo: O que pretende com a campanha. Obrigatório.
    :param orcamento: Quanto quer investir, em euros, tal como foi escrito
        (por exemplo ``"1500"`` ou ``"1500,50"``). Tem de ser maior do que zero.
    :param prazo: Dia até ao qual quer a campanha, no formato ``AAAA-MM-DD``.
        Obrigatório; não pode ser um dia que já passou.
    :param plataformas: Nomes das plataformas onde quer anunciar, de
        :data:`~gestor_campanhas.modelos.PLATAFORMAS`. Pelo menos uma.
    :return: O pedido criado.
    :raises ErroValidacao: Se algum dos valores não respeitar as regras.
    """
    objetivo = objetivo.strip()
    if not objetivo:
        raise ErroValidacao("O objetivo não pode ficar vazio.")
    centimos = dinheiro.para_centimos(orcamento)
    if centimos <= 0:
        raise ErroValidacao("O orçamento tem de ser maior do que zero.")
    dia = validacao.data(prazo, "data do prazo")
    if dia is None:
        raise ErroValidacao("O prazo não pode ficar vazio.")
    if dia < relogio.hoje():
        raise ErroValidacao("O prazo não pode ser um dia que já passou.")
    return pedidos.criar(ligacao, cliente.id, objetivo, centimos, dia, _plataformas_validadas(plataformas))


def listar_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> list[PedidoCampanha]:
    """Lista os pedidos feitos por um cliente, em qualquer estado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :return: Pedidos desse cliente, do mais recente para o mais antigo.
    """
    return pedidos.listar_por_cliente(ligacao, cliente.id)


def obter_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoCampanha:
    """Procura um pedido pelo número, confirmando que é do cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :param identificador: Número do pedido, mostrado na primeira coluna da lista.
    :return: O pedido.
    :raises ErroValidacao: Se o cliente não tiver nenhum pedido com esse número.
    """
    pedido = pedidos.obter_por_id(ligacao, identificador)
    if pedido is None or pedido.cliente_id != cliente.id:
        raise ErroValidacao(f"Não tem nenhum pedido com o número {identificador}.")
    return pedido


def cancelar(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoCampanha:
    """Cancela um pedido do cliente que ainda esteja pendente.

    O pedido não é apagado: fica na lista, com o estado cancelado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a cancelar.
    :param identificador: Número do pedido.
    :return: O pedido, já cancelado.
    :raises ErroValidacao: Se o pedido não for do cliente ou já não estiver pendente.
    """
    pedido = obter_do_cliente(ligacao, cliente, identificador)
    if pedido.estado != modelos.PENDENTE:
        raise ErroValidacao(
            f"Só é possível cancelar um pedido pendente. Este pedido está no estado {pedido.nome_estado}."
        )
    return pedidos.definir_estado(ligacao, pedido.id, modelos.CANCELADO)


def listar_todos(ligacao: sqlite3.Connection) -> list[PedidoCampanha]:
    """Lista os pedidos de todos os clientes, para o Administrador.

    :param ligacao: Ligação aberta à base de dados.
    :return: Primeiro os pedidos por decidir, depois os já decididos; dentro
        de cada grupo, do mais antigo para o mais recente.
    """
    todos = pedidos.listar_todos(ligacao)
    return sorted(todos, key=lambda pedido: (pedido.estado not in POR_DECIDIR, pedido.id))


def obter(ligacao: sqlite3.Connection, identificador: int) -> PedidoCampanha:
    """Procura um pedido pelo número, seja de quem for.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do pedido.
    :return: O pedido.
    :raises ErroValidacao: Se não existir nenhum pedido com esse número.
    """
    pedido = pedidos.obter_por_id(ligacao, identificador)
    if pedido is None:
        raise ErroValidacao(f"Não existe nenhum pedido com o número {identificador}.")
    return pedido


def analisar(ligacao: sqlite3.Connection, identificador: int) -> PedidoCampanha:
    """Abre um pedido para o Administrador o analisar.

    Um pedido pendente passa a estar em análise, e o cliente deixa de o poder
    cancelar. Nos outros estados, o pedido fica como está.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do pedido.
    :return: O pedido, já com o estado atualizado.
    :raises ErroValidacao: Se não existir nenhum pedido com esse número.
    """
    pedido = obter(ligacao, identificador)
    if pedido.estado == modelos.PENDENTE:
        pedido = pedidos.definir_estado(ligacao, pedido.id, modelos.EM_ANALISE)
    return pedido


def _por_decidir(ligacao: sqlite3.Connection, identificador: int) -> PedidoCampanha:
    """Devolve um pedido, confirmando que ainda não foi decidido nem cancelado."""
    pedido = obter(ligacao, identificador)
    if pedido.estado not in POR_DECIDIR:
        raise ErroValidacao(f"Este pedido já não pode ser decidido: está no estado {pedido.nome_estado}.")
    return pedido


def aprovar(
    ligacao: sqlite3.Connection, identificador: int, nome: str, budget: str, marketeer_id: int
) -> PedidoCampanha:
    """Aprova um pedido e cria a campanha correspondente.

    A campanha fica com o objetivo do pedido, com o prazo do pedido como data
    de fim, com o budget inicial indicado e com o marketeer escolhido. O
    budget inicial fica registado no histórico do budget da campanha. O
    cliente e o marketeer são avisados por email.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do pedido.
    :param nome: Nome a dar à campanha. Obrigatório.
    :param budget: Budget inicial em euros, tal como foi escrito. Maior do que zero.
    :param marketeer_id: Número do marketeer que fica responsável. Tem de
        ter a conta ativa.
    :return: O pedido, já aprovado e com o número da campanha criada.
    :raises ErroValidacao: Se o pedido não existir ou já tiver sido decidido,
        ou se algum dos valores não respeitar as regras. Nesse caso nada é criado.
    """
    pedido = _por_decidir(ligacao, identificador)
    nome = validacao.nome(nome)
    centimos = campanhas.budget_validado(budget)
    marketeer = campanhas.marketeer_ativo(ligacao, marketeer_id)
    campanha = campanhas_bd.criar(
        ligacao, nome, pedido.objetivo, pedido.cliente_id, marketeer.id, None, pedido.prazo, centimos
    )
    alteracoes_budget.registar(
        ligacao, campanha.id, None, centimos, f"{campanhas.MOTIVO_BUDGET_INICIAL}, do pedido de campanha n.º {pedido.id}"
    )
    pedido = pedidos.definir_estado(ligacao, pedido.id, modelos.APROVADO, campanha_id=campanha.id)
    cliente = utilizadores.obter_por_id(ligacao, pedido.cliente_id)
    correio.enviar(
        cliente.email,
        "O seu pedido de campanha foi aprovado",
        f"Olá, {cliente.nome}.\n\n"
        f"O seu pedido n.º {pedido.id} ({pedido.objetivo}) foi aprovado.\n"
        f"Foi criada a campanha {campanha.nome}, com um budget inicial de {dinheiro.formatar(centimos)}.\n"
        f"O marketeer responsável é {marketeer.nome}.",
    )
    campanhas.avisar_marketeer(marketeer, campanha)
    return pedido


def rejeitar(ligacao: sqlite3.Connection, identificador: int, motivo: str) -> PedidoCampanha:
    """Rejeita um pedido, indicando o motivo. O cliente é avisado por email.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do pedido.
    :param motivo: Porque é que o pedido não avança. Obrigatório.
    :return: O pedido, já rejeitado.
    :raises ErroValidacao: Se o pedido não existir ou já tiver sido decidido,
        ou se o motivo ficar vazio.
    """
    pedido = _por_decidir(ligacao, identificador)
    motivo = motivo.strip()
    if not motivo:
        raise ErroValidacao("O motivo da rejeição não pode ficar vazio.")
    pedido = pedidos.definir_estado(ligacao, pedido.id, modelos.REJEITADO, motivo_rejeicao=motivo)
    cliente = utilizadores.obter_por_id(ligacao, pedido.cliente_id)
    correio.enviar(
        cliente.email,
        "O seu pedido de campanha foi rejeitado",
        f"Olá, {cliente.nome}.\n\n"
        f"O seu pedido n.º {pedido.id} ({pedido.objetivo}) foi rejeitado.\n"
        f"Motivo: {motivo}\n\n"
        "Pode fazer um pedido novo quando quiser.",
    )
    return pedido
