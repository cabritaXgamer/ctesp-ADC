"""Testes do painel de marketeers: trabalho, carga e inatividade."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.repositorios import atividades
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import utilizadores
from tests.conftest import PASSWORD_TESTE


@pytest.fixture
def relogio_falso(monkeypatch):
    """Relógio que começa a 19 de novembro de 2026, às 10h00, e que os testes podem acertar.

    Devolve um dicionário: mudar ``relogio_falso["agora"]`` muda a hora atual.
    """
    estado = {"agora": datetime(2026, 11, 19, 10, 0)}
    monkeypatch.setattr(relogio, "agora", lambda: estado["agora"])
    return estado


@pytest.fixture(autouse=True)
def dia_19_de_novembro(relogio_falso):
    """Todos os testes começam a 19 de novembro de 2026, às 10h00."""
    return relogio_falso


@pytest.fixture
def miguel(contas):
    """O marketeer Miguel, da fixture ``contas``."""
    return contas[modelos.MARKETEER]


@pytest.fixture
def marta(ligacao):
    """Uma segunda marketeer."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


@pytest.fixture
def natal(ligacao, contas, miguel):
    """Campanha da Carla, do Miguel, de 1 a 24 de dezembro, com um budget de 1500 €."""
    return campanhas_bd.criar(
        ligacao, "Natal 2026", "", contas[modelos.CLIENTE].id, miguel.id, date(2026, 12, 1), date(2026, 12, 24), 150000
    )


@pytest.fixture
def bicicletas(ligacao, contas, marta):
    """Campanha da Carla, da Marta, sem datas."""
    return campanhas_bd.criar(ligacao, "Bicicletas", "", contas[modelos.CLIENTE].id, marta.id)


# --- base de dados -----------------------------------------------------------


def test_repositorio_regista_e_lista_as_atividades_da_mais_recente_para_a_mais_antiga(
    ligacao, miguel, marta, relogio_falso
):
    primeira = atividades.registar(ligacao, miguel.id, "Criou o criativo Banner")
    atividades.registar(ligacao, marta.id, "De outra pessoa")
    relogio_falso["agora"] = datetime(2026, 11, 19, 11, 0)
    segunda = atividades.registar(ligacao, miguel.id, "Editou o criativo Banner")

    lista = atividades.listar_por_utilizador(ligacao, miguel.id)

    assert lista == [segunda, primeira]
    assert primeira.descricao == "Criou o criativo Banner"
    assert primeira.registada_em == datetime(2026, 11, 19, 10, 0)
    assert segunda.registada_em == datetime(2026, 11, 19, 11, 0)


def test_repositorio_lista_so_as_atividades_mais_recentes(ligacao, miguel):
    for numero in range(7):
        atividades.registar(ligacao, miguel.id, f"Atividade {numero}")

    lista = atividades.listar_por_utilizador(ligacao, miguel.id, limite=3)

    assert [atividade.descricao for atividade in lista] == ["Atividade 6", "Atividade 5", "Atividade 4"]


def test_repositorio_devolve_a_ultima_atividade_de_cada_marketeer(ligacao, miguel, marta, relogio_falso):
    atividades.registar(ligacao, miguel.id, "Antiga")
    relogio_falso["agora"] = datetime(2026, 11, 20, 9, 0)
    atividades.registar(ligacao, miguel.id, "Recente")

    assert atividades.ultima_por_utilizador(ligacao) == {miguel.id: datetime(2026, 11, 20, 9, 0)}


def test_repositorio_lista_os_criativos_das_campanhas_de_um_marketeer(ligacao, miguel, natal, bicicletas):
    banner = criativos_bd.criar(ligacao, natal.id, "Banner", "")
    criativos_bd.criar(ligacao, bicicletas.id, "Anúncio", "")
    video = criativos_bd.criar(ligacao, natal.id, "Vídeo", "")

    assert criativos_bd.listar_por_marketeer(ligacao, miguel.id) == [banner, video]


def test_repositorio_devolve_o_criativo_mais_recente_de_cada_marketeer(
    ligacao, miguel, marta, natal, bicicletas, relogio_falso
):
    criativos_bd.criar(ligacao, natal.id, "Banner", "")
    relogio_falso["agora"] = datetime(2026, 11, 21, 15, 30)
    criativos_bd.criar(ligacao, natal.id, "Vídeo", "")
    relogio_falso["agora"] = datetime(2026, 11, 20, 8, 0)
    criativos_bd.criar(ligacao, bicicletas.id, "Anúncio", "")

    assert criativos_bd.ultima_criacao_por_marketeer(ligacao) == {
        miguel.id: datetime(2026, 11, 21, 15, 30),
        marta.id: datetime(2026, 11, 20, 8, 0),
    }
