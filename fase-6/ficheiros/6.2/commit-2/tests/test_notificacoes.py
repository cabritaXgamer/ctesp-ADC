"""Testes das notificações."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import notificacoes as repositorio
from gestor_campanhas.repositorios import utilizadores
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_19_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 19 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 19, 10, 0))


@pytest.fixture
def cliente(contas):
    """A cliente Carla, da fixture ``contas``."""
    return contas[modelos.CLIENTE]


@pytest.fixture
def marketeer(contas):
    """O marketeer Miguel, da fixture ``contas``."""
    return contas[modelos.MARKETEER]


@pytest.fixture
def natal(ligacao, cliente, marketeer):
    """Campanha da Carla, do Miguel, com um budget de 1500 €."""
    return campanhas_bd.criar(
        ligacao, "Natal 2026", "Vender mais", cliente.id, marketeer.id, date(2026, 12, 1), date(2026, 12, 24), 150000
    )


@pytest.fixture
def banner(ligacao, natal):
    """Criativo da campanha Natal 2026, em preparação."""
    return criativos_bd.criar(ligacao, natal.id, "Banner de Natal", "Árvore com os produtos", 40000)


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_uma_notificacao(ligacao, cliente):
    notificacao = repositorio.criar(ligacao, cliente.id, "Foi criado o criativo Banner", modelos.SOBRE_CRIATIVO, 3)

    assert notificacao == repositorio.obter_por_id(ligacao, notificacao.id)
    assert notificacao.utilizador_id == cliente.id
    assert notificacao.texto == "Foi criado o criativo Banner"
    assert notificacao.sobre == modelos.SOBRE_CRIATIVO
    assert notificacao.item_id == 3
    assert notificacao.criada_em == datetime(2026, 11, 19, 10, 0)
    assert notificacao.lida is False


@pytest.mark.parametrize(
    ("sobre", "nome"),
    [
        (modelos.SOBRE_CAMPANHA, "Campanha n.º 7"),
        (modelos.SOBRE_PEDIDO_BUDGET, "Pedido de budget n.º 7"),
        (modelos.SOBRE_CRIATIVO, "Criativo n.º 7"),
    ],
)
def test_nome_do_item_da_notificacao(ligacao, cliente, sobre, nome):
    assert repositorio.criar(ligacao, cliente.id, "Texto", sobre, 7).nome_item == nome


def test_repositorio_devolve_none_quando_a_notificacao_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_as_notificacoes_da_mais_recente_para_a_mais_antiga(ligacao, cliente, marketeer):
    primeira = repositorio.criar(ligacao, cliente.id, "Primeira", modelos.SOBRE_CRIATIVO, 1)
    repositorio.criar(ligacao, marketeer.id, "De outro", modelos.SOBRE_CRIATIVO, 1)
    segunda = repositorio.criar(ligacao, cliente.id, "Segunda", modelos.SOBRE_CRIATIVO, 2)

    lista = repositorio.listar_por_utilizador(ligacao, cliente.id)

    assert [notificacao.id for notificacao in lista] == [segunda.id, primeira.id]


def test_repositorio_conta_e_marca_as_notificacoes_por_ler(ligacao, cliente, marketeer):
    primeira = repositorio.criar(ligacao, cliente.id, "Primeira", modelos.SOBRE_CRIATIVO, 1)
    repositorio.criar(ligacao, cliente.id, "Segunda", modelos.SOBRE_CRIATIVO, 2)
    repositorio.criar(ligacao, cliente.id, "Terceira", modelos.SOBRE_CRIATIVO, 3)
    repositorio.criar(ligacao, marketeer.id, "De outro", modelos.SOBRE_CRIATIVO, 1)

    assert repositorio.marcar_como_lida(ligacao, primeira.id).lida is True
    assert repositorio.contar_por_ler(ligacao, cliente.id) == 2
    assert repositorio.marcar_todas_como_lidas(ligacao, cliente.id) == 2
    assert repositorio.contar_por_ler(ligacao, cliente.id) == 0
    assert repositorio.contar_por_ler(ligacao, marketeer.id) == 1
