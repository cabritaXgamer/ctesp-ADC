"""Menu de cada perfil, mostrado depois de o utilizador entrar.

Os três perfis usam o mesmo ciclo de menu. O que muda de perfil para perfil
é a lista de opções, definida em :data:`OPCOES`.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.modelos import Utilizador

#: Opções de cada perfil. Cada opção é um par ``(descrição, função)``; a
#: função recebe a ligação à base de dados e o utilizador que entrou.
#: A opção "Terminar sessão" é acrescentada automaticamente no fim.
OPCOES: dict[str, list] = {
    modelos.ADMINISTRADOR: [],
    modelos.MARKETEER: [],
    modelos.CLIENTE: [],
}


def executar(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Mostra o menu do perfil do utilizador até ele terminar a sessão.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que entrou.
    """
    opcoes = OPCOES[utilizador.perfil]
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(opcoes, start=1)]
    menu.append(("0", "Terminar sessão"))
    while True:
        escolha = comum.escolher_opcao(f"{utilizador.nome_perfil} — {utilizador.nome}", menu)
        if escolha == "0":
            print("Sessão terminada.")
            return
        _, funcao = opcoes[int(escolha) - 1]
        funcao(ligacao, utilizador)
