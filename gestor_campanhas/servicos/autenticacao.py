"""Entrada na aplicação com email e password."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import seguranca
from gestor_campanhas.erros import ErroAutenticacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.repositorios import utilizadores

#: Mensagem mostrada quando o email ou a password estão errados. É a mesma
#: nos dois casos, para não revelar se um email tem conta.
MENSAGEM_CREDENCIAIS = "Email ou password incorretos."


def autenticar(ligacao: sqlite3.Connection, email: str, password: str) -> Utilizador:
    """Confirma as credenciais e devolve o utilizador que entrou.

    :param ligacao: Ligação aberta à base de dados.
    :param email: Email introduzido.
    :param password: Password introduzida.
    :return: O utilizador autenticado.
    :raises ErroAutenticacao: Se o email não existir, a password estiver
        errada ou a conta estiver desativada.
    """
    utilizador = utilizadores.obter_por_email(ligacao, email)
    if utilizador is None:
        raise ErroAutenticacao(MENSAGEM_CREDENCIAIS)
    guardado = utilizadores.obter_hash(ligacao, utilizador.id)
    if not seguranca.verificar_password(password, guardado):
        raise ErroAutenticacao(MENSAGEM_CREDENCIAIS)
    if not utilizador.ativo:
        raise ErroAutenticacao("Esta conta está desativada. Fale com o administrador.")
    return utilizador
