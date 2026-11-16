"""Pedidos de nova campanha, nos menus do Cliente e do Administrador.

O Cliente faz pedidos, acompanha o estado deles e pode cancelar os que ainda
estão pendentes. O Administrador vê os pedidos de todos os clientes e decide
cada um.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import dinheiro, modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import PedidoCampanha, Utilizador
from gestor_campanhas.servicos import campanhas, pedidos

#: Número máximo de caracteres do objetivo que cabem na lista de pedidos.
LARGURA_OBJETIVO = 40


def resumir(texto: str, largura: int = LARGURA_OBJETIVO) -> str:
    """Encurta um texto para caber numa coluna de uma tabela.

    :param texto: Texto original.
    :param largura: Número máximo de caracteres.
    :return: O texto, cortado e terminado em ``...`` se for mais comprido do
        que a largura.
    """
    if len(texto) <= largura:
        return texto
    return texto[: largura - 3].rstrip() + "..."


def mostrar_pedidos(lista: list[PedidoCampanha]) -> None:
    """Mostra uma tabela de pedidos, com o total no fim.

    :param lista: Pedidos a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Feito em", "Objetivo", "Orçamento", "Prazo", "Estado"],
        [
            [
                str(pedido.id),
                pedido.criado_em.strftime("%Y-%m-%d"),
                resumir(pedido.objetivo),
                dinheiro.formatar(pedido.orcamento_centimos),
                pedido.prazo.isoformat(),
                pedido.nome_estado,
            ]
            for pedido in lista
        ],
    )
    print(f"\n{len(lista)} {'pedido' if len(lista) == 1 else 'pedidos'}.")


def ler_plataformas() -> list[str]:
    """Mostra as plataformas numeradas e pede os números das escolhidas.

    Repete a pergunta enquanto a resposta não for uma lista de números das
    plataformas mostradas, separados por vírgulas.

    :return: Nomes das plataformas escolhidas.
    """
    print("Plataformas:")
    for numero, nome in enumerate(modelos.PLATAFORMAS, start=1):
        print(f"  {numero}. {nome}")
    while True:
        resposta = input("Números das plataformas, separados por vírgulas (por exemplo 1,2): ")
        partes = [parte.strip() for parte in resposta.split(",") if parte.strip()]
        if partes and all(parte.isdigit() and 1 <= int(parte) <= len(modelos.PLATAFORMAS) for parte in partes):
            return [modelos.PLATAFORMAS[int(parte) - 1] for parte in partes]
        print(f"Escreva números entre 1 e {len(modelos.PLATAFORMAS)}, separados por vírgulas.")


def novo(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede os dados de um pedido de campanha e regista-o.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    """
    comum.titulo("Novo pedido de campanha")
    objetivo = comum.ler_texto("Objetivo da campanha")
    orcamento = comum.ler_texto("Orçamento em euros (por exemplo 1500 ou 1500,50)")
    prazo = comum.ler_texto("Prazo pretendido (AAAA-MM-DD)")
    plataformas = ler_plataformas()
    try:
        pedido = pedidos.criar(ligacao, cliente, objetivo, orcamento, prazo, plataformas)
    except ErroValidacao as erro:
        print(f"\n{erro} O pedido não foi registado.")
    else:
        print(f"\nPedido registado com o número {pedido.id}. Fica pendente até ser analisado.")
    comum.pausa()


def mostrar_detalhes(pedido: PedidoCampanha, com_cliente: bool = False) -> None:
    """Mostra todos os dados de um pedido, um por linha.

    O motivo só aparece nos pedidos rejeitados e o número da campanha só
    aparece nos aprovados.

    :param pedido: Pedido a mostrar.
    :param com_cliente: ``True`` para mostrar também o nome do cliente, como
        no menu do Administrador.
    """
    print(f"Pedido n.º {pedido.id}")
    if com_cliente:
        print(f"  Cliente:      {pedido.cliente_nome}")
    print(f"  Feito em:     {pedido.criado_em.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Objetivo:     {pedido.objetivo}")
    print(f"  Orçamento:    {dinheiro.formatar(pedido.orcamento_centimos)}")
    print(f"  Prazo:        {pedido.prazo.isoformat()}")
    print(f"  Plataformas:  {', '.join(pedido.plataformas)}")
    print(f"  Estado:       {pedido.nome_estado}")
    if pedido.estado == modelos.REJEITADO:
        print(f"  Motivo:       {pedido.motivo_rejeicao}")
    if pedido.campanha_id is not None:
        print(f"  Campanha:     n.º {pedido.campanha_id}")


def pedir_pedido(ligacao: sqlite3.Connection, cliente: Utilizador) -> PedidoCampanha | None:
    """Pede o número de um pedido do cliente e devolve-o.

    Se o número não for de um pedido dele, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a usar o menu.
    :return: O pedido, ou ``None`` se foi cancelado com Enter ou o número não serve.
    """
    numero = comum.ler_numero("Número do pedido (Enter para cancelar)")
    if numero is None:
        return None
    try:
        return pedidos.obter_do_cliente(ligacao, cliente, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None


def ver(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um pedido e mostra todos os dados dele.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    """
    comum.titulo("Ver pedido")
    pedido = pedir_pedido(ligacao, cliente)
    if pedido is None:
        return
    print()
    mostrar_detalhes(pedido)
    comum.pausa()


def cancelar(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um pedido e cancela-o, depois de pedir confirmação.

    Só um pedido pendente pode ser cancelado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a cancelar.
    """
    comum.titulo("Cancelar pedido")
    pedido = pedir_pedido(ligacao, cliente)
    if pedido is None:
        return
    print()
    mostrar_detalhes(pedido)
    print()
    if pedido.estado != modelos.PENDENTE:
        print(f"Só é possível cancelar um pedido pendente. Este pedido está no estado {pedido.nome_estado}.")
    elif comum.confirmar("Cancelar este pedido?"):
        pedidos.cancelar(ligacao, cliente, pedido.id)
        print("\nPedido cancelado.")
    else:
        print("\nNada foi alterado.")
    comum.pausa()


#: Opções do menu de pedidos do Cliente. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados e o
#: cliente.
ACOES = [
    ("Novo pedido", novo),
    ("Ver pedido", ver),
    ("Cancelar pedido", cancelar),
]


def do_cliente(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Pedidos de campanha" do menu do Cliente.

    Mostra os pedidos do cliente e as opções para os gerir. A lista volta a
    aparecer depois de cada opção, já com as alterações.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Cliente que está a usar o menu.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo("Os meus pedidos de campanha")
        lista = pedidos.listar_do_cliente(ligacao, utilizador)
        if lista:
            mostrar_pedidos(lista)
        else:
            print("Ainda não fez nenhum pedido.")
        escolha = comum.escolher_opcao("Pedidos de campanha", menu)
        if escolha == "0":
            return
        _, funcao = ACOES[int(escolha) - 1]
        funcao(ligacao, utilizador)


def mostrar_todos(lista: list[PedidoCampanha]) -> None:
    """Mostra uma tabela com os pedidos de todos os clientes, com o total no fim.

    :param lista: Pedidos a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Feito em", "Cliente", "Objetivo", "Orçamento", "Prazo", "Estado"],
        [
            [
                str(pedido.id),
                pedido.criado_em.strftime("%Y-%m-%d"),
                pedido.cliente_nome,
                resumir(pedido.objetivo),
                dinheiro.formatar(pedido.orcamento_centimos),
                pedido.prazo.isoformat(),
                pedido.nome_estado,
            ]
            for pedido in lista
        ],
    )
    por_decidir = sum(1 for pedido in lista if pedido.estado in pedidos.POR_DECIDIR)
    print(f"\n{len(lista)} {'pedido' if len(lista) == 1 else 'pedidos'}, {por_decidir} por decidir.")


def aprovar(ligacao: sqlite3.Connection, pedido: PedidoCampanha) -> None:
    """Pede os dados da campanha a criar e aprova o pedido.

    O budget inicial proposto é o orçamento do pedido; com Enter, mantém-se.

    :param ligacao: Ligação aberta à base de dados.
    :param pedido: Pedido a aprovar.
    """
    comum.titulo("Aprovar pedido")
    marketeers = campanhas.marketeers_disponiveis(ligacao)
    if not marketeers:
        print("Não há marketeers com a conta ativa. Adicione um marketeer antes de aprovar o pedido.")
        return
    nome = comum.ler_texto("Nome da campanha")
    budget = comum.ler_texto_com_valor("Budget inicial em euros", dinheiro.formatar(pedido.orcamento_centimos))
    print()
    comum.mostrar_tabela(
        ["N.º", "Marketeer", "Email"],
        [[str(marketeer.id), marketeer.nome, marketeer.email] for marketeer in marketeers],
    )
    print()
    marketeer_id = comum.ler_numero("Número do marketeer responsável (Enter para cancelar)")
    if marketeer_id is None:
        print("\nO pedido não foi aprovado.")
        return
    try:
        aprovado = pedidos.aprovar(ligacao, pedido.id, nome, budget, marketeer_id)
    except ErroValidacao as erro:
        print(f"\n{erro} O pedido não foi aprovado.")
    else:
        print(f"\nPedido aprovado. Foi criada a campanha n.º {aprovado.campanha_id}.")
        print("O cliente e o marketeer foram avisados por email.")


def rejeitar(ligacao: sqlite3.Connection, pedido: PedidoCampanha) -> None:
    """Pede o motivo e rejeita o pedido, depois de pedir confirmação.

    :param ligacao: Ligação aberta à base de dados.
    :param pedido: Pedido a rejeitar.
    """
    comum.titulo("Rejeitar pedido")
    motivo = comum.ler_texto("Motivo da rejeição")
    if not comum.confirmar("Rejeitar este pedido?"):
        print("\nO pedido não foi rejeitado.")
        return
    pedidos.rejeitar(ligacao, pedido.id, motivo)
    print("\nPedido rejeitado. O cliente foi avisado por email.")


def decidir(ligacao: sqlite3.Connection) -> None:
    """Pede o número de um pedido, mostra-o e deixa aprová-lo ou rejeitá-lo.

    Ao ser aberto, um pedido pendente passa a estar em análise.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Analisar pedido")
    numero = comum.ler_numero("Número do pedido (Enter para cancelar)")
    if numero is None:
        return
    try:
        pedido = pedidos.analisar(ligacao, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    print()
    mostrar_detalhes(pedido, com_cliente=True)
    if pedido.estado not in pedidos.POR_DECIDIR:
        print("\nEste pedido já não pode ser decidido.")
        comum.pausa()
        return
    escolha = comum.escolher_opcao(
        "Decisão", [("1", "Aprovar e criar a campanha"), ("2", "Rejeitar"), ("0", "Decidir mais tarde")]
    )
    if escolha == "1":
        aprovar(ligacao, pedido)
    elif escolha == "2":
        rejeitar(ligacao, pedido)
    else:
        print("\nO pedido fica em análise.")
    comum.pausa()


def do_administrador(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Pedidos de campanha" do menu do Administrador.

    Mostra os pedidos de todos os clientes, com os que estão por decidir em
    primeiro lugar. A lista volta a aparecer depois de cada decisão.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a usar o menu.
    """
    while True:
        comum.titulo("Pedidos de campanha de todos os clientes")
        lista = pedidos.listar_todos(ligacao)
        if lista:
            mostrar_todos(lista)
        else:
            print("Ainda não há pedidos de campanha.")
        escolha = comum.escolher_opcao("Pedidos de campanha", [("1", "Analisar pedido"), ("0", "Voltar")])
        if escolha == "0":
            return
        decidir(ligacao)
