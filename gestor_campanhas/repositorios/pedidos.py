"""Acesso à tabela ``pedidos_campanha``.

Todas as leituras trazem também o nome do cliente, que está na tabela
``utilizadores``. As plataformas são guardadas num só texto, separadas por
vírgulas.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import relogio
from gestor_campanhas.modelos import PedidoCampanha

#: Texto que separa as plataformas quando são guardadas.
_SEPARADOR = ", "

#: Consulta comum a todas as leituras. Junta cada pedido ao cliente que o fez.
_SELECIONAR = """
SELECT pedidos_campanha.id, pedidos_campanha.cliente_id, pedidos_campanha.objetivo,
       pedidos_campanha.orcamento_centimos, pedidos_campanha.prazo, pedidos_campanha.plataformas,
       pedidos_campanha.estado, pedidos_campanha.motivo_rejeicao, pedidos_campanha.campanha_id,
       pedidos_campanha.criado_em, utilizadores.nome AS cliente_nome
FROM pedidos_campanha
JOIN utilizadores ON utilizadores.id = pedidos_campanha.cliente_id
"""


def _de_linha(linha: sqlite3.Row) -> PedidoCampanha:
    """Converte uma linha da consulta num :class:`~gestor_campanhas.modelos.PedidoCampanha`."""
    return PedidoCampanha(
        id=linha["id"],
        cliente_id=linha["cliente_id"],
        objetivo=linha["objetivo"],
        orcamento_centimos=linha["orcamento_centimos"],
        prazo=date.fromisoformat(linha["prazo"]),
        plataformas=linha["plataformas"].split(_SEPARADOR) if linha["plataformas"] else [],
        estado=linha["estado"],
        criado_em=relogio.de_texto(linha["criado_em"]),
        motivo_rejeicao=linha["motivo_rejeicao"],
        campanha_id=linha["campanha_id"],
        cliente_nome=linha["cliente_nome"],
    )


def criar(
    ligacao: sqlite3.Connection,
    cliente_id: int,
    objetivo: str,
    orcamento_centimos: int,
    prazo: date,
    plataformas: list[str],
) -> PedidoCampanha:
    """Acrescenta um pedido de campanha, no estado pendente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente_id: Identificador do cliente que faz o pedido.
    :param objetivo: O que o cliente pretende com a campanha.
    :param orcamento_centimos: Quanto o cliente quer investir, em cêntimos.
    :param prazo: Dia até ao qual o cliente quer a campanha.
    :param plataformas: Nomes das plataformas onde quer anunciar.
    :return: O pedido criado, já com o identificador.
    :raises sqlite3.IntegrityError: Se o cliente não existir.
    """
    cursor = ligacao.execute(
        "INSERT INTO pedidos_campanha (cliente_id, objetivo, orcamento_centimos, prazo, plataformas, criado_em) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            cliente_id,
            objetivo,
            orcamento_centimos,
            prazo.isoformat(),
            _SEPARADOR.join(plataformas),
            relogio.para_texto(relogio.agora()),
        ),
    )
    ligacao.commit()
    return obter_por_id(ligacao, cursor.lastrowid)


def obter_por_id(ligacao: sqlite3.Connection, identificador: int) -> PedidoCampanha | None:
    """Procura um pedido pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do pedido.
    :return: O pedido, ou ``None`` se não existir.
    """
    linha = ligacao.execute(f"{_SELECIONAR} WHERE pedidos_campanha.id = ?", (identificador,)).fetchone()
    return _de_linha(linha) if linha else None


def listar_por_cliente(ligacao: sqlite3.Connection, cliente_id: int) -> list[PedidoCampanha]:
    """Devolve os pedidos feitos por um cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente_id: Identificador do cliente.
    :return: Pedidos desse cliente, do mais recente para o mais antigo.
    """
    linhas = ligacao.execute(
        f"{_SELECIONAR} WHERE pedidos_campanha.cliente_id = ? ORDER BY pedidos_campanha.id DESC", (cliente_id,)
    ).fetchall()
    return [_de_linha(linha) for linha in linhas]


def definir_estado(
    ligacao: sqlite3.Connection,
    identificador: int,
    estado: str,
    motivo_rejeicao: str = "",
    campanha_id: int | None = None,
) -> PedidoCampanha:
    """Altera o estado de um pedido.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do pedido.
    :param estado: Estado novo: um dos de :data:`~gestor_campanhas.modelos.NOMES_ESTADOS_PEDIDO`.
    :param motivo_rejeicao: Motivo indicado pelo Administrador, quando o pedido é rejeitado.
    :param campanha_id: Identificador da campanha criada, quando o pedido é aprovado.
    :return: O pedido, já com o estado novo.
    :raises sqlite3.IntegrityError: Se o estado não for um dos previstos.
    """
    ligacao.execute(
        "UPDATE pedidos_campanha SET estado = ?, motivo_rejeicao = ?, campanha_id = ? WHERE id = ?",
        (estado, motivo_rejeicao, campanha_id, identificador),
    )
    ligacao.commit()
    return obter_por_id(ligacao, identificador)
