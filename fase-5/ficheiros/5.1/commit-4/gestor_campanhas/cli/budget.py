"""Pedidos de alteração de budget, nos menus dos perfis.

O Cliente pede a alteração do budget de uma campanha, acompanha os seus
pedidos e pode cancelar os que ainda estão pendentes. Estas opções aparecem
na opção "Pedidos de campanha" do Cliente, por baixo dos pedidos de nova
campanha.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import dinheiro, modelos, relogio
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import PedidoBudget, Utilizador
from gestor_campanhas.servicos import budget, campanhas


def valor(centimos: int | None) -> str:
    """Escreve um budget como é mostrado nas listas.

    :param centimos: Valor em cêntimos, ou ``None``.
    :return: O valor em euros, ou ``"Por definir"`` se não houver valor.
    """
    return "Por definir" if centimos is None else dinheiro.formatar(centimos)


def mostrar_pedidos_do_cliente(lista: list[PedidoBudget]) -> None:
    """Mostra uma tabela com os pedidos de alteração de budget de um cliente, com o total no fim.

    As colunas ``De`` e ``Para`` são o budget da campanha quando o pedido foi
    feito e o budget pedido.

    :param lista: Pedidos a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Feito em", "Campanha", "De", "Para", "Estado"],
        [
            [
                str(pedido.id),
                pedido.criado_em.strftime("%Y-%m-%d"),
                pedido.campanha_nome,
                valor(pedido.budget_atual_centimos),
                valor(pedido.budget_pedido_centimos),
                pedido.nome_estado,
            ]
            for pedido in lista
        ],
    )
    print(f"\n{len(lista)} {'pedido' if len(lista) == 1 else 'pedidos'} de alteração de budget.")


def mostrar_detalhes(pedido: PedidoBudget) -> None:
    """Mostra todos os dados de um pedido de alteração de budget, um por linha.

    O motivo da rejeição só aparece nos pedidos rejeitados.

    :param pedido: Pedido a mostrar.
    """
    print(f"Pedido de budget n.º {pedido.id}")
    print(f"  Campanha:     {pedido.campanha_nome}")
    print(f"  Feito em:     {pedido.criado_em.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Budget de:    {valor(pedido.budget_atual_centimos)}")
    print(f"  Budget para:  {valor(pedido.budget_pedido_centimos)}")
    print(f"  Motivo:       {pedido.motivo}")
    print(f"  Estado:       {pedido.nome_estado}")
    if pedido.motivo_rejeicao:
        print(f"  Rejeição:     {pedido.motivo_rejeicao}")


def pedir_alteracao(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede a campanha, o budget pretendido e o motivo, e regista o pedido.

    Mostra primeiro as campanhas do cliente que ainda não terminaram, para
    se escolher a campanha pelo número.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    """
    comum.titulo("Pedir alteração de budget")
    hoje = relogio.hoje()
    lista = [campanha for campanha in campanhas.listar_do_cliente(ligacao, cliente) if not campanha.terminada(hoje)]
    if not lista:
        print("Não tem campanhas a decorrer ou por começar. Só se pode alterar o budget de uma campanha que não terminou.")
        comum.pausa()
        return
    comum.mostrar_tabela(
        ["N.º", "Campanha", "Budget", "Estado"],
        [
            [str(campanha.id), campanha.nome, valor(campanha.budget_centimos), campanhas.estado(campanha)]
            for campanha in lista
        ],
    )
    print()
    numero = comum.ler_numero("Número da campanha (Enter para cancelar)")
    if numero is None:
        return
    try:
        campanha = budget.campanha_para_pedido(ligacao, cliente, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    print(f"\nBudget atual da campanha {campanha.nome}: {valor(campanha.budget_centimos)}.")
    novo = comum.ler_texto("Budget pretendido em euros (por exemplo 2000 ou 2000,50)")
    motivo = comum.ler_texto("Motivo do pedido")
    try:
        pedido = budget.pedir(ligacao, cliente, campanha.id, novo, motivo)
    except ErroValidacao as erro:
        print(f"\n{erro} O pedido não foi registado.")
    else:
        print(f"\nPedido registado com o número {pedido.id}.")
        print("Fica pendente até o marketeer dar o parecer e o administrador o decidir.")
    comum.pausa()


def pedir_pedido(ligacao: sqlite3.Connection, cliente: Utilizador) -> PedidoBudget | None:
    """Pede o número de um pedido de alteração de budget do cliente e devolve-o.

    Se o número não for de um pedido dele, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a usar o menu.
    :return: O pedido, ou ``None`` se foi cancelado com Enter ou o número não serve.
    """
    numero = comum.ler_numero("Número do pedido de budget (Enter para cancelar)")
    if numero is None:
        return None
    try:
        return budget.obter_do_cliente(ligacao, cliente, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None


def ver_pedido(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um pedido de alteração de budget e mostra todos os dados dele.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    """
    comum.titulo("Ver pedido de budget")
    pedido = pedir_pedido(ligacao, cliente)
    if pedido is None:
        return
    print()
    mostrar_detalhes(pedido)
    comum.pausa()


def cancelar_pedido(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um pedido de alteração de budget e cancela-o, depois de pedir confirmação.

    Só um pedido pendente pode ser cancelado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a cancelar.
    """
    comum.titulo("Cancelar pedido de budget")
    pedido = pedir_pedido(ligacao, cliente)
    if pedido is None:
        return
    print()
    mostrar_detalhes(pedido)
    print()
    if pedido.estado != modelos.PENDENTE:
        print(f"Só é possível cancelar um pedido pendente. Este pedido está no estado {pedido.nome_estado}.")
    elif comum.confirmar("Cancelar este pedido?"):
        budget.cancelar(ligacao, cliente, pedido.id)
        print("\nPedido cancelado.")
    else:
        print("\nNada foi alterado.")
    comum.pausa()
