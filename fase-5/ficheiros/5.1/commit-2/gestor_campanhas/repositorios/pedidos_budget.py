"""Acesso à tabela ``pedidos_budget``.

Todas as leituras trazem também o nome da campanha, o do cliente e o do
marketeer responsável, que estão nas tabelas ``campanhas`` e
``utilizadores``. O cliente de um pedido é sempre o cliente da campanha.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import relogio
from gestor_campanhas.modelos import PedidoBudget

#: Consulta comum a todas as leituras. Junta cada pedido à campanha, ao
#: cliente e ao marketeer responsável.
_SELECIONAR = """
SELECT pedidos_budget.id, pedidos_budget.campanha_id, pedidos_budget.budget_atual_centimos,
       pedidos_budget.budget_pedido_centimos, pedidos_budget.motivo, pedidos_budget.estado,
       pedidos_budget.parecer_viavel, pedidos_budget.parecer_justificacao, pedidos_budget.motivo_rejeicao,
       pedidos_budget.criado_em, pedidos_budget.decidido_em,
       campanhas.nome AS campanha_nome, campanhas.cliente_id, clientes.nome AS cliente_nome,
       campanhas.marketeer_id, marketeers.nome AS marketeer_nome
FROM pedidos_budget
JOIN campanhas ON campanhas.id = pedidos_budget.campanha_id
JOIN utilizadores AS clientes ON clientes.id = campanhas.cliente_id
JOIN utilizadores AS marketeers ON marketeers.id = campanhas.marketeer_id
"""

#: Estados em que um pedido ainda espera pela decisão do Administrador.
_POR_DECIDIR = "('pendente', 'em_analise')"


def _de_linha(linha: sqlite3.Row) -> PedidoBudget:
    """Converte uma linha da consulta num :class:`~gestor_campanhas.modelos.PedidoBudget`."""
    viavel = linha["parecer_viavel"]
    return PedidoBudget(
        id=linha["id"],
        campanha_id=linha["campanha_id"],
        budget_atual_centimos=linha["budget_atual_centimos"],
        budget_pedido_centimos=linha["budget_pedido_centimos"],
        motivo=linha["motivo"],
        estado=linha["estado"],
        criado_em=relogio.de_texto(linha["criado_em"]),
        parecer_viavel=None if viavel is None else bool(viavel),
        parecer_justificacao=linha["parecer_justificacao"],
        motivo_rejeicao=linha["motivo_rejeicao"],
        decidido_em=relogio.de_texto(linha["decidido_em"]) if linha["decidido_em"] else None,
        campanha_nome=linha["campanha_nome"],
        cliente_id=linha["cliente_id"],
        cliente_nome=linha["cliente_nome"],
        marketeer_id=linha["marketeer_id"],
        marketeer_nome=linha["marketeer_nome"],
    )


def criar(
    ligacao: sqlite3.Connection,
    campanha_id: int,
    budget_atual_centimos: int | None,
    budget_pedido_centimos: int,
    motivo: str,
) -> PedidoBudget:
    """Acrescenta um pedido de alteração de budget, no estado pendente.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :param budget_atual_centimos: Budget da campanha neste momento, em
        cêntimos, ou ``None`` se ainda não tem.
    :param budget_pedido_centimos: Budget pretendido, em cêntimos.
    :param motivo: Porque é que o cliente quer alterar o budget.
    :return: O pedido criado, já com o identificador.
    :raises sqlite3.IntegrityError: Se a campanha não existir.
    """
    cursor = ligacao.execute(
        "INSERT INTO pedidos_budget (campanha_id, budget_atual_centimos, budget_pedido_centimos, motivo, criado_em) "
        "VALUES (?, ?, ?, ?, ?)",
        (campanha_id, budget_atual_centimos, budget_pedido_centimos, motivo, relogio.para_texto(relogio.agora())),
    )
    ligacao.commit()
    return obter_por_id(ligacao, cursor.lastrowid)


def obter_por_id(ligacao: sqlite3.Connection, identificador: int) -> PedidoBudget | None:
    """Procura um pedido pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do pedido.
    :return: O pedido, ou ``None`` se não existir.
    """
    linha = ligacao.execute(f"{_SELECIONAR} WHERE pedidos_budget.id = ?", (identificador,)).fetchone()
    return _de_linha(linha) if linha else None


def listar_por_cliente(ligacao: sqlite3.Connection, cliente_id: int) -> list[PedidoBudget]:
    """Devolve os pedidos feitos para as campanhas de um cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente_id: Identificador do cliente.
    :return: Pedidos desse cliente, do mais recente para o mais antigo.
    """
    linhas = ligacao.execute(
        f"{_SELECIONAR} WHERE campanhas.cliente_id = ? ORDER BY pedidos_budget.id DESC", (cliente_id,)
    ).fetchall()
    return [_de_linha(linha) for linha in linhas]


def obter_por_decidir(ligacao: sqlite3.Connection, campanha_id: int) -> PedidoBudget | None:
    """Procura o pedido de uma campanha que ainda espera pela decisão do Administrador.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :return: O pedido pendente ou em análise dessa campanha, ou ``None`` se não houver.
    """
    linha = ligacao.execute(
        f"{_SELECIONAR} WHERE pedidos_budget.campanha_id = ? AND pedidos_budget.estado IN {_POR_DECIDIR}",
        (campanha_id,),
    ).fetchone()
    return _de_linha(linha) if linha else None


def definir_estado(ligacao: sqlite3.Connection, identificador: int, estado: str) -> PedidoBudget:
    """Altera o estado de um pedido.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do pedido.
    :param estado: Estado novo: um dos de :data:`~gestor_campanhas.modelos.NOMES_ESTADOS_PEDIDO`.
    :return: O pedido, já com o estado novo.
    :raises sqlite3.IntegrityError: Se o estado não for um dos previstos.
    """
    ligacao.execute("UPDATE pedidos_budget SET estado = ? WHERE id = ?", (estado, identificador))
    ligacao.commit()
    return obter_por_id(ligacao, identificador)
