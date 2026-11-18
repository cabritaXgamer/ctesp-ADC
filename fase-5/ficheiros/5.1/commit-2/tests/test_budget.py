"""Testes dos pedidos de alteração de budget."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos_budget as repositorio
from gestor_campanhas.repositorios import utilizadores
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_18_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 18 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 18, 10, 0))


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


@pytest.fixture
def natal(ligacao, contas):
    """Campanha da Carla, com um budget de 1500 €, que ainda não começou."""
    return campanhas_bd.criar(
        ligacao,
        "Natal 2026",
        "Vender mais",
        contas[modelos.CLIENTE].id,
        contas[modelos.MARKETEER].id,
        date(2026, 12, 1),
        date(2026, 12, 24),
        150000,
    )


@pytest.fixture
def padaria(ligacao, contas, jose):
    """Campanha do José, sem budget e sem datas."""
    return campanhas_bd.criar(ligacao, "Bolo-rei", "", jose.id, contas[modelos.MARKETEER].id)


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_um_pedido(ligacao, contas, natal):
    pedido = repositorio.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios em vídeo")

    assert pedido == repositorio.obter_por_id(ligacao, pedido.id)
    assert pedido.campanha_id == natal.id
    assert pedido.campanha_nome == "Natal 2026"
    assert pedido.cliente_id == contas[modelos.CLIENTE].id
    assert pedido.cliente_nome == "Carla Cliente"
    assert pedido.marketeer_id == contas[modelos.MARKETEER].id
    assert pedido.marketeer_nome == "Miguel Marketeer"
    assert pedido.budget_atual_centimos == 150000
    assert pedido.budget_pedido_centimos == 200000
    assert pedido.motivo == "Mais anúncios em vídeo"
    assert pedido.estado == modelos.PENDENTE
    assert pedido.nome_estado == "Pendente"
    assert pedido.criado_em == datetime(2026, 11, 18, 10, 0)
    assert pedido.parecer_viavel is None
    assert pedido.nome_parecer == "Por dar"
    assert pedido.parecer_justificacao == ""
    assert pedido.motivo_rejeicao == ""
    assert pedido.decidido_em is None


def test_repositorio_guarda_um_pedido_de_uma_campanha_sem_budget(ligacao, padaria):
    pedido = repositorio.criar(ligacao, padaria.id, None, 50000, "Começar a campanha")

    assert pedido.budget_atual_centimos is None
    assert pedido.cliente_nome == "José Padeiro"


def test_repositorio_devolve_none_quando_o_pedido_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_os_pedidos_do_cliente_do_mais_recente_para_o_mais_antigo(ligacao, contas, jose, natal, padaria):
    primeiro = repositorio.criar(ligacao, natal.id, 150000, 200000, "Primeiro")
    do_jose = repositorio.criar(ligacao, padaria.id, None, 50000, "Do José")
    segundo = repositorio.criar(ligacao, natal.id, 150000, 100000, "Segundo")

    assert repositorio.listar_por_cliente(ligacao, contas[modelos.CLIENTE].id) == [segundo, primeiro]
    assert repositorio.listar_por_cliente(ligacao, jose.id) == [do_jose]


def test_repositorio_encontra_o_pedido_por_decidir_de_uma_campanha(ligacao, natal):
    cancelado = repositorio.criar(ligacao, natal.id, 150000, 200000, "Antigo")
    repositorio.definir_estado(ligacao, cancelado.id, modelos.CANCELADO)
    assert repositorio.obter_por_decidir(ligacao, natal.id) is None

    pendente = repositorio.criar(ligacao, natal.id, 150000, 180000, "Novo")
    assert repositorio.obter_por_decidir(ligacao, natal.id) == pendente

    em_analise = repositorio.definir_estado(ligacao, pendente.id, modelos.EM_ANALISE)
    assert repositorio.obter_por_decidir(ligacao, natal.id) == em_analise


def test_repositorio_altera_o_estado(ligacao, natal):
    pedido = repositorio.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios")

    cancelado = repositorio.definir_estado(ligacao, pedido.id, modelos.CANCELADO)

    assert cancelado.estado == modelos.CANCELADO
    assert cancelado.nome_estado == "Cancelado"


@pytest.mark.parametrize(("viavel", "nome"), [(True, "Viável"), (False, "Não viável"), (None, "Por dar")])
def test_nome_do_parecer(viavel, nome):
    pedido = modelos.PedidoBudget(1, 1, 100, 200, "Motivo", parecer_viavel=viavel)

    assert pedido.nome_parecer == nome
