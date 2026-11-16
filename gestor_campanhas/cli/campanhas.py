"""Campanhas, no menu do Marketeer."""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, Utilizador
from gestor_campanhas.servicos import campanhas

#: O que se escreve para apagar uma data quando se edita uma campanha.
APAGAR = "-"


def data(valor: date | None) -> str:
    """Escreve uma data como é mostrada nas listas.

    :param valor: Data, ou ``None``.
    :return: A data no formato ``AAAA-MM-DD``, ou ``"-"`` se não houver data.
    """
    return valor.isoformat() if valor else "-"


def mostrar_campanhas(lista: list[Campanha]) -> None:
    """Mostra uma tabela de campanhas, com o total no fim.

    :param lista: Campanhas a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Nome", "Cliente", "Início", "Fim"],
        [
            [str(campanha.id), campanha.nome, campanha.cliente_nome, data(campanha.data_inicio), data(campanha.data_fim)]
            for campanha in lista
        ],
    )
    print(f"\n{len(lista)} {'campanha' if len(lista) == 1 else 'campanhas'}.")


def pedir_campanha(ligacao: sqlite3.Connection, marketeer: Utilizador) -> Campanha | None:
    """Pede o número de uma campanha do marketeer e devolve-a.

    Se o número não for de uma campanha dele, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a usar o menu.
    :return: A campanha, ou ``None`` se o pedido foi cancelado ou o número não serve.
    """
    numero = comum.ler_numero("Número da campanha (Enter para cancelar)")
    if numero is None:
        return None
    try:
        return campanhas.obter_do_marketeer(ligacao, marketeer, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None


def criar(ligacao: sqlite3.Connection, marketeer: Utilizador) -> None:
    """Pede os dados de uma campanha nova e cria-a.

    Mostra primeiro os clientes ativos, para se escolher o cliente pelo número.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a criar a campanha.
    """
    comum.titulo("Criar campanha")
    clientes = campanhas.clientes_disponiveis(ligacao)
    if not clientes:
        print("Ainda não há clientes com a conta ativa. Peça ao administrador para adicionar o cliente.")
        comum.pausa()
        return
    comum.mostrar_tabela(
        ["N.º", "Cliente", "Empresa"], [[str(cliente.id), cliente.nome, cliente.empresa] for cliente in clientes]
    )
    print()
    cliente_id = comum.ler_numero("Número do cliente (Enter para cancelar)")
    if cliente_id is None:
        return
    nome = comum.ler_texto("Nome da campanha")
    objetivo = comum.ler_texto("Objetivo (opcional)", obrigatorio=False)
    inicio = comum.ler_texto("Data de início (AAAA-MM-DD, opcional)", obrigatorio=False)
    fim = comum.ler_texto("Data de fim (AAAA-MM-DD, opcional)", obrigatorio=False)
    try:
        campanha = campanhas.criar(ligacao, marketeer, nome, objetivo, cliente_id, inicio, fim)
    except ErroValidacao as erro:
        print(f"\n{erro} A campanha não foi criada.")
    else:
        print(f"\nCampanha criada com o número {campanha.id}, para {campanha.cliente_nome}.")
    comum.pausa()


def _ler_data_com_valor(pergunta: str, atual: date | None) -> str:
    """Pede uma data, mostrando a atual. Enter mantém-na e :data:`APAGAR` apaga-a."""
    sem_data = "sem data"
    resposta = comum.ler_texto_com_valor(pergunta, data(atual) if atual else sem_data)
    return "" if resposta in (APAGAR, sem_data) else resposta


def editar(ligacao: sqlite3.Connection, marketeer: Utilizador) -> None:
    """Pede o número de uma campanha e deixa alterar o nome, o objetivo e as datas.

    Para cada dado é mostrado o valor atual; com Enter, o valor mantém-se.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a editar.
    """
    comum.titulo("Editar campanha")
    campanha = pedir_campanha(ligacao, marketeer)
    if campanha is None:
        return
    print(f"\nA editar a campanha {campanha.nome}, de {campanha.cliente_nome}.")
    print("Carregue em Enter para manter o valor que está entre parênteses retos.")
    print(f"Para apagar uma data, escreva {APAGAR}\n")
    nome = comum.ler_texto_com_valor("Nome", campanha.nome)
    objetivo = comum.ler_texto_com_valor("Objetivo", campanha.objetivo)
    inicio = _ler_data_com_valor("Data de início (AAAA-MM-DD)", campanha.data_inicio)
    fim = _ler_data_com_valor("Data de fim (AAAA-MM-DD)", campanha.data_fim)
    try:
        campanhas.editar(ligacao, marketeer, campanha.id, nome, objetivo, inicio, fim)
    except ErroValidacao as erro:
        print(f"\n{erro} A campanha não foi alterada.")
    else:
        print("\nCampanha guardada.")
    comum.pausa()


#: Opções do menu de campanhas do Marketeer. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados e o
#: marketeer.
ACOES = [
    ("Criar campanha", criar),
    ("Editar campanha", editar),
]


def do_marketeer(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Campanhas" do menu do Marketeer.

    Mostra as campanhas do marketeer e as opções para as gerir. A lista volta
    a aparecer depois de cada opção, já com as alterações.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Marketeer que está a usar o menu.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo("As minhas campanhas")
        lista = campanhas.listar_do_marketeer(ligacao, utilizador)
        if lista:
            mostrar_campanhas(lista)
        else:
            print("Ainda não tem campanhas.")
        escolha = comum.escolher_opcao("Campanhas", menu)
        if escolha == "0":
            return
        _, funcao = ACOES[int(escolha) - 1]
        funcao(ligacao, utilizador)
