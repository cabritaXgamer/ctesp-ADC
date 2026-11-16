"""Testes das campanhas vistas pelo Cliente."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio
from gestor_campanhas.cli import campanhas as menu
from gestor_campanhas.cli import perfis
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import campanhas as servico


@pytest.fixture(autouse=True)
def dia_16_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 16 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 16, 10, 0))


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(ligacao, "José Padeiro", "jose@padaria.pt", "x", modelos.CLIENTE)


@pytest.fixture
def miguel(ligacao, contas):
    """O marketeer da fixture ``contas``, já com telefone."""
    marketeer = contas[modelos.MARKETEER]
    return utilizadores.atualizar_dados(ligacao, marketeer.id, marketeer.nome, "910000002", "", "")


@pytest.fixture
def natal(ligacao, contas, miguel):
    """Uma campanha da Carla, com budget, por começar."""
    return repositorio.criar(
        ligacao,
        "Natal",
        "Vender mais",
        contas[modelos.CLIENTE].id,
        miguel.id,
        date(2026, 12, 1),
        date(2026, 12, 24),
        150000,
    )


@pytest.fixture
def saldos(ligacao, contas, miguel):
    """Outra campanha da Carla, sem datas e sem budget."""
    return repositorio.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, miguel.id)


# --- base de dados -----------------------------------------------------------


def test_repositorio_lista_so_as_campanhas_do_cliente(ligacao, contas, natal, saldos, jose, miguel):
    do_jose = repositorio.criar(ligacao, "Bolo-rei", "", jose.id, miguel.id)

    assert repositorio.listar_por_cliente(ligacao, contas[modelos.CLIENTE].id) == [natal, saldos]
    assert repositorio.listar_por_cliente(ligacao, jose.id) == [do_jose]


# --- regras ------------------------------------------------------------------


def test_cliente_ve_as_suas_campanhas_com_e_sem_budget(ligacao, contas, natal, saldos):
    lista = servico.listar_do_cliente(ligacao, contas[modelos.CLIENTE])

    assert lista == [natal, saldos]
    assert [campanha.budget_centimos for campanha in lista] == [150000, None]


def test_cliente_nao_ve_as_campanhas_de_outro(ligacao, contas, natal, jose):
    assert servico.listar_do_cliente(ligacao, jose) == []
    assert servico.obter_do_cliente(ligacao, contas[modelos.CLIENTE], natal.id) == natal
    with pytest.raises(ErroValidacao, match=f"Não tem nenhuma campanha com o número {natal.id}"):
        servico.obter_do_cliente(ligacao, jose, natal.id)
    with pytest.raises(ErroValidacao, match="Não tem nenhuma campanha com o número 999"):
        servico.obter_do_cliente(ligacao, jose, 999)


def test_responsavel_tem_os_contactos_do_marketeer(ligacao, natal):
    marketeer = servico.responsavel(ligacao, natal)

    assert marketeer.nome == "Miguel Marketeer"
    assert marketeer.email == "miguel@agencia.pt"
    assert marketeer.telefone == "910000002"


def test_responsavel_muda_quando_a_campanha_e_reatribuida(ligacao, natal, emails):
    marta = utilizadores.criar(ligacao, "Marta Marques", "marta@agencia.pt", "x", modelos.MARKETEER)
    alterada = servico.atribuir_marketeer(ligacao, natal.id, marta.id)

    assert servico.responsavel(ligacao, alterada).email == "marta@agencia.pt"


# --- menu: lista -------------------------------------------------------------


def test_menu_avisa_quando_o_cliente_nao_tem_campanhas(teclado, ligacao, contas, capsys):
    teclado("0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    assert 'Ainda não tem campanhas. Pode pedir uma na opção "Pedidos de campanha".' in capsys.readouterr().out


def test_menu_mostra_as_campanhas_do_cliente_com_o_budget(teclado, ligacao, contas, natal, saldos, jose, miguel, capsys):
    repositorio.criar(ligacao, "Bolo-rei", "", jose.id, miguel.id)
    teclado("0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "N.º  Nome    Início      Fim         Budget       Estado       Marketeer" in saida
    assert "Natal   2026-12-01  2026-12-24  1 500,00 €   Por começar  Miguel Marketeer" in saida
    assert "Saldos  -           -           Por definir  Em curso     Miguel Marketeer" in saida
    assert "Bolo-rei" not in saida
    assert "2 campanhas." in saida
    assert "O budget de cada campanha é definido pelo administrador." in saida


def test_opcao_campanhas_esta_no_menu_do_cliente():
    opcoes = dict(perfis.OPCOES[modelos.CLIENTE])

    assert opcoes["Campanhas"] is menu.do_cliente
