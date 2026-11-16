"""Pedidos de nova campanha, no menu do Cliente."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import dinheiro, modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import PedidoCampanha, Utilizador
from gestor_campanhas.servicos import pedidos

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


#: Opções do menu de pedidos do Cliente. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados e o
#: cliente.
ACOES = [
    ("Novo pedido", novo),
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
