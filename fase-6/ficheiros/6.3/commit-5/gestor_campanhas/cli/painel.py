"""Painel de marketeers, no menu do Administrador.

A tabela principal compara os marketeers com a conta ativa: campanhas
ativas, criativos ativos, em atraso e concluídos, a data da última
atividade e se o marketeer está sem atividade. A partir daí, o Administrador
vê o trabalho de cada marketeer, compara a carga num período e muda o número
de dias ao fim dos quais um marketeer é dado como parado.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import modelos
from gestor_campanhas.cli import campanhas as menu_campanhas
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.servicos import campanhas, gestao
from gestor_campanhas.servicos import painel as servico


def mostrar_carga(lista: list[servico.Carga], dias: int) -> None:
    """Mostra a tabela principal do painel, com a situação de cada marketeer.

    :param lista: Indicadores de cada marketeer, calculados sem período.
    :param dias: Número de dias sem atividade em vigor.
    """
    comum.mostrar_tabela(
        ["N.º", "Marketeer", "Campanhas ativas", "Ativos", "Em atraso", "Concluídos", "Última atividade", "Situação"],
        [
            [
                str(indicadores.marketeer.id),
                indicadores.marketeer.nome,
                str(indicadores.campanhas_ativas),
                str(indicadores.ativos),
                str(indicadores.em_atraso),
                str(indicadores.concluidos),
                indicadores.ultima_atividade.strftime("%Y-%m-%d") if indicadores.ultima_atividade else "-",
                servico.situacao(indicadores, dias),
            ]
            for indicadores in lista
        ],
    )


def em_dias(dias: int) -> str:
    """Escreve um número de dias, no singular ou no plural.

    :param dias: Número de dias.
    :return: Por exemplo ``"1 dia"`` ou ``"7 dias"``.
    """
    return f"{dias} {'dia' if dias == 1 else 'dias'}"


def explicar(dias: int) -> None:
    """Explica o que conta em cada coluna da tabela principal.

    :param dias: Número de dias sem atividade em vigor.
    """
    print("\nAtivos: criativos em preparação, em revisão ou rejeitados. Concluídos: aprovados ou publicados.")
    print("Em atraso: criativos ativos com o prazo já passado.")
    print(f"Sem atividade: sem criativos ativos, ou sem mexer nos criativos há {em_dias(dias)} ou mais.")


def ver_trabalho(ligacao: sqlite3.Connection) -> None:
    """Pede o número de um marketeer e mostra as campanhas dele, com os criativos, e as últimas atividades.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Ver o trabalho de um marketeer")
    numero = comum.ler_numero("Número do marketeer (Enter para cancelar)")
    if numero is None:
        return
    try:
        marketeer = gestao.obter(ligacao, modelos.MARKETEER, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    comum.titulo(f"Trabalho de {marketeer.nome}")
    lista = servico.trabalho(ligacao, marketeer)
    if not lista:
        print("Não é responsável por nenhuma campanha.")
    for campanha, criativos in lista:
        print(f"\nCampanha n.º {campanha.id}: {campanha.nome} ({campanha.cliente_nome}), {campanhas.estado(campanha)}")
        if not criativos:
            print("  Ainda não tem criativos.")
            continue
        comum.mostrar_tabela(
            ["N.º", "Criativo", "Estado", "Prazo", "Situação"],
            [
                [
                    str(criativo.id),
                    criativo.nome,
                    criativo.nome_estado,
                    menu_campanhas.data(criativo.prazo),
                    "Em atraso" if servico.em_atraso(criativo) else "",
                ]
                for criativo in criativos
            ],
        )
    recentes = servico.ultimas_atividades(ligacao, marketeer)
    if recentes:
        print("\nÚltimas atividades")
        for atividade in recentes:
            print(f"  {atividade.registada_em.strftime('%Y-%m-%d %H:%M')}  {atividade.descricao}")
    else:
        print("\nÚltimas atividades: nenhuma registada.")
    comum.pausa()


def descrever_periodo(desde: date | None, ate: date | None) -> str:
    """Escreve um período por palavras, para o título da comparação.

    :param desde: Primeiro dia, ou ``None``.
    :param ate: Último dia, ou ``None``.
    :return: Por exemplo ``"de 2026-11-01 a 2026-11-30"``.
    """
    if desde and ate:
        return f"de {desde.isoformat()} a {ate.isoformat()}"
    if desde:
        return f"a partir de {desde.isoformat()}"
    if ate:
        return f"até {ate.isoformat()}"
    return "sem limite de datas"


def comparar(ligacao: sqlite3.Connection) -> None:
    """Pede um período e compara a carga dos marketeers nesse período.

    Só contam os criativos com o prazo dentro do período.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Comparar num período")
    print("Contam os criativos com o prazo dentro do período.")
    desde = comum.ler_data("Desde")
    ate = comum.ler_data("Até")
    try:
        lista = servico.carga(ligacao, desde, ate)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    comum.titulo(f"Carga de trabalho {descrever_periodo(desde, ate)}")
    if not lista:
        print("Não há marketeers com a conta ativa.")
    else:
        comum.mostrar_tabela(
            ["N.º", "Marketeer", "Criativos", "Ativos", "Em atraso", "Concluídos"],
            [
                [
                    str(indicadores.marketeer.id),
                    indicadores.marketeer.nome,
                    str(indicadores.ativos + indicadores.concluidos),
                    str(indicadores.ativos),
                    str(indicadores.em_atraso),
                    str(indicadores.concluidos),
                ]
                for indicadores in lista
            ],
        )
    comum.pausa()


def mudar_dias(ligacao: sqlite3.Connection) -> None:
    """Mostra e deixa mudar o número de dias ao fim dos quais um marketeer fica sem atividade.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Mudar os dias sem atividade")
    dias = servico.dias_sem_atividade(ligacao)
    print(f"Um marketeer fica sem atividade ao fim de {em_dias(dias)} sem mexer nos criativos.")
    novo = comum.ler_numero("Número de dias novo (Enter para manter)")
    if novo is None:
        return
    try:
        servico.definir_dias_sem_atividade(ligacao, novo)
    except ErroValidacao as erro:
        print(f"\n{erro} Nada foi alterado.")
    else:
        print(f"\nGuardado. Um marketeer fica sem atividade ao fim de {em_dias(novo)}.")
    comum.pausa()


#: Opções do painel. Cada opção é um par ``(descrição, função)``; a função
#: recebe a ligação à base de dados.
ACOES = [
    ("Ver o trabalho de um marketeer", ver_trabalho),
    ("Comparar num período", comparar),
    ("Mudar os dias sem atividade", mudar_dias),
]


def painel(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Painel de marketeers" do menu do Administrador.

    A tabela volta a aparecer depois de cada opção, já com as alterações.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a consultar.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo("Painel de marketeers")
        dias = servico.dias_sem_atividade(ligacao)
        lista = servico.carga(ligacao)
        if not lista:
            print("Não há marketeers com a conta ativa.")
        else:
            mostrar_carga(lista, dias)
            explicar(dias)
            parados = [indicadores.marketeer.nome for indicadores in lista if servico.situacao(indicadores, dias)]
            if parados:
                print(f"Marketeers sem atividade: {len(parados)} ({', '.join(parados)}).")
            else:
                print("Nenhum marketeer está sem atividade.")
        escolha = comum.escolher_opcao("Painel", menu)
        if escolha == "0":
            return
        _, funcao = ACOES[int(escolha) - 1]
        funcao(ligacao)
