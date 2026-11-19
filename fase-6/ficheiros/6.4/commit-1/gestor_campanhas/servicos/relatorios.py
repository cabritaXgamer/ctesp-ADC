"""Relatório das campanhas de um cliente, em CSV.

O relatório tem uma linha por criativo, com os dados da campanha a que
pertence: o estado, as datas, o marketeer, o budget, a despesa e o
restante. Uma campanha sem criativos tem uma linha só com os dados da
campanha.

O ficheiro usa ``;`` para separar as colunas e a vírgula nas casas
decimais, e é gravado em UTF-8 com a marca inicial (BOM). É o formato que o
Excel em português abre diretamente, com os acentos certos e os valores
reconhecidos como números. Os valores em euros vão sem o símbolo ``€`` e sem
o espaço dos milhares, pela mesma razão.
"""

from __future__ import annotations

import csv
import sqlite3
from datetime import date
from pathlib import Path

from gestor_campanhas import relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.servicos import campanhas, criativos, ficheiros

#: Títulos das colunas do relatório, pela ordem em que aparecem.
CABECALHOS = [
    "Campanha",
    "Estado da campanha",
    "Início",
    "Fim",
    "Marketeer",
    "Budget (€)",
    "Despesa (€)",
    "Restante (€)",
    "Criativo",
    "Estado do criativo",
    "Plataforma",
    "Prazo",
    "Custo (€)",
]

#: Carácter que separa as colunas.
SEPARADOR = ";"


def valor(centimos: int | None) -> str:
    """Escreve um valor em euros como fica no relatório.

    :param centimos: Valor em cêntimos, ou ``None``.
    :return: Por exemplo ``"1500,00"`` ou ``"-200,50"``; ``""`` se não houver valor.
    """
    if centimos is None:
        return ""
    sinal = "-" if centimos < 0 else ""
    euros, resto = divmod(abs(centimos), 100)
    return f"{sinal}{euros},{resto:02d}"


def _data(dia: date | None) -> str:
    """Escreve uma data no formato ``AAAA-MM-DD``, ou ``""`` se não houver."""
    return dia.isoformat() if dia else ""


def linhas(ligacao: sqlite3.Connection, cliente: Utilizador) -> list[list[str]]:
    """Monta as linhas do relatório das campanhas de um cliente, sem os títulos.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente a quem o relatório se refere.
    :return: Uma lista de colunas (já escritas como texto) por linha, pela
        ordem de :data:`CABECALHOS`. As campanhas vêm pela ordem em que foram
        criadas e os criativos de cada uma também.
    """
    despesas = criativos.despesas(ligacao)
    resultado = []
    for campanha in campanhas.listar_do_cliente(ligacao, cliente):
        gasto = despesas.get(campanha.id, 0)
        dados_campanha = [
            campanha.nome,
            campanhas.estado(campanha),
            _data(campanha.data_inicio),
            _data(campanha.data_fim),
            campanha.marketeer_nome,
            valor(campanha.budget_centimos),
            valor(gasto),
            valor(criativos.restante(campanha, gasto)),
        ]
        lista = criativos_bd.listar_por_campanha(ligacao, campanha.id)
        if not lista:
            resultado.append(dados_campanha + ["", "", "", "", ""])
        for criativo in lista:
            resultado.append(
                dados_campanha
                + [
                    criativo.nome,
                    criativo.nome_estado,
                    criativo.plataforma,
                    _data(criativo.prazo),
                    valor(criativo.custo_centimos),
                ]
            )
    return resultado


def nome_do_ficheiro(hoje: date | None = None) -> str:
    """Devolve o nome do ficheiro do relatório, com a data do dia.

    :param hoje: Dia do relatório. Se for ``None``, usa-se o dia atual.
    :return: Por exemplo ``"relatorio-campanhas-2026-11-19.csv"``.
    """
    return f"relatorio-campanhas-{(hoje or relogio.hoje()).isoformat()}.csv"


def exportar(ligacao: sqlite3.Connection, cliente: Utilizador, destino: str) -> Path:
    """Grava o relatório das campanhas do cliente numa pasta.

    Nenhum ficheiro que já esteja na pasta é apagado: se já houver um
    relatório com o mesmo nome, o novo fica com um número entre parênteses
    (ver :func:`gestor_campanhas.servicos.ficheiros.caminho_livre`).

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente a quem o relatório se refere.
    :param destino: Pasta onde o ficheiro fica, tal como foi escrita.
    :return: Caminho do ficheiro gravado.
    :raises ErroValidacao: Se o cliente não tiver campanhas ou se a pasta
        não existir.
    """
    conteudo = linhas(ligacao, cliente)
    if not conteudo:
        raise ErroValidacao("Ainda não tem campanhas, por isso não há nada para exportar.")
    caminho = ficheiros.caminho_livre(destino, nome_do_ficheiro())
    # newline="" deixa o módulo csv escolher o fim de linha, como manda a documentação dele.
    with caminho.open("w", encoding="utf-8-sig", newline="") as ficheiro:
        escritor = csv.writer(ficheiro, delimiter=SEPARADOR)
        escritor.writerow(CABECALHOS)
        escritor.writerows(conteudo)
    return caminho
