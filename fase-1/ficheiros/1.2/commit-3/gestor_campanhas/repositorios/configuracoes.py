"""Acesso à tabela ``configuracoes``.

Guarda definições que podem ser alteradas durante a utilização da aplicação,
como pares chave/valor. Os valores são sempre texto.
"""

from __future__ import annotations

import sqlite3


def obter(ligacao: sqlite3.Connection, chave: str, omissao: str | None = None) -> str | None:
    """Lê o valor de uma definição.

    :param ligacao: Ligação aberta à base de dados.
    :param chave: Nome da definição.
    :param omissao: Valor a devolver se a definição ainda não existir.
    :return: O valor guardado, ou ``omissao``.
    """
    linha = ligacao.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,)).fetchone()
    return linha["valor"] if linha else omissao


def definir(ligacao: sqlite3.Connection, chave: str, valor: str) -> None:
    """Guarda o valor de uma definição, substituindo o anterior se existir.

    :param ligacao: Ligação aberta à base de dados.
    :param chave: Nome da definição.
    :param valor: Valor a guardar.
    """
    ligacao.execute(
        "INSERT INTO configuracoes (chave, valor) VALUES (?, ?) "
        "ON CONFLICT (chave) DO UPDATE SET valor = excluded.valor",
        (chave, valor),
    )
    ligacao.commit()
