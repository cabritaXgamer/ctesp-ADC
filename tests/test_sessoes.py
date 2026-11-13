"""Testes das sessões: registo de entradas e saídas e inatividade."""

from datetime import datetime, timedelta

import pytest

from gestor_campanhas import config, modelos, relogio
from gestor_campanhas.cli import perfis, principal
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import configuracoes
from gestor_campanhas.repositorios import sessoes as repositorio
from gestor_campanhas.servicos import sessoes
from tests.conftest import PASSWORD_TESTE

INICIO = datetime(2026, 11, 13, 9, 0, 0)


@pytest.fixture
def relogio_falso(monkeypatch):
    """Substitui o relógio da aplicação por um que os testes controlam.

    Devolve um objeto com ``agora`` (a hora atual simulada) e
    ``avancar(minutos=..., segundos=...)``.
    """

    class Relogio:
        agora = INICIO

        def avancar(self, **tempo):
            self.agora += timedelta(**tempo)

    falso = Relogio()
    monkeypatch.setattr(relogio, "agora", lambda: falso.agora)
    return falso


def todas_as_sessoes(ligacao):
    return ligacao.execute("SELECT * FROM sessoes ORDER BY id").fetchall()


# --- definições --------------------------------------------------------------


def test_configuracoes_guardam_e_substituem_valores(ligacao):
    assert configuracoes.obter(ligacao, "cor") is None
    assert configuracoes.obter(ligacao, "cor", "azul") == "azul"

    configuracoes.definir(ligacao, "cor", "verde")
    configuracoes.definir(ligacao, "cor", "roxo")

    assert configuracoes.obter(ligacao, "cor") == "roxo"


def test_limite_de_inatividade_por_omissao(ligacao):
    assert sessoes.minutos_de_inatividade(ligacao) == config.MINUTOS_INATIVIDADE


def test_limite_de_inatividade_pode_ser_alterado(ligacao):
    sessoes.definir_minutos_de_inatividade(ligacao, 5)

    assert sessoes.minutos_de_inatividade(ligacao) == 5


def test_limite_de_inatividade_tem_de_ser_positivo(ligacao):
    with pytest.raises(ErroValidacao):
        sessoes.definir_minutos_de_inatividade(ligacao, 0)


# --- registo de entradas e saídas --------------------------------------------


def test_iniciar_regista_a_entrada(ligacao, contas, relogio_falso):
    sessao = sessoes.iniciar(ligacao, contas[modelos.MARKETEER])

    registo = repositorio.obter(ligacao, sessao.id)
    assert registo.utilizador_id == contas[modelos.MARKETEER].id
    assert registo.entrada == INICIO
    assert registo.saida is None
    assert registo.motivo_saida is None


def test_terminar_regista_a_saida_e_o_motivo(ligacao, contas, relogio_falso):
    sessao = sessoes.iniciar(ligacao, contas[modelos.MARKETEER])
    relogio_falso.avancar(minutes=7)

    sessoes.terminar(ligacao, sessao)

    registo = repositorio.obter(ligacao, sessao.id)
    assert registo.saida == INICIO + timedelta(minutes=7)
    assert registo.motivo_saida == modelos.LOGOUT
    assert sessao.aberta is False


def test_terminar_duas_vezes_mantem_o_primeiro_registo(ligacao, contas, relogio_falso):
    sessao = sessoes.iniciar(ligacao, contas[modelos.MARKETEER])
    relogio_falso.avancar(minutes=1)
    sessoes.terminar(ligacao, sessao)
    relogio_falso.avancar(minutes=30)

    sessoes.terminar(ligacao, sessao, modelos.INATIVIDADE)

    registo = repositorio.obter(ligacao, sessao.id)
    assert registo.saida == INICIO + timedelta(minutes=1)
    assert registo.motivo_saida == modelos.LOGOUT


# --- inatividade -------------------------------------------------------------


def test_sessao_so_expira_depois_do_limite(ligacao, contas, relogio_falso):
    sessao = sessoes.iniciar(ligacao, contas[modelos.CLIENTE])

    relogio_falso.avancar(minutes=config.MINUTOS_INATIVIDADE)
    assert sessao.expirou() is False

    relogio_falso.avancar(seconds=1)
    assert sessao.expirou() is True


def test_atividade_adia_a_expiracao(ligacao, contas, relogio_falso):
    sessao = sessoes.iniciar(ligacao, contas[modelos.CLIENTE])
    relogio_falso.avancar(minutes=10)
    sessao.registar_atividade()

    relogio_falso.avancar(minutes=10)

    assert sessao.expirou() is False


def test_saida_por_inatividade_fica_com_a_hora_do_limite(ligacao, contas, relogio_falso):
    sessao = sessoes.iniciar(ligacao, contas[modelos.CLIENTE])
    relogio_falso.avancar(minutes=45)

    sessoes.terminar(ligacao, sessao, modelos.INATIVIDADE)

    registo = repositorio.obter(ligacao, sessao.id)
    assert registo.saida == INICIO + timedelta(minutes=config.MINUTOS_INATIVIDADE)
    assert registo.motivo_saida == modelos.INATIVIDADE


# --- menus -------------------------------------------------------------------


def test_entrar_e_terminar_sessao_fica_registado(teclado, ligacao, contas, relogio_falso):
    teclado("1", "miguel@agencia.pt", PASSWORD_TESTE, "0", "0")

    principal.executar(ligacao)

    (registo,) = todas_as_sessoes(ligacao)
    assert registo["utilizador_id"] == contas[modelos.MARKETEER].id
    assert registo["entrada"] == "2026-11-13 09:00:00"
    assert registo["motivo_saida"] == modelos.LOGOUT


def test_password_errada_nao_cria_sessao(teclado, ligacao, contas):
    teclado("1", "miguel@agencia.pt", "errada", "", "0")

    principal.executar(ligacao)

    assert todas_as_sessoes(ligacao) == []


def test_menu_termina_a_sessao_por_inatividade(ligacao, contas, relogio_falso, monkeypatch, capsys):
    sessao = sessoes.iniciar(ligacao, contas[modelos.MARKETEER])

    def responder_ao_fim_de_20_minutos(_pergunta=""):
        relogio_falso.avancar(minutes=20)
        return "0"

    monkeypatch.setattr("builtins.input", responder_ao_fim_de_20_minutos)

    perfis.executar(ligacao, sessao)

    (registo,) = todas_as_sessoes(ligacao)
    assert registo["motivo_saida"] == modelos.INATIVIDADE
    assert registo["saida"] == "2026-11-13 09:15:00"
    saida = capsys.readouterr().out
    assert "terminou por inatividade" in saida
    assert "Sessão terminada." not in saida


def test_interromper_o_programa_regista_a_saida(teclado, ligacao, contas, relogio_falso):
    teclado("miguel@agencia.pt", PASSWORD_TESTE)  # a entrada acaba com a sessão aberta

    with pytest.raises(EOFError):
        principal.entrar(ligacao)

    (registo,) = todas_as_sessoes(ligacao)
    assert registo["motivo_saida"] == modelos.LOGOUT
