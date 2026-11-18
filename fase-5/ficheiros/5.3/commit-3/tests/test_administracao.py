"""Testes das decisões do Administrador sobre pedidos e campanhas."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.cli import campanhas as menu_campanhas
from gestor_campanhas.cli import gestao as menu_gestao
from gestor_campanhas.cli import pedidos as menu_pedidos
from gestor_campanhas.cli import perfis
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import pedidos as pedidos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import campanhas, gestao, pedidos
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

    assert campanhas.definir_budget(ligacao, natal.id, "2000", "Mais anúncios").budget_centimos == 200000


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


# --- menu: pedidos -----------------------------------------------------------


def test_menu_avisa_quando_nao_ha_pedidos(teclado, ligacao, contas, capsys):
    teclado("0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Ainda não há pedidos de campanha." in capsys.readouterr().out


def test_menu_mostra_os_pedidos_de_todos_os_clientes(teclado, ligacao, contas, pedido, capsys):
    pedidos_bd.definir_estado(ligacao, pedido.id, modelos.CANCELADO)
    jose = utilizadores.criar(ligacao, "José Padeiro", "jose@padaria.pt", "x", modelos.CLIENTE)
    pedidos_bd.criar(ligacao, jose.id, "Divulgar o bolo-rei", 60000, date(2026, 12, 15), ["Facebook"])
    teclado("0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "N.º  Feito em    Cliente        Objetivo             Orçamento   Prazo       Estado" in saida
    assert "2026-11-16  José Padeiro   Divulgar o bolo-rei  600,00 €    2026-12-15  Pendente" in saida
    assert "2026-11-16  Carla Cliente  Vender mais          1 500,00 €  2026-12-20  Cancelado" in saida
    assert saida.index("José Padeiro") < saida.index("Carla Cliente")
    assert "2 pedidos, 1 por decidir." in saida


def test_menu_aprova_um_pedido(teclado, ligacao, contas, pedido, marta, capsys):
    teclado("1", str(pedido.id), "1", "Natal 2026", "", str(marta.id), "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    aprovado = pedidos.obter(ligacao, pedido.id)
    campanha = campanhas.obter(ligacao, aprovado.campanha_id)
    assert "  Cliente:      Carla Cliente" in saida
    assert "  Estado:       Em análise" in saida
    assert "Marta Marques     marta@agencia.pt" in saida
    assert f"Pedido aprovado. Foi criada a campanha n.º {campanha.id}." in saida
    assert "O cliente e o marketeer foram avisados por email." in saida
    assert campanha.nome == "Natal 2026"
    assert campanha.budget_centimos == 150000
    assert campanha.marketeer_id == marta.id


def test_menu_aprova_com_outro_budget(teclado, ligacao, contas, pedido, marta):
    teclado("1", str(pedido.id), "1", "Natal 2026", "900,50", str(marta.id), "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert campanhas.listar_todas(ligacao)[0].budget_centimos == 90050


def test_menu_nao_aprova_sem_marketeer(teclado, ligacao, contas, pedido, capsys):
    teclado("1", str(pedido.id), "1", "Natal 2026", "", "", "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "O pedido não foi aprovado." in capsys.readouterr().out
    assert pedidos.obter(ligacao, pedido.id).estado == modelos.EM_ANALISE
    assert campanhas.listar_todas(ligacao) == []


def test_menu_mostra_o_erro_da_aprovacao(teclado, ligacao, contas, pedido, capsys):
    teclado("1", str(pedido.id), "1", "Natal 2026", "", str(contas[modelos.CLIENTE].id), "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Não existe nenhum marketeer com o número" in capsys.readouterr().out
    assert campanhas.listar_todas(ligacao) == []


def test_menu_rejeita_um_pedido_com_motivo(teclado, ligacao, contas, pedido, emails, capsys):
    teclado("1", str(pedido.id), "2", "Orçamento insuficiente", "s", "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    rejeitado = pedidos.obter(ligacao, pedido.id)
    assert "Pedido rejeitado. O cliente foi avisado por email." in saida
    assert rejeitado.estado == modelos.REJEITADO
    assert rejeitado.motivo_rejeicao == "Orçamento insuficiente"
    assert len(emails()) == 1


def test_menu_nao_rejeita_sem_confirmacao(teclado, ligacao, contas, pedido, capsys):
    teclado("1", str(pedido.id), "2", "Motivo", "n", "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "O pedido não foi rejeitado." in capsys.readouterr().out
    assert pedidos.obter(ligacao, pedido.id).estado == modelos.EM_ANALISE


def test_menu_deixa_a_decisao_para_mais_tarde(teclado, ligacao, contas, pedido, capsys):
    teclado("1", str(pedido.id), "0", "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "O pedido fica em análise." in capsys.readouterr().out
    assert pedidos.obter(ligacao, pedido.id).estado == modelos.EM_ANALISE


def test_menu_nao_deixa_decidir_um_pedido_ja_decidido(teclado, ligacao, contas, pedido, capsys):
    pedidos_bd.definir_estado(ligacao, pedido.id, modelos.REJEITADO, "Sem verba")
    teclado("1", str(pedido.id), "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "  Motivo:       Sem verba" in saida
    assert "Este pedido já não pode ser decidido." in saida
    assert "Aprovar e criar a campanha" not in saida


def test_menu_avisa_quando_o_pedido_nao_existe(teclado, ligacao, contas, capsys):
    teclado("1", "999", "", "0")

    menu_pedidos.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Não existe nenhum pedido com o número 999." in capsys.readouterr().out


def test_opcoes_novas_estao_no_menu_do_administrador():
    descricoes = [descricao for descricao, _ in perfis.OPCOES[modelos.ADMINISTRADOR]]

    assert "Pedidos de campanha" in descricoes
    assert "Pedidos de campanha" not in [descricao for descricao, _ in perfis.OPCOES[modelos.MARKETEER]]


# --- menu: campanhas ---------------------------------------------------------


def test_menu_avisa_quando_nao_ha_campanhas(teclado, ligacao, contas, capsys):
    teclado("0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Ainda não há campanhas." in saida
    assert "1. Definir budget" in saida
    assert "2. Atribuir marketeer" in saida


def test_menu_mostra_as_campanhas_de_todos_os_marketeers(teclado, ligacao, contas, natal, marta, capsys):
    campanhas_bd.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, marta.id, budget_centimos=80000)
    teclado("0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "N.º  Nome    Cliente        Marketeer         Início      Fim         Budget       Estado" in saida
    assert "Natal   Carla Cliente  Miguel Marketeer  2026-12-01  2026-12-24  Por definir  Por começar" in saida
    assert "Saldos  Carla Cliente  Marta Marques     -           -           800,00 €     Em curso" in saida
    assert "2 campanhas." in saida


def test_menu_define_o_budget(teclado, ligacao, contas, natal, capsys):
    teclado("1", str(natal.id), "1500,50", "", "0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Campanha Natal, de Carla Cliente. Budget atual: Por definir." in saida
    assert "Budget definido: 1 500,50 €." in saida
    assert campanhas.obter(ligacao, natal.id).budget_centimos == 150050


def test_menu_mostra_o_erro_do_budget(teclado, ligacao, contas, natal, capsys):
    teclado("1", str(natal.id), "zero", "", "0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "O valor não é válido. Exemplos de valores válidos: 1500 ou 1500,50. O budget não foi alterado." in (
        capsys.readouterr().out
    )
    assert campanhas.obter(ligacao, natal.id).budget_centimos is None


def test_menu_atribui_a_campanha_a_outro_marketeer(teclado, ligacao, contas, natal, marta, capsys):
    teclado("2", str(natal.id), str(marta.id), "", "0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Campanha Natal, de Carla Cliente. Responsável atual: Miguel Marketeer." in saida
    assert "A campanha passou para Marta Marques. Foi enviado um aviso por email." in saida
    assert campanhas.obter(ligacao, natal.id).marketeer_id == marta.id


def test_menu_mostra_o_erro_da_atribuicao(teclado, ligacao, contas, natal, capsys):
    teclado("2", str(natal.id), str(contas[modelos.MARKETEER].id), "", "0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Miguel Marketeer já é responsável por esta campanha. O responsável não foi alterado." in (
        capsys.readouterr().out
    )


def test_menu_avisa_quando_a_campanha_nao_existe(teclado, ligacao, contas, capsys):
    teclado("1", "999", "", "2", "", "0")

    menu_campanhas.do_administrador(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Não existe nenhuma campanha com o número 999." in capsys.readouterr().out


def test_opcao_campanhas_do_administrador_abre_o_menu_certo():
    opcoes = dict(perfis.OPCOES[modelos.ADMINISTRADOR])

    assert opcoes["Campanhas"] is menu_campanhas.do_administrador
    assert dict(perfis.OPCOES[modelos.MARKETEER])["Campanhas"] is menu_campanhas.do_marketeer


# --- campanhas ativas de cada conta ------------------------------------------


@pytest.fixture
def varias(ligacao, contas, natal, marta):
    """Além da ``natal`` (por começar), uma campanha em curso e outra terminada."""
    carla, miguel = contas[modelos.CLIENTE], contas[modelos.MARKETEER]
    jose = utilizadores.criar(ligacao, "José Padeiro", "jose@padaria.pt", "x", modelos.CLIENTE)
    campanhas_bd.criar(ligacao, "Saldos", "", carla.id, marta.id)
    campanhas_bd.criar(ligacao, "Verão", "", jose.id, miguel.id, None, date(2026, 8, 31))
    return jose


def test_campanha_so_esta_terminada_depois_da_data_de_fim(natal):
    assert not natal.terminada(date(2026, 12, 24))
    assert natal.terminada(date(2026, 12, 25))
    natal.data_fim = None
    assert not natal.terminada(date(2030, 1, 1))


def test_conta_as_campanhas_ativas_por_cliente_e_por_marketeer(ligacao, contas, varias, marta):
    carla, miguel = contas[modelos.CLIENTE], contas[modelos.MARKETEER]

    assert campanhas.contar_ativas(ligacao, modelos.CLIENTE) == {carla.id: 2}
    assert campanhas.contar_ativas(ligacao, modelos.MARKETEER) == {miguel.id: 1, marta.id: 1}


def test_lista_de_clientes_mostra_as_campanhas_ativas(teclado, ligacao, contas, varias, capsys):
    teclado("0")

    menu_gestao.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Email             Telefone  Estado  Campanhas ativas" in saida
    assert "carla@empresa.pt            Ativa   2" in saida
    assert "jose@padaria.pt             Ativa   0" in saida


def test_lista_de_marketeers_mostra_as_campanhas_ativas(teclado, ligacao, contas, varias, capsys):
    teclado("0")

    menu_gestao.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "marta@agencia.pt             Ativa   1" in saida
    assert "miguel@agencia.pt            Ativa   1" in saida


# --- desativar um marketeer com campanhas ------------------------------------


def test_marketeer_com_campanhas_por_terminar_nao_pode_ser_desativado(ligacao, contas, natal, emails):
    miguel = contas[modelos.MARKETEER]

    with pytest.raises(ErroValidacao, match="Miguel Marketeer é responsável por 1 campanha que ainda não terminou"):
        gestao.definir_estado(ligacao, modelos.MARKETEER, miguel.id, False)

    assert utilizadores.obter_por_id(ligacao, miguel.id).ativo
    assert emails() == []


def test_mensagem_diz_quantas_campanhas_faltam_reatribuir(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    campanhas_bd.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, miguel.id)

    with pytest.raises(ErroValidacao, match="por 2 campanhas que ainda não terminaram. Atribua-as a outro marketeer"):
        gestao.definir_estado(ligacao, modelos.MARKETEER, miguel.id, False)


def test_marketeer_pode_ser_desativado_depois_de_reatribuir_as_campanhas(ligacao, contas, natal, marta):
    miguel = contas[modelos.MARKETEER]
    campanhas.atribuir_marketeer(ligacao, natal.id, marta.id)

    assert not gestao.definir_estado(ligacao, modelos.MARKETEER, miguel.id, False).ativo


def test_campanhas_terminadas_nao_impedem_a_desativacao(ligacao, contas):
    miguel = contas[modelos.MARKETEER]
    campanhas_bd.criar(ligacao, "Verão", "", contas[modelos.CLIENTE].id, miguel.id, None, date(2026, 8, 31))

    assert not gestao.definir_estado(ligacao, modelos.MARKETEER, miguel.id, False).ativo


def test_cliente_com_campanhas_pode_ser_desativado(ligacao, contas, natal):
    assert not gestao.definir_estado(ligacao, modelos.CLIENTE, contas[modelos.CLIENTE].id, False).ativo


def test_menu_explica_porque_nao_desativa_o_marketeer(teclado, ligacao, contas, natal, capsys):
    miguel = contas[modelos.MARKETEER]
    teclado("4", str(miguel.id), "s", "", "0")

    menu_gestao.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Atribua-as a outro marketeer antes de desativar a conta. Nada foi alterado." in saida
    assert "Conta desativada." not in saida
    assert utilizadores.obter_por_id(ligacao, miguel.id).ativo
