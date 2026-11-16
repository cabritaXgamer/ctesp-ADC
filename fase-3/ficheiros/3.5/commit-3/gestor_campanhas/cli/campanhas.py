"""Campanhas, nos menus dos três perfis.

O marketeer vê as campanhas que lhe estão atribuídas, com o cliente, as
datas, o budget e o estado, e pode criar, editar, consultar e eliminar
cada uma.

O Administrador vê as campanhas de todos os marketeers, define o budget de
cada uma e escolhe o marketeer responsável.

O Cliente vê as suas campanhas, com o budget de cada uma, e os contactos do
marketeer responsável.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import dinheiro
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


def budget(campanha: Campanha) -> str:
    """Escreve o budget de uma campanha como é mostrado nas listas.

    :param campanha: Campanha a descrever.
    :return: O valor em euros, ou ``"Por definir"`` se ainda não foi atribuído.
    """
    if campanha.budget_centimos is None:
        return "Por definir"
    return dinheiro.formatar(campanha.budget_centimos)


def mostrar_campanhas(lista: list[Campanha]) -> None:
    """Mostra uma tabela de campanhas, com o total no fim.

    :param lista: Campanhas a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Nome", "Cliente", "Início", "Fim", "Budget", "Estado"],
        [
            [
                str(campanha.id),
                campanha.nome,
                campanha.cliente_nome,
                data(campanha.data_inicio),
                data(campanha.data_fim),
                budget(campanha),
                campanhas.estado(campanha),
            ]
            for campanha in lista
        ],
    )
    print(f"\n{len(lista)} {'campanha' if len(lista) == 1 else 'campanhas'}.")


def mostrar_detalhes(campanha: Campanha) -> None:
    """Mostra todos os dados de uma campanha, um por linha.

    :param campanha: Campanha a mostrar.
    """
    print(f"Campanha n.º {campanha.id}")
    print(f"  Nome:      {campanha.nome}")
    print(f"  Cliente:   {campanha.cliente_nome}")
    print(f"  Objetivo:  {campanha.objetivo or '-'}")
    print(f"  Início:    {data(campanha.data_inicio)}")
    print(f"  Fim:       {data(campanha.data_fim)}")
    print(f"  Budget:    {budget(campanha)}")
    print(f"  Estado:    {campanhas.estado(campanha)}")


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


def ver(ligacao: sqlite3.Connection, marketeer: Utilizador) -> None:
    """Pede o número de uma campanha e mostra todos os dados dela.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    """
    comum.titulo("Ver campanha")
    campanha = pedir_campanha(ligacao, marketeer)
    if campanha is None:
        return
    print()
    mostrar_detalhes(campanha)
    comum.pausa()


def eliminar(ligacao: sqlite3.Connection, marketeer: Utilizador) -> None:
    """Pede o número de uma campanha e elimina-a, depois de pedir confirmação.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a eliminar.
    """
    comum.titulo("Eliminar campanha")
    campanha = pedir_campanha(ligacao, marketeer)
    if campanha is None:
        return
    print()
    mostrar_detalhes(campanha)
    print("\nUma campanha eliminada não pode ser recuperada.")
    if comum.confirmar("Eliminar esta campanha?"):
        campanhas.eliminar(ligacao, marketeer, campanha.id)
        print(f"\nA campanha {campanha.nome} foi eliminada.")
    else:
        print("\nNada foi alterado.")
    comum.pausa()


#: Opções do menu de campanhas do Marketeer. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados e o
#: marketeer.
ACOES = [
    ("Criar campanha", criar),
    ("Editar campanha", editar),
    ("Ver campanha", ver),
    ("Eliminar campanha", eliminar),
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


def mostrar_todas(lista: list[Campanha]) -> None:
    """Mostra uma tabela com as campanhas de todos os marketeers, com o total no fim.

    :param lista: Campanhas a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Nome", "Cliente", "Marketeer", "Início", "Fim", "Budget", "Estado"],
        [
            [
                str(campanha.id),
                campanha.nome,
                campanha.cliente_nome,
                campanha.marketeer_nome,
                data(campanha.data_inicio),
                data(campanha.data_fim),
                budget(campanha),
                campanhas.estado(campanha),
            ]
            for campanha in lista
        ],
    )
    print(f"\n{len(lista)} {'campanha' if len(lista) == 1 else 'campanhas'}.")


def pedir_qualquer_campanha(ligacao: sqlite3.Connection) -> Campanha | None:
    """Pede o número de uma campanha, seja de que marketeer for, e devolve-a.

    Se o número não existir, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :return: A campanha, ou ``None`` se o pedido foi cancelado ou o número não existe.
    """
    numero = comum.ler_numero("Número da campanha (Enter para cancelar)")
    if numero is None:
        return None
    try:
        return campanhas.obter(ligacao, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None


def definir_budget(ligacao: sqlite3.Connection) -> None:
    """Pede o número de uma campanha e o budget a atribuir-lhe.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Definir budget")
    campanha = pedir_qualquer_campanha(ligacao)
    if campanha is None:
        return
    print(f"\nCampanha {campanha.nome}, de {campanha.cliente_nome}. Budget atual: {budget(campanha)}.")
    valor = comum.ler_texto("Budget em euros (por exemplo 1500 ou 1500,50)")
    try:
        campanha = campanhas.definir_budget(ligacao, campanha.id, valor)
    except ErroValidacao as erro:
        print(f"\n{erro} O budget não foi alterado.")
    else:
        print(f"\nBudget definido: {budget(campanha)}.")
    comum.pausa()


def atribuir_marketeer(ligacao: sqlite3.Connection) -> None:
    """Pede o número de uma campanha e o do marketeer que passa a ser responsável.

    Mostra os marketeers com a conta ativa, para se escolher pelo número.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Atribuir marketeer")
    campanha = pedir_qualquer_campanha(ligacao)
    if campanha is None:
        return
    print(f"\nCampanha {campanha.nome}, de {campanha.cliente_nome}. Responsável atual: {campanha.marketeer_nome}.\n")
    marketeers = campanhas.marketeers_disponiveis(ligacao)
    comum.mostrar_tabela(
        ["N.º", "Marketeer", "Email"],
        [[str(marketeer.id), marketeer.nome, marketeer.email] for marketeer in marketeers],
    )
    print()
    marketeer_id = comum.ler_numero("Número do marketeer responsável (Enter para cancelar)")
    if marketeer_id is None:
        return
    try:
        campanha = campanhas.atribuir_marketeer(ligacao, campanha.id, marketeer_id)
    except ErroValidacao as erro:
        print(f"\n{erro} O responsável não foi alterado.")
    else:
        print(f"\nA campanha passou para {campanha.marketeer_nome}, que foi avisado por email.")
    comum.pausa()


#: Opções do menu de campanhas do Administrador. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados.
ACOES_DO_ADMINISTRADOR = [
    ("Definir budget", definir_budget),
    ("Atribuir marketeer", atribuir_marketeer),
]


def do_administrador(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Campanhas" do menu do Administrador.

    Mostra as campanhas de todos os marketeers e as opções para definir o
    budget e o responsável de cada uma.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a usar o menu.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES_DO_ADMINISTRADOR, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo("Todas as campanhas")
        lista = campanhas.listar_todas(ligacao)
        if lista:
            mostrar_todas(lista)
        else:
            print("Ainda não há campanhas.")
        escolha = comum.escolher_opcao("Campanhas", menu)
        if escolha == "0":
            return
        _, funcao = ACOES_DO_ADMINISTRADOR[int(escolha) - 1]
        funcao(ligacao)


def mostrar_do_cliente(lista: list[Campanha]) -> None:
    """Mostra uma tabela com as campanhas de um cliente, com o total no fim.

    :param lista: Campanhas a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Nome", "Início", "Fim", "Budget", "Estado", "Marketeer"],
        [
            [
                str(campanha.id),
                campanha.nome,
                data(campanha.data_inicio),
                data(campanha.data_fim),
                budget(campanha),
                campanhas.estado(campanha),
                campanha.marketeer_nome,
            ]
            for campanha in lista
        ],
    )
    print(f"\n{len(lista)} {'campanha' if len(lista) == 1 else 'campanhas'}.")


def do_cliente(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Campanhas" do menu do Cliente.

    Mostra as campanhas do cliente, com o budget de cada uma. O cliente não
    altera nada aqui: o budget é definido pelo Administrador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Cliente que está a usar o menu.
    """
    while True:
        comum.titulo("As minhas campanhas")
        lista = campanhas.listar_do_cliente(ligacao, utilizador)
        if lista:
            mostrar_do_cliente(lista)
            print("O budget de cada campanha é definido pelo administrador.")
        else:
            print('Ainda não tem campanhas. Pode pedir uma na opção "Pedidos de campanha".')
        escolha = comum.escolher_opcao("Campanhas", [("0", "Voltar")])
        if escolha == "0":
            return
