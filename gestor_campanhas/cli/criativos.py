"""Criativos, no menu do Marketeer.

O marketeer escolhe uma das suas campanhas e vê os criativos dela, com o
custo, o prazo, o público-alvo e a plataforma de cada um. A partir daí pode
criar, editar e eliminar criativos.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import dinheiro, modelos
from gestor_campanhas.cli import campanhas as menu_campanhas
from gestor_campanhas.cli import comum
from gestor_campanhas.cli.pedidos import resumir
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, Criativo, Utilizador
from gestor_campanhas.servicos import campanhas, criativos


#: O que se escreve para apagar um valor quando se edita um criativo.
APAGAR = "-"

#: Número máximo de caracteres do público-alvo que cabem na lista.
LARGURA_PUBLICO = 25


def custo(criativo: Criativo) -> str:
    """Escreve o custo de um criativo como é mostrado nas listas.

    :param criativo: Criativo a descrever.
    :return: O valor em euros, ou ``"Por definir"`` se ainda não foi indicado.
    """
    if criativo.custo_centimos is None:
        return "Por definir"
    return dinheiro.formatar(criativo.custo_centimos)


def mostrar_criativos(lista: list[Criativo]) -> None:
    """Mostra uma tabela de criativos, com o total no fim.

    :param lista: Criativos a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Nome", "Custo", "Prazo", "Público-alvo", "Plataforma", "Estado"],
        [
            [
                str(criativo.id),
                criativo.nome,
                custo(criativo),
                menu_campanhas.data(criativo.prazo),
                resumir(criativo.publico_alvo, LARGURA_PUBLICO) or "-",
                criativo.plataforma or "-",
                criativo.nome_estado,
            ]
            for criativo in lista
        ],
    )
    print(f"\n{len(lista)} {'criativo' if len(lista) == 1 else 'criativos'}.")


def mostrar_detalhes(criativo: Criativo) -> None:
    """Mostra todos os dados de um criativo, um por linha.

    :param criativo: Criativo a mostrar.
    """
    print(f"Criativo n.º {criativo.id}")
    print(f"  Nome:        {criativo.nome}")
    print(f"  Campanha:    {criativo.campanha_nome}")
    print(f"  Descrição:   {criativo.descricao or '-'}")
    print(f"  Custo:       {custo(criativo)}")
    print(f"  Prazo:       {menu_campanhas.data(criativo.prazo)}")
    print(f"  Público:     {criativo.publico_alvo or '-'}")
    print(f"  Plataforma:  {criativo.plataforma or '-'}")
    print(f"  Estado:      {criativo.nome_estado}")


def pedir_criativo(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> Criativo | None:
    """Pede o número de um criativo da campanha e devolve-o.

    Se o número não for de um criativo desta campanha, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a usar o menu.
    :param campanha: Campanha que está a ser vista.
    :return: O criativo, ou ``None`` se o pedido foi cancelado ou o número não serve.
    """
    numero = comum.ler_numero("Número do criativo (Enter para cancelar)")
    if numero is None:
        return None
    try:
        criativo = criativos.obter_do_marketeer(ligacao, marketeer, numero)
        if criativo.campanha_id != campanha.id:
            raise ErroValidacao(f"Esta campanha não tem nenhum criativo com o número {numero}.")
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None
    return criativo


def ler_plataforma(atual: str | None = None) -> str:
    """Mostra as plataformas numeradas e pede o número de uma delas.

    Repete a pergunta enquanto a resposta não for o número de uma plataforma.

    :param atual: Plataforma que o criativo já tem, quando se está a editar.
        Com ``None`` (ao criar), Enter deixa o criativo sem plataforma; ao
        editar, Enter mantém a atual e :data:`APAGAR` apaga-a.
    :return: Nome da plataforma escolhida, ou ``""`` se ficar sem plataforma.
    """
    print("Plataformas:")
    for numero, nome in enumerate(modelos.PLATAFORMAS, start=1):
        print(f"  {numero}. {nome}")
    if atual is None:
        pergunta = "Número da plataforma (Enter para escolher mais tarde)"
    else:
        pergunta = f"Número da plataforma [{atual or 'nenhuma'}]"
    while True:
        resposta = input(f"{pergunta}: ").strip()
        if not resposta:
            return atual or ""
        if resposta == APAGAR and atual is not None:
            return ""
        if resposta.isdigit() and 1 <= int(resposta) <= len(modelos.PLATAFORMAS):
            return modelos.PLATAFORMAS[int(resposta) - 1]
        print(f"Escreva um número entre 1 e {len(modelos.PLATAFORMAS)}.")


def criar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede os dados de um criativo novo e cria-o na campanha.

    Só o nome é obrigatório: o custo, o prazo, o público-alvo e a plataforma
    podem ser indicados mais tarde, em "Editar criativo".

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a criar o criativo.
    :param campanha: Campanha onde o criativo fica.
    """
    comum.titulo("Criar criativo")
    nome = comum.ler_texto("Nome do criativo")
    descricao = comum.ler_texto("Descrição (opcional)", obrigatorio=False)
    valor = comum.ler_texto("Custo estimado em euros (por exemplo 400 ou 399,90, opcional)", obrigatorio=False)
    prazo = comum.ler_texto("Prazo (AAAA-MM-DD, opcional)", obrigatorio=False)
    publico = comum.ler_texto("Público-alvo (opcional)", obrigatorio=False)
    plataforma = ler_plataforma()
    try:
        criativo = criativos.criar(ligacao, marketeer, campanha.id, nome, descricao, valor, prazo, publico, plataforma)
    except ErroValidacao as erro:
        print(f"\n{erro} O criativo não foi criado.")
    else:
        print(f"\nCriativo criado com o número {criativo.id}.")
    comum.pausa()


def _ler_com_valor(pergunta: str, atual: str, vazio: str) -> str:
    """Pede um valor, mostrando o atual (ou ``vazio`` se não houver).

    Enter mantém o valor atual e :data:`APAGAR` apaga-o.
    """
    resposta = comum.ler_texto_com_valor(pergunta, atual or vazio)
    return "" if resposta in (APAGAR, vazio) else resposta


def _texto_do_prazo(prazo: date | None) -> str:
    """Escreve o prazo como é pedido ao editar, ou ``""`` se não houver."""
    return prazo.isoformat() if prazo else ""


def editar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e deixa alterar todos os dados dele.

    Para cada dado é mostrado o valor atual; com Enter, o valor mantém-se, e
    com :data:`APAGAR` o valor é apagado.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a editar.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Editar criativo")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is None:
        return
    print(f"\nA editar o criativo {criativo.nome}.")
    print("Carregue em Enter para manter o valor que está entre parênteses retos.")
    print(f"Para apagar um valor, escreva {APAGAR}\n")
    nome = comum.ler_texto_com_valor("Nome", criativo.nome)
    descricao = _ler_com_valor("Descrição", criativo.descricao, "sem descrição")
    valor = _ler_com_valor("Custo estimado em euros", custo(criativo), "Por definir")
    prazo = _ler_com_valor("Prazo (AAAA-MM-DD)", _texto_do_prazo(criativo.prazo), "sem prazo")
    publico = _ler_com_valor("Público-alvo", criativo.publico_alvo, "sem público-alvo")
    plataforma = ler_plataforma(criativo.plataforma)
    try:
        criativos.editar(ligacao, marketeer, criativo.id, nome, descricao, valor, prazo, publico, plataforma)
    except ErroValidacao as erro:
        print(f"\n{erro} O criativo não foi alterado.")
    else:
        print("\nCriativo guardado.")
    comum.pausa()


def eliminar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e elimina-o, depois de pedir confirmação.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a eliminar.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Eliminar criativo")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is None:
        return
    print()
    mostrar_detalhes(criativo)
    print("\nUm criativo eliminado não pode ser recuperado.")
    if comum.confirmar("Eliminar este criativo?"):
        criativos.eliminar(ligacao, marketeer, criativo.id)
        print(f"\nO criativo {criativo.nome} foi eliminado.")
    else:
        print("\nNada foi alterado.")
    comum.pausa()


#: Opções do menu de criativos de uma campanha. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados, o
#: marketeer e a campanha.
ACOES = [
    ("Criar criativo", criar),
    ("Editar criativo", editar),
    ("Eliminar criativo", eliminar),
]


def da_campanha(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Mostra os criativos de uma campanha e as opções para os gerir.

    A lista volta a aparecer depois de cada opção, já com as alterações.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a usar o menu.
    :param campanha: Campanha escolhida.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo(f"Criativos da campanha {campanha.nome} ({campanha.cliente_nome})")
        lista = criativos.listar_da_campanha(ligacao, campanha)
        if lista:
            mostrar_criativos(lista)
        else:
            print("Esta campanha ainda não tem criativos.")
        escolha = comum.escolher_opcao("Criativos", menu)
        if escolha == "0":
            return
        _, funcao = ACOES[int(escolha) - 1]
        funcao(ligacao, marketeer, campanha)


def do_marketeer(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Criativos" do menu do Marketeer.

    Mostra as campanhas do marketeer e pede o número de uma delas. Depois
    mostra os criativos dessa campanha (ver :func:`da_campanha`).

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Marketeer que está a usar o menu.
    """
    while True:
        comum.titulo("Criativos — escolher a campanha")
        lista = campanhas.listar_do_marketeer(ligacao, utilizador)
        if not lista:
            print('Ainda não tem campanhas. Crie uma na opção "Campanhas".')
            comum.pausa()
            return
        menu_campanhas.mostrar_campanhas(lista)
        print()
        numero = comum.ler_numero("Número da campanha (Enter para voltar)")
        if numero is None:
            return
        try:
            campanha = campanhas.obter_do_marketeer(ligacao, utilizador, numero)
        except ErroValidacao as erro:
            print(f"\n{erro}")
            comum.pausa()
            continue
        da_campanha(ligacao, utilizador, campanha)
