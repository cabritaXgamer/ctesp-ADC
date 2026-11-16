"""Testes dos pedidos de campanha."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.repositorios import pedidos as repositorio
from gestor_campanhas.repositorios import utilizadores
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_16_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 16 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 16, 10, 0))


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


def objetivos(lista):
    return [pedido.objetivo for pedido in lista]


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_um_pedido(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    pedido = repositorio.criar(ligacao, cliente.id, "Vender mais", 150050, date(2026, 12, 20), ["Facebook", "TikTok"])

    assert pedido == repositorio.obter_por_id(ligacao, pedido.id)
    assert pedido.cliente_id == cliente.id
    assert pedido.cliente_nome == "Carla Cliente"
    assert pedido.objetivo == "Vender mais"
    assert pedido.orcamento_centimos == 150050
    assert pedido.prazo == date(2026, 12, 20)
    assert pedido.plataformas == ["Facebook", "TikTok"]
    assert pedido.estado == modelos.PENDENTE
    assert pedido.nome_estado == "Pendente"
    assert pedido.criado_em == datetime(2026, 11, 16, 10, 0)
    assert pedido.motivo_rejeicao == ""
    assert pedido.campanha_id is None


def test_repositorio_devolve_none_quando_o_pedido_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_os_pedidos_do_cliente_do_mais_recente_para_o_mais_antigo(ligacao, contas, jose):
    carla = contas[modelos.CLIENTE]
    repositorio.criar(ligacao, carla.id, "Primeiro", 1000, date(2026, 12, 1), ["Facebook"])
    repositorio.criar(ligacao, jose.id, "Do José", 1000, date(2026, 12, 1), ["Facebook"])
    repositorio.criar(ligacao, carla.id, "Segundo", 1000, date(2026, 12, 1), ["Facebook"])

    assert objetivos(repositorio.listar_por_cliente(ligacao, carla.id)) == ["Segundo", "Primeiro"]
    assert objetivos(repositorio.listar_por_cliente(ligacao, jose.id)) == ["Do José"]


def test_repositorio_altera_o_estado_e_guarda_o_motivo(ligacao, contas):
    pedido = repositorio.criar(ligacao, contas[modelos.CLIENTE].id, "Vender", 1000, date(2026, 12, 1), ["Facebook"])

    rejeitado = repositorio.definir_estado(ligacao, pedido.id, modelos.REJEITADO, "Orçamento insuficiente")

    assert rejeitado.estado == modelos.REJEITADO
    assert rejeitado.nome_estado == "Rejeitado"
    assert rejeitado.motivo_rejeicao == "Orçamento insuficiente"
