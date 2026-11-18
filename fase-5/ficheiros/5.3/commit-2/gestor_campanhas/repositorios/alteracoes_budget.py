"""Acesso à tabela ``alteracoes_budget``, o histórico do budget das campanhas.

Cada linha regista uma alteração: o budget antes e depois, o motivo e a
data. As linhas só são acrescentadas, nunca alteradas nem apagadas (a não
ser quando a campanha é apagada).
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import relogio
from gestor_campanhas.modelos import AlteracaoBudget


def _de_linha(linha: sqlite3.Row) -> AlteracaoBudget:
    """Converte uma linha da tabela numa :class:`~gestor_campanhas.modelos.AlteracaoBudget`."""
    return AlteracaoBudget(
        id=linha["id"],
        campanha_id=linha["campanha_id"],
        budget_anterior_centimos=linha["budget_anterior_centimos"],
        budget_novo_centimos=linha["budget_novo_centimos"],
        motivo=linha["motivo"],
        alterado_em=relogio.de_texto(linha["alterado_em"]),
        pedido_budget_id=linha["pedido_budget_id"],
    )


def registar(
    ligacao: sqlite3.Connection,
    campanha_id: int,
    budget_anterior_centimos: int | None,
    budget_novo_centimos: int,
    motivo: str,
    pedido_budget_id: int | None = None,
) -> AlteracaoBudget:
    """Acrescenta uma alteração ao histórico do budget de uma campanha, com a data e hora atuais.

    Não altera o budget da campanha: isso é feito em
    :func:`gestor_campanhas.repositorios.campanhas.definir_budget`.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :param budget_anterior_centimos: Budget antes da alteração, ou ``None``.
    :param budget_novo_centimos: Budget depois da alteração.
    :param motivo: Porque é que o budget mudou.
    :param pedido_budget_id: Identificador do pedido de alteração de budget
        que deu origem à alteração, se houver.
    :return: A alteração registada, já com o identificador.
    :raises sqlite3.IntegrityError: Se a campanha ou o pedido não existirem.
    """
    cursor = ligacao.execute(
        "INSERT INTO alteracoes_budget "
        "(campanha_id, budget_anterior_centimos, budget_novo_centimos, motivo, pedido_budget_id, alterado_em) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            campanha_id,
            budget_anterior_centimos,
            budget_novo_centimos,
            motivo,
            pedido_budget_id,
            relogio.para_texto(relogio.agora()),
        ),
    )
    ligacao.commit()
    linha = ligacao.execute("SELECT * FROM alteracoes_budget WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _de_linha(linha)


def listar_por_campanha(ligacao: sqlite3.Connection, campanha_id: int) -> list[AlteracaoBudget]:
    """Devolve o histórico do budget de uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :return: Alterações dessa campanha, da mais antiga para a mais recente.
    """
    linhas = ligacao.execute(
        "SELECT * FROM alteracoes_budget WHERE campanha_id = ? ORDER BY id", (campanha_id,)
    ).fetchall()
    return [_de_linha(linha) for linha in linhas]
