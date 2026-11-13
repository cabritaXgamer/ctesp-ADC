"""Acesso à tabela ``sessoes``."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Sessao


def _de_linha(linha: sqlite3.Row) -> Sessao:
    """Converte uma linha da tabela numa :class:`~gestor_campanhas.modelos.Sessao`."""
    return Sessao(
        id=linha["id"],
        utilizador_id=linha["utilizador_id"],
        entrada=relogio.de_texto(linha["entrada"]),
        saida=relogio.de_texto(linha["saida"]) if linha["saida"] else None,
        motivo_saida=linha["motivo_saida"],
    )


def abrir(ligacao: sqlite3.Connection, utilizador_id: int, entrada: datetime) -> Sessao:
    """Regista a entrada de um utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador_id: Identificador do utilizador que entrou.
    :param entrada: Data e hora da entrada.
    :return: A sessão criada, ainda sem saída.
    """
    cursor = ligacao.execute(
        "INSERT INTO sessoes (utilizador_id, entrada) VALUES (?, ?)",
        (utilizador_id, relogio.para_texto(entrada)),
    )
    ligacao.commit()
    return obter(ligacao, cursor.lastrowid)


def fechar(ligacao: sqlite3.Connection, identificador: int, saida: datetime, motivo: str) -> None:
    """Regista a saída de uma sessão que ainda está aberta.

    Uma sessão que já tem saída fica como está.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador da sessão.
    :param saida: Data e hora da saída.
    :param motivo: ``"logout"`` ou ``"inatividade"``.
    """
    ligacao.execute(
        "UPDATE sessoes SET saida = ?, motivo_saida = ? WHERE id = ? AND saida IS NULL",
        (relogio.para_texto(saida), motivo, identificador),
    )
    ligacao.commit()


def obter(ligacao: sqlite3.Connection, identificador: int) -> Sessao | None:
    """Procura uma sessão pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador da sessão.
    :return: A sessão, ou ``None`` se não existir.
    """
    linha = ligacao.execute(
        "SELECT id, utilizador_id, entrada, saida, motivo_saida FROM sessoes WHERE id = ?", (identificador,)
    ).fetchone()
    return _de_linha(linha) if linha else None


def listar_por_perfil(
    ligacao: sqlite3.Connection,
    perfil: str,
    desde: datetime | None = None,
    ate: datetime | None = None,
) -> list[tuple[Sessao, str]]:
    """Lista as sessões dos utilizadores de um perfil, da mais recente para a mais antiga.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil dos utilizadores, por exemplo ``"marketeer"``.
    :param desde: Se indicado, só entram sessões com entrada a partir deste momento.
    :param ate: Se indicado, só entram sessões com entrada antes deste momento.
    :return: Lista de pares ``(sessão, nome do utilizador)``.
    """
    consulta = (
        "SELECT s.id, s.utilizador_id, s.entrada, s.saida, s.motivo_saida, u.nome "
        "FROM sessoes s JOIN utilizadores u ON u.id = s.utilizador_id "
        "WHERE u.perfil = ?"
    )
    valores: list = [perfil]
    if desde is not None:
        consulta += " AND s.entrada >= ?"
        valores.append(relogio.para_texto(desde))
    if ate is not None:
        consulta += " AND s.entrada < ?"
        valores.append(relogio.para_texto(ate))
    consulta += " ORDER BY s.entrada DESC, s.id DESC"
    return [(_de_linha(linha), linha["nome"]) for linha in ligacao.execute(consulta, valores)]
