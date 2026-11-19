"""Testes dos comentários dos criativos."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import comentarios as repositorio
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import utilizadores
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_19_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 19 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 19, 10, 0))


@pytest.fixture
def natal(ligacao, contas):
    """Campanha da Carla, do Miguel, com um budget de 1500 €."""
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
def banner(ligacao, natal):
    """Criativo da campanha Natal 2026, em preparação."""
    return criativos_bd.criar(ligacao, natal.id, "Banner de Natal", "Árvore com os produtos", 40000)


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


@pytest.fixture
def marta(ligacao):
    """Uma segunda marketeer, sem campanhas."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_um_comentario(ligacao, contas, banner):
    comentario = repositorio.criar(ligacao, banner.id, contas[modelos.CLIENTE].id, "O logótipo devia ser maior")

    assert comentario == repositorio.obter_por_id(ligacao, comentario.id)
    assert comentario.criativo_id == banner.id
    assert comentario.autor_id == contas[modelos.CLIENTE].id
    assert comentario.autor_nome == "Carla Cliente"
    assert comentario.autor_perfil == modelos.CLIENTE
    assert comentario.texto == "O logótipo devia ser maior"
    assert comentario.criado_em == datetime(2026, 11, 19, 10, 0)
    assert comentario.resposta_a is None


def test_repositorio_guarda_uma_resposta(ligacao, contas, banner):
    comentario = repositorio.criar(ligacao, banner.id, contas[modelos.CLIENTE].id, "O logótipo devia ser maior")

    resposta = repositorio.criar(ligacao, banner.id, contas[modelos.MARKETEER].id, "Vou aumentá-lo", comentario.id)

    assert resposta.resposta_a == comentario.id
    assert resposta.autor_nome == "Miguel Marketeer"
    assert resposta.autor_perfil == modelos.MARKETEER


def test_repositorio_devolve_none_quando_o_comentario_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_os_comentarios_de_um_criativo_por_ordem(ligacao, contas, natal, banner):
    video = criativos_bd.criar(ligacao, natal.id, "Vídeo da montra", "")
    cliente = contas[modelos.CLIENTE].id
    primeiro = repositorio.criar(ligacao, banner.id, cliente, "Primeiro")
    repositorio.criar(ligacao, video.id, cliente, "Sobre o vídeo")
    segundo = repositorio.criar(ligacao, banner.id, cliente, "Segundo")

    lista = repositorio.listar_por_criativo(ligacao, banner.id)

    assert [comentario.id for comentario in lista] == [primeiro.id, segundo.id]
