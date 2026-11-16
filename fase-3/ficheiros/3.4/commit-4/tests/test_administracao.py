"""Testes das decisões do Administrador sobre pedidos e campanhas."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos as pedidos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import campanhas, pedidos
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_16_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 16 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 16, 10, 0))


@pytest.fixture(autouse=True)
def caixa_de_saida(emails):
    """Todos os testes deste ficheiro escrevem os emails numa pasta temporária."""
    return emails


@pytest.fixture
def marta(ligacao, contas):
    """Um segundo marketeer, além do ``Miguel Marketeer`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


@pytest.fixture
def natal(ligacao, contas):
    """Uma campanha do Miguel para a Carla, sem budget."""
    return campanhas_bd.criar(
        ligacao,
        "Natal",
        "Vender mais",
        contas[modelos.CLIENTE].id,
        contas[modelos.MARKETEER].id,
        date(2026, 12, 1),
        date(2026, 12, 24),
    )


@pytest.fixture
def pedido(ligacao, contas):
    """Um pedido pendente da Carla."""
    return pedidos_bd.criar(
        ligacao, contas[modelos.CLIENTE].id, "Vender mais", 150000, date(2026, 12, 20), ["Facebook", "Instagram"]
    )


# --- base de dados -----------------------------------------------------------


def test_repositorio_lista_todas_as_campanhas(ligacao, contas, natal, marta):
    saldos = campanhas_bd.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, marta.id)

    assert campanhas_bd.listar_todas(ligacao) == [natal, saldos]


def test_repositorio_altera_o_budget_e_o_marketeer(ligacao, natal, marta):
    assert campanhas_bd.definir_budget(ligacao, natal.id, 150050).budget_centimos == 150050

    alterada = campanhas_bd.definir_marketeer(ligacao, natal.id, marta.id)

    assert alterada.marketeer_id == marta.id
    assert alterada.marketeer_nome == "Marta Marques"
    assert alterada.budget_centimos == 150050


def test_repositorio_lista_os_pedidos_de_todos_os_clientes(ligacao, contas, pedido):
    jose = utilizadores.criar(ligacao, "José Padeiro", "jose@padaria.pt", "x", modelos.CLIENTE)
    outro = pedidos_bd.criar(ligacao, jose.id, "Do José", 1000, date(2026, 12, 1), ["Facebook"])

    assert pedidos_bd.listar_todos(ligacao) == [pedido, outro]


# --- budget ------------------------------------------------------------------


def test_administrador_define_o_budget_de_uma_campanha(ligacao, natal):
    alterada = campanhas.definir_budget(ligacao, natal.id, "1500,50")

    assert alterada.budget_centimos == 150050
    assert campanhas.obter(ligacao, natal.id) == alterada


def test_budget_pode_ser_alterado_mais_tarde(ligacao, natal):
    campanhas.definir_budget(ligacao, natal.id, "1500")

    assert campanhas.definir_budget(ligacao, natal.id, "2000").budget_centimos == 200000


@pytest.mark.parametrize(("valor", "mensagem"), [("muito", "O valor não é válido"), ("0", "maior do que zero")])
def test_budget_invalido_nao_e_guardado(ligacao, natal, valor, mensagem):
    with pytest.raises(ErroValidacao, match=mensagem):
        campanhas.definir_budget(ligacao, natal.id, valor)

    assert campanhas.obter(ligacao, natal.id).budget_centimos is None


def test_budget_de_campanha_que_nao_existe_da_erro(ligacao):
    with pytest.raises(ErroValidacao, match="Não existe nenhuma campanha com o número 999"):
        campanhas.definir_budget(ligacao, 999, "1500")


def test_administrador_ve_as_campanhas_de_todos_os_marketeers(ligacao, contas, natal, marta):
    saldos = campanhas_bd.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, marta.id)

    assert campanhas.listar_todas(ligacao) == [natal, saldos]


# --- marketeer responsável ---------------------------------------------------


def test_administrador_atribui_a_campanha_a_outro_marketeer(ligacao, contas, natal, marta, emails):
    alterada = campanhas.atribuir_marketeer(ligacao, natal.id, marta.id)

    assert alterada.marketeer_id == marta.id
    assert campanhas.listar_do_marketeer(ligacao, marta) == [alterada]
    assert campanhas.listar_do_marketeer(ligacao, contas[modelos.MARKETEER]) == []
    (aviso,) = emails()
    assert "Para: marta@agencia.pt" in aviso
    assert "Assunto: Foi-lhe atribuída uma campanha" in aviso
    assert "Passou a ser responsável pela campanha Natal, do cliente Carla Cliente." in aviso


def test_atribuir_ao_marketeer_que_ja_e_responsavel_da_erro(ligacao, contas, natal, emails):
    with pytest.raises(ErroValidacao, match="Miguel Marketeer já é responsável por esta campanha"):
        campanhas.atribuir_marketeer(ligacao, natal.id, contas[modelos.MARKETEER].id)

    assert emails() == []


def test_campanha_so_pode_ser_atribuida_a_um_marketeer_ativo(ligacao, contas, natal, marta, emails):
    utilizadores.definir_ativo(ligacao, marta.id, False)

    with pytest.raises(ErroValidacao, match="Este marketeer tem a conta desativada"):
        campanhas.atribuir_marketeer(ligacao, natal.id, marta.id)
    with pytest.raises(ErroValidacao, match="Não existe nenhum marketeer com o número"):
        campanhas.atribuir_marketeer(ligacao, natal.id, contas[modelos.CLIENTE].id)
    with pytest.raises(ErroValidacao, match="Não existe nenhum marketeer com o número 999"):
        campanhas.atribuir_marketeer(ligacao, natal.id, 999)

    assert campanhas.obter(ligacao, natal.id) == natal
    assert emails() == []


def test_marketeers_disponiveis_sao_os_ativos_por_ordem_alfabetica(ligacao, contas, marta):
    assert [marketeer.nome for marketeer in campanhas.marketeers_disponiveis(ligacao)] == [
        "Marta Marques",
        "Miguel Marketeer",
    ]

    utilizadores.definir_ativo(ligacao, marta.id, False)

    assert [marketeer.nome for marketeer in campanhas.marketeers_disponiveis(ligacao)] == ["Miguel Marketeer"]


# --- decisão dos pedidos -----------------------------------------------------


def test_administrador_ve_primeiro_os_pedidos_por_decidir(ligacao, contas, pedido):
    carla = contas[modelos.CLIENTE]
    segundo = pedidos_bd.criar(ligacao, carla.id, "Segundo", 1000, date(2026, 12, 1), ["Facebook"])
    terceiro = pedidos_bd.criar(ligacao, carla.id, "Terceiro", 1000, date(2026, 12, 1), ["Facebook"])
    pedidos_bd.definir_estado(ligacao, pedido.id, modelos.CANCELADO)
    pedidos_bd.definir_estado(ligacao, segundo.id, modelos.EM_ANALISE)

    assert [encontrado.id for encontrado in pedidos.listar_todos(ligacao)] == [segundo.id, terceiro.id, pedido.id]


def test_analisar_poe_o_pedido_em_analise(ligacao, contas, pedido):
    assert pedidos.analisar(ligacao, pedido.id).estado == modelos.EM_ANALISE
    assert pedidos.analisar(ligacao, pedido.id).estado == modelos.EM_ANALISE

    with pytest.raises(ErroValidacao, match="Só é possível cancelar um pedido pendente"):
        pedidos.cancelar(ligacao, contas[modelos.CLIENTE], pedido.id)


def test_analisar_nao_altera_um_pedido_ja_decidido(ligacao, pedido):
    pedidos_bd.definir_estado(ligacao, pedido.id, modelos.CANCELADO)

    assert pedidos.analisar(ligacao, pedido.id).estado == modelos.CANCELADO


def test_analisar_pedido_que_nao_existe_da_erro(ligacao):
    with pytest.raises(ErroValidacao, match="Não existe nenhum pedido com o número 999"):
        pedidos.analisar(ligacao, 999)


def test_aprovar_cria_a_campanha_e_avisa_o_cliente_e_o_marketeer(ligacao, contas, pedido, marta, emails):
    aprovado = pedidos.aprovar(ligacao, pedido.id, " Natal 2026 ", "1200", marta.id)

    assert aprovado.estado == modelos.APROVADO
    campanha = campanhas.obter(ligacao, aprovado.campanha_id)
    assert campanha.nome == "Natal 2026"
    assert campanha.objetivo == "Vender mais"
    assert campanha.cliente_id == contas[modelos.CLIENTE].id
    assert campanha.marketeer_id == marta.id
    assert campanha.budget_centimos == 120000
    assert campanha.data_inicio is None
    assert campanha.data_fim == date(2026, 12, 20)
    textos = "\n".join(emails())
    assert "Para: carla@empresa.pt" in textos
    assert "Assunto: O seu pedido de campanha foi aprovado" in textos
    assert "Foi criada a campanha Natal 2026, com um budget inicial de 1 200,00 €." in textos
    assert "O marketeer responsável é Marta Marques." in textos
    assert "Para: marta@agencia.pt" in textos
    assert "Passou a ser responsável pela campanha Natal 2026, do cliente Carla Cliente." in textos


@pytest.mark.parametrize(
    ("nome", "budget", "mensagem"),
    [("  ", "1200", "nome não pode ficar vazio"), ("Natal", "zero", "O valor não é válido"), ("Natal", "0", "maior do que zero")],
)
def test_aprovacao_com_dados_invalidos_nao_cria_nada(ligacao, pedido, marta, emails, nome, budget, mensagem):
    with pytest.raises(ErroValidacao, match=mensagem):
        pedidos.aprovar(ligacao, pedido.id, nome, budget, marta.id)

    assert pedidos.obter(ligacao, pedido.id).estado == modelos.PENDENTE
    assert campanhas.listar_todas(ligacao) == []
    assert emails() == []


def test_aprovacao_exige_um_marketeer_ativo(ligacao, pedido, marta):
    utilizadores.definir_ativo(ligacao, marta.id, False)

    with pytest.raises(ErroValidacao, match="Este marketeer tem a conta desativada"):
        pedidos.aprovar(ligacao, pedido.id, "Natal", "1200", marta.id)

    assert campanhas.listar_todas(ligacao) == []


def test_rejeitar_guarda_o_motivo_e_avisa_o_cliente(ligacao, pedido, emails):
    rejeitado = pedidos.rejeitar(ligacao, pedido.id, "  Orçamento insuficiente para o prazo ")

    assert rejeitado.estado == modelos.REJEITADO
    assert rejeitado.motivo_rejeicao == "Orçamento insuficiente para o prazo"
    assert rejeitado.campanha_id is None
    (aviso,) = emails()
    assert "Para: carla@empresa.pt" in aviso
    assert "Assunto: O seu pedido de campanha foi rejeitado" in aviso
    assert "Motivo: Orçamento insuficiente para o prazo" in aviso
    assert campanhas.listar_todas(ligacao) == []


def test_rejeitar_sem_motivo_da_erro(ligacao, pedido, emails):
    with pytest.raises(ErroValidacao, match="O motivo da rejeição não pode ficar vazio"):
        pedidos.rejeitar(ligacao, pedido.id, "   ")

    assert pedidos.obter(ligacao, pedido.id).estado == modelos.PENDENTE
    assert emails() == []


@pytest.mark.parametrize("estado", [modelos.APROVADO, modelos.REJEITADO, modelos.CANCELADO])
def test_um_pedido_so_e_decidido_uma_vez(ligacao, pedido, marta, estado):
    pedidos_bd.definir_estado(ligacao, pedido.id, estado)

    with pytest.raises(ErroValidacao, match="Este pedido já não pode ser decidido"):
        pedidos.aprovar(ligacao, pedido.id, "Natal", "1200", marta.id)
    with pytest.raises(ErroValidacao, match="Este pedido já não pode ser decidido"):
        pedidos.rejeitar(ligacao, pedido.id, "Motivo")


def test_eliminar_a_campanha_nao_apaga_o_pedido_aprovado(ligacao, pedido, marta):
    aprovado = pedidos.aprovar(ligacao, pedido.id, "Natal", "1200", marta.id)

    campanhas.eliminar(ligacao, marta, aprovado.campanha_id)

    depois = pedidos.obter(ligacao, pedido.id)
    assert depois.estado == modelos.APROVADO
    assert depois.campanha_id is None
