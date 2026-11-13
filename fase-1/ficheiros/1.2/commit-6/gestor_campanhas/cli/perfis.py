"""Menu de cada perfil, mostrado depois de o utilizador entrar.

Os três perfis usam o mesmo ciclo de menu. O que muda de perfil para perfil
é a lista de opções, definida em :data:`OPCOES`.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.servicos import sessoes
from gestor_campanhas.servicos.sessoes import SessaoAtiva

#: Opções de cada perfil. Cada opção é um par ``(descrição, função)``; a
#: função recebe a ligação à base de dados e o utilizador que entrou.
#: A opção "Terminar sessão" é acrescentada automaticamente no fim.
OPCOES: dict[str, list] = {
    modelos.ADMINISTRADOR: [],
    modelos.MARKETEER: [],
    modelos.CLIENTE: [],
}


def executar(ligacao: sqlite3.Connection, sessao: SessaoAtiva) -> None:
    """Mostra o menu do perfil até a sessão terminar.

    A sessão termina quando o utilizador escolhe "Terminar sessão" ou quando
    responde ao menu depois de ter passado o limite de inatividade. Nos dois
    casos a saída fica registada, com o respetivo motivo.

    :param ligacao: Ligação aberta à base de dados.
    :param sessao: Sessão do utilizador que entrou.
    """
    utilizador = sessao.utilizador
    opcoes = OPCOES[utilizador.perfil]
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(opcoes, start=1)]
    menu.append(("0", "Terminar sessão"))
    while True:
        escolha = comum.escolher_opcao(f"{utilizador.nome_perfil} — {utilizador.nome}", menu)
        if sessao.expirou():
            sessoes.terminar(ligacao, sessao, modelos.INATIVIDADE)
            minutos = int(sessao.limite.total_seconds() // 60)
            print(f"A sessão terminou por inatividade (mais de {minutos} minutos sem atividade).")
            print("Entre de novo para continuar.")
            comum.pausa()
            return
        sessao.registar_atividade()
        if escolha == "0":
            sessoes.terminar(ligacao, sessao, modelos.LOGOUT)
            print("Sessão terminada.")
            return
        _, funcao = opcoes[int(escolha) - 1]
        funcao(ligacao, utilizador)
