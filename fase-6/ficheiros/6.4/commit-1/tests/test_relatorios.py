"""Testes do relatório das campanhas em CSV."""

import csv
from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import ficheiros
from gestor_campanhas.servicos import relatorios as servico
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
def natal(ligacao, contas, cliente):
    """Campanha da Carla, do Miguel, de 1 a 24 de dezembro, com um budget de 1500 €."""
    campanha = campanhas_bd.criar(
        ligacao,
        "Natal 2026",
        "",
        cliente.id,
        contas[modelos.MARKETEER].id,
        date(2026, 12, 1),
        date(2026, 12, 24),
        150000,
    )
    criativos_bd.criar(ligacao, campanha.id, "Banner de Natal", "", 40000, date(2026, 11, 25), "", "Facebook")
    video = criativos_bd.criar(ligacao, campanha.id, "Vídeo da montra", "", 120000, None, "", "Instagram")
    criativos_bd.definir_estado(ligacao, video.id, modelos.EM_REVISAO)
    return campanha


@pytest.fixture
def pascoa(ligacao, contas, cliente):
    """Campanha da Carla, sem budget, sem datas e sem criativos."""
    return campanhas_bd.criar(ligacao, "Páscoa", "", cliente.id, contas[modelos.MARKETEER].id)


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, com uma campanha própria."""
    jose = utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )
    campanhas_bd.criar(ligacao, "Bolo-rei", "", jose.id, contas[modelos.MARKETEER].id)
    return jose


@pytest.mark.parametrize(
    ("centimos", "texto"),
    [(150000, "1500,00"), (5, "0,05"), (0, "0,00"), (-20050, "-200,50"), (None, "")],
)
def test_valor_em_euros_no_relatorio(centimos, texto):
    assert servico.valor(centimos) == texto


def test_nome_do_ficheiro_tem_a_data_do_dia():
    assert servico.nome_do_ficheiro() == "relatorio-campanhas-2026-11-19.csv"


def test_linhas_do_relatorio(ligacao, cliente, natal, pascoa, jose):
    assert servico.linhas(ligacao, cliente) == [
        [
            "Natal 2026", "Por começar", "2026-12-01", "2026-12-24", "Miguel Marketeer",
            "1500,00", "1600,00", "-100,00",
            "Banner de Natal", "Em preparação", "Facebook", "2026-11-25", "400,00",
        ],
        [
            "Natal 2026", "Por começar", "2026-12-01", "2026-12-24", "Miguel Marketeer",
            "1500,00", "1600,00", "-100,00",
            "Vídeo da montra", "Em revisão", "Instagram", "", "1200,00",
        ],
        ["Páscoa", "Em curso", "", "", "Miguel Marketeer", "", "0,00", "", "", "", "", "", ""],
    ]


def test_cliente_sem_campanhas_nao_tem_linhas(ligacao, cliente):
    assert servico.linhas(ligacao, cliente) == []


def test_exportar_grava_o_csv(ligacao, cliente, natal, pascoa, tmp_path):
    caminho = servico.exportar(ligacao, cliente, str(tmp_path))

    assert caminho == tmp_path / "relatorio-campanhas-2026-11-19.csv"
    assert caminho.read_bytes().startswith(b"\xef\xbb\xbfCampanha;Estado da campanha;")
    with caminho.open(encoding="utf-8-sig", newline="") as ficheiro:
        conteudo = list(csv.reader(ficheiro, delimiter=";"))
    assert conteudo[0] == servico.CABECALHOS
    assert conteudo[1:] == servico.linhas(ligacao, cliente)


def test_exportar_nao_apaga_um_relatorio_que_ja_existe(ligacao, cliente, natal, tmp_path):
    primeiro = servico.exportar(ligacao, cliente, str(tmp_path))

    segundo = servico.exportar(ligacao, cliente, str(tmp_path))

    assert segundo == tmp_path / "relatorio-campanhas-2026-11-19 (1).csv"
    assert primeiro.exists()


def test_exportar_sem_campanhas_nao_grava_nada(ligacao, cliente, tmp_path):
    with pytest.raises(ErroValidacao, match="Ainda não tem campanhas, por isso não há nada para exportar."):
        servico.exportar(ligacao, cliente, str(tmp_path))

    assert list(tmp_path.iterdir()) == []


def test_exportar_para_uma_pasta_que_nao_existe(ligacao, cliente, natal, tmp_path):
    with pytest.raises(ErroValidacao, match="não existe"):
        servico.exportar(ligacao, cliente, str(tmp_path / "nao_existe"))


def test_caminho_livre_numera_os_nomes_repetidos(tmp_path):
    (tmp_path / "banner.png").write_bytes(b"1")
    (tmp_path / "banner (1).png").write_bytes(b"2")

    assert ficheiros.caminho_livre(str(tmp_path), "banner.png") == tmp_path / "banner (2).png"
    assert ficheiros.caminho_livre(str(tmp_path), "novo.png") == tmp_path / "novo.png"
