"""Testes da gestão de clientes e de marketeers pelo Administrador."""

import pytest

from gestor_campanhas import modelos, seguranca
from gestor_campanhas.cli import gestao as menu
from gestor_campanhas.cli import perfis
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import gestao


@pytest.fixture
def clientes(ligacao, contas):
    """Mais três clientes, além da ``Carla Cliente`` da fixture ``contas``."""
    dados = [
        ("José Padeiro", "jose@padaria.pt", "910000004", "Padaria Central, Lda."),
        ("beatriz lopes", "beatriz@bicicletas.pt", "", "Bicicletas do Sul, Lda."),
        ("Álvaro Josué", "alvaro@oficina.pt", "910000006", ""),
    ]
    palavra_passe = seguranca.gerar_hash("segredo-123")
    return [
        utilizadores.criar(ligacao, nome, email, palavra_passe, modelos.CLIENTE, telefone=telefone, empresa=empresa)
        for nome, email, telefone, empresa in dados
    ]


def nomes(contas):
    return [conta.nome for conta in contas]


# --- regras ------------------------------------------------------------------


def test_lista_so_o_perfil_pedido_por_ordem_alfabetica(ligacao, clientes):
    assert nomes(gestao.listar(ligacao, modelos.CLIENTE)) == [
        "Álvaro Josué",
        "beatriz lopes",
        "Carla Cliente",
        "José Padeiro",
    ]
    assert nomes(gestao.listar(ligacao, modelos.MARKETEER)) == ["Miguel Marketeer"]


def test_lista_vazia_quando_nao_ha_contas_do_perfil(ligacao):
    assert gestao.listar(ligacao, modelos.CLIENTE) == []


@pytest.mark.parametrize(
    ("pesquisa", "esperados"),
    [
        ("carla", ["Carla Cliente"]),
        ("LOPES", ["beatriz lopes"]),
        ("jos", ["Álvaro Josué", "José Padeiro"]),
        ("josé", ["José Padeiro"]),
        ("alvaro", ["Álvaro Josué"]),
        ("  padeiro  ", ["José Padeiro"]),
        ("zzz", []),
    ],
)
def test_pesquisa_por_parte_do_nome_sem_contar_acentos_nem_maiusculas(ligacao, clientes, pesquisa, esperados):
    assert nomes(gestao.listar(ligacao, modelos.CLIENTE, pesquisa)) == esperados


def test_simplificar_tira_acentos_maiusculas_e_espacos():
    assert gestao.simplificar("  JOSÉ Conceição ") == "jose conceicao"


# --- apresentação ------------------------------------------------------------


def test_menu_mostra_todos_os_clientes(teclado, ligacao, contas, clientes, capsys):
    teclado("0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "N.º  Nome           Empresa                  Email                  Telefone   Estado" in saida
    assert "José Padeiro   Padaria Central, Lda.    jose@padaria.pt        910000004  Ativa" in saida
    assert "Miguel Marketeer" not in saida
    assert "4 clientes." in saida


def test_menu_mostra_o_resultado_da_pesquisa(teclado, ligacao, contas, clientes, capsys):
    teclado("1", "carla", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    _, depois_da_pesquisa = capsys.readouterr().out.split('Clientes com "carla" no nome')
    assert "Carla Cliente" in depois_da_pesquisa
    assert "José Padeiro" not in depois_da_pesquisa
    assert "1 cliente." in depois_da_pesquisa


def test_menu_avisa_quando_a_pesquisa_nao_encontra_ninguem(teclado, ligacao, contas, clientes, capsys):
    teclado("1", "zzz", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    assert 'Não há clientes com "zzz" no nome.' in capsys.readouterr().out


def test_menu_avisa_quando_nao_ha_clientes(teclado, ligacao, capsys):
    administrador = utilizadores.criar(ligacao, "Ana", "ana@agencia.pt", "x", modelos.ADMINISTRADOR)
    teclado("0")

    menu.clientes(ligacao, administrador)

    assert "Ainda não há clientes." in capsys.readouterr().out


def test_estado_da_conta_por_palavras(contas):
    conta = contas[modelos.CLIENTE]

    assert menu.estado(conta) == "Ativa"
    conta.ativo = False
    assert menu.estado(conta) == "Desativada"


def test_opcao_so_existe_no_menu_do_administrador():
    descricoes = {perfil: [descricao for descricao, _ in opcoes] for perfil, opcoes in perfis.OPCOES.items()}

    assert "Clientes" in descricoes[modelos.ADMINISTRADOR]
    assert "Clientes" not in descricoes[modelos.MARKETEER]
    assert "Clientes" not in descricoes[modelos.CLIENTE]
