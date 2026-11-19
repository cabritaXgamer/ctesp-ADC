"""Acesso à tabela ``atividades``.

Cada linha é uma alteração feita por um marketeer: criar, editar ou eliminar
um criativo, mudar o estado dele, anexar um ficheiro, responder a um
comentário. O registo só cresce: não há funções para alterar ou apagar linhas.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Atividade


def _de_linha(linha: sqlite3.Row) -> Atividade:
    """Converte uma linha da tabela numa :class:`~gestor_campanhas.modelos.Atividade`."""
    return Atividade(
        id=linha["id"],
        utilizador_id=linha["utilizador_id"],
        descricao=linha["descricao"],
        registada_em=relogio.de_texto(linha["registada_em"]),
    )


def registar(ligacao: sqlite3.Connection, utilizador_id: int, descricao: str) -> Atividade:
    """Regista uma alteração feita por um marketeer, com a data e a hora atuais.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do marketeer.
    :param descricao: O que fez.
    :return: A atividade registada.
    :raises sqlite3.IntegrityError: Se o utilizador não existir.
    """
    cursor = ligacao.execute(
        "INSERT INTO atividades (utilizador_id, descricao, registada_em) VALUES (?, ?, ?)",
        (utilizador_id, descricao, relogio.para_texto(relogio.agora())),
    )
    ligacao.commit()
    linha = ligacao.execute("SELECT * FROM atividades WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _de_linha(linha)


def listar_por_utilizador(ligacao: sqlite3.Connection, utilizador_id: int, limite: int = 5) -> list[Atividade]:
    """Devolve as atividades mais recentes de um marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do marketeer.
    :param limite: Número máximo de atividades a devolver.
    :return: Atividades, da mais recente para a mais antiga.
    """
    linhas = ligacao.execute(
        "SELECT * FROM atividades WHERE utilizador_id = ? ORDER BY id DESC LIMIT ?", (utilizador_id, limite)
    ).fetchall()
    return [_de_linha(linha) for linha in linhas]


def ultima_por_utilizador(ligacao: sqlite3.Connection) -> dict[int, datetime]:
    """Devolve a data da atividade mais recente de cada marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :return: Dicionário do identificador do marketeer para a data e hora da
        última atividade. Quem nunca teve atividade não aparece.
    """
    linhas = ligacao.execute(
        "SELECT utilizador_id, MAX(registada_em) AS ultima FROM atividades GROUP BY utilizador_id"
    ).fetchall()
    return {linha["utilizador_id"]: relogio.de_texto(linha["ultima"]) for linha in linhas}
