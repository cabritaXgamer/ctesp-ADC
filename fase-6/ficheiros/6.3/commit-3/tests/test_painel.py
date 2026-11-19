"""Testes do painel de marketeers: trabalho, carga e inatividade."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import atividades
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import comentarios as servico_comentarios
from gestor_campanhas.servicos import criativos as servico_criativos
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


# --- registo da atividade ----------------------------------------------------


def _descricoes(ligacao, marketeer):
    """Devolve as descrições das atividades de um marketeer, da mais antiga para a mais recente."""
    return [atividade.descricao for atividade in reversed(atividades.listar_por_utilizador(ligacao, marketeer.id, 20))]


def test_alteracoes_aos_criativos_ficam_na_atividade_do_marketeer(ligacao, miguel, natal, tmp_path):
    criativo = servico_criativos.criar(ligacao, miguel, natal.id, "Banner")
    servico_criativos.editar(ligacao, miguel, criativo.id, "Banner grande")
    origem = tmp_path / "banner.png"
    origem.write_bytes(b"imagem")
    servico_criativos.anexar(ligacao, miguel, criativo.id, str(origem))
    servico_criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.EM_REVISAO)
    servico_criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.EM_PREPARACAO)
    servico_criativos.eliminar(ligacao, miguel, criativo.id)

    assert _descricoes(ligacao, miguel) == [
        "Criou o criativo Banner (campanha Natal 2026)",
        "Editou o criativo Banner grande (campanha Natal 2026)",
        "Anexou o ficheiro banner.png ao criativo Banner grande (campanha Natal 2026)",
        "Passou a Em revisão o criativo Banner grande (campanha Natal 2026)",
        "Passou a Em preparação o criativo Banner grande (campanha Natal 2026)",
        "Eliminou o criativo Banner grande (campanha Natal 2026)",
    ]


def test_resposta_a_um_comentario_fica_na_atividade_do_marketeer(ligacao, contas, miguel, natal):
    banner = criativos_bd.criar(ligacao, natal.id, "Banner", "")
    comentario = servico_comentarios.comentar(ligacao, contas[modelos.CLIENTE], banner.id, "Maior, por favor")

    servico_comentarios.responder(ligacao, miguel, comentario.id, "Combinado")

    assert _descricoes(ligacao, miguel) == ["Respondeu a um comentário do criativo Banner (campanha Natal 2026)"]


def test_alteracao_recusada_nao_fica_na_atividade(ligacao, miguel, natal):
    with pytest.raises(ErroValidacao):
        servico_criativos.criar(ligacao, miguel, natal.id, "")

    assert _descricoes(ligacao, miguel) == []
