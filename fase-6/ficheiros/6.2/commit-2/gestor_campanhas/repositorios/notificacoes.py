"""Acesso à tabela ``notificacoes``.

A coluna ``item_id`` não é uma chave estrangeira, porque pode apontar para
tabelas diferentes, conforme a coluna ``sobre``. Se o item for apagado, a
notificação fica; quem a abrir é avisado de que o item já não existe.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Notificacao

#: Consulta comum a todas as leituras.
_SELECIONAR = "SELECT id, utilizador_id, texto, sobre, item_id, lida, criada_em FROM notificacoes"


def _de_linha(linha: sqlite3.Row) -> Notificacao:
    """Converte uma linha da tabela numa :class:`~gestor_campanhas.modelos.Notificacao`."""
    return Notificacao(
        id=linha["id"],
        utilizador_id=linha["utilizador_id"],
        texto=linha["texto"],
        sobre=linha["sobre"],
        item_id=linha["item_id"],
        criada_em=relogio.de_texto(linha["criada_em"]),
        lida=bool(linha["lida"]),
    )


def criar(ligacao: sqlite3.Connection, utilizador_id: int, texto: str, sobre: str, item_id: int) -> Notificacao:
    """Guarda uma notificação nova, por ler.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador de quem a recebe.
    :param texto: O que aconteceu.
    :param sobre: Tipo do item a que se refere.
    :param item_id: Identificador do item.
    :return: A notificação guardada, já com o identificador.
    :raises sqlite3.IntegrityError: Se o utilizador não existir ou o tipo do
        item não for um dos previstos.
    """
    cursor = ligacao.execute(
        "INSERT INTO notificacoes (utilizador_id, texto, sobre, item_id, criada_em) VALUES (?, ?, ?, ?, ?)",
        (utilizador_id, texto, sobre, item_id, relogio.para_texto(relogio.agora())),
    )
    ligacao.commit()
    return obter_por_id(ligacao, cursor.lastrowid)


def obter_por_id(ligacao: sqlite3.Connection, identificador: int) -> Notificacao | None:
    """Procura uma notificação pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador da notificação.
    :return: A notificação, ou ``None`` se não existir.
    """
    linha = ligacao.execute(f"{_SELECIONAR} WHERE id = ?", (identificador,)).fetchone()
    return _de_linha(linha) if linha else None


def listar_por_utilizador(ligacao: sqlite3.Connection, utilizador_id: int) -> list[Notificacao]:
    """Devolve as notificações de um utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do utilizador.
    :return: Notificações, da mais recente para a mais antiga.
    """
    linhas = ligacao.execute(f"{_SELECIONAR} WHERE utilizador_id = ? ORDER BY id DESC", (utilizador_id,)).fetchall()
    return [_de_linha(linha) for linha in linhas]


def contar_por_ler(ligacao: sqlite3.Connection, utilizador_id: int) -> int:
    """Conta as notificações por ler de um utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do utilizador.
    :return: Número de notificações por ler.
    """
    return ligacao.execute(
        "SELECT COUNT(*) FROM notificacoes WHERE utilizador_id = ? AND lida = 0", (utilizador_id,)
    ).fetchone()[0]


def marcar_como_lida(ligacao: sqlite3.Connection, identificador: int) -> Notificacao:
    """Marca uma notificação como lida.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador da notificação.
    :return: A notificação, já lida.
    """
    ligacao.execute("UPDATE notificacoes SET lida = 1 WHERE id = ?", (identificador,))
    ligacao.commit()
    return obter_por_id(ligacao, identificador)


def marcar_todas_como_lidas(ligacao: sqlite3.Connection, utilizador_id: int) -> int:
    """Marca como lidas todas as notificações por ler de um utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do utilizador.
    :return: Número de notificações que estavam por ler.
    """
    cursor = ligacao.execute("UPDATE notificacoes SET lida = 1 WHERE utilizador_id = ? AND lida = 0", (utilizador_id,))
    ligacao.commit()
    return cursor.rowcount
