"""Testes da decisão dos pedidos de alteração de budget e do histórico do budget."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio
from gestor_campanhas.cli import campanhas as menu_campanhas
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import alteracoes_budget as historico_bd
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos_budget as pedidos_bd
from gestor_campanhas.servicos import budget as servico
from gestor_campanhas.servicos import campanhas
from gestor_campanhas.servicos import pedidos as servico_pedidos


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


# --- histórico das alterações feitas pelo Administrador ----------------------


@pytest.fixture
def saldos(ligacao, contas):
    """Campanha da Carla criada por um marketeer, ainda sem budget."""
    return campanhas_bd.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id)


def test_primeiro_budget_fica_no_historico_como_budget_inicial(ligacao, saldos):
    campanhas.definir_budget(ligacao, saldos.id, "800")

    (alteracao,) = campanhas.historico_budget(ligacao, saldos)
    assert alteracao.budget_anterior_centimos is None
    assert alteracao.budget_novo_centimos == 80000
    assert alteracao.motivo == "Budget inicial"
    assert alteracao.alterado_em == datetime(2026, 11, 18, 10, 0)


def test_primeiro_budget_pode_ter_motivo(ligacao, saldos):
    campanhas.definir_budget(ligacao, saldos.id, "800", "Acordado em reunião")

    assert campanhas.historico_budget(ligacao, saldos)[0].motivo == "Acordado em reunião"


def test_alterar_um_budget_obriga_a_indicar_o_motivo(ligacao, natal):
    with pytest.raises(ErroValidacao, match="Indique o motivo da alteração do budget"):
        campanhas.definir_budget(ligacao, natal.id, "2000", "   ")

    assert campanhas.obter(ligacao, natal.id).budget_centimos == 150000
    assert campanhas.historico_budget(ligacao, natal) == []


def test_alteracao_com_motivo_fica_no_historico(ligacao, natal):
    alterada = campanhas.definir_budget(ligacao, natal.id, "1800", "  Desconto do fornecedor ")

    assert alterada.budget_centimos == 180000
    (alteracao,) = campanhas.historico_budget(ligacao, natal)
    assert alteracao.budget_anterior_centimos == 150000
    assert alteracao.budget_novo_centimos == 180000
    assert alteracao.motivo == "Desconto do fornecedor"
    assert alteracao.pedido_budget_id is None


def test_budget_igual_ao_atual_nao_e_alteracao(ligacao, natal):
    with pytest.raises(ErroValidacao, match="O budget novo é igual ao budget atual"):
        campanhas.definir_budget(ligacao, natal.id, "1500,00", "Nada")

    assert campanhas.historico_budget(ligacao, natal) == []


def test_aprovar_um_pedido_de_campanha_regista_o_budget_inicial(ligacao, contas):
    pedido_campanha = servico_pedidos.criar(
        ligacao, contas[modelos.CLIENTE], "Vender", "1200", "2026-12-20", ["Facebook"]
    )

    aprovado = servico_pedidos.aprovar(ligacao, pedido_campanha.id, "Natal", "1000", contas[modelos.MARKETEER].id)

    campanha = campanhas.obter(ligacao, aprovado.campanha_id)
    (alteracao,) = campanhas.historico_budget(ligacao, campanha)
    assert alteracao.budget_anterior_centimos is None
    assert alteracao.budget_novo_centimos == 100000
    assert alteracao.motivo == f"Budget inicial, do pedido de campanha n.º {pedido_campanha.id}"


def test_menu_pede_o_motivo_quando_a_campanha_ja_tem_budget(teclado, ligacao, contas, natal, capsys):
    teclado("1", str(natal.id), "1800", "Desconto do fornecedor", "", "0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Budget definido: 1 800,00 €. A alteração ficou registada no histórico do budget." in saida
    assert campanhas.historico_budget(ligacao, natal)[0].motivo == "Desconto do fornecedor"


def test_menu_nao_pede_o_motivo_do_primeiro_budget(teclado, ligacao, contas, saldos, capsys):
    teclado("1", str(saldos.id), "800", "", "0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Budget definido: 800,00 €." in capsys.readouterr().out
    assert campanhas.historico_budget(ligacao, saldos)[0].motivo == "Budget inicial"


# --- decisão dos pedidos -----------------------------------------------------


def test_aprovar_altera_o_budget_e_regista_no_historico(ligacao, natal, pedido):
    aprovado = servico.aprovar(ligacao, pedido.id)

    assert aprovado.estado == modelos.APROVADO
    assert aprovado.decidido_em == datetime(2026, 11, 18, 10, 0)
    assert campanhas.obter(ligacao, natal.id).budget_centimos == 200000
    (alteracao,) = campanhas.historico_budget(ligacao, natal)
    assert alteracao.budget_anterior_centimos == 150000
    assert alteracao.budget_novo_centimos == 200000
    assert alteracao.motivo == f"Pedido de budget n.º {pedido.id}: Mais anúncios em vídeo"
    assert alteracao.pedido_budget_id == pedido.id


def test_aprovar_usa_o_budget_atual_da_campanha_como_valor_anterior(ligacao, natal, pedido):
    campanhas.definir_budget(ligacao, natal.id, "1600", "Correção")

    servico.aprovar(ligacao, pedido.id)

    anterior, ultima = campanhas.historico_budget(ligacao, natal)
    assert anterior.budget_novo_centimos == 160000
    assert ultima.budget_anterior_centimos == 160000
    assert ultima.budget_novo_centimos == 200000


def test_aprovar_mesmo_com_parecer_desfavoravel(ligacao, natal, pedido):
    pedidos_bd.definir_parecer(ligacao, pedido.id, False, "Não há criativos", modelos.EM_ANALISE)

    assert servico.aprovar(ligacao, pedido.id).estado == modelos.APROVADO
    assert campanhas.obter(ligacao, natal.id).budget_centimos == 200000


def test_rejeitar_guarda_o_motivo_e_nao_muda_o_budget(ligacao, natal, pedido):
    rejeitado = servico.rejeitar(ligacao, pedido.id, "  Sem margem este ano ")

    assert rejeitado.estado == modelos.REJEITADO
    assert rejeitado.motivo_rejeicao == "Sem margem este ano"
    assert rejeitado.decidido_em == datetime(2026, 11, 18, 10, 0)
    assert campanhas.obter(ligacao, natal.id).budget_centimos == 150000
    assert campanhas.historico_budget(ligacao, natal) == []


def test_rejeitar_sem_motivo_nao_decide(ligacao, pedido):
    with pytest.raises(ErroValidacao, match="O motivo da rejeição não pode ficar vazio"):
        servico.rejeitar(ligacao, pedido.id, "  ")

    assert pedidos_bd.obter_por_id(ligacao, pedido.id).estado == modelos.EM_ANALISE


@pytest.mark.parametrize("decidir", [servico.aprovar, lambda ligacao, numero: servico.rejeitar(ligacao, numero, "Não")])
def test_pedido_sem_parecer_nao_pode_ser_decidido(ligacao, natal, decidir):
    sem_parecer = pedidos_bd.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios")

    with pytest.raises(ErroValidacao, match="Este pedido ainda não tem o parecer do marketeer"):
        decidir(ligacao, sem_parecer.id)

    assert pedidos_bd.obter_por_id(ligacao, sem_parecer.id).estado == modelos.PENDENTE
    assert campanhas.obter(ligacao, natal.id).budget_centimos == 150000


@pytest.mark.parametrize("estado", [modelos.APROVADO, modelos.REJEITADO, modelos.CANCELADO])
def test_pedido_decidido_ou_cancelado_nao_pode_ser_decidido_outra_vez(ligacao, natal, pedido, estado):
    pedidos_bd.definir_estado(ligacao, pedido.id, estado)

    with pytest.raises(ErroValidacao, match="Este pedido já não pode ser decidido"):
        servico.aprovar(ligacao, pedido.id)

    assert campanhas.obter(ligacao, natal.id).budget_centimos == 150000


def test_aprovar_nao_faz_nada_se_o_budget_ja_for_o_pedido(ligacao, natal, pedido):
    campanhas.definir_budget(ligacao, natal.id, "2000", "Já acordado por telefone")

    with pytest.raises(ErroValidacao, match="O budget da campanha já é 2 000,00 €"):
        servico.aprovar(ligacao, pedido.id)

    assert pedidos_bd.obter_por_id(ligacao, pedido.id).estado == modelos.EM_ANALISE
    assert len(campanhas.historico_budget(ligacao, natal)) == 1


def test_pedido_que_nao_existe_da_erro(ligacao):
    with pytest.raises(ErroValidacao, match="Não existe nenhum pedido de budget com o número 999"):
        servico.obter(ligacao, 999)


def test_lista_do_administrador_mostra_primeiro_os_por_decidir(ligacao, contas, natal, pedido):
    outra = campanhas_bd.criar(ligacao, "Outra", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id)
    servico.rejeitar(ligacao, pedido.id, "Não")
    novo = pedidos_bd.criar(ligacao, outra.id, None, 50000, "Começar")

    assert [p.id for p in servico.listar_todos(ligacao)] == [novo.id, pedido.id]
