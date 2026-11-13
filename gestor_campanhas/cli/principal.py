"""Menu inicial da aplicação.

É o primeiro menu que o utilizador vê, antes de se autenticar.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import __version__
from gestor_campanhas.cli import comum, perfis, recuperacao
from gestor_campanhas.erros import ErroAutenticacao
from gestor_campanhas.servicos import autenticacao, sessoes

#: Opções do menu inicial, como pares ``(chave, descrição)``.
OPCOES = [
    ("1", "Entrar"),
    ("2", "Recuperar a password"),
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
        if escolha == "2":
            recuperacao.recuperar(ligacao)


def entrar(ligacao: sqlite3.Connection) -> None:
    """Pede o email e a password e, se estiverem certos, abre o menu do perfil.

    Quando as credenciais estão erradas, mostra a mensagem e volta ao menu
    inicial. Quando estão certas, fica registada uma sessão, com a hora de
    entrada. A saída é sempre registada, mesmo que o programa seja
    interrompido a meio.

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
    sessao = sessoes.iniciar(ligacao, utilizador)
    try:
        perfis.executar(ligacao, sessao)
    finally:
        # Se o programa for interrompido com a sessão aberta, a saída fica
        # registada na mesma. Se já foi registada, isto não faz nada.
        sessoes.terminar(ligacao, sessao)
