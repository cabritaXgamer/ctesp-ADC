"""Testes dos pedidos de alteração de budget."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos_budget as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import budget as servico
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_18_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 18 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 18, 10, 0))


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


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
def padaria(ligacao, contas, jose):
    """Campanha do José, sem budget e sem datas."""
    return campanhas_bd.criar(ligacao, "Bolo-rei", "", jose.id, contas[modelos.MARKETEER].id)


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_um_pedido(ligacao, contas, natal):
    pedido = repositorio.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios em vídeo")

    assert pedido == repositorio.obter_por_id(ligacao, pedido.id)
    assert pedido.campanha_id == natal.id
    assert pedido.campanha_nome == "Natal 2026"
    assert pedido.cliente_id == contas[modelos.CLIENTE].id
    assert pedido.cliente_nome == "Carla Cliente"
    assert pedido.marketeer_id == contas[modelos.MARKETEER].id
    assert pedido.marketeer_nome == "Miguel Marketeer"
    assert pedido.budget_atual_centimos == 150000
    assert pedido.budget_pedido_centimos == 200000
    assert pedido.motivo == "Mais anúncios em vídeo"
    assert pedido.estado == modelos.PENDENTE
    assert pedido.nome_estado == "Pendente"
    assert pedido.criado_em == datetime(2026, 11, 18, 10, 0)
    assert pedido.parecer_viavel is None
    assert pedido.nome_parecer == "Por dar"
    assert pedido.parecer_justificacao == ""
    assert pedido.motivo_rejeicao == ""
    assert pedido.decidido_em is None


def test_repositorio_guarda_um_pedido_de_uma_campanha_sem_budget(ligacao, padaria):
    pedido = repositorio.criar(ligacao, padaria.id, None, 50000, "Começar a campanha")

    assert pedido.budget_atual_centimos is None
    assert pedido.cliente_nome == "José Padeiro"


def test_repositorio_devolve_none_quando_o_pedido_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_os_pedidos_do_cliente_do_mais_recente_para_o_mais_antigo(ligacao, contas, jose, natal, padaria):
    primeiro = repositorio.criar(ligacao, natal.id, 150000, 200000, "Primeiro")
    do_jose = repositorio.criar(ligacao, padaria.id, None, 50000, "Do José")
    segundo = repositorio.criar(ligacao, natal.id, 150000, 100000, "Segundo")

    assert repositorio.listar_por_cliente(ligacao, contas[modelos.CLIENTE].id) == [segundo, primeiro]
    assert repositorio.listar_por_cliente(ligacao, jose.id) == [do_jose]


def test_repositorio_encontra_o_pedido_por_decidir_de_uma_campanha(ligacao, natal):
    cancelado = repositorio.criar(ligacao, natal.id, 150000, 200000, "Antigo")
    repositorio.definir_estado(ligacao, cancelado.id, modelos.CANCELADO)
    assert repositorio.obter_por_decidir(ligacao, natal.id) is None

    pendente = repositorio.criar(ligacao, natal.id, 150000, 180000, "Novo")
    assert repositorio.obter_por_decidir(ligacao, natal.id) == pendente

    em_analise = repositorio.definir_estado(ligacao, pendente.id, modelos.EM_ANALISE)
    assert repositorio.obter_por_decidir(ligacao, natal.id) == em_analise


def test_repositorio_altera_o_estado(ligacao, natal):
    pedido = repositorio.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios")

    cancelado = repositorio.definir_estado(ligacao, pedido.id, modelos.CANCELADO)

    assert cancelado.estado == modelos.CANCELADO
    assert cancelado.nome_estado == "Cancelado"


@pytest.mark.parametrize(("viavel", "nome"), [(True, "Viável"), (False, "Não viável"), (None, "Por dar")])
def test_nome_do_parecer(viavel, nome):
    pedido = modelos.PedidoBudget(1, 1, 100, 200, "Motivo", parecer_viavel=viavel)

    assert pedido.nome_parecer == nome

# --- pedir -------------------------------------------------------------------


def test_cliente_pede_a_alteracao_do_budget(ligacao, contas, natal):
    carla = contas[modelos.CLIENTE]

    pedido = servico.pedir(ligacao, carla, natal.id, "2000,50", "  Mais anúncios em vídeo ")

    assert pedido.campanha_id == natal.id
    assert pedido.budget_atual_centimos == 150000
    assert pedido.budget_pedido_centimos == 200050
    assert pedido.motivo == "Mais anúncios em vídeo"
    assert pedido.estado == modelos.PENDENTE
    assert servico.listar_do_cliente(ligacao, carla) == [pedido]


def test_cliente_pode_pedir_um_budget_mais_baixo(ligacao, contas, natal):
    pedido = servico.pedir(ligacao, contas[modelos.CLIENTE], natal.id, "1000", "Menos anúncios")

    assert pedido.budget_pedido_centimos == 100000


def test_cliente_pode_pedir_budget_para_uma_campanha_sem_budget(ligacao, jose, padaria):
    pedido = servico.pedir(ligacao, jose, padaria.id, "500", "Começar a campanha")

    assert pedido.budget_atual_centimos is None
    assert pedido.budget_pedido_centimos == 50000


@pytest.mark.parametrize(
    ("budget", "motivo", "mensagem"),
    [
        ("muito", "Mais anúncios", "O valor não é válido"),
        ("0", "Mais anúncios", "O budget tem de ser maior do que zero"),
        ("1500", "Mais anúncios", "O valor pedido é igual ao budget atual da campanha"),
        ("2000", "   ", "O motivo não pode ficar vazio"),
    ],
)
def test_pedido_com_dados_invalidos_nao_e_registado(ligacao, contas, natal, budget, motivo, mensagem):
    carla = contas[modelos.CLIENTE]

    with pytest.raises(ErroValidacao, match=mensagem):
        servico.pedir(ligacao, carla, natal.id, budget, motivo)

    assert servico.listar_do_cliente(ligacao, carla) == []


def test_cliente_so_pede_para_as_suas_campanhas(ligacao, contas, natal, jose):
    with pytest.raises(ErroValidacao, match=f"Não tem nenhuma campanha com o número {natal.id}"):
        servico.pedir(ligacao, jose, natal.id, "2000", "Mais anúncios")

    assert servico.listar_do_cliente(ligacao, contas[modelos.CLIENTE]) == []


def test_campanha_terminada_nao_aceita_pedidos(ligacao, contas):
    carla = contas[modelos.CLIENTE]
    verao = campanhas_bd.criar(
        ligacao, "Verão", "", carla.id, contas[modelos.MARKETEER].id, date(2026, 7, 1), date(2026, 8, 31), 50000
    )

    with pytest.raises(ErroValidacao, match="A campanha Verão já terminou. O budget já não pode ser alterado."):
        servico.pedir(ligacao, carla, verao.id, "800", "Mais anúncios")


def test_campanha_que_acaba_hoje_ainda_aceita_pedidos(ligacao, contas):
    carla = contas[modelos.CLIENTE]
    hoje = campanhas_bd.criar(
        ligacao, "Hoje", "", carla.id, contas[modelos.MARKETEER].id, date(2026, 11, 1), date(2026, 11, 18), 50000
    )

    assert servico.pedir(ligacao, carla, hoje.id, "800", "Mais anúncios").estado == modelos.PENDENTE


@pytest.mark.parametrize("estado", [modelos.PENDENTE, modelos.EM_ANALISE])
def test_so_um_pedido_por_decidir_de_cada_vez(ligacao, contas, natal, estado):
    carla = contas[modelos.CLIENTE]
    primeiro = servico.pedir(ligacao, carla, natal.id, "2000", "Mais anúncios")
    repositorio.definir_estado(ligacao, primeiro.id, estado)

    with pytest.raises(ErroValidacao, match=rf"já tem um pedido de alteração de budget por decidir \(n.º {primeiro.id}\)"):
        servico.pedir(ligacao, carla, natal.id, "2500", "Ainda mais anúncios")


@pytest.mark.parametrize("estado", [modelos.APROVADO, modelos.REJEITADO, modelos.CANCELADO])
def test_depois_de_decidido_pode_haver_um_pedido_novo(ligacao, contas, natal, estado):
    carla = contas[modelos.CLIENTE]
    primeiro = servico.pedir(ligacao, carla, natal.id, "2000", "Mais anúncios")
    repositorio.definir_estado(ligacao, primeiro.id, estado)

    segundo = servico.pedir(ligacao, carla, natal.id, "2500", "Ainda mais anúncios")

    assert segundo.estado == modelos.PENDENTE


def test_cliente_so_ve_os_seus_pedidos_de_budget(ligacao, contas, natal, jose):
    carla = contas[modelos.CLIENTE]
    pedido = servico.pedir(ligacao, carla, natal.id, "2000", "Mais anúncios")

    assert servico.listar_do_cliente(ligacao, jose) == []
    assert servico.obter_do_cliente(ligacao, carla, pedido.id) == pedido
    with pytest.raises(ErroValidacao, match=f"Não tem nenhum pedido de budget com o número {pedido.id}"):
        servico.obter_do_cliente(ligacao, jose, pedido.id)
    with pytest.raises(ErroValidacao, match="Não tem nenhum pedido de budget com o número 999"):
        servico.obter_do_cliente(ligacao, carla, 999)


# --- cancelar ----------------------------------------------------------------


@pytest.fixture
def pedido(ligacao, contas, natal):
    """Um pedido pendente da Carla, para passar o budget do Natal de 1500 € para 2000 €."""
    return servico.pedir(ligacao, contas[modelos.CLIENTE], natal.id, "2000", "Mais anúncios em vídeo")


def test_cliente_cancela_um_pedido_pendente(ligacao, contas, pedido):
    carla = contas[modelos.CLIENTE]

    cancelado = servico.cancelar(ligacao, carla, pedido.id)

    assert cancelado.estado == modelos.CANCELADO
    assert servico.listar_do_cliente(ligacao, carla) == [cancelado]


@pytest.mark.parametrize("estado", [modelos.EM_ANALISE, modelos.APROVADO, modelos.REJEITADO, modelos.CANCELADO])
def test_so_um_pedido_pendente_pode_ser_cancelado(ligacao, contas, pedido, estado):
    repositorio.definir_estado(ligacao, pedido.id, estado)

    with pytest.raises(ErroValidacao, match="Só é possível cancelar um pedido pendente"):
        servico.cancelar(ligacao, contas[modelos.CLIENTE], pedido.id)

    assert repositorio.obter_por_id(ligacao, pedido.id).estado == estado


def test_cliente_nao_cancela_pedidos_de_outro(ligacao, pedido, jose):
    with pytest.raises(ErroValidacao, match="Não tem nenhum pedido de budget"):
        servico.cancelar(ligacao, jose, pedido.id)

    assert repositorio.obter_por_id(ligacao, pedido.id).estado == modelos.PENDENTE