"""Testes da consulta de horários de entrada e saída dos marketeers."""

from datetime import date, datetime, timedelta

import pytest

from gestor_campanhas import modelos
from gestor_campanhas.cli import admin, comum, perfis
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import sessoes as repositorio
from gestor_campanhas.servicos import sessoes


@pytest.fixture
def historico(ligacao, contas):
    """Três sessões de marketeer em dias diferentes e uma de cliente."""
    marketeer = contas[modelos.MARKETEER].id
    dias = [
        (datetime(2026, 11, 10, 9, 0), datetime(2026, 11, 10, 12, 30), modelos.LOGOUT),
        (datetime(2026, 11, 11, 14, 0), datetime(2026, 11, 11, 14, 15), modelos.INATIVIDADE),
        (datetime(2026, 11, 12, 23, 50), None, None),
    ]
    for entrada, saida, motivo in dias:
        sessao = repositorio.abrir(ligacao, marketeer, entrada)
        if saida:
            repositorio.fechar(ligacao, sessao.id, saida, motivo)
    outra = repositorio.abrir(ligacao, contas[modelos.CLIENTE].id, datetime(2026, 11, 11, 10, 0))
    repositorio.fechar(ligacao, outra.id, datetime(2026, 11, 11, 11, 0), modelos.LOGOUT)


def entradas(registos):
    return [sessao.entrada.strftime("%m-%d") for sessao, _ in registos]


# --- regras ------------------------------------------------------------------


def test_lista_so_marketeers_da_mais_recente_para_a_mais_antiga(ligacao, historico):
    registos = sessoes.horarios_dos_marketeers(ligacao)

    assert entradas(registos) == ["11-12", "11-11", "11-10"]
    assert {nome for _, nome in registos} == {"Miguel Marketeer"}


def test_filtro_inclui_o_primeiro_e_o_ultimo_dia_inteiros(ligacao, historico):
    registos = sessoes.horarios_dos_marketeers(ligacao, date(2026, 11, 11), date(2026, 11, 12))

    assert entradas(registos) == ["11-12", "11-11"]


def test_filtro_so_com_uma_das_datas(ligacao, historico):
    assert entradas(sessoes.horarios_dos_marketeers(ligacao, desde=date(2026, 11, 12))) == ["11-12"]
    assert entradas(sessoes.horarios_dos_marketeers(ligacao, ate=date(2026, 11, 10))) == ["11-10"]


def test_datas_trocadas_dao_erro(ligacao, historico):
    with pytest.raises(ErroValidacao, match="posterior"):
        sessoes.horarios_dos_marketeers(ligacao, date(2026, 11, 12), date(2026, 11, 10))


def test_duracao_de_uma_sessao(ligacao, historico):
    registos = sessoes.horarios_dos_marketeers(ligacao)

    assert sessoes.duracao(registos[2][0]) == timedelta(hours=3, minutes=30)
    assert sessoes.duracao(registos[0][0]) is None


# --- apresentação ------------------------------------------------------------


def test_formatar_duracao():
    assert admin.formatar_duracao(timedelta(hours=3, minutes=30)) == "3h30"
    assert admin.formatar_duracao(timedelta(minutes=5, seconds=59)) == "0h05"
    assert admin.formatar_duracao(None) == ""


def test_mostrar_tabela_alinha_as_colunas(capsys):
    comum.mostrar_tabela(["Nome", "Idade"], [["Ana", "30"], ["Bernardo", "5"]])

    assert capsys.readouterr().out.splitlines() == [
        "Nome      Idade",
        "--------  -----",
        "Ana       30",
        "Bernardo  5",
    ]


def test_ler_data_aceita_vazio_e_repete_se_for_invalida(teclado, capsys):
    teclado("", "13/11/2026", "2026-11-13")

    assert comum.ler_data("Desde") is None
    assert comum.ler_data("Desde") == date(2026, 11, 13)
    assert "Data inválida" in capsys.readouterr().out


def test_menu_mostra_os_horarios_filtrados(teclado, ligacao, contas, historico, capsys):
    teclado("2026-11-10", "2026-11-11", "")

    admin.horarios(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Miguel Marketeer  2026-11-10 09:00  2026-11-10 12:30  3h30     Terminou a sessão" in saida
    assert "Miguel Marketeer  2026-11-11 14:00  2026-11-11 14:15  0h15     Inatividade" in saida
    assert "2026-11-12" not in saida
    assert "2 sessões." in saida


def test_menu_mostra_sessao_em_curso(teclado, ligacao, contas, historico, capsys):
    teclado("2026-11-12", "", "")

    admin.horarios(ligacao, contas[modelos.ADMINISTRADOR])

    assert "(em curso)" in capsys.readouterr().out


def test_menu_sem_sessoes_no_periodo(teclado, ligacao, contas, historico, capsys):
    teclado("2026-01-01", "2026-01-31", "")

    admin.horarios(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Não há sessões de marketeers neste período." in capsys.readouterr().out


def test_menu_com_datas_trocadas_mostra_o_erro(teclado, ligacao, contas, historico, capsys):
    teclado("2026-11-12", "2026-11-10", "")

    admin.horarios(ligacao, contas[modelos.ADMINISTRADOR])

    assert "A data inicial não pode ser posterior à data final." in capsys.readouterr().out


def test_opcao_so_existe_no_menu_do_administrador():
    descricoes = {perfil: [descricao for descricao, _ in opcoes] for perfil, opcoes in perfis.OPCOES.items()}

    assert "Horários de entrada e saída dos marketeers" in descricoes[modelos.ADMINISTRADOR]
    assert "Horários de entrada e saída dos marketeers" not in descricoes[modelos.MARKETEER]
    assert "Horários de entrada e saída dos marketeers" not in descricoes[modelos.CLIENTE]
