"""Testes das campanhas vistas pelo Cliente."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio
from gestor_campanhas.repositorios import campanhas as repositorio
from gestor_campanhas.repositorios import utilizadores


@pytest.fixture(autouse=True)
def dia_16_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 16 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 16, 10, 0))


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(ligacao, "José Padeiro", "jose@padaria.pt", "x", modelos.CLIENTE)


@pytest.fixture
def miguel(ligacao, contas):
    """O marketeer da fixture ``contas``, já com telefone."""
    marketeer = contas[modelos.MARKETEER]
    return utilizadores.atualizar_dados(ligacao, marketeer.id, marketeer.nome, "910000002", "", "")


@pytest.fixture
def natal(ligacao, contas, miguel):
    """Uma campanha da Carla, com budget, por começar."""
    return repositorio.criar(
        ligacao,
        "Natal",
        "Vender mais",
        contas[modelos.CLIENTE].id,
        miguel.id,
        date(2026, 12, 1),
        date(2026, 12, 24),
        150000,
    )


@pytest.fixture
def saldos(ligacao, contas, miguel):
    """Outra campanha da Carla, sem datas e sem budget."""
    return repositorio.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, miguel.id)


# --- base de dados -----------------------------------------------------------


def test_repositorio_lista_so_as_campanhas_do_cliente(ligacao, contas, natal, saldos, jose, miguel):
    do_jose = repositorio.criar(ligacao, "Bolo-rei", "", jose.id, miguel.id)

    assert repositorio.listar_por_cliente(ligacao, contas[modelos.CLIENTE].id) == [natal, saldos]
    assert repositorio.listar_por_cliente(ligacao, jose.id) == [do_jose]
