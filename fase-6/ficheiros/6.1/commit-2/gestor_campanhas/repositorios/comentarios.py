"""Acesso à tabela ``comentarios``.

Os comentários e as respostas ficam na mesma tabela: uma resposta é um
comentário com a coluna ``resposta_a`` preenchida. Todas as leituras trazem
também o nome e o perfil de quem escreveu, que estão na tabela
``utilizadores``.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Comentario

#: Consulta comum a todas as leituras. Junta cada comentário ao seu autor.
_SELECIONAR = """
SELECT comentarios.id, comentarios.criativo_id, comentarios.autor_id, comentarios.texto,
       comentarios.resposta_a, comentarios.criado_em,
       utilizadores.nome AS autor_nome, utilizadores.perfil AS autor_perfil
FROM comentarios
JOIN utilizadores ON utilizadores.id = comentarios.autor_id
"""


def _de_linha(linha: sqlite3.Row) -> Comentario:
    """Converte uma linha da consulta num :class:`~gestor_campanhas.modelos.Comentario`."""
    return Comentario(
        id=linha["id"],
        criativo_id=linha["criativo_id"],
        autor_id=linha["autor_id"],
        texto=linha["texto"],
        criado_em=relogio.de_texto(linha["criado_em"]),
        resposta_a=linha["resposta_a"],
        autor_nome=linha["autor_nome"],
        autor_perfil=linha["autor_perfil"],
    )


def criar(
    ligacao: sqlite3.Connection, criativo_id: int, autor_id: int, texto: str, resposta_a: int | None = None
) -> Comentario:
    """Guarda um comentário, ou a resposta a um comentário.

    :param ligacao: Ligação aberta à base de dados.
    :param criativo_id: Identificador do criativo.
    :param autor_id: Identificador de quem escreve.
    :param texto: O que foi escrito.
    :param resposta_a: Identificador do comentário a que se responde, ou
        ``None`` para um comentário novo.
    :return: O comentário guardado, já com o identificador.
    :raises sqlite3.IntegrityError: Se o criativo, o autor ou o comentário
        a que se responde não existirem.
    """
    cursor = ligacao.execute(
        "INSERT INTO comentarios (criativo_id, autor_id, texto, resposta_a, criado_em) VALUES (?, ?, ?, ?, ?)",
        (criativo_id, autor_id, texto, resposta_a, relogio.para_texto(relogio.agora())),
    )
    ligacao.commit()
    return obter_por_id(ligacao, cursor.lastrowid)


def obter_por_id(ligacao: sqlite3.Connection, identificador: int) -> Comentario | None:
    """Procura um comentário pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do comentário.
    :return: O comentário, ou ``None`` se não existir.
    """
    linha = ligacao.execute(f"{_SELECIONAR} WHERE comentarios.id = ?", (identificador,)).fetchone()
    return _de_linha(linha) if linha else None


def listar_por_criativo(ligacao: sqlite3.Connection, criativo_id: int) -> list[Comentario]:
    """Devolve os comentários e as respostas de um criativo.

    :param ligacao: Ligação aberta à base de dados.
    :param criativo_id: Identificador do criativo.
    :return: Comentários e respostas, pela ordem em que foram escritos.
    """
    linhas = ligacao.execute(
        f"{_SELECIONAR} WHERE comentarios.criativo_id = ? ORDER BY comentarios.id", (criativo_id,)
    ).fetchall()
    return [_de_linha(linha) for linha in linhas]
