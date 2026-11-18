"""Testes do resumo global do budget."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import budget as servico
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_18_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 18 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 18, 10, 0))


@pytest.fixture
def clientes(ligacao, contas):
    """Três clientes: a Carla (da fixture ``contas``), o José e a Beatriz, que não tem campanhas."""
    def criar(nome, email):
        return utilizadores.criar(ligacao, nome, email, seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE)

    return {
        "carla": contas[modelos.CLIENTE],
        "jose": criar("José Padeiro", "jose@padaria.pt"),
        "beatriz": criar("Beatriz Lopes", "beatriz@bicicletas.pt"),
    }


@pytest.fixture
def campanhas_demo(ligacao, contas, clientes):
    """Campanhas como as de demonstração, mais uma da Carla sem budget e outra acima do budget.

    ===========  =================  ==========  =========
    Cliente      Campanha           Budget      Despesa
    ===========  =================  ==========  =========
    Carla        Natal 2026         1500 €      1300 €
    Carla        Saldos             sem budget  200 €
    Carla        Páscoa             500 €       700 €
    José         Regresso às aulas  800 €       300 €
    ===========  =================  ==========  =========
    """
    miguel = contas[modelos.MARKETEER].id

    def campanha(nome, cliente, budget, custos):
        criada = campanhas_bd.criar(
            ligacao, nome, "", clientes[cliente].id, miguel, date(2026, 12, 1), date(2026, 12, 24), budget
        )
        for numero, custo in enumerate(custos, start=1):
            criativos_bd.criar(ligacao, criada.id, f"Criativo {numero}", "", custo)
        return criada

    return {
        "natal": campanha("Natal 2026", "carla", 150000, [40000, 90000]),
        "saldos": campanha("Saldos", "carla", None, [20000]),
        "pascoa": campanha("Páscoa", "carla", 50000, [70000]),
        "aulas": campanha("Regresso às aulas", "jose", 80000, [30000, None]),
    }


# --- contas ------------------------------------------------------------------


@pytest.mark.parametrize(
    ("budget", "gasto", "acima"),
    [(150000, 130000, False), (150000, 150000, False), (150000, 150001, True), (None, 999999, False)],
)
def test_acima_do_budget(budget, gasto, acima):
    campanha = modelos.Campanha(1, "Natal", "", 1, 2, budget_centimos=budget)

    assert servico.acima_do_budget(campanha, gasto) is acima


def test_resumo_por_cliente(ligacao, campanhas_demo):
    carla, jose = servico.resumo_por_cliente(ligacao)

    assert carla.cliente_nome == "Carla Cliente"
    assert carla.campanhas == 3
    assert carla.budget_centimos == 200000
    assert carla.despesa_centimos == 220000
    assert carla.restante_centimos == -20000
    assert carla.sem_budget == 1
    assert carla.acima_do_budget == 1

    assert jose.cliente_nome == "José Padeiro"
    assert jose.campanhas == 1
    assert jose.budget_centimos == 80000
    assert jose.despesa_centimos == 30000
    assert jose.restante_centimos == 50000
    assert jose.sem_budget == 0
    assert jose.acima_do_budget == 0


def test_clientes_sem_campanhas_nao_aparecem_no_resumo(ligacao, campanhas_demo, clientes):
    nomes = [resumo.cliente_nome for resumo in servico.resumo_por_cliente(ligacao)]

    assert "Beatriz Lopes" not in nomes


def test_resumo_sem_campanhas_esta_vazio(ligacao, contas):
    assert servico.resumo_por_cliente(ligacao) == []
    assert servico.campanhas_acima_do_budget(ligacao) == []


def test_resumo_por_ordem_alfabetica_do_cliente(ligacao, contas, clientes):
    miguel = contas[modelos.MARKETEER].id
    campanhas_bd.criar(ligacao, "Primeira", "", clientes["jose"].id, miguel)
    campanhas_bd.criar(ligacao, "Segunda", "", clientes["beatriz"].id, miguel)
    campanhas_bd.criar(ligacao, "Terceira", "", clientes["carla"].id, miguel)

    nomes = [resumo.cliente_nome for resumo in servico.resumo_por_cliente(ligacao)]

    assert nomes == ["Beatriz Lopes", "Carla Cliente", "José Padeiro"]


def test_somar_da_os_totais(ligacao, campanhas_demo):
    total = servico.somar(servico.resumo_por_cliente(ligacao))

    assert total.cliente_nome == "Total"
    assert total.campanhas == 4
    assert total.budget_centimos == 280000
    assert total.despesa_centimos == 250000
    assert total.restante_centimos == 30000
    assert total.sem_budget == 1
    assert total.acima_do_budget == 1


def test_somar_uma_lista_vazia_da_zero():
    total = servico.somar([])

    assert (total.campanhas, total.budget_centimos, total.despesa_centimos, total.restante_centimos) == (0, 0, 0, 0)


def test_campanhas_acima_do_budget(ligacao, campanhas_demo):
    ((campanha, gasto),) = servico.campanhas_acima_do_budget(ligacao)

    assert campanha.nome == "Páscoa"
    assert gasto == 70000


def test_campanhas_do_cliente_com_a_despesa(ligacao, campanhas_demo, clientes):
    lista = servico.campanhas_do_cliente(ligacao, clientes["carla"].id)

    assert [(campanha.nome, gasto) for campanha, gasto in lista] == [
        ("Natal 2026", 130000),
        ("Saldos", 20000),
        ("Páscoa", 70000),
    ]


@pytest.mark.parametrize("cliente", ["beatriz", None])
def test_campanhas_de_um_cliente_sem_campanhas_da_erro(ligacao, campanhas_demo, clientes, cliente):
    numero = clientes[cliente].id if cliente else 999

    with pytest.raises(ErroValidacao, match=f"Não há nenhum cliente com campanhas com o número {numero}"):
        servico.campanhas_do_cliente(ligacao, numero)
