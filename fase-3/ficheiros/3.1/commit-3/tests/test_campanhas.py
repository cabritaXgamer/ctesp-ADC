"""Testes das campanhas."""

from datetime import date

import pytest

from gestor_campanhas import modelos, seguranca
from gestor_campanhas.repositorios import campanhas as repositorio
from gestor_campanhas.repositorios import utilizadores
from tests.conftest import PASSWORD_TESTE


@pytest.fixture
def marta(ligacao, contas):
    """Um segundo marketeer, além do ``Miguel Marketeer`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao,
        "José Padeiro",
        "jose@padaria.pt",
        seguranca.gerar_hash(PASSWORD_TESTE),
        modelos.CLIENTE,
        empresa="Padaria Central, Lda.",
    )


def nomes(lista):
    return [campanha.nome for campanha in lista]


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_uma_campanha(ligacao, contas):
    cliente, marketeer = contas[modelos.CLIENTE], contas[modelos.MARKETEER]

    campanha = repositorio.criar(
        ligacao, "Natal", "Vender mais em dezembro", cliente.id, marketeer.id, date(2026, 12, 1), date(2026, 12, 24)
    )

    assert campanha == repositorio.obter_por_id(ligacao, campanha.id)
    assert campanha.nome == "Natal"
    assert campanha.objetivo == "Vender mais em dezembro"
    assert campanha.data_inicio == date(2026, 12, 1)
    assert campanha.data_fim == date(2026, 12, 24)
    assert campanha.budget_centimos is None
    assert campanha.cliente_nome == "Carla Cliente"
    assert campanha.marketeer_nome == "Miguel Marketeer"


def test_repositorio_aceita_campanha_sem_datas(ligacao, contas):
    campanha = repositorio.criar(ligacao, "Natal", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id)

    assert campanha.data_inicio is None
    assert campanha.data_fim is None


def test_repositorio_devolve_none_quando_a_campanha_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_so_as_campanhas_do_marketeer(ligacao, contas, marta):
    cliente, miguel = contas[modelos.CLIENTE], contas[modelos.MARKETEER]
    repositorio.criar(ligacao, "Natal", "", cliente.id, miguel.id)
    repositorio.criar(ligacao, "Saldos", "", cliente.id, marta.id)
    repositorio.criar(ligacao, "Páscoa", "", cliente.id, miguel.id)

    assert nomes(repositorio.listar_por_marketeer(ligacao, miguel.id)) == ["Natal", "Páscoa"]
    assert nomes(repositorio.listar_por_marketeer(ligacao, marta.id)) == ["Saldos"]


def test_repositorio_atualiza_os_dados_e_apaga_as_datas(ligacao, contas):
    campanha = repositorio.criar(
        ligacao, "Natal", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id, date(2026, 12, 1)
    )

    alterada = repositorio.atualizar(ligacao, campanha.id, "Natal 2026", "Novo objetivo", None, date(2026, 12, 31))

    assert alterada.nome == "Natal 2026"
    assert alterada.objetivo == "Novo objetivo"
    assert alterada.data_inicio is None
    assert alterada.data_fim == date(2026, 12, 31)
