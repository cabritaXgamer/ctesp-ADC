"""Testes das notificações."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import notificacoes as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import budget as servico_budget
from gestor_campanhas.servicos import campanhas as servico_campanhas
from gestor_campanhas.servicos import comentarios as servico_comentarios
from gestor_campanhas.servicos import criativos as servico_criativos
from gestor_campanhas.servicos import notificacoes as servico
from gestor_campanhas.servicos import pedidos as servico_pedidos
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
def marketeer(contas):
    """O marketeer Miguel, da fixture ``contas``."""
    return contas[modelos.MARKETEER]


@pytest.fixture
def natal(ligacao, cliente, marketeer):
    """Campanha da Carla, do Miguel, com um budget de 1500 €."""
    return campanhas_bd.criar(
        ligacao, "Natal 2026", "Vender mais", cliente.id, marketeer.id, date(2026, 12, 1), date(2026, 12, 24), 150000
    )


@pytest.fixture
def banner(ligacao, natal):
    """Criativo da campanha Natal 2026, em preparação."""
    return criativos_bd.criar(ligacao, natal.id, "Banner de Natal", "Árvore com os produtos", 40000)


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_uma_notificacao(ligacao, cliente):
    notificacao = repositorio.criar(ligacao, cliente.id, "Foi criado o criativo Banner", modelos.SOBRE_CRIATIVO, 3)

    assert notificacao == repositorio.obter_por_id(ligacao, notificacao.id)
    assert notificacao.utilizador_id == cliente.id
    assert notificacao.texto == "Foi criado o criativo Banner"
    assert notificacao.sobre == modelos.SOBRE_CRIATIVO
    assert notificacao.item_id == 3
    assert notificacao.criada_em == datetime(2026, 11, 19, 10, 0)
    assert notificacao.lida is False


@pytest.mark.parametrize(
    ("sobre", "nome"),
    [
        (modelos.SOBRE_CAMPANHA, "Campanha n.º 7"),
        (modelos.SOBRE_PEDIDO_BUDGET, "Pedido de budget n.º 7"),
        (modelos.SOBRE_CRIATIVO, "Criativo n.º 7"),
    ],
)
def test_nome_do_item_da_notificacao(ligacao, cliente, sobre, nome):
    assert repositorio.criar(ligacao, cliente.id, "Texto", sobre, 7).nome_item == nome


def test_repositorio_devolve_none_quando_a_notificacao_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_as_notificacoes_da_mais_recente_para_a_mais_antiga(ligacao, cliente, marketeer):
    primeira = repositorio.criar(ligacao, cliente.id, "Primeira", modelos.SOBRE_CRIATIVO, 1)
    repositorio.criar(ligacao, marketeer.id, "De outro", modelos.SOBRE_CRIATIVO, 1)
    segunda = repositorio.criar(ligacao, cliente.id, "Segunda", modelos.SOBRE_CRIATIVO, 2)

    lista = repositorio.listar_por_utilizador(ligacao, cliente.id)

    assert [notificacao.id for notificacao in lista] == [segunda.id, primeira.id]


def test_repositorio_conta_e_marca_as_notificacoes_por_ler(ligacao, cliente, marketeer):
    primeira = repositorio.criar(ligacao, cliente.id, "Primeira", modelos.SOBRE_CRIATIVO, 1)
    repositorio.criar(ligacao, cliente.id, "Segunda", modelos.SOBRE_CRIATIVO, 2)
    repositorio.criar(ligacao, cliente.id, "Terceira", modelos.SOBRE_CRIATIVO, 3)
    repositorio.criar(ligacao, marketeer.id, "De outro", modelos.SOBRE_CRIATIVO, 1)

    assert repositorio.marcar_como_lida(ligacao, primeira.id).lida is True
    assert repositorio.contar_por_ler(ligacao, cliente.id) == 2
    assert repositorio.marcar_todas_como_lidas(ligacao, cliente.id) == 2
    assert repositorio.contar_por_ler(ligacao, cliente.id) == 0
    assert repositorio.contar_por_ler(ligacao, marketeer.id) == 1


# --- regras ------------------------------------------------------------------


def test_notificar_guarda_a_notificacao_e_envia_um_email(ligacao, cliente, emails):
    notificacao = servico.notificar(
        ligacao, cliente, "Novo criativo", "Foi criado o criativo Banner de Natal.", modelos.SOBRE_CRIATIVO, 3
    )

    assert servico.listar(ligacao, cliente) == [notificacao]
    (email,) = emails()
    assert "Para: carla@empresa.pt" in email
    assert "Assunto: Novo criativo" in email
    assert (
        "Olá, Carla Cliente.\n\nFoi criado o criativo Banner de Natal.\n"
        'Pode consultá-lo na opção "Criativos" do seu menu.\n'
    ) in email


@pytest.mark.parametrize(
    ("sobre", "perfil", "onde"),
    [
        (modelos.SOBRE_CAMPANHA, modelos.MARKETEER, '"Campanhas"'),
        (modelos.SOBRE_PEDIDO_BUDGET, modelos.MARKETEER, 'Pode dar o parecer na opção "Pedidos de budget"'),
        (modelos.SOBRE_PEDIDO_BUDGET, modelos.CLIENTE, '"Pedidos de campanha"'),
        (modelos.SOBRE_CRIATIVO, modelos.MARKETEER, '"Criativos"'),
    ],
)
def test_email_diz_onde_encontrar_o_item(ligacao, contas, emails, sobre, perfil, onde):
    servico.notificar(ligacao, contas[perfil], "Aviso", "Aconteceu algo.", sobre, 1)

    assert onde in emails()[0]


def test_contar_por_ler(ligacao, cliente, marketeer):
    servico.notificar(ligacao, cliente, "A", "Um.", modelos.SOBRE_CRIATIVO, 1)
    servico.notificar(ligacao, cliente, "B", "Dois.", modelos.SOBRE_CRIATIVO, 2)
    servico.notificar(ligacao, marketeer, "C", "Três.", modelos.SOBRE_CRIATIVO, 3)

    assert servico.contar_por_ler(ligacao, cliente) == 2
    assert servico.contar_por_ler(ligacao, marketeer) == 1


def test_abrir_marca_a_notificacao_como_lida(ligacao, cliente):
    notificacao = servico.notificar(ligacao, cliente, "A", "Um.", modelos.SOBRE_CRIATIVO, 1)

    aberta = servico.abrir(ligacao, cliente, notificacao.id)

    assert aberta.lida is True
    assert servico.contar_por_ler(ligacao, cliente) == 0
    assert servico.abrir(ligacao, cliente, notificacao.id).lida is True


def test_nao_se_abre_a_notificacao_de_outro(ligacao, cliente, jose):
    notificacao = servico.notificar(ligacao, cliente, "A", "Um.", modelos.SOBRE_CRIATIVO, 1)

    with pytest.raises(ErroValidacao, match=f"Não tem nenhuma notificação com o número {notificacao.id}."):
        servico.abrir(ligacao, jose, notificacao.id)

    assert servico.contar_por_ler(ligacao, cliente) == 1


def test_marcar_todas_como_lidas(ligacao, cliente, marketeer):
    servico.notificar(ligacao, cliente, "A", "Um.", modelos.SOBRE_CRIATIVO, 1)
    servico.notificar(ligacao, cliente, "B", "Dois.", modelos.SOBRE_CRIATIVO, 2)
    servico.notificar(ligacao, marketeer, "C", "Três.", modelos.SOBRE_CRIATIVO, 3)

    assert servico.marcar_todas_como_lidas(ligacao, cliente) == 2
    assert servico.contar_por_ler(ligacao, cliente) == 0
    assert servico.contar_por_ler(ligacao, marketeer) == 1


# --- quem é notificado, e de quê ---------------------------------------------


def _unica(ligacao, utilizador):
    """Devolve a única notificação de um utilizador (falha se houver outro número)."""
    (notificacao,) = servico.listar(ligacao, utilizador)
    return notificacao


@pytest.fixture
def marta(ligacao):
    """Uma segunda marketeer, sem campanhas."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


def test_marketeer_e_notificado_quando_recebe_uma_campanha(ligacao, natal, marta, emails):
    servico_campanhas.atribuir_marketeer(ligacao, natal.id, marta.id)

    notificacao = _unica(ligacao, marta)
    assert notificacao.texto == "Passou a ser responsável pela campanha Natal 2026, do cliente Carla Cliente."
    assert (notificacao.sobre, notificacao.item_id) == (modelos.SOBRE_CAMPANHA, natal.id)
    (email,) = emails()
    assert "Assunto: Foi-lhe atribuída uma campanha" in email


def test_marketeer_e_notificado_da_campanha_de_um_pedido_aprovado(ligacao, cliente, marketeer):
    pedido = servico_pedidos.criar(ligacao, cliente, "Vender bolo-rei", "600", "2026-12-15", ["Facebook"])

    aprovado = servico_pedidos.aprovar(ligacao, pedido.id, "Bolo-rei", "600", marketeer.id)

    notificacao = _unica(ligacao, marketeer)
    assert notificacao.texto == "Passou a ser responsável pela campanha Bolo-rei, do cliente Carla Cliente."
    assert notificacao.item_id == aprovado.campanha_id


def test_marketeer_e_notificado_de_um_pedido_de_budget(ligacao, cliente, marketeer, natal):
    pedido = servico_budget.pedir(ligacao, cliente, natal.id, "2000", "Mais vídeos")

    notificacao = _unica(ligacao, marketeer)
    assert notificacao.texto == (
        f"Carla Cliente pediu para alterar o budget da campanha Natal 2026 de 1 500,00 € para 2 000,00 € "
        f"(pedido n.º {pedido.id})."
    )
    assert (notificacao.sobre, notificacao.item_id) == (modelos.SOBRE_PEDIDO_BUDGET, pedido.id)
    assert servico.listar(ligacao, cliente) == []


def test_pedido_de_budget_de_uma_campanha_sem_budget_diz_por_definir(ligacao, cliente, marketeer):
    campanha = campanhas_bd.criar(ligacao, "Sem budget", "", cliente.id, marketeer.id)

    servico_budget.pedir(ligacao, cliente, campanha.id, "900", "Começar")

    assert "de Por definir para 900,00 €" in _unica(ligacao, marketeer).texto


@pytest.fixture
def pedido_com_parecer(ligacao, cliente, marketeer, natal):
    """Pedido de budget da Carla (1500 € para 2000 €), já com parecer viável."""
    pedido = servico_budget.pedir(ligacao, cliente, natal.id, "2000", "Mais vídeos")
    servico_budget.dar_parecer(ligacao, marketeer, pedido.id, True, "Faz sentido")
    return pedido


def test_cliente_e_notificado_da_aprovacao_do_pedido_de_budget(ligacao, cliente, pedido_com_parecer):
    servico_budget.aprovar(ligacao, pedido_com_parecer.id)

    notificacao = _unica(ligacao, cliente)
    assert notificacao.texto == (
        f"O seu pedido de budget n.º {pedido_com_parecer.id} foi aprovado. "
        "O budget da campanha Natal 2026 passou a 2 000,00 €."
    )
    assert (notificacao.sobre, notificacao.item_id) == (modelos.SOBRE_PEDIDO_BUDGET, pedido_com_parecer.id)


def test_cliente_e_notificado_da_rejeicao_do_pedido_de_budget(ligacao, cliente, pedido_com_parecer):
    servico_budget.rejeitar(ligacao, pedido_com_parecer.id, "Sem orçamento este mês")

    assert _unica(ligacao, cliente).texto == (
        f"O seu pedido de budget n.º {pedido_com_parecer.id}, para a campanha Natal 2026, foi rejeitado. "
        "Motivo: Sem orçamento este mês"
    )


def test_pedido_de_budget_que_nao_pode_ser_decidido_nao_notifica_o_cliente(ligacao, cliente, marketeer, natal):
    pedido = servico_budget.pedir(ligacao, cliente, natal.id, "2000", "Mais vídeos")

    with pytest.raises(ErroValidacao):
        servico_budget.aprovar(ligacao, pedido.id)

    assert servico.listar(ligacao, cliente) == []


def test_cliente_e_notificado_quando_um_criativo_e_criado(ligacao, cliente, marketeer, natal):
    criativo = servico_criativos.criar(ligacao, marketeer, natal.id, "Banner de Natal")

    notificacao = _unica(ligacao, cliente)
    assert notificacao.texto == "Foi criado o criativo Banner de Natal, da campanha Natal 2026."
    assert (notificacao.sobre, notificacao.item_id) == (modelos.SOBRE_CRIATIVO, criativo.id)
    assert servico.listar(ligacao, marketeer) == []


def test_cliente_e_notificado_quando_um_criativo_e_alterado(ligacao, cliente, marketeer, banner):
    servico_criativos.editar(ligacao, marketeer, banner.id, "Banner grande")

    assert _unica(ligacao, cliente).texto == "O criativo Banner grande, da campanha Natal 2026, foi alterado."


def test_cliente_e_notificado_quando_um_criativo_vai_para_revisao(ligacao, cliente, marketeer, banner):
    servico_criativos.mudar_estado(ligacao, marketeer, banner.id, modelos.EM_REVISAO)

    assert _unica(ligacao, cliente).texto == (
        "O criativo Banner de Natal, da campanha Natal 2026, passou a Em revisão e está à espera da sua aprovação."
    )


def test_cliente_e_notificado_das_outras_mudancas_de_estado(ligacao, cliente, marketeer, banner):
    criativos_bd.definir_estado(ligacao, banner.id, modelos.APROVADO)

    servico_criativos.mudar_estado(ligacao, marketeer, banner.id, modelos.PUBLICADO)

    assert _unica(ligacao, cliente).texto == "O criativo Banner de Natal, da campanha Natal 2026, passou a Publicado."


def test_cliente_e_notificado_quando_e_anexado_um_ficheiro(ligacao, cliente, marketeer, banner, tmp_path):
    origem = tmp_path / "banner.png"
    origem.write_bytes(b"imagem")

    servico_criativos.anexar(ligacao, marketeer, banner.id, str(origem))

    assert _unica(ligacao, cliente).texto == (
        "Foi anexado o ficheiro banner.png ao criativo Banner de Natal, da campanha Natal 2026."
    )


def test_criativo_eliminado_notifica_sobre_a_campanha(ligacao, cliente, marketeer, natal, banner):
    servico_criativos.eliminar(ligacao, marketeer, banner.id)

    notificacao = _unica(ligacao, cliente)
    assert notificacao.texto == "O criativo Banner de Natal, da campanha Natal 2026, foi eliminado."
    assert (notificacao.sobre, notificacao.item_id) == (modelos.SOBRE_CAMPANHA, natal.id)


def test_criativo_invalido_nao_notifica_ninguem(ligacao, cliente, marketeer, natal):
    with pytest.raises(ErroValidacao):
        servico_criativos.criar(ligacao, marketeer, natal.id, "")

    assert servico.listar(ligacao, cliente) == []


def test_marketeer_e_notificado_de_um_comentario(ligacao, cliente, marketeer, banner):
    servico_comentarios.comentar(ligacao, cliente, banner.id, "O logótipo devia ser maior")

    notificacao = _unica(ligacao, marketeer)
    assert notificacao.texto == (
        "Carla Cliente comentou o criativo Banner de Natal, da campanha Natal 2026: O logótipo devia ser maior"
    )
    assert (notificacao.sobre, notificacao.item_id) == (modelos.SOBRE_CRIATIVO, banner.id)


def test_cliente_e_notificado_da_resposta_ao_comentario(ligacao, cliente, marketeer, banner):
    comentario = servico_comentarios.comentar(ligacao, cliente, banner.id, "O logótipo devia ser maior")

    servico_comentarios.responder(ligacao, marketeer, comentario.id, "Vou aumentá-lo")

    notificacao = _unica(ligacao, cliente)
    assert notificacao.texto == (
        "Miguel Marketeer respondeu ao seu comentário sobre o criativo Banner de Natal: Vou aumentá-lo"
    )
    assert (notificacao.sobre, notificacao.item_id) == (modelos.SOBRE_CRIATIVO, banner.id)
