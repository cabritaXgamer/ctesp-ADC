"""Testes das campanhas."""

from datetime import date

import pytest

from gestor_campanhas import modelos, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import campanhas as servico
from tests.conftest import PASSWORD_TESTE


@pytest.fixture
def marta(ligacao, contas):
    """Um segundo marketeer, além do ``Miguel Marketeer`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao,
        "José Padeiro",
        "jose@padaria.pt",
        seguranca.gerar_hash(PASSWORD_TESTE),
        modelos.CLIENTE,
        empresa="Padaria Central, Lda.",
    )


def nomes(lista):
    return [campanha.nome for campanha in lista]


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_uma_campanha(ligacao, contas):
    cliente, marketeer = contas[modelos.CLIENTE], contas[modelos.MARKETEER]

    campanha = repositorio.criar(
        ligacao, "Natal", "Vender mais em dezembro", cliente.id, marketeer.id, date(2026, 12, 1), date(2026, 12, 24)
    )

    assert campanha == repositorio.obter_por_id(ligacao, campanha.id)
    assert campanha.nome == "Natal"
    assert campanha.objetivo == "Vender mais em dezembro"
    assert campanha.data_inicio == date(2026, 12, 1)
    assert campanha.data_fim == date(2026, 12, 24)
    assert campanha.budget_centimos is None
    assert campanha.cliente_nome == "Carla Cliente"
    assert campanha.marketeer_nome == "Miguel Marketeer"


def test_repositorio_aceita_campanha_sem_datas(ligacao, contas):
    campanha = repositorio.criar(ligacao, "Natal", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id)

    assert campanha.data_inicio is None
    assert campanha.data_fim is None


def test_repositorio_devolve_none_quando_a_campanha_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_so_as_campanhas_do_marketeer(ligacao, contas, marta):
    cliente, miguel = contas[modelos.CLIENTE], contas[modelos.MARKETEER]
    repositorio.criar(ligacao, "Natal", "", cliente.id, miguel.id)
    repositorio.criar(ligacao, "Saldos", "", cliente.id, marta.id)
    repositorio.criar(ligacao, "Páscoa", "", cliente.id, miguel.id)

    assert nomes(repositorio.listar_por_marketeer(ligacao, miguel.id)) == ["Natal", "Páscoa"]
    assert nomes(repositorio.listar_por_marketeer(ligacao, marta.id)) == ["Saldos"]


def test_repositorio_atualiza_os_dados_e_apaga_as_datas(ligacao, contas):
    campanha = repositorio.criar(
        ligacao, "Natal", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id, date(2026, 12, 1)
    )

    alterada = repositorio.atualizar(ligacao, campanha.id, "Natal 2026", "Novo objetivo", None, date(2026, 12, 31))

    assert alterada.nome == "Natal 2026"
    assert alterada.objetivo == "Novo objetivo"
    assert alterada.data_inicio is None
    assert alterada.data_fim == date(2026, 12, 31)


# --- criar -------------------------------------------------------------------


def test_marketeer_cria_campanha_e_fica_responsavel(ligacao, contas):
    cliente, miguel = contas[modelos.CLIENTE], contas[modelos.MARKETEER]

    campanha = servico.criar(ligacao, miguel, "  Natal ", " Vender mais ", cliente.id, "2026-12-01", "2026-12-24")

    assert campanha.nome == "Natal"
    assert campanha.objetivo == "Vender mais"
    assert campanha.cliente_id == cliente.id
    assert campanha.marketeer_id == miguel.id
    assert campanha.data_inicio == date(2026, 12, 1)
    assert campanha.data_fim == date(2026, 12, 24)
    assert campanha.budget_centimos is None
    assert servico.listar_do_marketeer(ligacao, miguel) == [campanha]


def test_campanha_pode_ser_criada_so_com_nome_e_cliente(ligacao, contas):
    campanha = servico.criar(ligacao, contas[modelos.MARKETEER], "Natal", "", contas[modelos.CLIENTE].id)

    assert campanha.objetivo == ""
    assert campanha.data_inicio is None
    assert campanha.data_fim is None


@pytest.mark.parametrize(
    ("nome", "inicio", "fim", "mensagem"),
    [
        ("   ", "", "", "nome não pode ficar vazio"),
        ("Natal", "1 de dezembro", "", "A data de início não é válida"),
        ("Natal", "", "2026-13-01", "A data de fim não é válida"),
        ("Natal", "2026-12-24", "2026-12-01", "não pode ser anterior"),
    ],
)
def test_campanha_com_dados_invalidos_nao_e_criada(ligacao, contas, nome, inicio, fim, mensagem):
    miguel = contas[modelos.MARKETEER]

    with pytest.raises(ErroValidacao, match=mensagem):
        servico.criar(ligacao, miguel, nome, "", contas[modelos.CLIENTE].id, inicio, fim)

    assert servico.listar_do_marketeer(ligacao, miguel) == []


def test_campanha_so_pode_ser_criada_para_um_cliente(ligacao, contas):
    miguel = contas[modelos.MARKETEER]

    with pytest.raises(ErroValidacao, match="Não existe nenhum cliente com o número 999"):
        servico.criar(ligacao, miguel, "Natal", "", 999)
    with pytest.raises(ErroValidacao, match="Não existe nenhum cliente"):
        servico.criar(ligacao, miguel, "Natal", "", contas[modelos.ADMINISTRADOR].id)


def test_campanha_nao_pode_ser_criada_para_cliente_desativado(ligacao, contas):
    cliente = contas[modelos.CLIENTE]
    utilizadores.definir_ativo(ligacao, cliente.id, False)

    with pytest.raises(ErroValidacao, match="conta desativada"):
        servico.criar(ligacao, contas[modelos.MARKETEER], "Natal", "", cliente.id)


def test_clientes_disponiveis_sao_os_ativos_por_ordem_alfabetica(ligacao, contas, jose):
    utilizadores.criar(ligacao, "Beatriz Lopes", "beatriz@bicicletas.pt", "x", modelos.CLIENTE)
    utilizadores.definir_ativo(ligacao, jose.id, False)

    assert [cliente.nome for cliente in servico.clientes_disponiveis(ligacao)] == ["Beatriz Lopes", "Carla Cliente"]


# --- editar ------------------------------------------------------------------


@pytest.fixture
def natal(ligacao, contas):
    """Uma campanha do Miguel para a Carla."""
    return servico.criar(
        ligacao, contas[modelos.MARKETEER], "Natal", "Vender mais", contas[modelos.CLIENTE].id, "2026-12-01", "2026-12-24"
    )


def test_marketeer_edita_a_sua_campanha(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]

    alterada = servico.editar(ligacao, miguel, natal.id, "Natal 2026", "Outro objetivo", "", "2026-12-31")

    assert alterada.nome == "Natal 2026"
    assert alterada.objetivo == "Outro objetivo"
    assert alterada.data_inicio is None
    assert alterada.data_fim == date(2026, 12, 31)
    assert alterada.cliente_id == natal.cliente_id
    assert servico.obter_do_marketeer(ligacao, miguel, natal.id) == alterada


def test_marketeer_nao_edita_campanhas_de_outro(ligacao, contas, natal, marta):
    with pytest.raises(ErroValidacao, match=f"Não tem nenhuma campanha com o número {natal.id}"):
        servico.editar(ligacao, marta, natal.id, "Roubada", "", "", "")

    assert repositorio.obter_por_id(ligacao, natal.id) == natal


def test_editar_campanha_que_nao_existe_da_erro(ligacao, contas):
    with pytest.raises(ErroValidacao, match="Não tem nenhuma campanha com o número 999"):
        servico.editar(ligacao, contas[modelos.MARKETEER], 999, "Natal", "", "", "")


@pytest.mark.parametrize(
    ("nome", "inicio", "fim"),
    [("", "2026-12-01", "2026-12-24"), ("Natal", "ontem", ""), ("Natal", "2026-12-24", "2026-12-01")],
)
def test_edicao_invalida_nao_altera_nada(ligacao, contas, natal, nome, inicio, fim):
    with pytest.raises(ErroValidacao):
        servico.editar(ligacao, contas[modelos.MARKETEER], natal.id, nome, "Mudou", inicio, fim)

    assert repositorio.obter_por_id(ligacao, natal.id) == natal
