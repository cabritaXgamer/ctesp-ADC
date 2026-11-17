"""Acesso à tabela ``criativos``.

Todas as leituras trazem também o nome da campanha a que o criativo pertence,
que está na tabela ``campanhas``.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Criativo

#: Consulta comum a todas as leituras. Junta cada criativo à sua campanha,
#: para se saber o nome dela.
_SELECIONAR = """
SELECT criativos.id, criativos.campanha_id, criativos.nome, criativos.descricao,
       criativos.estado, campanhas.nome AS campanha_nome
FROM criativos
JOIN campanhas ON campanhas.id = criativos.campanha_id
"""


def _de_linha(linha: sqlite3.Row) -> Criativo:
    """Converte uma linha da consulta num :class:`~gestor_campanhas.modelos.Criativo`."""
    return Criativo(
        id=linha["id"],
        campanha_id=linha["campanha_id"],
        nome=linha["nome"],
        descricao=linha["descricao"],
        estado=linha["estado"],
        campanha_nome=linha["campanha_nome"],
    )


def criar(ligacao: sqlite3.Connection, campanha_id: int, nome: str, descricao: str) -> Criativo:
    """Acrescenta um criativo a uma campanha. O criativo começa em preparação.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :param nome: Nome do criativo.
    :param descricao: O que o criativo mostra ou diz.
    :return: O criativo criado, já com o identificador.
    :raises sqlite3.IntegrityError: Se a campanha não existir.
    """
    cursor = ligacao.execute(
        "INSERT INTO criativos (campanha_id, nome, descricao, criado_em) VALUES (?, ?, ?, ?)",
        (campanha_id, nome, descricao, relogio.para_texto(relogio.agora())),
    )
    ligacao.commit()
    return obter_por_id(ligacao, cursor.lastrowid)


def obter_por_id(ligacao: sqlite3.Connection, identificador: int) -> Criativo | None:
    """Procura um criativo pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do criativo.
    :return: O criativo, ou ``None`` se não existir.
    """
    linha = ligacao.execute(f"{_SELECIONAR} WHERE criativos.id = ?", (identificador,)).fetchone()
    return _de_linha(linha) if linha else None


def listar_por_campanha(ligacao: sqlite3.Connection, campanha_id: int) -> list[Criativo]:
    """Devolve os criativos de uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :return: Criativos dessa campanha, pela ordem em que foram criados.
    """
    linhas = ligacao.execute(
        f"{_SELECIONAR} WHERE criativos.campanha_id = ? ORDER BY criativos.id", (campanha_id,)
    ).fetchall()
    return [_de_linha(linha) for linha in linhas]


def atualizar(ligacao: sqlite3.Connection, identificador: int, nome: str, descricao: str) -> Criativo:
    """Altera o nome e a descrição de um criativo.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do criativo.
    :param nome: Nome novo.
    :param descricao: Descrição nova.
    :return: O criativo, já com os dados novos.
    """
    ligacao.execute(
        "UPDATE criativos SET nome = ?, descricao = ? WHERE id = ?", (nome, descricao, identificador)
    )
    ligacao.commit()
    return obter_por_id(ligacao, identificador)


def eliminar(ligacao: sqlite3.Connection, identificador: int) -> None:
    """Apaga um criativo.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do criativo.
    """
    ligacao.execute("DELETE FROM criativos WHERE id = ?", (identificador,))
    ligacao.commit()


def contar_por_campanha(ligacao: sqlite3.Connection, campanha_id: int) -> int:
    """Conta os criativos de uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :return: Número de criativos dessa campanha.
    """
    return ligacao.execute("SELECT COUNT(*) FROM criativos WHERE campanha_id = ?", (campanha_id,)).fetchone()[0]
