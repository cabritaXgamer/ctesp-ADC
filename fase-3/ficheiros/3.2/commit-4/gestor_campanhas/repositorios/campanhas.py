"""Acesso à tabela ``campanhas``.

Todas as leituras trazem também o nome do cliente e o do marketeer, que estão
na tabela ``utilizadores``. As datas são guardadas como texto, no formato
``AAAA-MM-DD``.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Campanha

#: Consulta comum a todas as leituras. Junta cada campanha ao cliente e ao
#: marketeer, para se saber o nome de cada um.
_SELECIONAR = """
SELECT campanhas.id, campanhas.nome, campanhas.objetivo, campanhas.cliente_id,
       campanhas.marketeer_id, campanhas.budget_centimos, campanhas.data_inicio,
       campanhas.data_fim, clientes.nome AS cliente_nome, marketeers.nome AS marketeer_nome
FROM campanhas
JOIN utilizadores AS clientes ON clientes.id = campanhas.cliente_id
JOIN utilizadores AS marketeers ON marketeers.id = campanhas.marketeer_id
"""


def _data_de_texto(texto: str | None) -> date | None:
    """Converte o texto guardado numa data. ``None`` continua ``None``."""
    return date.fromisoformat(texto) if texto else None


def _data_para_texto(data: date | None) -> str | None:
    """Converte uma data no texto que é guardado. ``None`` continua ``None``."""
    return data.isoformat() if data else None


def _de_linha(linha: sqlite3.Row) -> Campanha:
    """Converte uma linha da consulta numa :class:`~gestor_campanhas.modelos.Campanha`."""
    return Campanha(
        id=linha["id"],
        nome=linha["nome"],
        objetivo=linha["objetivo"],
        cliente_id=linha["cliente_id"],
        marketeer_id=linha["marketeer_id"],
        budget_centimos=linha["budget_centimos"],
        data_inicio=_data_de_texto(linha["data_inicio"]),
        data_fim=_data_de_texto(linha["data_fim"]),
        cliente_nome=linha["cliente_nome"],
        marketeer_nome=linha["marketeer_nome"],
    )


def criar(
    ligacao: sqlite3.Connection,
    nome: str,
    objetivo: str,
    cliente_id: int,
    marketeer_id: int,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    budget_centimos: int | None = None,
) -> Campanha:
    """Acrescenta uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param nome: Nome da campanha.
    :param objetivo: O que se pretende com a campanha.
    :param cliente_id: Identificador do cliente a quem pertence.
    :param marketeer_id: Identificador do marketeer responsável.
    :param data_inicio: Primeiro dia da campanha.
    :param data_fim: Último dia da campanha.
    :param budget_centimos: Budget em cêntimos, ou ``None`` se ainda não foi definido.
    :return: A campanha criada, já com o identificador.
    :raises sqlite3.IntegrityError: Se o cliente ou o marketeer não existirem.
    """
    cursor = ligacao.execute(
        "INSERT INTO campanhas "
        "(nome, objetivo, cliente_id, marketeer_id, budget_centimos, data_inicio, data_fim, criada_em) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            nome,
            objetivo,
            cliente_id,
            marketeer_id,
            budget_centimos,
            _data_para_texto(data_inicio),
            _data_para_texto(data_fim),
            relogio.para_texto(relogio.agora()),
        ),
    )
    ligacao.commit()
    return obter_por_id(ligacao, cursor.lastrowid)


def obter_por_id(ligacao: sqlite3.Connection, identificador: int) -> Campanha | None:
    """Procura uma campanha pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador da campanha.
    :return: A campanha, ou ``None`` se não existir.
    """
    linha = ligacao.execute(f"{_SELECIONAR} WHERE campanhas.id = ?", (identificador,)).fetchone()
    return _de_linha(linha) if linha else None


def listar_por_marketeer(ligacao: sqlite3.Connection, marketeer_id: int) -> list[Campanha]:
    """Devolve as campanhas de que um marketeer é responsável.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer_id: Identificador do marketeer.
    :return: Campanhas desse marketeer, pela ordem em que foram criadas.
    """
    linhas = ligacao.execute(
        f"{_SELECIONAR} WHERE campanhas.marketeer_id = ? ORDER BY campanhas.id", (marketeer_id,)
    ).fetchall()
    return [_de_linha(linha) for linha in linhas]


def atualizar(
    ligacao: sqlite3.Connection,
    identificador: int,
    nome: str,
    objetivo: str,
    data_inicio: date | None,
    data_fim: date | None,
) -> Campanha:
    """Altera o nome, o objetivo e as datas de uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador da campanha.
    :param nome: Nome novo.
    :param objetivo: Objetivo novo.
    :param data_inicio: Primeiro dia novo, ou ``None`` para ficar sem data.
    :param data_fim: Último dia novo, ou ``None`` para ficar sem data.
    :return: A campanha, já com os dados novos.
    """
    ligacao.execute(
        "UPDATE campanhas SET nome = ?, objetivo = ?, data_inicio = ?, data_fim = ? WHERE id = ?",
        (nome, objetivo, _data_para_texto(data_inicio), _data_para_texto(data_fim), identificador),
    )
    ligacao.commit()
    return obter_por_id(ligacao, identificador)


def eliminar(ligacao: sqlite3.Connection, identificador: int) -> None:
    """Apaga uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador da campanha.
    """
    ligacao.execute("DELETE FROM campanhas WHERE id = ?", (identificador,))
    ligacao.commit()
