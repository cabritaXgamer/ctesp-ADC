"""Testes das decisões do Administrador sobre pedidos e campanhas."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos as pedidos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import campanhas
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_16_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 16 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 16, 10, 0))


@pytest.fixture(autouse=True)
def caixa_de_saida(emails):
    """Todos os testes deste ficheiro escrevem os emails numa pasta temporária."""
    return emails


@pytest.fixture
def marta(ligacao, contas):
    """Um segundo marketeer, além do ``Miguel Marketeer`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


@pytest.fixture
def natal(ligacao, contas):
    """Uma campanha do Miguel para a Carla, sem budget."""
    return campanhas_bd.criar(
        ligacao,
        "Natal",
        "Vender mais",
        contas[modelos.CLIENTE].id,
        contas[modelos.MARKETEER].id,
        date(2026, 12, 1),
        date(2026, 12, 24),
    )


@pytest.fixture
def pedido(ligacao, contas):
    """Um pedido pendente da Carla."""
    return pedidos_bd.criar(
        ligacao, contas[modelos.CLIENTE].id, "Vender mais", 150000, date(2026, 12, 20), ["Facebook", "Instagram"]
    )


# --- base de dados -----------------------------------------------------------


def test_repositorio_lista_todas_as_campanhas(ligacao, contas, natal, marta):
    saldos = campanhas_bd.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, marta.id)

    assert campanhas_bd.listar_todas(ligacao) == [natal, saldos]


def test_repositorio_altera_o_budget_e_o_marketeer(ligacao, natal, marta):
    assert campanhas_bd.definir_budget(ligacao, natal.id, 150050).budget_centimos == 150050

    alterada = campanhas_bd.definir_marketeer(ligacao, natal.id, marta.id)

    assert alterada.marketeer_id == marta.id
    assert alterada.marketeer_nome == "Marta Marques"
    assert alterada.budget_centimos == 150050


def test_repositorio_lista_os_pedidos_de_todos_os_clientes(ligacao, contas, pedido):
    jose = utilizadores.criar(ligacao, "José Padeiro", "jose@padaria.pt", "x", modelos.CLIENTE)
    outro = pedidos_bd.criar(ligacao, jose.id, "Do José", 1000, date(2026, 12, 1), ["Facebook"])

    assert pedidos_bd.listar_todos(ligacao) == [pedido, outro]


# --- budget ------------------------------------------------------------------


def test_administrador_define_o_budget_de_uma_campanha(ligacao, natal):
    alterada = campanhas.definir_budget(ligacao, natal.id, "1500,50")

    assert alterada.budget_centimos == 150050
    assert campanhas.obter(ligacao, natal.id) == alterada


def test_budget_pode_ser_alterado_mais_tarde(ligacao, natal):
    campanhas.definir_budget(ligacao, natal.id, "1500")

    assert campanhas.definir_budget(ligacao, natal.id, "2000").budget_centimos == 200000


@pytest.mark.parametrize(("valor", "mensagem"), [("muito", "O valor não é válido"), ("0", "maior do que zero")])
def test_budget_invalido_nao_e_guardado(ligacao, natal, valor, mensagem):
    with pytest.raises(ErroValidacao, match=mensagem):
        campanhas.definir_budget(ligacao, natal.id, valor)

    assert campanhas.obter(ligacao, natal.id).budget_centimos is None


def test_budget_de_campanha_que_nao_existe_da_erro(ligacao):
    with pytest.raises(ErroValidacao, match="Não existe nenhuma campanha com o número 999"):
        campanhas.definir_budget(ligacao, 999, "1500")


def test_administrador_ve_as_campanhas_de_todos_os_marketeers(ligacao, contas, natal, marta):
    saldos = campanhas_bd.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, marta.id)

    assert campanhas.listar_todas(ligacao) == [natal, saldos]
