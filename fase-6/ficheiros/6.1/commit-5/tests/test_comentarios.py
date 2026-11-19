"""Testes dos comentários dos criativos."""

from datetime import date, datetime

import pytest

from gestor_campanhas import config, dados_demo, modelos, relogio, seguranca
from gestor_campanhas.cli import criativos as menu
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


# --- menus -------------------------------------------------------------------


def test_detalhe_do_marketeer_sem_comentarios(teclado, ligacao, contas, natal, banner, capsys):
    teclado(str(banner.id), "")

    menu.ver(ligacao, contas[modelos.MARKETEER], natal)

    assert "Comentários: nenhum." in capsys.readouterr().out


def test_detalhe_do_marketeer_mostra_os_comentarios_e_as_respostas(
    teclado, ligacao, contas, natal, banner, comentario, capsys
):
    resposta = servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "Vou aumentá-lo")
    segundo = servico.comentar(ligacao, contas[modelos.CLIENTE], banner.id, "Mudem a cor do fundo")
    teclado(str(banner.id), "")

    menu.ver(ligacao, contas[modelos.MARKETEER], natal)

    saida = capsys.readouterr().out
    assert (
        "Comentários\n"
        f"  N.º {comentario.id}, de Carla Cliente, em 2026-11-19 10:00:\n"
        "    O logótipo devia ser maior\n"
        "    Resposta de Miguel Marketeer, em 2026-11-19 10:00:\n"
        "      Vou aumentá-lo\n"
        f"  N.º {segundo.id}, de Carla Cliente, em 2026-11-19 10:00:\n"
        "    Mudem a cor do fundo\n"
        "    (ainda sem resposta)\n"
    ) in saida
    assert resposta.id != segundo.id


def test_detalhe_do_cliente_mostra_os_comentarios(teclado, ligacao, contas, banner, comentario, capsys):
    teclado(str(banner.id), "")

    menu.ver_do_cliente(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert f"N.º {comentario.id}, de Carla Cliente, em 2026-11-19 10:00:" in saida
    assert "(ainda sem resposta)" in saida


def test_menu_do_cliente_guarda_um_comentario(teclado, ligacao, contas, banner, capsys):
    teclado(str(banner.id), "Mudem a cor do fundo", "")

    menu.comentar(ligacao, contas[modelos.CLIENTE])

    saida = capsys.readouterr().out
    assert "Criativo Banner de Natal, da campanha Natal 2026. Estado: Em preparação." in saida
    assert "Comentários: nenhum." in saida
    assert "Comentário guardado. O marketeer vai vê-lo no detalhe do criativo." in saida
    assert [comentario.texto for comentario in repositorio.listar_por_criativo(ligacao, banner.id)] == [
        "Mudem a cor do fundo"
    ]


def test_menu_do_cliente_cancela_o_comentario_com_enter(teclado, ligacao, contas, banner, capsys):
    teclado(str(banner.id), "")

    menu.comentar(ligacao, contas[modelos.CLIENTE])

    assert repositorio.listar_por_criativo(ligacao, banner.id) == []


def test_menu_do_cliente_nao_comenta_criativos_de_outro(teclado, ligacao, banner, jose, capsys):
    teclado(str(banner.id), "")

    menu.comentar(ligacao, jose)

    assert f"Não tem nenhum criativo com o número {banner.id}." in capsys.readouterr().out
    assert repositorio.listar_por_criativo(ligacao, banner.id) == []


def test_menu_do_marketeer_guarda_a_resposta(teclado, ligacao, contas, natal, banner, comentario, capsys):
    teclado(str(banner.id), str(comentario.id), "Vou aumentá-lo", "")

    menu.responder(ligacao, contas[modelos.MARKETEER], natal)

    saida = capsys.readouterr().out
    assert "Criativo Banner de Natal" in saida
    assert "(ainda sem resposta)" in saida
    assert "Resposta guardada. O cliente vai vê-la no detalhe do criativo." in saida
    respostas = servico.conversa(ligacao, banner)[0][1]
    assert [resposta.texto for resposta in respostas] == ["Vou aumentá-lo"]


def test_menu_do_marketeer_avisa_quando_nao_ha_comentarios(teclado, ligacao, contas, natal, banner, capsys):
    teclado(str(banner.id), "")

    menu.responder(ligacao, contas[modelos.MARKETEER], natal)

    assert "O criativo Banner de Natal ainda não tem comentários do cliente." in capsys.readouterr().out


def test_menu_do_marketeer_so_responde_a_comentarios_do_criativo(
    teclado, ligacao, contas, natal, banner, comentario, capsys
):
    resposta = servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "Vou aumentá-lo")
    teclado(str(banner.id), str(resposta.id), "")

    menu.responder(ligacao, contas[modelos.MARKETEER], natal)

    saida = capsys.readouterr().out
    assert f"Este criativo não tem nenhum comentário do cliente com o número {resposta.id}." in saida
    assert len(repositorio.listar_por_criativo(ligacao, banner.id)) == 2


def test_lista_do_marketeer_avisa_dos_comentarios_por_responder(
    teclado, ligacao, contas, natal, banner, comentario, capsys
):
    teclado("0")

    menu.da_campanha(ligacao, contas[modelos.MARKETEER], natal)

    assert f"Há 1 comentário do cliente por responder (criativo n.º {banner.id})." in capsys.readouterr().out


def test_lista_do_marketeer_conta_os_comentarios_de_varios_criativos(
    teclado, ligacao, contas, natal, banner, comentario, capsys
):
    video = criativos_bd.criar(ligacao, natal.id, "Vídeo da montra", "")
    servico.comentar(ligacao, contas[modelos.CLIENTE], video.id, "Está ótimo")
    teclado("0")

    menu.da_campanha(ligacao, contas[modelos.MARKETEER], natal)

    saida = capsys.readouterr().out
    assert f"Há 2 comentários do cliente por responder (criativos n.º {banner.id}, {video.id})." in saida


def test_lista_do_marketeer_sem_comentarios_por_responder_nao_avisa(
    teclado, ligacao, contas, natal, banner, comentario, capsys
):
    servico.responder(ligacao, contas[modelos.MARKETEER], comentario.id, "Vou aumentá-lo")
    teclado("0")

    menu.da_campanha(ligacao, contas[modelos.MARKETEER], natal)

    assert "por responder" not in capsys.readouterr().out


# --- dados de demonstração ---------------------------------------------------


def _demo_ate_aos_criativos(ligacao):
    dados_demo.criar_contas(ligacao)
    dados_demo.criar_campanhas(ligacao)
    dados_demo.criar_criativos(ligacao)


def test_dados_demo_criam_um_comentario_da_carla_ao_video(ligacao):
    _demo_ate_aos_criativos(ligacao)

    criados = dados_demo.criar_comentarios(ligacao)

    assert criados == ["Gostava que o vídeo mostrasse a montra à noite, com as luzes acesas."]
    carla = utilizadores.obter_por_email(ligacao, "cliente@empresa.pt")
    video = next(c for c in criativos_bd.listar_por_cliente(ligacao, carla.id) if c.nome == "Vídeo da montra")
    (comentario,) = repositorio.listar_por_criativo(ligacao, video.id)
    assert comentario.autor_id == carla.id
    assert comentario.resposta_a is None


def test_dados_demo_nao_repetem_comentarios(ligacao):
    _demo_ate_aos_criativos(ligacao)
    dados_demo.criar_comentarios(ligacao)

    assert dados_demo.criar_comentarios(ligacao) == []


def test_dados_demo_nao_comentam_um_criativo_que_foi_eliminado(ligacao):
    _demo_ate_aos_criativos(ligacao)
    carla = utilizadores.obter_por_email(ligacao, "cliente@empresa.pt")
    video = next(c for c in criativos_bd.listar_por_cliente(ligacao, carla.id) if c.nome == "Vídeo da montra")
    criativos_bd.eliminar(ligacao, video.id)

    assert dados_demo.criar_comentarios(ligacao) == []


def test_dados_demo_mostram_quantos_comentarios_criaram(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))

    dados_demo.main()
    dados_demo.main()

    saida = capsys.readouterr().out
    assert "Comentários criados: 1 (os restantes já existiam)." in saida
    assert "Comentários criados: 0 (os restantes já existiam)." in saida
