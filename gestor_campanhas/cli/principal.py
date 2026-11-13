"""Menu inicial da aplicação.

É o primeiro menu que o utilizador vê, antes de se autenticar.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import __version__
from gestor_campanhas.cli import comum, perfis
from gestor_campanhas.erros import ErroAutenticacao
from gestor_campanhas.servicos import autenticacao

#: Opções do menu inicial, como pares ``(chave, descrição)``.
OPCOES = [
    ("1", "Entrar"),
    ("0", "Sair"),
]


def executar(ligacao: sqlite3.Connection) -> None:
    """Mostra o menu inicial até o utilizador escolher sair.

    :param ligacao: Ligação aberta à base de dados, a passar aos menus
        que precisam de ler ou guardar dados.
    """
    while True:
        escolha = comum.escolher_opcao(f"Gestor de Campanhas v{__version__}", OPCOES)
        if escolha == "0":
            print("Até breve!")
            return
        if escolha == "1":
            entrar(ligacao)


def entrar(ligacao: sqlite3.Connection) -> None:
    """Pede o email e a password e, se estiverem certos, abre o menu do perfil.

    Quando as credenciais estão erradas, mostra a mensagem e volta ao menu
    inicial.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Entrar")
    email = comum.ler_texto("Email")
    password = comum.ler_password()
    try:
        utilizador = autenticacao.autenticar(ligacao, email, password)
    except ErroAutenticacao as erro:
        print(erro)
        comum.pausa()
        return
    print(f"Bem-vindo, {utilizador.nome}.")
    perfis.executar(ligacao, utilizador)
