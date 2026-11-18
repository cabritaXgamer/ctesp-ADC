"""Regras dos pedidos de alteração de budget.

O cliente de uma campanha pode pedir que o budget dela seja alterado,
indicando o valor que pretende e o motivo. O pedido começa no estado
pendente; enquanto estiver pendente, o cliente pode cancelá-lo.

Cada campanha só pode ter um pedido de cada vez à espera de decisão, para
não haver dois valores pedidos ao mesmo tempo para o mesmo budget.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos, relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, PedidoBudget, Utilizador
from gestor_campanhas.repositorios import pedidos_budget
from gestor_campanhas.servicos import campanhas

#: Estados em que um pedido ainda espera pela decisão do Administrador.
POR_DECIDIR = (modelos.PENDENTE, modelos.EM_ANALISE)


def campanha_para_pedido(ligacao: sqlite3.Connection, cliente: Utilizador, campanha_id: int) -> Campanha:
    """Procura uma campanha do cliente e confirma que aceita um pedido de alteração de budget.

    O menu usa esta função logo depois de o cliente escolher a campanha, para
    o avisar antes de lhe pedir o valor e o motivo.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    :param campanha_id: Número da campanha.
    :return: A campanha.
    :raises ErroValidacao: Se a campanha não for do cliente, se já tiver
        terminado ou se já tiver um pedido por decidir.
    """
    campanha = campanhas.obter_do_cliente(ligacao, cliente, campanha_id)
    if campanha.terminada(relogio.hoje()):
        raise ErroValidacao(f"A campanha {campanha.nome} já terminou. O budget já não pode ser alterado.")
    anterior = pedidos_budget.obter_por_decidir(ligacao, campanha.id)
    if anterior is not None:
        raise ErroValidacao(
            f"A campanha {campanha.nome} já tem um pedido de alteração de budget por decidir (n.º {anterior.id})."
        )
    return campanha


def pedir(
    ligacao: sqlite3.Connection, cliente: Utilizador, campanha_id: int, budget: str, motivo: str
) -> PedidoBudget:
    """Regista um pedido de alteração do budget de uma campanha do cliente.

    O pedido guarda o budget que a campanha tem neste momento, para se poder
    comparar com o valor pedido mesmo depois de o budget mudar.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    :param campanha_id: Número da campanha. Tem de ser do cliente e não pode
        ter terminado.
    :param budget: Budget pretendido, em euros, tal como foi escrito (por
        exemplo ``"2000"`` ou ``"2000,50"``). Tem de ser maior do que zero e
        diferente do budget atual.
    :param motivo: Porque é que quer alterar o budget. Obrigatório.
    :return: O pedido criado, no estado pendente.
    :raises ErroValidacao: Se a campanha não for do cliente, se já tiver
        terminado, se já tiver um pedido por decidir, ou se algum dos valores
        não respeitar as regras.
    """
    campanha = campanha_para_pedido(ligacao, cliente, campanha_id)
    centimos = campanhas.budget_validado(budget)
    if centimos == campanha.budget_centimos:
        raise ErroValidacao("O valor pedido é igual ao budget atual da campanha.")
    motivo = motivo.strip()
    if not motivo:
        raise ErroValidacao("O motivo não pode ficar vazio.")
    return pedidos_budget.criar(ligacao, campanha.id, campanha.budget_centimos, centimos, motivo)


def listar_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> list[PedidoBudget]:
    """Lista os pedidos de alteração de budget de um cliente, em qualquer estado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :return: Pedidos desse cliente, do mais recente para o mais antigo.
    """
    return pedidos_budget.listar_por_cliente(ligacao, cliente.id)


def obter_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoBudget:
    """Procura um pedido de alteração de budget pelo número, confirmando que é do cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :param identificador: Número do pedido, mostrado na primeira coluna da lista.
    :return: O pedido.
    :raises ErroValidacao: Se o cliente não tiver nenhum pedido de budget com esse número.
    """
    pedido = pedidos_budget.obter_por_id(ligacao, identificador)
    if pedido is None or pedido.cliente_id != cliente.id:
        raise ErroValidacao(f"Não tem nenhum pedido de budget com o número {identificador}.")
    return pedido


def cancelar(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoBudget:
    """Cancela um pedido de alteração de budget do cliente que ainda esteja pendente.

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
    return pedidos_budget.definir_estado(ligacao, pedido.id, modelos.CANCELADO)
