"""Alterações que cada utilizador pode fazer à sua própria conta."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.repositorios import utilizadores


def validar_password(password: str) -> None:
    """Confirma que uma password nova respeita as regras.

    :param password: Password proposta.
    :raises ErroValidacao: Se tiver menos caracteres do que
        :data:`gestor_campanhas.seguranca.TAMANHO_MINIMO`.
    """
    if len(password) < seguranca.TAMANHO_MINIMO:
        raise ErroValidacao(f"A password tem de ter pelo menos {seguranca.TAMANHO_MINIMO} caracteres.")


def alterar_password(
    ligacao: sqlite3.Connection, utilizador: Utilizador, atual: str, nova: str, confirmacao: str
) -> None:
    """Troca a password de um utilizador, depois de confirmar a atual.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que está a alterar a sua password.
    :param atual: Password atual, para confirmar que é o próprio.
    :param nova: Password nova.
    :param confirmacao: Password nova, escrita segunda vez.
    :raises ErroValidacao: Se a password atual estiver errada, se a nova não
        respeitar as regras, se for igual à atual ou se a confirmação for
        diferente.
    """
    guardado = utilizadores.obter_hash(ligacao, utilizador.id)
    if not seguranca.verificar_password(atual, guardado):
        raise ErroValidacao("A password atual não está correta.")
    validar_password(nova)
    if nova == atual:
        raise ErroValidacao("A password nova tem de ser diferente da atual.")
    if nova != confirmacao:
        raise ErroValidacao("A confirmação não é igual à password nova.")
    utilizadores.atualizar_password(ligacao, utilizador.id, seguranca.gerar_hash(nova))


def atualizar_dados(
    ligacao: sqlite3.Connection,
    utilizador: Utilizador,
    nome: str,
    telefone: str,
    empresa: str = "",
    nif: str = "",
) -> None:
    """Altera os dados de contacto de um utilizador e, nos clientes, os da empresa.

    O objeto ``utilizador`` fica atualizado com os dados novos. O email e o
    perfil não podem ser alterados pelo próprio. Os dados da empresa só são
    considerados quando o utilizador é um cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que está a alterar os seus dados.
    :param nome: Nome novo. Não pode ficar vazio.
    :param telefone: Telefone novo: vazio, ou 9 a 15 algarismos, com ou sem ``+`` no início.
    :param empresa: Nome da empresa (só clientes).
    :param nif: Número de contribuinte: vazio ou 9 algarismos (só clientes).
    :raises ErroValidacao: Se algum dos valores não respeitar as regras.
    """
    nome, telefone, empresa, nif = nome.strip(), telefone.replace(" ", ""), empresa.strip(), nif.replace(" ", "")
    if not nome:
        raise ErroValidacao("O nome não pode ficar vazio.")
    algarismos = telefone[1:] if telefone.startswith("+") else telefone
    if telefone and not (algarismos.isdigit() and 9 <= len(algarismos) <= 15):
        raise ErroValidacao("O telefone tem de ter entre 9 e 15 algarismos.")
    if utilizador.perfil == modelos.CLIENTE:
        if nif and not (nif.isdigit() and len(nif) == 9):
            raise ErroValidacao("O NIF tem de ter 9 algarismos.")
    else:
        empresa, nif = utilizador.empresa, utilizador.nif
    novo = utilizadores.atualizar_dados(ligacao, utilizador.id, nome, telefone, empresa, nif)
    utilizador.nome, utilizador.telefone = novo.nome, novo.telefone
    utilizador.empresa, utilizador.nif = novo.empresa, novo.nif
