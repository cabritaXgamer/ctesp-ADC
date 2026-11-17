"""Acesso à tabela ``criativos``.

Todas as leituras trazem também o nome da campanha a que o criativo pertence,
que está na tabela ``campanhas``. Os prazos são guardados como texto, no
formato ``AAAA-MM-DD``.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Criativo

#: Consulta comum a todas as leituras. Junta cada criativo à sua campanha,
#: para se saber o nome dela.
_SELECIONAR = """
SELECT criativos.id, criativos.campanha_id, criativos.nome, criativos.descricao,
       criativos.custo_centimos, criativos.prazo, criativos.publico_alvo,
       criativos.plataforma, criativos.estado, campanhas.nome AS campanha_nome
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
        custo_centimos=linha["custo_centimos"],
        prazo=date.fromisoformat(linha["prazo"]) if linha["prazo"] else None,
        publico_alvo=linha["publico_alvo"],
        plataforma=linha["plataforma"],
        estado=linha["estado"],
        campanha_nome=linha["campanha_nome"],
    )


def criar(
    ligacao: sqlite3.Connection,
    campanha_id: int,
    nome: str,
    descricao: str,
    custo_centimos: int | None = None,
    prazo: date | None = None,
    publico_alvo: str = "",
    plataforma: str = "",
) -> Criativo:
    """Acrescenta um criativo a uma campanha. O criativo começa em preparação.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha_id: Identificador da campanha.
    :param nome: Nome do criativo.
    :param descricao: O que o criativo mostra ou diz.
    :param custo_centimos: Custo estimado em cêntimos, ou ``None``.
    :param prazo: Dia em que deve estar pronto, ou ``None``.
    :param publico_alvo: A quem se destina.
    :param plataforma: Plataforma onde vai ser publicado.
    :return: O criativo criado, já com o identificador.
    :raises sqlite3.IntegrityError: Se a campanha não existir.
    """
    cursor = ligacao.execute(
        "INSERT INTO criativos "
        "(campanha_id, nome, descricao, custo_centimos, prazo, publico_alvo, plataforma, criado_em) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            campanha_id,
            nome,
            descricao,
            custo_centimos,
            prazo.isoformat() if prazo else None,
            publico_alvo,
            plataforma,
            relogio.para_texto(relogio.agora()),
        ),
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


def atualizar(
    ligacao: sqlite3.Connection,
    identificador: int,
    nome: str,
    descricao: str,
    custo_centimos: int | None = None,
    prazo: date | None = None,
    publico_alvo: str = "",
    plataforma: str = "",
) -> Criativo:
    """Altera os dados de um criativo. O estado não muda.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do criativo.
    :param nome: Nome novo.
    :param descricao: Descrição nova.
    :param custo_centimos: Custo novo em cêntimos, ou ``None`` para ficar por indicar.
    :param prazo: Prazo novo, ou ``None`` para ficar sem prazo.
    :param publico_alvo: Público-alvo novo.
    :param plataforma: Plataforma nova.
    :return: O criativo, já com os dados novos.
    """
    ligacao.execute(
        "UPDATE criativos SET nome = ?, descricao = ?, custo_centimos = ?, prazo = ?, publico_alvo = ?, "
        "plataforma = ? WHERE id = ?",
        (
            nome,
            descricao,
            custo_centimos,
            prazo.isoformat() if prazo else None,
            publico_alvo,
            plataforma,
            identificador,
        ),
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
