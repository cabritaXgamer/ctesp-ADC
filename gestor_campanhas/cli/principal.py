"""Menu inicial da aplicação.

É o primeiro menu que o utilizador vê, antes de se autenticar.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import __version__
from gestor_campanhas.cli import comum

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
            print("A autenticação ainda não está disponível nesta versão.")
            comum.pausa()
