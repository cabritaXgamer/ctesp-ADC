"""Notificações, nos menus do Marketeer e do Cliente.

A opção "Notificações" mostra as notificações do utilizador, da mais recente
para a mais antiga, e diz quais estão por ler. Abrir uma notificação marca-a
como lida e mostra logo o item a que se refere: a campanha, o pedido de
alteração de budget ou o criativo.

Enquanto houver notificações por ler, o menu do perfil diz quantas são.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.cli import budget as menu_budget
from gestor_campanhas.cli import campanhas as menu_campanhas
from gestor_campanhas.cli import comum
from gestor_campanhas.cli import criativos as menu_criativos
from gestor_campanhas.cli.pedidos import resumir
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Notificacao, Utilizador
from gestor_campanhas.servicos import budget, campanhas, criativos, notificacoes

#: Número máximo de caracteres do texto de uma notificação que cabem na lista.
LARGURA_TEXTO = 60


def contagem(total: int, por_ler: int) -> str:
    """Escreve quantas notificações há e quantas estão por ler.

    :param total: Número de notificações.
    :param por_ler: Número de notificações por ler.
    :return: Por exemplo ``"3 notificações, 1 por ler."``.
    """
    palavra = "notificação" if total == 1 else "notificações"
    return f"{total} {palavra}, {por_ler} por ler."


def mostrar_notificacoes(lista: list[Notificacao]) -> None:
    """Mostra uma tabela de notificações, com o total no fim.

    :param lista: Notificações a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Data", "Estado", "Sobre", "Mensagem"],
        [
            [
                str(notificacao.id),
                notificacao.criada_em.strftime("%Y-%m-%d %H:%M"),
                "Lida" if notificacao.lida else "Por ler",
                notificacao.nome_item,
                resumir(notificacao.texto, LARGURA_TEXTO),
            ]
            for notificacao in lista
        ],
    )
    print(f"\n{contagem(len(lista), sum(1 for notificacao in lista if not notificacao.lida))}")


def avisar_se_houver_por_ler(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Diz quantas notificações o utilizador tem por ler. Não mostra nada se não tiver nenhuma.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que entrou.
    """
    por_ler = notificacoes.contar_por_ler(ligacao, utilizador)
    if por_ler == 1:
        print('\nTem 1 notificação por ler, na opção "Notificações".')
    elif por_ler:
        print(f'\nTem {por_ler} notificações por ler, na opção "Notificações".')


def mostrar_item(ligacao: sqlite3.Connection, utilizador: Utilizador, notificacao: Notificacao) -> None:
    """Mostra o item a que uma notificação se refere, com os dados que o utilizador pode ver.

    Se o item já não existir, ou se o utilizador já não lhe tiver acesso (por
    exemplo, porque a campanha passou para outro marketeer), mostra uma mensagem.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que abriu a notificação.
    :param notificacao: Notificação aberta.
    """
    do_marketeer = utilizador.perfil == modelos.MARKETEER
    try:
        if notificacao.sobre == modelos.SOBRE_CAMPANHA:
            procurar = campanhas.obter_do_marketeer if do_marketeer else campanhas.obter_do_cliente
            campanha = procurar(ligacao, utilizador, notificacao.item_id)
            menu_campanhas.mostrar_detalhes(campanha, criativos.despesa(ligacao, campanha))
        elif notificacao.sobre == modelos.SOBRE_PEDIDO_BUDGET:
            procurar = budget.obter_do_marketeer if do_marketeer else budget.obter_do_cliente
            menu_budget.mostrar_detalhes(procurar(ligacao, utilizador, notificacao.item_id), com_parecer=do_marketeer)
        else:
            procurar = criativos.obter_do_marketeer if do_marketeer else criativos.obter_do_cliente
            criativo = procurar(ligacao, utilizador, notificacao.item_id)
            menu_criativos.mostrar_detalhes(criativo)
            menu_criativos.mostrar_comentarios(ligacao, criativo)
    except ErroValidacao as erro:
        print(f"{erro} O item desta notificação já não está disponível.")


def abrir(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Pede o número de uma notificação, marca-a como lida e mostra-a, com o item a que se refere.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que está a consultar.
    """
    comum.titulo("Abrir notificação")
    numero = comum.ler_numero("Número da notificação (Enter para cancelar)")
    if numero is None:
        return
    try:
        notificacao = notificacoes.abrir(ligacao, utilizador, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    print(f"\nNotificação n.º {notificacao.id}, de {notificacao.criada_em.strftime('%Y-%m-%d %H:%M')}")
    print(f"  {notificacao.texto}\n")
    mostrar_item(ligacao, utilizador, notificacao)
    comum.pausa()


def marcar_todas(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Marca como lidas todas as notificações do utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que está a consultar.
    """
    total = notificacoes.marcar_todas_como_lidas(ligacao, utilizador)
    if total == 0:
        print("\nNão havia notificações por ler.")
    elif total == 1:
        print("\n1 notificação marcada como lida.")
    else:
        print(f"\n{total} notificações marcadas como lidas.")
    comum.pausa()


#: Opções do menu de notificações. Cada opção é um par ``(descrição, função)``;
#: a função recebe a ligação à base de dados e o utilizador.
ACOES = [
    ("Abrir notificação", abrir),
    ("Marcar todas como lidas", marcar_todas),
]


def do_utilizador(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Notificações" dos menus do Marketeer e do Cliente.

    A lista volta a aparecer depois de cada opção, já com as alterações.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que está a usar o menu.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo("As minhas notificações")
        lista = notificacoes.listar(ligacao, utilizador)
        if lista:
            mostrar_notificacoes(lista)
        else:
            print("Ainda não tem notificações.")
        escolha = comum.escolher_opcao("Notificações", menu)
        if escolha == "0":
            return
        _, funcao = ACOES[int(escolha) - 1]
        funcao(ligacao, utilizador)
