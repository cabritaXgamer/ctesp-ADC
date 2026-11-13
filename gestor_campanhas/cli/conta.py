"""Opções da conta, comuns ao menu de todos os perfis."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.servicos import contas


def editar_dados(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Mostra os dados da conta e deixa alterá-los.

    Para cada dado é mostrado o valor atual; com Enter, o valor mantém-se.
    O email não pode ser alterado. A empresa e o NIF só são pedidos aos
    clientes.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que entrou.
    """
    comum.titulo("Editar os meus dados")
    print(f"Email: {utilizador.email} (não pode ser alterado)")
    print("Carregue em Enter para manter o valor que está entre parênteses retos.\n")
    nome = comum.ler_texto_com_valor("Nome", utilizador.nome)
    telefone = comum.ler_texto_com_valor("Telefone", utilizador.telefone)
    empresa, nif = utilizador.empresa, utilizador.nif
    if utilizador.perfil == modelos.CLIENTE:
        empresa = comum.ler_texto_com_valor("Empresa", utilizador.empresa)
        nif = comum.ler_texto_com_valor("NIF", utilizador.nif)
    try:
        contas.atualizar_dados(ligacao, utilizador, nome, telefone, empresa, nif)
    except ErroValidacao as erro:
        print(f"\n{erro} Os dados não foram alterados.")
    else:
        print("\nDados guardados.")
    comum.pausa()


def alterar_password(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Pede a password atual e a nova, duas vezes, e faz a alteração.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que entrou.
    """
    comum.titulo("Alterar a password")
    atual = comum.ler_password("Password atual")
    nova = comum.ler_password("Password nova")
    confirmacao = comum.ler_password("Repita a password nova")
    try:
        contas.alterar_password(ligacao, utilizador, atual, nova, confirmacao)
    except ErroValidacao as erro:
        print(f"\n{erro} A password não foi alterada.")
    else:
        print("\nPassword alterada.")
    comum.pausa()
