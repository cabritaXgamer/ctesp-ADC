"""Testes da decisão dos pedidos de alteração de budget e do histórico do budget."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio
from gestor_campanhas.repositorios import alteracoes_budget as historico_bd
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos_budget as pedidos_bd


@pytest.fixture(autouse=True)
def dia_18_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 18 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 18, 10, 0))


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
def pedido(ligacao, natal):
    """Um pedido para passar o budget do Natal de 1500 € para 2000 €, já com parecer favorável."""
    criado = pedidos_bd.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios em vídeo")
    return pedidos_bd.definir_parecer(ligacao, criado.id, True, "Há margem", modelos.EM_ANALISE)


# --- base de dados -----------------------------------------------------------


def test_historico_regista_e_le_as_alteracoes(ligacao, natal, pedido):
    primeira = historico_bd.registar(ligacao, natal.id, None, 150000, "Budget inicial")
    segunda = historico_bd.registar(ligacao, natal.id, 150000, 200000, "Mais anúncios", pedido.id)

    assert historico_bd.listar_por_campanha(ligacao, natal.id) == [primeira, segunda]
    assert primeira.budget_anterior_centimos is None
    assert primeira.budget_novo_centimos == 150000
    assert primeira.motivo == "Budget inicial"
    assert primeira.alterado_em == datetime(2026, 11, 18, 10, 0)
    assert primeira.pedido_budget_id is None
    assert segunda.pedido_budget_id == pedido.id


def test_historico_de_uma_campanha_nao_mostra_o_das_outras(ligacao, contas, natal):
    outra = campanhas_bd.criar(ligacao, "Outra", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id)
    historico_bd.registar(ligacao, natal.id, None, 150000, "Budget inicial")

    assert historico_bd.listar_por_campanha(ligacao, outra.id) == []


def test_repositorio_regista_a_decisao_com_a_data(ligacao, pedido):
    rejeitado = pedidos_bd.decidir(ligacao, pedido.id, modelos.REJEITADO, "Sem margem")

    assert rejeitado.estado == modelos.REJEITADO
    assert rejeitado.motivo_rejeicao == "Sem margem"
    assert rejeitado.decidido_em == datetime(2026, 11, 18, 10, 0)


def test_repositorio_lista_os_pedidos_de_todas_as_campanhas(ligacao, contas, natal, pedido):
    outra = campanhas_bd.criar(ligacao, "Outra", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id)
    segundo = pedidos_bd.criar(ligacao, outra.id, None, 50000, "Começar")

    assert pedidos_bd.listar_todos(ligacao) == [pedido, segundo]
