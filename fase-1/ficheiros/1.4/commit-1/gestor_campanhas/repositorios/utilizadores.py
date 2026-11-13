"""Acesso à tabela ``utilizadores``."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import relogio
from gestor_campanhas.modelos import Utilizador

_COLUNAS = "id, nome, email, perfil, ativo, telefone, empresa, nif"


def _de_linha(linha: sqlite3.Row) -> Utilizador:
    """Converte uma linha da tabela num :class:`~gestor_campanhas.modelos.Utilizador`."""
    return Utilizador(
        id=linha["id"],
        nome=linha["nome"],
        email=linha["email"],
        perfil=linha["perfil"],
        ativo=bool(linha["ativo"]),
        telefone=linha["telefone"],
        empresa=linha["empresa"],
        nif=linha["nif"],
    )


def normalizar_email(email: str) -> str:
    """Põe um email na forma em que é guardado: sem espaços e em minúsculas.

    :param email: Email tal como foi escrito.
    :return: Email normalizado.
    """
    return email.strip().lower()


def criar(
    ligacao: sqlite3.Connection,
    nome: str,
    email: str,
    password_hash: str,
    perfil: str,
    telefone: str = "",
    empresa: str = "",
    nif: str = "",
) -> Utilizador:
    """Acrescenta um utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param nome: Nome da pessoa.
    :param email: Email, que tem de ser único.
    :param password_hash: Hash da password (ver :mod:`gestor_campanhas.seguranca`).
    :param perfil: Um dos perfis de :mod:`gestor_campanhas.modelos`.
    :param telefone: Contacto telefónico.
    :param empresa: Nome da empresa, para clientes.
    :param nif: Número de contribuinte, para clientes.
    :return: O utilizador criado, já com o identificador.
    :raises sqlite3.IntegrityError: Se o email já existir ou o perfil for inválido.
    """
    cursor = ligacao.execute(
        "INSERT INTO utilizadores (nome, email, password_hash, perfil, telefone, empresa, nif, criado_em) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            nome.strip(),
            normalizar_email(email),
            password_hash,
            perfil,
            telefone.strip(),
            empresa.strip(),
            nif.strip(),
            relogio.para_texto(relogio.agora()),
        ),
    )
    ligacao.commit()
    return obter_por_id(ligacao, cursor.lastrowid)


def obter_por_id(ligacao: sqlite3.Connection, identificador: int) -> Utilizador | None:
    """Procura um utilizador pelo identificador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do utilizador.
    :return: O utilizador, ou ``None`` se não existir.
    """
    linha = ligacao.execute(f"SELECT {_COLUNAS} FROM utilizadores WHERE id = ?", (identificador,)).fetchone()
    return _de_linha(linha) if linha else None


def obter_por_email(ligacao: sqlite3.Connection, email: str) -> Utilizador | None:
    """Procura um utilizador pelo email.

    :param ligacao: Ligação aberta à base de dados.
    :param email: Email a procurar. Maiúsculas e espaços à volta não contam.
    :return: O utilizador, ou ``None`` se não existir.
    """
    linha = ligacao.execute(
        f"SELECT {_COLUNAS} FROM utilizadores WHERE email = ?", (normalizar_email(email),)
    ).fetchone()
    return _de_linha(linha) if linha else None


def obter_hash(ligacao: sqlite3.Connection, identificador: int) -> str | None:
    """Devolve o hash da password de um utilizador.

    O hash não faz parte de :class:`~gestor_campanhas.modelos.Utilizador`,
    para não andar pela aplicação sem necessidade.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do utilizador.
    :return: O hash guardado, ou ``None`` se o utilizador não existir.
    """
    linha = ligacao.execute("SELECT password_hash FROM utilizadores WHERE id = ?", (identificador,)).fetchone()
    return linha["password_hash"] if linha else None


def contar(ligacao: sqlite3.Connection) -> int:
    """Conta os utilizadores que existem.

    :param ligacao: Ligação aberta à base de dados.
    :return: Número de utilizadores.
    """
    return ligacao.execute("SELECT COUNT(*) FROM utilizadores").fetchone()[0]


def atualizar_password(ligacao: sqlite3.Connection, identificador: int, password_hash: str) -> None:
    """Substitui o hash da password de um utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do utilizador.
    :param password_hash: Hash da nova password.
    """
    ligacao.execute("UPDATE utilizadores SET password_hash = ? WHERE id = ?", (password_hash, identificador))
    ligacao.commit()


def atualizar_dados(
    ligacao: sqlite3.Connection, identificador: int, nome: str, telefone: str, empresa: str, nif: str
) -> Utilizador:
    """Altera o nome, o telefone e os dados da empresa de um utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Identificador do utilizador.
    :param nome: Novo nome.
    :param telefone: Novo telefone.
    :param empresa: Novo nome da empresa.
    :param nif: Novo número de contribuinte.
    :return: O utilizador, já com os dados novos.
    """
    ligacao.execute(
        "UPDATE utilizadores SET nome = ?, telefone = ?, empresa = ?, nif = ? WHERE id = ?",
        (nome, telefone, empresa, nif, identificador),
    )
    ligacao.commit()
    return obter_por_id(ligacao, identificador)

