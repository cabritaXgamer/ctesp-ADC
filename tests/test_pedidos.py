"""Testes dos pedidos de campanha."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.cli import pedidos as menu
from gestor_campanhas.cli import perfis
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import pedidos as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import pedidos as servico
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_16_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 16 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 16, 10, 0))


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


def objetivos(lista):
    return [pedido.objetivo for pedido in lista]


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_um_pedido(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    pedido = repositorio.criar(ligacao, cliente.id, "Vender mais", 150050, date(2026, 12, 20), ["Facebook", "TikTok"])

    assert pedido == repositorio.obter_por_id(ligacao, pedido.id)
    assert pedido.cliente_id == cliente.id
    assert pedido.cliente_nome == "Carla Cliente"
    assert pedido.objetivo == "Vender mais"
    assert pedido.orcamento_centimos == 150050
    assert pedido.prazo == date(2026, 12, 20)
    assert pedido.plataformas == ["Facebook", "TikTok"]
    assert pedido.estado == modelos.PENDENTE
    assert pedido.nome_estado == "Pendente"
    assert pedido.criado_em == datetime(2026, 11, 16, 10, 0)
    assert pedido.motivo_rejeicao == ""
    assert pedido.campanha_id is None


def test_repositorio_devolve_none_quando_o_pedido_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_os_pedidos_do_cliente_do_mais_recente_para_o_mais_antigo(ligacao, contas, jose):
    carla = contas[modelos.CLIENTE]
    repositorio.criar(ligacao, carla.id, "Primeiro", 1000, date(2026, 12, 1), ["Facebook"])
    repositorio.criar(ligacao, jose.id, "Do José", 1000, date(2026, 12, 1), ["Facebook"])
    repositorio.criar(ligacao, carla.id, "Segundo", 1000, date(2026, 12, 1), ["Facebook"])

    assert objetivos(repositorio.listar_por_cliente(ligacao, carla.id)) == ["Segundo", "Primeiro"]
    assert objetivos(repositorio.listar_por_cliente(ligacao, jose.id)) == ["Do José"]


def test_repositorio_altera_o_estado_e_guarda_o_motivo(ligacao, contas):
    pedido = repositorio.criar(ligacao, contas[modelos.CLIENTE].id, "Vender", 1000, date(2026, 12, 1), ["Facebook"])

    rejeitado = repositorio.definir_estado(ligacao, pedido.id, modelos.REJEITADO, "Orçamento insuficiente")

    assert rejeitado.estado == modelos.REJEITADO
    assert rejeitado.nome_estado == "Rejeitado"
    assert rejeitado.motivo_rejeicao == "Orçamento insuficiente"


# --- pedir -------------------------------------------------------------------


def test_cliente_pede_uma_campanha(ligacao, contas):
    carla = contas[modelos.CLIENTE]

    pedido = servico.criar(ligacao, carla, "  Vender mais ", "1500,50", "2026-12-20", ["TikTok", "Facebook"])

    assert pedido.objetivo == "Vender mais"
    assert pedido.orcamento_centimos == 150050
    assert pedido.prazo == date(2026, 12, 20)
    assert pedido.plataformas == ["Facebook", "TikTok"]
    assert pedido.estado == modelos.PENDENTE
    assert servico.listar_do_cliente(ligacao, carla) == [pedido]


def test_prazo_pode_ser_o_proprio_dia(ligacao, contas):
    pedido = servico.criar(ligacao, contas[modelos.CLIENTE], "Vender", "100", "2026-11-16", ["Facebook"])

    assert pedido.prazo == date(2026, 11, 16)


def test_plataformas_repetidas_contam_uma_vez(ligacao, contas):
    pedido = servico.criar(ligacao, contas[modelos.CLIENTE], "Vender", "100", "2026-12-01", ["TikTok", "TikTok"])

    assert pedido.plataformas == ["TikTok"]


@pytest.mark.parametrize(
    ("objetivo", "orcamento", "prazo", "plataformas", "mensagem"),
    [
        ("  ", "100", "2026-12-01", ["Facebook"], "O objetivo não pode ficar vazio"),
        ("Vender", "muito", "2026-12-01", ["Facebook"], "O valor não é válido"),
        ("Vender", "0", "2026-12-01", ["Facebook"], "tem de ser maior do que zero"),
        ("Vender", "100", "", ["Facebook"], "O prazo não pode ficar vazio"),
        ("Vender", "100", "20/12/2026", ["Facebook"], "A data do prazo não é válida"),
        ("Vender", "100", "2026-11-15", ["Facebook"], "não pode ser um dia que já passou"),
        ("Vender", "100", "2026-12-01", [], "Escolha pelo menos uma plataforma"),
        ("Vender", "100", "2026-12-01", ["Facebook", "Rádio"], "A plataforma Rádio não existe"),
    ],
)
def test_pedido_com_dados_invalidos_nao_e_registado(ligacao, contas, objetivo, orcamento, prazo, plataformas, mensagem):
    carla = contas[modelos.CLIENTE]

    with pytest.raises(ErroValidacao, match=mensagem):
        servico.criar(ligacao, carla, objetivo, orcamento, prazo, plataformas)

    assert servico.listar_do_cliente(ligacao, carla) == []


def test_cliente_so_ve_os_seus_pedidos(ligacao, contas, jose):
    carla = contas[modelos.CLIENTE]
    pedido = servico.criar(ligacao, carla, "Da Carla", "100", "2026-12-01", ["Facebook"])

    assert servico.listar_do_cliente(ligacao, jose) == []
    assert servico.obter_do_cliente(ligacao, carla, pedido.id) == pedido
    with pytest.raises(ErroValidacao, match=f"Não tem nenhum pedido com o número {pedido.id}"):
        servico.obter_do_cliente(ligacao, jose, pedido.id)
    with pytest.raises(ErroValidacao, match="Não tem nenhum pedido com o número 999"):
        servico.obter_do_cliente(ligacao, carla, 999)


# --- cancelar ----------------------------------------------------------------


@pytest.fixture
def pedido(ligacao, contas):
    """Um pedido pendente da Carla."""
    return servico.criar(ligacao, contas[modelos.CLIENTE], "Vender mais", "1500", "2026-12-20", ["Facebook", "Instagram"])


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


def test_cliente_nao_cancela_pedidos_de_outro(ligacao, contas, pedido, jose):
    with pytest.raises(ErroValidacao, match="Não tem nenhum pedido"):
        servico.cancelar(ligacao, jose, pedido.id)

    assert repositorio.obter_por_id(ligacao, pedido.id).estado == modelos.PENDENTE


# --- menu do cliente: lista e novo pedido ------------------------------------


def test_menu_avisa_quando_o_cliente_nao_tem_pedidos(teclado, ligacao, contas, capsys):
    teclado("0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "Os meus pedidos de campanha" in saida
    assert "Ainda não fez nenhum pedido." in saida
    assert "1. Novo pedido" in saida


def test_menu_mostra_so_os_pedidos_do_cliente(teclado, ligacao, contas, pedido, jose, capsys):
    servico.criar(ligacao, jose, "Do José", "100", "2026-12-01", ["Facebook"])
    teclado("0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "N.º  Feito em    Objetivo     Orçamento   Prazo       Estado" in saida
    assert f"{pedido.id}    2026-11-16  Vender mais  1 500,00 €  2026-12-20  Pendente" in saida
    assert "Do José" not in saida
    assert "1 pedido." in saida


def test_menu_regista_um_pedido_novo(teclado, ligacao, contas, capsys):
    carla = contas[modelos.CLIENTE]
    teclado("1", "Vender mais no Natal", "1500,50", "2026-12-20", "2, 1", "", "0")

    menu.do_cliente(ligacao, carla)

    saida = capsys.readouterr().out
    (registado,) = servico.listar_do_cliente(ligacao, carla)
    assert "  1. Facebook" in saida
    assert "  6. YouTube" in saida
    assert f"Pedido registado com o número {registado.id}. Fica pendente até ser analisado." in saida
    assert registado.objetivo == "Vender mais no Natal"
    assert registado.orcamento_centimos == 150050
    assert registado.plataformas == ["Facebook", "Instagram"]


def test_menu_repete_as_plataformas_ate_a_resposta_ser_valida(teclado, capsys):
    teclado("", "sete", "1,9", "3")

    assert menu.ler_plataformas() == ["Google Ads"]
    assert capsys.readouterr().out.count("Escreva números entre 1 e 6, separados por vírgulas.") == 3


def test_menu_mostra_o_erro_e_nao_regista(teclado, ligacao, contas, capsys):
    carla = contas[modelos.CLIENTE]
    teclado("1", "Vender", "100", "2026-01-01", "1", "", "0")

    menu.do_cliente(ligacao, carla)

    assert "O prazo não pode ser um dia que já passou. O pedido não foi registado." in capsys.readouterr().out
    assert servico.listar_do_cliente(ligacao, carla) == []


def test_resumir_corta_os_textos_compridos():
    assert menu.resumir("Curto") == "Curto"
    assert menu.resumir("a" * 40) == "a" * 40
    assert menu.resumir("Aumentar as vendas da loja durante o mês de dezembro") == "Aumentar as vendas da loja durante o..."
    assert len(menu.resumir("a" * 41)) == 40


def test_opcao_pedidos_esta_no_menu_do_cliente():
    descricoes = [descricao for descricao, _ in perfis.OPCOES[modelos.CLIENTE]]

    assert descricoes[0] == "Pedidos de campanha"


# --- menu do cliente: ver e cancelar -----------------------------------------


def test_menu_mostra_os_detalhes_de_um_pedido(teclado, ligacao, contas, pedido, capsys):
    teclado("2", str(pedido.id), "", "0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert f"Pedido n.º {pedido.id}" in saida
    assert "  Feito em:     2026-11-16 10:00" in saida
    assert "  Objetivo:     Vender mais" in saida
    assert "  Orçamento:    1 500,00 €" in saida
    assert "  Prazo:        2026-12-20" in saida
    assert "  Plataformas:  Facebook, Instagram" in saida
    assert "  Estado:       Pendente" in saida
    assert "Motivo:" not in saida
    assert "Campanha:" not in saida


def test_detalhes_de_um_pedido_rejeitado_mostram_o_motivo(ligacao, pedido, capsys):
    rejeitado = repositorio.definir_estado(ligacao, pedido.id, modelos.REJEITADO, "Orçamento insuficiente")

    menu.mostrar_detalhes(rejeitado)

    saida = capsys.readouterr().out
    assert "  Estado:       Rejeitado" in saida
    assert "  Motivo:       Orçamento insuficiente" in saida


def test_menu_nao_mostra_pedidos_de_outro_cliente(teclado, ligacao, pedido, jose, capsys):
    teclado("2", str(pedido.id), "", "0")

    menu.do_cliente(ligacao, jose)

    saida = capsys.readouterr().out
    assert f"Não tem nenhum pedido com o número {pedido.id}." in saida
    assert "Vender mais" not in saida


def test_menu_cancela_um_pedido_depois_de_confirmar(teclado, ligacao, contas, pedido, capsys):
    teclado("3", str(pedido.id), "s", "", "0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "Pedido cancelado." in saida
    assert "2026-12-20  Cancelado" in saida
    assert repositorio.obter_por_id(ligacao, pedido.id).estado == modelos.CANCELADO


def test_menu_nao_cancela_sem_confirmacao(teclado, ligacao, contas, pedido, capsys):
    teclado("3", str(pedido.id), "n", "", "0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    assert "Nada foi alterado." in capsys.readouterr().out
    assert repositorio.obter_por_id(ligacao, pedido.id).estado == modelos.PENDENTE


def test_menu_nao_pede_confirmacao_quando_o_pedido_ja_nao_esta_pendente(teclado, ligacao, contas, pedido, capsys):
    repositorio.definir_estado(ligacao, pedido.id, modelos.EM_ANALISE)
    teclado("3", str(pedido.id), "", "0")

    menu.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "Só é possível cancelar um pedido pendente. Este pedido está no estado Em análise." in saida
    assert "Cancelar este pedido?" not in saida
