"""Testes dos pedidos de alteração de budget."""

from datetime import date, datetime

import pytest

from gestor_campanhas import config, dados_demo, modelos, relogio, seguranca
from gestor_campanhas.cli import budget as menu
from gestor_campanhas.cli import campanhas as menu_campanhas
from gestor_campanhas.cli import pedidos as menu_pedidos
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos_budget as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import budget as servico
from gestor_campanhas.servicos import pedidos as servico_pedidos
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


def test_repositorio_guarda_o_parecer_e_muda_o_estado(ligacao, natal):
    pedido = repositorio.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios")

    com_parecer = repositorio.definir_parecer(ligacao, pedido.id, False, "Não há criativos para isso", modelos.EM_ANALISE)

    assert com_parecer.parecer_viavel is False
    assert com_parecer.nome_parecer == "Não viável"
    assert com_parecer.parecer_justificacao == "Não há criativos para isso"
    assert com_parecer.estado == modelos.EM_ANALISE

    outro = repositorio.definir_parecer(ligacao, pedido.id, True, "Afinal há", modelos.EM_ANALISE)

    assert outro.parecer_viavel is True
    assert outro.parecer_justificacao == "Afinal há"


def test_repositorio_lista_os_pedidos_das_campanhas_do_marketeer(ligacao, contas, natal):
    marta = utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )
    da_marta = campanhas_bd.criar(ligacao, "Primavera", "", contas[modelos.CLIENTE].id, marta.id)
    primeiro = repositorio.criar(ligacao, natal.id, 150000, 200000, "Primeiro")
    outro = repositorio.criar(ligacao, da_marta.id, None, 50000, "Da Marta")
    segundo = repositorio.criar(ligacao, natal.id, 150000, 100000, "Segundo")

    assert repositorio.listar_por_marketeer(ligacao, contas[modelos.MARKETEER].id) == [primeiro, segundo]
    assert repositorio.listar_por_marketeer(ligacao, marta.id) == [outro]


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


# --- parecer do marketeer ----------------------------------------------------


@pytest.fixture
def marta(ligacao):
    """Uma segunda marketeer, sem campanhas."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


def test_marketeer_da_parecer_e_o_pedido_fica_em_analise(ligacao, contas, pedido):
    miguel = contas[modelos.MARKETEER]

    com_parecer = servico.dar_parecer(ligacao, miguel, pedido.id, True, "  Há margem para mais vídeo ")

    assert com_parecer.parecer_viavel is True
    assert com_parecer.parecer_justificacao == "Há margem para mais vídeo"
    assert com_parecer.estado == modelos.EM_ANALISE


def test_marketeer_pode_mudar_o_parecer_antes_da_decisao(ligacao, contas, pedido):
    miguel = contas[modelos.MARKETEER]
    servico.dar_parecer(ligacao, miguel, pedido.id, True, "Há margem")

    novo = servico.dar_parecer(ligacao, miguel, pedido.id, False, "Afinal os criativos não ficam prontos")

    assert novo.parecer_viavel is False
    assert novo.parecer_justificacao == "Afinal os criativos não ficam prontos"
    assert novo.estado == modelos.EM_ANALISE


def test_depois_do_parecer_o_cliente_ja_nao_cancela(ligacao, contas, pedido):
    servico.dar_parecer(ligacao, contas[modelos.MARKETEER], pedido.id, True, "Há margem")

    with pytest.raises(ErroValidacao, match="Este pedido está no estado Em análise"):
        servico.cancelar(ligacao, contas[modelos.CLIENTE], pedido.id)


def test_parecer_sem_justificacao_nao_e_guardado(ligacao, contas, pedido):
    with pytest.raises(ErroValidacao, match="A justificação do parecer não pode ficar vazia"):
        servico.dar_parecer(ligacao, contas[modelos.MARKETEER], pedido.id, True, "   ")

    assert repositorio.obter_por_id(ligacao, pedido.id).parecer_viavel is None


@pytest.mark.parametrize("estado", [modelos.APROVADO, modelos.REJEITADO, modelos.CANCELADO])
def test_pedido_decidido_ou_cancelado_nao_aceita_parecer(ligacao, contas, pedido, estado):
    repositorio.definir_estado(ligacao, pedido.id, estado)

    with pytest.raises(ErroValidacao, match="Este pedido já não aceita parecer"):
        servico.dar_parecer(ligacao, contas[modelos.MARKETEER], pedido.id, True, "Há margem")


def test_marketeer_so_da_parecer_nas_suas_campanhas(ligacao, pedido, marta):
    with pytest.raises(ErroValidacao, match=f"Não há nenhum pedido de budget com o número {pedido.id} nas suas campanhas"):
        servico.dar_parecer(ligacao, marta, pedido.id, True, "Há margem")

    assert repositorio.obter_por_id(ligacao, pedido.id).parecer_viavel is None


def test_marketeer_novo_da_campanha_passa_a_ver_o_pedido(ligacao, contas, pedido, natal, marta):
    campanhas_bd.definir_marketeer(ligacao, natal.id, marta.id)

    assert servico.listar_do_marketeer(ligacao, marta) == [repositorio.obter_por_id(ligacao, pedido.id)]
    assert servico.listar_do_marketeer(ligacao, contas[modelos.MARKETEER]) == []


def test_lista_do_marketeer_mostra_primeiro_os_por_decidir(ligacao, contas, natal, padaria):
    miguel = contas[modelos.MARKETEER]
    antigo = repositorio.criar(ligacao, natal.id, 150000, 200000, "Antigo")
    repositorio.definir_estado(ligacao, antigo.id, modelos.CANCELADO)
    do_jose = repositorio.criar(ligacao, padaria.id, None, 50000, "Do José")
    novo = repositorio.criar(ligacao, natal.id, 150000, 180000, "Novo")

    assert [p.id for p in servico.listar_do_marketeer(ligacao, miguel)] == [do_jose.id, novo.id, antigo.id]


# --- menu do cliente ---------------------------------------------------------


def test_menu_mostra_os_dois_tipos_de_pedido(teclado, ligacao, contas, pedido, capsys):
    teclado("0")

    menu_pedidos.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "Pedidos de nova campanha\n\nNenhum." in saida
    assert "Pedidos de alteração de budget" in saida
    assert "N.º  Feito em    Campanha    De          Para        Estado" in saida
    assert f"{pedido.id}    2026-11-18  Natal 2026  1 500,00 €  2 000,00 €  Pendente" in saida
    assert "1 pedido de alteração de budget." in saida
    assert "4. Pedir alteração de budget" in saida
    assert "5. Ver pedido de budget" in saida
    assert "6. Cancelar pedido de budget" in saida


def test_menu_sem_pedidos_de_budget_diz_nenhum(teclado, ligacao, contas, capsys):
    servico_pedidos.criar(ligacao, contas[modelos.CLIENTE], "Vender", "100", "2026-12-01", ["Facebook"])
    teclado("0")

    menu_pedidos.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "1 pedido." in saida
    assert "Pedidos de alteração de budget\n\nNenhum." in saida


def test_menu_regista_um_pedido_de_budget(teclado, ligacao, contas, natal, capsys):
    carla = contas[modelos.CLIENTE]
    teclado("4", str(natal.id), "2000", "Mais anúncios em vídeo", "", "0")

    menu_pedidos.do_cliente(ligacao, carla)

    saida = capsys.readouterr().out
    (registado,) = servico.listar_do_cliente(ligacao, carla)
    assert "N.º  Campanha    Budget      Estado" in saida
    assert f"{natal.id}    Natal 2026  1 500,00 €  Por começar" in saida
    assert "Budget atual da campanha Natal 2026: 1 500,00 €." in saida
    assert f"Pedido registado com o número {registado.id}." in saida
    assert "Fica pendente até o marketeer dar o parecer e o administrador o decidir." in saida
    assert registado.budget_pedido_centimos == 200000
    assert registado.motivo == "Mais anúncios em vídeo"


def test_menu_so_mostra_as_campanhas_que_nao_terminaram(teclado, ligacao, contas, natal, capsys):
    carla = contas[modelos.CLIENTE]
    campanhas_bd.criar(
        ligacao, "Verão", "", carla.id, contas[modelos.MARKETEER].id, date(2026, 7, 1), date(2026, 8, 31), 50000
    )
    teclado("")

    menu.pedir_alteracao(ligacao, carla)

    saida = capsys.readouterr().out
    assert "Natal 2026" in saida
    assert "Verão" not in saida


def test_menu_sem_campanhas_por_terminar_avisa(teclado, ligacao, jose, capsys):
    teclado("")

    menu.pedir_alteracao(ligacao, jose)

    assert "Não tem campanhas a decorrer ou por começar." in capsys.readouterr().out


def test_menu_avisa_logo_quando_a_campanha_ja_tem_um_pedido(teclado, ligacao, contas, pedido, natal, capsys):
    teclado(str(natal.id), "")

    menu.pedir_alteracao(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert f"já tem um pedido de alteração de budget por decidir (n.º {pedido.id})" in saida
    assert "Budget pretendido" not in saida


def test_menu_mostra_o_erro_e_nao_regista_o_pedido(teclado, ligacao, contas, natal, capsys):
    carla = contas[modelos.CLIENTE]
    teclado(str(natal.id), "1500", "Igual", "")

    menu.pedir_alteracao(ligacao, carla)

    assert "O valor pedido é igual ao budget atual da campanha. O pedido não foi registado." in capsys.readouterr().out
    assert servico.listar_do_cliente(ligacao, carla) == []


def test_menu_nao_aceita_campanhas_de_outro_cliente(teclado, ligacao, jose, padaria, natal, capsys):
    teclado(str(natal.id), "")

    menu.pedir_alteracao(ligacao, jose)

    assert f"Não tem nenhuma campanha com o número {natal.id}." in capsys.readouterr().out


def test_menu_mostra_os_detalhes_de_um_pedido_de_budget(teclado, ligacao, contas, pedido, capsys):
    teclado("5", str(pedido.id), "", "0")

    menu_pedidos.do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert f"Pedido de budget n.º {pedido.id}" in saida
    assert "  Campanha:     Natal 2026" in saida
    assert "  Feito em:     2026-11-18 10:00" in saida
    assert "  Budget de:    1 500,00 €" in saida
    assert "  Budget para:  2 000,00 €" in saida
    assert "  Motivo:       Mais anúncios em vídeo" in saida
    assert "  Estado:       Pendente" in saida
    assert "Rejeição:" not in saida


def test_detalhes_de_um_pedido_rejeitado_mostram_o_motivo(ligacao, natal, capsys):
    pedido = repositorio.criar(ligacao, natal.id, 150000, 200000, "Mais anúncios")
    ligacao.execute(
        "UPDATE pedidos_budget SET estado = 'rejeitado', motivo_rejeicao = 'Sem margem' WHERE id = ?", (pedido.id,)
    )

    menu.mostrar_detalhes(repositorio.obter_por_id(ligacao, pedido.id))

    assert "  Rejeição:     Sem margem" in capsys.readouterr().out


def test_menu_nao_mostra_pedidos_de_budget_de_outro(teclado, ligacao, pedido, jose, capsys):
    teclado(str(pedido.id), "")

    menu.ver_pedido(ligacao, jose)

    assert f"Não tem nenhum pedido de budget com o número {pedido.id}." in capsys.readouterr().out


def test_menu_cancela_um_pedido_de_budget(teclado, ligacao, contas, pedido, capsys):
    teclado("6", str(pedido.id), "s", "", "0")

    menu_pedidos.do_cliente(ligacao, contas[modelos.CLIENTE])

    assert "Pedido cancelado." in capsys.readouterr().out
    assert repositorio.obter_por_id(ligacao, pedido.id).estado == modelos.CANCELADO


def test_menu_nao_cancela_sem_confirmacao(teclado, ligacao, contas, pedido, capsys):
    teclado(str(pedido.id), "n", "")

    menu.cancelar_pedido(ligacao, contas[modelos.CLIENTE])

    assert "Nada foi alterado." in capsys.readouterr().out
    assert repositorio.obter_por_id(ligacao, pedido.id).estado == modelos.PENDENTE


def test_menu_nao_cancela_um_pedido_em_analise(teclado, ligacao, contas, pedido, capsys):
    repositorio.definir_estado(ligacao, pedido.id, modelos.EM_ANALISE)
    teclado(str(pedido.id), "")

    menu.cancelar_pedido(ligacao, contas[modelos.CLIENTE])

    assert "Só é possível cancelar um pedido pendente. Este pedido está no estado Em análise." in capsys.readouterr().out


def test_campanhas_do_cliente_explicam_como_pedir_outro_budget(teclado, ligacao, contas, natal, capsys):
    teclado("0")

    menu_campanhas.do_cliente(ligacao, contas[modelos.CLIENTE])

    assert 'Para pedir outro valor, use a opção "Pedidos de campanha".' in capsys.readouterr().out


# --- dados de demonstração ---------------------------------------------------


def test_dados_demo_criam_um_pedido_de_budget_pendente(ligacao):
    dados_demo.criar_contas(ligacao)
    dados_demo.criar_campanhas(ligacao)

    criados = dados_demo.criar_pedidos_budget(ligacao)

    assert criados == ["Reforçar os anúncios em vídeo na última semana antes do Natal"]
    carla = utilizadores.obter_por_email(ligacao, "cliente@empresa.pt")
    (pedido,) = servico.listar_do_cliente(ligacao, carla)
    assert pedido.campanha_nome == "Natal 2026"
    assert pedido.budget_atual_centimos == 150000
    assert pedido.budget_pedido_centimos == 200000
    assert pedido.estado == modelos.PENDENTE


def test_dados_demo_nao_repetem_pedidos_de_budget(ligacao):
    dados_demo.criar_contas(ligacao)
    dados_demo.criar_campanhas(ligacao)
    dados_demo.criar_pedidos_budget(ligacao)

    assert dados_demo.criar_pedidos_budget(ligacao) == []


def test_dados_demo_mostram_quantos_pedidos_de_budget_criaram(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))

    dados_demo.main()
    dados_demo.main()

    saida = capsys.readouterr().out
    assert "Pedidos de alteração de budget criados: 1 (os restantes já existiam)." in saida
    assert "Pedidos de alteração de budget criados: 0 (os restantes já existiam)." in saida
