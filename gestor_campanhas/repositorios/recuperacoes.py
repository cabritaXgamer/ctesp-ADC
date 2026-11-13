"""Acesso à tabela ``recuperacoes``, com os códigos de recuperação de password."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from gestor_campanhas import relogio


def criar(ligacao: sqlite3.Connection, utilizador_id: int, codigo_hash: str, expira_em: datetime) -> None:
    """Guarda um código novo e anula os anteriores do mesmo utilizador.

    Só o código mais recente de cada utilizador pode ser usado.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do utilizador que pediu o código.
    :param codigo_hash: Hash do código (o código em si nunca é guardado).
    :param expira_em: Momento a partir do qual o código deixa de valer.
    """
    ligacao.execute("UPDATE recuperacoes SET usado = 1 WHERE utilizador_id = ?", (utilizador_id,))
    ligacao.execute(
        "INSERT INTO recuperacoes (utilizador_id, codigo_hash, expira_em) VALUES (?, ?, ?)",
        (utilizador_id, codigo_hash, relogio.para_texto(expira_em)),
    )
    ligacao.commit()


def obter_ativa(ligacao: sqlite3.Connection, utilizador_id: int, agora: datetime) -> tuple[int, str] | None:
    """Procura o código que um utilizador pode usar neste momento.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do utilizador.
    :param agora: Momento atual, para excluir os códigos fora de prazo.
    :return: Par ``(identificador do pedido, hash do código)``, ou ``None``
        se não houver nenhum código por usar e dentro do prazo.
    """
    linha = ligacao.execute(
        "SELECT id, codigo_hash FROM recuperacoes "
        "WHERE utilizador_id = ? AND usado = 0 AND expira_em >= ? ORDER BY id DESC LIMIT 1",
        (utilizador_id, relogio.para_texto(agora)),
    ).fetchone()
    return (linha["id"], linha["codigo_hash"]) if linha else None


def marcar_usada(ligacao: sqlite3.Connection, identificador: int) -> None:
    """Marca um código como usado, para não poder ser usado outra vez.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do pedido de recuperação.
    """
    ligacao.execute("UPDATE recuperacoes SET usado = 1 WHERE id = ?", (identificador,))
    ligacao.commit()
