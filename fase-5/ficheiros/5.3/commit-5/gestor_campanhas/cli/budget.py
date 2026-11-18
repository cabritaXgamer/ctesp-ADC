"""Pedidos de alteração de budget, nos menus dos perfis.

O Cliente pede a alteração do budget de uma campanha, acompanha os seus
pedidos e pode cancelar os que ainda estão pendentes. Estas opções aparecem
na opção "Pedidos de campanha" do Cliente, por baixo dos pedidos de nova
campanha.

O Marketeer vê os pedidos das campanhas de que é responsável e dá o seu
parecer sobre cada um, na opção "Pedidos de budget".

O Administrador vê os pedidos de todas as campanhas, com o parecer do
marketeer, e aprova-os ou rejeita-os, também na opção "Pedidos de budget".
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import dinheiro, modelos, relogio
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import PedidoBudget, Utilizador
from gestor_campanhas.servicos import budget, campanhas, criativos


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


def mostrar_detalhes(pedido: PedidoBudget, com_parecer: bool = False) -> None:
    """Mostra todos os dados de um pedido de alteração de budget, um por linha.

    O motivo da rejeição só aparece nos pedidos rejeitados.

    :param pedido: Pedido a mostrar.
    :param com_parecer: ``True`` para mostrar também o cliente e o parecer do
        marketeer, como nos menus do Marketeer e do Administrador.
    """
    print(f"Pedido de budget n.º {pedido.id}")
    print(f"  Campanha:     {pedido.campanha_nome}")
    if com_parecer:
        print(f"  Cliente:      {pedido.cliente_nome}")
    print(f"  Feito em:     {pedido.criado_em.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Budget de:    {valor(pedido.budget_atual_centimos)}")
    print(f"  Budget para:  {valor(pedido.budget_pedido_centimos)}")
    print(f"  Motivo:       {pedido.motivo}")
    print(f"  Estado:       {pedido.nome_estado}")
    if pedido.motivo_rejeicao:
        print(f"  Rejeição:     {pedido.motivo_rejeicao}")
    if com_parecer:
        print(f"  Parecer:      {pedido.nome_parecer}")
        if pedido.parecer_justificacao:
            print(f"  Justificação: {pedido.parecer_justificacao}")


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


def mostrar_pedidos_com_parecer(lista: list[PedidoBudget]) -> None:
    """Mostra uma tabela de pedidos de alteração de budget, com o cliente e o parecer.

    No fim mostra o total e quantos estão por decidir. É a tabela dos menus
    do Marketeer e do Administrador.

    :param lista: Pedidos a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Feito em", "Campanha", "Cliente", "De", "Para", "Estado", "Parecer"],
        [
            [
                str(pedido.id),
                pedido.criado_em.strftime("%Y-%m-%d"),
                pedido.campanha_nome,
                pedido.cliente_nome,
                valor(pedido.budget_atual_centimos),
                valor(pedido.budget_pedido_centimos),
                pedido.nome_estado,
                pedido.nome_parecer,
            ]
            for pedido in lista
        ],
    )
    por_decidir = sum(1 for pedido in lista if pedido.estado in budget.POR_DECIDIR)
    print(f"\n{len(lista)} {'pedido' if len(lista) == 1 else 'pedidos'}, {por_decidir} por decidir.")


def dar_parecer(ligacao: sqlite3.Connection, marketeer: Utilizador) -> None:
    """Pede o número de um pedido de budget, mostra-o e pede o parecer do marketeer.

    Além dos dados do pedido, mostra a despesa atual da campanha, para o
    marketeer comparar com o valor pedido.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a dar o parecer.
    """
    comum.titulo("Dar parecer")
    numero = comum.ler_numero("Número do pedido de budget (Enter para cancelar)")
    if numero is None:
        return
    try:
        pedido = budget.obter_do_marketeer(ligacao, marketeer, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    campanha = campanhas.obter(ligacao, pedido.campanha_id)
    print()
    mostrar_detalhes(pedido, com_parecer=True)
    print(f"\nDespesa atual da campanha: {dinheiro.formatar(criativos.despesa(ligacao, campanha))}.")
    if pedido.estado not in budget.POR_DECIDIR:
        print("\nEste pedido já não aceita parecer.")
        comum.pausa()
        return
    if pedido.parecer_viavel is not None:
        print("Já deu parecer sobre este pedido. O parecer novo substitui o anterior.")
    print()
    viavel = comum.confirmar("O pedido é viável?")
    justificacao = comum.ler_texto("Justificação")
    try:
        budget.dar_parecer(ligacao, marketeer, pedido.id, viavel, justificacao)
    except ErroValidacao as erro:
        print(f"\n{erro} O parecer não foi guardado.")
    else:
        print("\nParecer guardado. O pedido fica em análise, à espera da decisão do administrador.")
    comum.pausa()


def do_marketeer(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Pedidos de budget" do menu do Marketeer.

    Mostra os pedidos de alteração de budget das campanhas do marketeer, com
    os que estão por decidir em primeiro lugar. A lista volta a aparecer
    depois de cada parecer.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Marketeer que está a usar o menu.
    """
    while True:
        comum.titulo("Pedidos de alteração de budget das minhas campanhas")
        lista = budget.listar_do_marketeer(ligacao, utilizador)
        if lista:
            mostrar_pedidos_com_parecer(lista)
        else:
            print("Ainda não há pedidos de alteração de budget nas suas campanhas.")
        escolha = comum.escolher_opcao("Pedidos de budget", [("1", "Dar parecer"), ("0", "Voltar")])
        if escolha == "0":
            return
        dar_parecer(ligacao, utilizador)


def aprovar(ligacao: sqlite3.Connection, pedido: PedidoBudget) -> None:
    """Aprova o pedido, o que altera o budget da campanha, e mostra o resultado.

    :param ligacao: Ligação aberta à base de dados.
    :param pedido: Pedido a aprovar.
    """
    try:
        budget.aprovar(ligacao, pedido.id)
    except ErroValidacao as erro:
        print(f"\n{erro} O pedido não foi aprovado.")
        return
    campanha = campanhas.obter(ligacao, pedido.campanha_id)
    print(f"\nPedido aprovado. O budget da campanha {campanha.nome} passou a {valor(campanha.budget_centimos)}.")
    print("A alteração ficou registada no histórico do budget.")


def rejeitar(ligacao: sqlite3.Connection, pedido: PedidoBudget) -> None:
    """Pede o motivo e rejeita o pedido, depois de pedir confirmação.

    :param ligacao: Ligação aberta à base de dados.
    :param pedido: Pedido a rejeitar.
    """
    motivo = comum.ler_texto("Motivo da rejeição")
    if not comum.confirmar("Rejeitar este pedido?"):
        print("\nO pedido não foi rejeitado.")
        return
    try:
        budget.rejeitar(ligacao, pedido.id, motivo)
    except ErroValidacao as erro:
        print(f"\n{erro} O pedido não foi rejeitado.")
    else:
        print("\nPedido rejeitado. O budget da campanha não mudou.")


def decidir(ligacao: sqlite3.Connection) -> None:
    """Pede o número de um pedido de budget, mostra-o e deixa aprová-lo ou rejeitá-lo.

    Além dos dados do pedido e do parecer do marketeer, mostra o budget e a
    despesa atuais da campanha. Um pedido só pode ser decidido depois de o
    marketeer dar o parecer.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Analisar pedido de budget")
    numero = comum.ler_numero("Número do pedido de budget (Enter para cancelar)")
    if numero is None:
        return
    try:
        pedido = budget.obter(ligacao, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    campanha = campanhas.obter(ligacao, pedido.campanha_id)
    print()
    mostrar_detalhes(pedido, com_parecer=True)
    gasto = criativos.despesa(ligacao, campanha)
    print(f"\nBudget atual da campanha: {valor(campanha.budget_centimos)}. Despesa: {dinheiro.formatar(gasto)}.")
    if pedido.estado not in budget.POR_DECIDIR:
        print("\nEste pedido já não pode ser decidido.")
        comum.pausa()
        return
    if pedido.parecer_viavel is None:
        print("\nEste pedido ainda não tem o parecer do marketeer. Só pode ser decidido depois do parecer.")
        comum.pausa()
        return
    escolha = comum.escolher_opcao(
        "Decisão",
        [
            ("1", f"Aprovar e passar o budget para {valor(pedido.budget_pedido_centimos)}"),
            ("2", "Rejeitar"),
            ("0", "Decidir mais tarde"),
        ],
    )
    if escolha == "1":
        aprovar(ligacao, pedido)
    elif escolha == "2":
        rejeitar(ligacao, pedido)
    else:
        print("\nO pedido fica em análise.")
    comum.pausa()


def do_administrador(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Pedidos de budget" do menu do Administrador.

    Mostra os pedidos de alteração de budget de todas as campanhas, com os
    que estão por decidir em primeiro lugar. A lista volta a aparecer depois
    de cada decisão.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a usar o menu.
    """
    while True:
        comum.titulo("Pedidos de alteração de budget de todos os clientes")
        lista = budget.listar_todos(ligacao)
        if lista:
            mostrar_pedidos_com_parecer(lista)
        else:
            print("Ainda não há pedidos de alteração de budget.")
        escolha = comum.escolher_opcao("Pedidos de budget", [("1", "Analisar pedido"), ("0", "Voltar")])
        if escolha == "0":
            return
        decidir(ligacao)
