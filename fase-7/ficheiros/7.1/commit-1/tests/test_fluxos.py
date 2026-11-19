"""Testes dos fluxos completos, de uma ponta à outra.

Os outros ficheiros de testes experimentam cada regra sozinha. Estes seguem
o caminho que as pessoas fazem na aplicação, com os três perfis, e confirmam
que as peças encaixam: o que um perfil faz aparece aos outros, com as
notificações e os emails certos.

Os passos usam as funções das regras de negócio (``servicos``), pela mesma
ordem em que os menus as chamam.
"""

import re
from datetime import datetime, timedelta

import pytest

from gestor_campanhas import modelos, relogio
from gestor_campanhas.erros import ErroAutenticacao, ErroValidacao
from gestor_campanhas.servicos import (
    autenticacao,
    campanhas,
    comentarios,
    contas,
    criativos,
    gestao,
    notificacoes,
    painel,
    pedidos,
    relatorios,
)


@pytest.fixture(autouse=True)
def relogio_falso(monkeypatch):
    """Todos os testes começam a 20 de novembro de 2026, às 10h00.

    Devolve um dicionário: mudar ``relogio_falso["agora"]`` muda a hora atual.
    """
    estado = {"agora": datetime(2026, 11, 20, 10, 0)}
    monkeypatch.setattr(relogio, "agora", lambda: estado["agora"])
    return estado


@pytest.fixture
def admin(contas):
    """A administradora Ana, da fixture ``contas``."""
    return contas[modelos.ADMINISTRADOR]


@pytest.fixture
def miguel(contas):
    """O marketeer Miguel, da fixture ``contas``."""
    return contas[modelos.MARKETEER]


@pytest.fixture
def carla(contas):
    """A cliente Carla, da fixture ``contas``."""
    return contas[modelos.CLIENTE]


def passa_um_minuto(relogio_falso):
    """Adianta o relógio um minuto, para cada passo do fluxo ficar com a sua hora.

    As notificações e os emails ficam ordenados pela hora, por isso os passos
    feitos no mesmo minuto não teriam uma ordem certa.
    """
    relogio_falso["agora"] += timedelta(minutes=1)


def assuntos(lista_emails):
    """Devolve a linha do assunto de cada email, sem o ``Assunto:`` do início."""
    return [re.search(r"^Assunto: (.*)$", email, re.MULTILINE).group(1) for email in lista_emails]


def emails_para(lista_emails, endereco):
    """Devolve só os emails enviados para um endereço."""
    return [email for email in lista_emails if f"Para: {endereco}" in email]


def test_conta_nova_entra_e_troca_a_password(ligacao, emails):
    conta = gestao.criar(ligacao, modelos.CLIENTE, "Rui Rodrigues", "rui@loja.pt", empresa="Loja do Rui, Lda.")

    [email] = emails_para(emails(), "rui@loja.pt")
    password_inicial = re.search(r"^Password: (.*)$", email, re.MULTILINE).group(1)
    assert autenticacao.autenticar(ligacao, "rui@loja.pt", password_inicial).id == conta.id

    contas.alterar_password(ligacao, conta, password_inicial, "nova-password-1", "nova-password-1")

    assert autenticacao.autenticar(ligacao, "rui@loja.pt", "nova-password-1").id == conta.id
    with pytest.raises(ErroAutenticacao):
        autenticacao.autenticar(ligacao, "rui@loja.pt", password_inicial)


def test_conta_desativada_deixa_de_entrar_e_volta_a_entrar_depois_de_reativada(ligacao, emails):
    conta = gestao.criar(ligacao, modelos.MARKETEER, "Rita Reis", "rita@agencia.pt")
    password = re.search(r"^Password: (.*)$", emails_para(emails(), "rita@agencia.pt")[0], re.MULTILINE).group(1)

    gestao.definir_estado(ligacao, modelos.MARKETEER, conta.id, False)
    with pytest.raises(ErroAutenticacao):
        autenticacao.autenticar(ligacao, "rita@agencia.pt", password)

    gestao.definir_estado(ligacao, modelos.MARKETEER, conta.id, True)
    assert autenticacao.autenticar(ligacao, "rita@agencia.pt", password).id == conta.id


def test_do_pedido_de_campanha_ao_criativo_publicado(ligacao, emails, relogio_falso, miguel, carla, tmp_path):
    # O cliente pede uma campanha nova.
    pedido = pedidos.criar(ligacao, carla, "Lançar a coleção de inverno", "2000", "2026-12-31", ["Instagram"])
    assert pedido.estado == modelos.PENDENTE

    # O Administrador analisa o pedido e aprova-o, com o budget e o marketeer.
    passa_um_minuto(relogio_falso)
    pedidos.analisar(ligacao, pedido.id)
    pedido = pedidos.aprovar(ligacao, pedido.id, "Coleção de inverno", "2000", miguel.id)
    assert pedido.estado == modelos.APROVADO
    campanha = campanhas.obter_do_cliente(ligacao, carla, pedido.campanha_id)
    assert campanha.budget_centimos == 200000
    assert campanhas.responsavel(ligacao, campanha).id == miguel.id
    assert [c.id for c in campanhas.listar_do_marketeer(ligacao, miguel)] == [campanha.id]
    assert [n.sobre for n in notificacoes.listar(ligacao, miguel)] == [modelos.SOBRE_CAMPANHA]

    # O marketeer cria o criativo, anexa o ficheiro e envia-o para revisão.
    passa_um_minuto(relogio_falso)
    criativo = criativos.criar(
        ligacao, miguel, campanha.id, "Banner de inverno", custo="500", prazo="2026-12-10", plataforma="Instagram"
    )
    imagem = tmp_path / "banner-inverno.png"
    imagem.write_bytes(b"imagem")
    passa_um_minuto(relogio_falso)
    criativos.anexar(ligacao, miguel, criativo.id, str(imagem))
    passa_um_minuto(relogio_falso)
    criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.EM_REVISAO)

    # O cliente vê o criativo, com o ficheiro, e comenta; o marketeer responde.
    visto = criativos.obter_do_cliente(ligacao, carla, criativo.id)
    assert visto.estado == modelos.EM_REVISAO
    assert criativos.ficheiro_de(visto).read_bytes() == b"imagem"
    passa_um_minuto(relogio_falso)
    comentario = comentarios.comentar(ligacao, carla, criativo.id, "Podem pôr o logótipo maior?")
    assert comentarios.por_responder(ligacao, campanha) == {criativo.id: 1}
    passa_um_minuto(relogio_falso)
    comentarios.responder(ligacao, miguel, comentario.id, "Sim, fica maior na versão final.")
    assert comentarios.por_responder(ligacao, campanha) == {}

    # O cliente aprova e o marketeer publica.
    passa_um_minuto(relogio_falso)
    criativos.aprovar(ligacao, carla, criativo.id)
    passa_um_minuto(relogio_falso)
    criativo = criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.PUBLICADO)
    assert criativo.estado == modelos.PUBLICADO

    # O cliente foi notificado de cada passo do marketeer, pela ordem inversa.
    textos = [n.texto for n in notificacoes.listar(ligacao, carla)]
    assert len(textos) == 5
    assert textos[0].endswith("passou a Publicado.")
    assert textos[1].startswith("Miguel Marketeer respondeu ao seu comentário")
    assert "à espera da sua aprovação" in textos[2]
    assert textos[3].startswith("Foi anexado o ficheiro banner-inverno.png")
    assert textos[4].startswith("Foi criado o criativo Banner de inverno")

    # Os mesmos avisos chegaram por email, a seguir ao da aprovação do pedido.
    assert assuntos(emails_para(emails(), carla.email)) == [
        "O seu pedido de campanha foi aprovado",
        "Novo criativo",
        "Criativo alterado",
        "Criativo à espera da sua aprovação",
        "Resposta ao seu comentário",
        "Criativo alterado",
    ]
    assert assuntos(emails_para(emails(), miguel.email)) == [
        "Foi-lhe atribuída uma campanha",
        "Novo comentário a um criativo",
    ]

    # O Administrador vê o trabalho no painel: um criativo concluído.
    [indicadores] = painel.carga(ligacao)
    assert (indicadores.ativos, indicadores.concluidos, indicadores.em_atraso) == (0, 1, 0)
    assert painel.situacao(indicadores, painel.dias_sem_atividade(ligacao)) == "Sem criativos ativos"

    # E o cliente tem tudo no relatório.
    [linha] = relatorios.linhas(ligacao, carla)
    assert linha[0] == "Coleção de inverno"
    assert linha[5:8] == ["2000,00", "500,00", "1500,00"]
    assert linha[8:] == ["Banner de inverno", "Publicado", "Instagram", "2026-12-10", "500,00"]


def test_criativo_rejeitado_e_corrigido_volta_a_revisao_e_e_aprovado(ligacao, miguel, carla):
    campanha = campanhas.criar(ligacao, miguel, "Primavera", "Vender mais em março", carla.id)
    criativo = criativos.criar(ligacao, miguel, campanha.id, "Cartaz", custo="300")
    criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.EM_REVISAO)

    # O cliente rejeita, a dizer o que quer mudar.
    rejeitado = criativos.rejeitar(ligacao, carla, criativo.id, "Falta o preço da promoção")
    assert rejeitado.estado == modelos.REJEITADO
    assert criativos.obter_do_marketeer(ligacao, miguel, criativo.id).motivo_rejeicao == "Falta o preço da promoção"

    # Enquanto o marketeer não o corrige, o cliente já não o pode aprovar.
    with pytest.raises(ErroValidacao):
        criativos.aprovar(ligacao, carla, criativo.id)

    # O marketeer corrige e volta a enviar para revisão; o cliente aprova.
    criativos.editar(ligacao, miguel, criativo.id, "Cartaz", "Com o preço: 9,99 €", "300", "", "", "")
    criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.EM_REVISAO)
    aprovado = criativos.aprovar(ligacao, carla, criativo.id)

    assert aprovado.estado == modelos.APROVADO
    assert aprovado.motivo_rejeicao == ""
    assert aprovado.descricao == "Com o preço: 9,99 €"


def test_pedido_de_campanha_rejeitado_nao_cria_campanha(ligacao, emails, carla):
    pedido = pedidos.criar(ligacao, carla, "Anunciar a loja nova", "800", "2026-12-20", ["Facebook"])

    pedido = pedidos.rejeitar(ligacao, pedido.id, "O orçamento não chega para as duas plataformas")

    assert pedido.estado == modelos.REJEITADO
    assert pedido.campanha_id is None
    assert campanhas.listar_do_cliente(ligacao, carla) == []
    assert pedidos.listar_do_cliente(ligacao, carla)[0].motivo_rejeicao == (
        "O orçamento não chega para as duas plataformas"
    )
    assert assuntos(emails_para(emails(), carla.email)) == ["O seu pedido de campanha foi rejeitado"]
