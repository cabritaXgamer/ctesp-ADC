"""Testes dos dados de demonstração no seu conjunto.

Cada parte dos dados de demonstração (contas, campanhas, criativos...) tem
os seus testes junto das regras a que pertence. Estes confirmam o resultado
final, tal como fica numa instalação nova depois de correr
``python -m gestor_campanhas.dados_demo``: os criativos em vários estados,
o ficheiro anexado, as notificações e a atividade dos marketeers.
"""

from datetime import datetime

import pytest

from gestor_campanhas import config, dados_demo, modelos, relogio
from gestor_campanhas.repositorios import atividades, criativos, notificacoes, utilizadores
from gestor_campanhas.servicos import criativos as servico_criativos
from gestor_campanhas.servicos import painel


@pytest.fixture(autouse=True)
def dia_20_de_novembro(monkeypatch):
    """Os dados de demonstração são criados a 20 de novembro de 2026, às 10h00."""
    monkeypatch.setattr(relogio, "agora", lambda: datetime(2026, 11, 20, 10, 0))


def criar_tudo(ligacao):
    """Cria todos os dados de demonstração, pela ordem de :func:`dados_demo.main`."""
    dados_demo.criar_contas(ligacao)
    dados_demo.criar_campanhas(ligacao)
    dados_demo.registar_budgets_iniciais(ligacao)
    dados_demo.criar_pedidos(ligacao)
    dados_demo.criar_criativos(ligacao)
    dados_demo.criar_pedidos_budget(ligacao)
    dados_demo.criar_comentarios(ligacao)


def conta(ligacao, email):
    """Devolve a conta de demonstração com um email."""
    return utilizadores.obter_por_email(ligacao, email)


def criativos_por_nome(ligacao):
    """Devolve os criativos de demonstração, pelo nome."""
    cliente_ids = [conta(ligacao, c["email"]).id for c in dados_demo.CONTAS if c["perfil"] == modelos.CLIENTE]
    return {c.nome: c for cliente_id in cliente_ids for c in criativos.listar_por_cliente(ligacao, cliente_id)}


def test_criativos_ficam_nos_estados_indicados(ligacao):
    criar_tudo(ligacao)

    estados = {nome: criativo.estado for nome, criativo in criativos_por_nome(ligacao).items()}

    assert estados == {
        "Banner de Natal": modelos.EM_REVISAO,
        "Vídeo da montra": modelos.EM_PREPARACAO,
        "Cartaz dos lanches": modelos.PUBLICADO,
        "Anúncio da bicicleta elétrica": modelos.EM_PREPARACAO,
    }


def test_banner_de_natal_fica_com_o_ficheiro_de_exemplo(ligacao):
    criar_tudo(ligacao)

    banner = criativos_por_nome(ligacao)["Banner de Natal"]

    assert banner.ficheiro == "banner-natal.svg"
    copia = servico_criativos.ficheiro_de(banner)
    assert copia.read_bytes() == (config.PASTA_PROJETO / "exemplos" / "banner-natal.svg").read_bytes()


def test_cliente_e_marketeer_encontram_as_notificacoes_do_que_aconteceu(ligacao):
    criar_tudo(ligacao)

    def textos(email):
        return [n.texto for n in notificacoes.listar_por_utilizador(ligacao, conta(ligacao, email).id)]

    carla = textos("cliente@empresa.pt")
    assert len(carla) == 3
    assert any(texto.startswith("Miguel Marketeer respondeu ao seu comentário") for texto in carla)
    assert any("está à espera da sua aprovação" in texto for texto in carla)
    miguel = textos("marketeer@agencia.pt")
    assert len(miguel) == 3
    assert any("pediu para alterar o budget da campanha Natal 2026" in texto for texto in miguel)
    assert sum(texto.startswith("Carla Cliente comentou") for texto in miguel) == 2
    jose = textos("jose@padaria.pt")
    assert jose[0].endswith("passou a Publicado.")
    assert textos("marta@agencia.pt") == []
    assert textos("admin@agencia.pt") == []


def test_painel_mostra_a_atividade_dos_dois_marketeers(ligacao):
    criar_tudo(ligacao)

    por_nome = {c.marketeer.nome: c for c in painel.carga(ligacao)}

    miguel, marta = por_nome["Miguel Marketeer"], por_nome["Marta Marques"]
    assert (miguel.ativos, miguel.concluidos) == (2, 1)
    assert (marta.ativos, marta.concluidos) == (1, 0)
    assert len(atividades.listar_por_utilizador(ligacao, miguel.marketeer.id, limite=10)) == 5
    assert miguel.ultima_atividade == datetime(2026, 11, 20, 10, 0)


def test_repetir_nao_cria_nem_notifica_outra_vez(ligacao):
    criar_tudo(ligacao)
    antes = {
        c["email"]: len(notificacoes.listar_por_utilizador(ligacao, conta(ligacao, c["email"]).id))
        for c in dados_demo.CONTAS
    }

    criar_tudo(ligacao)

    depois = {
        c["email"]: len(notificacoes.listar_por_utilizador(ligacao, conta(ligacao, c["email"]).id))
        for c in dados_demo.CONTAS
    }
    assert depois == antes
    assert len(criativos_por_nome(ligacao)) == len(dados_demo.CRIATIVOS)


def test_criativos_que_ja_existiam_ficam_como_estao(ligacao):
    dados_demo.criar_contas(ligacao)
    dados_demo.criar_campanhas(ligacao)
    dados_demo.criar_criativos(ligacao)
    banner = criativos_por_nome(ligacao)["Banner de Natal"]
    criativos.definir_estado(ligacao, banner.id, modelos.EM_PREPARACAO)

    assert dados_demo.criar_criativos(ligacao) == []
    assert criativos.obter_por_id(ligacao, banner.id).estado == modelos.EM_PREPARACAO


def test_estados_dos_criativos_de_demonstracao_sao_validos():
    for criativo in dados_demo.CRIATIVOS:
        assert criativo["estado"] in modelos.NOMES_ESTADOS_CRIATIVO
        if criativo.get("ficheiro"):
            assert (config.PASTA_PROJETO / criativo["ficheiro"]).is_file()


def test_main_mostra_as_contas_e_o_que_criou(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))

    assert dados_demo.main() == 0

    saida = capsys.readouterr().out
    assert "Criativos criados: 4 (os restantes já existiam)." in saida
    assert "Comentários criados: 2 (os restantes já existiam)." in saida
    for c in dados_demo.CONTAS:
        assert f"password: {c['password']}" in saida
    assert (tmp_path / "ficheiros").is_dir()
