"""Gestão de clientes e de marketeers, no menu do Administrador."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.servicos import gestao


def estado(conta: Utilizador) -> str:
    """Escreve o estado de uma conta por palavras.

    :param conta: Conta a descrever.
    :return: ``"Ativa"`` ou ``"Desativada"``.
    """
    return "Ativa" if conta.ativo else "Desativada"


def mostrar_clientes(contas: list[Utilizador]) -> None:
    """Mostra uma tabela de clientes, com o total no fim.

    :param contas: Clientes a mostrar.
    """
    linhas = [
        [str(conta.id), conta.nome, conta.empresa, conta.email, conta.telefone, estado(conta)] for conta in contas
    ]
    comum.mostrar_tabela(["N.º", "Nome", "Empresa", "Email", "Telefone", "Estado"], linhas)
    print(f"\n{len(contas)} {'cliente' if len(contas) == 1 else 'clientes'}.")


def clientes(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Mostra a lista de clientes, com pesquisa opcional por nome.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a consultar.
    """
    comum.titulo("Clientes")
    pesquisa = comum.ler_texto("Pesquisar por nome (Enter para ver todos)", obrigatorio=False)
    contas = gestao.listar(ligacao, modelos.CLIENTE, pesquisa)
    print()
    if contas:
        mostrar_clientes(contas)
    elif pesquisa:
        print(f'Não há clientes com "{pesquisa}" no nome.')
    else:
        print("Ainda não há clientes.")
    comum.pausa()
