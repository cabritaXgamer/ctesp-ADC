"""Testes dos comentários dos criativos."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import comentarios as repositorio
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import comentarios as servico
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def dia_19_de_novembro(monkeypatch):
    """Fixa a data e a hora atuais em 19 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 19, 10, 0))


@pytest.fixture
def natal(ligacao, contas):
    """Campanha da Carla, do Miguel, com um budget de 1500 €."""
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
def banner(ligacao, natal):
    """Criativo da campanha Natal 2026, em preparação."""
    return criativos_bd.criar(ligacao, natal.id, "Banner de Natal", "Árvore com os produtos", 40000)


@pytest.fixture
def jose(ligacao, contas):
    """Um segundo cliente, além da ``Carla Cliente`` da fixture ``contas``."""
    return utilizadores.criar(
        ligacao, "José Padeiro", "jose@padaria.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.CLIENTE
    )


@pytest.fixture
def marta(ligacao):
    """Uma segunda marketeer, sem campanhas."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_um_comentario(ligacao, contas, banner):
    comentario = repositorio.criar(ligacao, banner.id, contas[modelos.CLIENTE].id, "O logótipo devia ser maior")

    assert comentario == repositorio.obter_por_id(ligacao, comentario.id)
    assert comentario.criativo_id == banner.id
    assert comentario.autor_id == contas[modelos.CLIENTE].id
    assert comentario.autor_nome == "Carla Cliente"
    assert comentario.autor_perfil == modelos.CLIENTE
    assert comentario.texto == "O logótipo devia ser maior"
    assert comentario.criado_em == datetime(2026, 11, 19, 10, 0)
    assert comentario.resposta_a is None


def test_repositorio_guarda_uma_resposta(ligacao, contas, banner):
    comentario = repositorio.criar(ligacao, banner.id, contas[modelos.CLIENTE].id, "O logótipo devia ser maior")

    resposta = repositorio.criar(ligacao, banner.id, contas[modelos.MARKETEER].id, "Vou aumentá-lo", comentario.id)

    assert resposta.resposta_a == comentario.id
    assert resposta.autor_nome == "Miguel Marketeer"
    assert resposta.autor_perfil == modelos.MARKETEER


def test_repositorio_devolve_none_quando_o_comentario_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_os_comentarios_de_um_criativo_por_ordem(ligacao, contas, natal, banner):
    video = criativos_bd.criar(ligacao, natal.id, "Vídeo da montra", "")
    cliente = contas[modelos.CLIENTE].id
    primeiro = repositorio.criar(ligacao, banner.id, cliente, "Primeiro")
    repositorio.criar(ligacao, video.id, cliente, "Sobre o vídeo")
    segundo = repositorio.criar(ligacao, banner.id, cliente, "Segundo")

    lista = repositorio.listar_por_criativo(ligacao, banner.id)

    assert [comentario.id for comentario in lista] == [primeiro.id, segundo.id]


# --- regras ------------------------------------------------------------------


def test_cliente_comenta_um_criativo(ligacao, contas, banner):
    comentario = servico.comentar(ligacao, contas[modelos.CLIENTE], banner.id, "  O logótipo devia ser maior  ")

    assert comentario.texto == "O logótipo devia ser maior"
    assert comentario.autor_id == contas[modelos.CLIENTE].id
    assert comentario.resposta_a is None


@pytest.mark.parametrize("estado", list(modelos.NOMES_ESTADOS_CRIATIVO))
def test_cliente_comenta_um_criativo_em_qualquer_estado(ligacao, contas, banner, estado):
    criativos_bd.definir_estado(ligacao, banner.id, estado)

    servico.comentar(ligacao, contas[modelos.CLIENTE], banner.id, "Gosto muito")

    assert len(repositorio.listar_por_criativo(ligacao, banner.id)) == 1


def test_comentario_vazio_nao_e_guardado(ligacao, contas, banner):
    with pytest.raises(ErroValidacao, match="O texto não pode ficar vazio."):
        servico.comentar(ligacao, contas[modelos.CLIENTE], banner.id, "   ")

    assert repositorio.listar_por_criativo(ligacao, banner.id) == []


def test_cliente_so_comenta_os_criativos_das_suas_campanhas(ligacao, banner, jose):
    with pytest.raises(ErroValidacao, match=f"Não tem nenhum criativo com o número {banner.id}."):
        servico.comentar(ligacao, jose, banner.id, "Não é meu")


@pytest.fixture
def comentario(ligacao, contas, banner):
    """Comentário da Carla sobre o Banner de Natal, ainda sem resposta."""
    return servico.comentar(ligacao, contas[modelos.CLIENTE], banner.id, "O logótipo devia ser maior")


def test_marketeer_responde_a_um_comentario(ligacao, contas, banner, comentario):
    resposta = servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "Vou aumentá-lo")

    assert resposta.resposta_a == comentario.id
    assert resposta.criativo_id == banner.id
    assert resposta.autor_id == contas[modelos.MARKETEER].id
    assert resposta.texto == "Vou aumentá-lo"


def test_um_comentario_pode_ter_varias_respostas(ligacao, contas, comentario):
    servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "Vou aumentá-lo")
    servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "Já está maior")

    assert len(repositorio.listar_por_criativo(ligacao, comentario.criativo_id)) == 3


def test_resposta_vazia_nao_e_guardada(ligacao, contas, comentario):
    with pytest.raises(ErroValidacao, match="O texto não pode ficar vazio."):
        servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "")


def test_nao_se_responde_a_uma_resposta(ligacao, contas, comentario):
    resposta = servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "Vou aumentá-lo")

    with pytest.raises(ErroValidacao, match="Só se pode responder a um comentário do cliente"):
        servico.responder(ligacao, contas[modelos.MARKETEER], resposta.id, "Outra vez")


def test_marketeer_so_responde_nos_criativos_das_suas_campanhas(ligacao, comentario, marta):
    with pytest.raises(ErroValidacao, match=f"Não há nenhum comentário com o número {comentario.id} nos seus criativos."):
        servico.responder(ligacao, marta, comentario.id, "Não é meu")


def test_marketeer_nao_responde_a_um_comentario_que_nao_existe(ligacao, contas):
    with pytest.raises(ErroValidacao, match="Não há nenhum comentário com o número 999"):
        servico.responder(ligacao, contas[modelos.MARKETEER], 999, "Olá")


def test_conversa_junta_cada_comentario_as_suas_respostas(ligacao, contas, banner, comentario):
    cliente, marketeer = contas[modelos.CLIENTE], contas[modelos.MARKETEER]
    segundo = servico.comentar(ligacao, cliente, banner.id, "Mudem a cor do fundo")
    resposta = servico.responder(ligacao, marketeer, comentario.id, "Vou aumentá-lo")

    resultado = servico.conversa(ligacao, banner)

    assert resultado == [(comentario, [resposta]), (segundo, [])]


def test_conversa_de_um_criativo_sem_comentarios(ligacao, banner):
    assert servico.conversa(ligacao, banner) == []


def test_conta_os_comentarios_por_responder_de_cada_criativo(ligacao, contas, natal, banner, comentario):
    cliente, marketeer = contas[modelos.CLIENTE], contas[modelos.MARKETEER]
    video = criativos_bd.criar(ligacao, natal.id, "Vídeo da montra", "")
    servico.comentar(ligacao, cliente, banner.id, "Mudem a cor do fundo")
    respondido = servico.comentar(ligacao, cliente, video.id, "Está ótimo")
    servico.responder(ligacao, marketeer, respondido.id, "Obrigado")

    assert servico.por_responder(ligacao, natal) == {banner.id: 2}
