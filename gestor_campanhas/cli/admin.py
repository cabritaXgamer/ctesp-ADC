"""Opções do menu do Administrador."""

from __future__ import annotations

import sqlite3
from datetime import timedelta

from gestor_campanhas import modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.servicos import sessoes

#: Texto mostrado na coluna "Motivo" para cada motivo de saída.
MOTIVOS = {
    modelos.LOGOUT: "Terminou a sessão",
    modelos.INATIVIDADE: "Inatividade",
    None: "",
}

_FORMATO_HORA = "%Y-%m-%d %H:%M"


def formatar_duracao(duracao: timedelta | None) -> str:
    """Escreve uma duração como horas e minutos, por exemplo ``1h05``.

    :param duracao: Duração a escrever, ou ``None`` para uma sessão em curso.
    :return: Texto para mostrar na tabela. Vazio se a duração for ``None``.
    """
    if duracao is None:
        return ""
    minutos = int(duracao.total_seconds() // 60)
    return f"{minutos // 60}h{minutos % 60:02d}"


def horarios(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Mostra as entradas e saídas dos marketeers, com filtro por datas.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a consultar.
    """
    comum.titulo("Horários de entrada e saída dos marketeers")
    desde = comum.ler_data("Desde")
    ate = comum.ler_data("Até")
    try:
        registos = sessoes.horarios_dos_marketeers(ligacao, desde, ate)
    except ErroValidacao as erro:
        print(erro)
        comum.pausa()
        return
    print()
    if not registos:
        print("Não há sessões de marketeers neste período.")
    else:
        linhas = [
            [
                nome,
                sessao.entrada.strftime(_FORMATO_HORA),
                sessao.saida.strftime(_FORMATO_HORA) if sessao.saida else "(em curso)",
                formatar_duracao(sessoes.duracao(sessao)),
                MOTIVOS[sessao.motivo_saida],
            ]
            for sessao, nome in registos
        ]
        comum.mostrar_tabela(["Marketeer", "Entrada", "Saída", "Duração", "Motivo"], linhas)
        print(f"\n{len(registos)} sessões.")
    comum.pausa()
