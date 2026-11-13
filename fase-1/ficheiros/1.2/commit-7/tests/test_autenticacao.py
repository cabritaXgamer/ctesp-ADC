"""Testes da entrada na aplicação: passwords, utilizadores, autenticação e menus."""

import sqlite3

import pytest

from gestor_campanhas import dados_demo, modelos, seguranca
from gestor_campanhas.cli import perfis, principal
from gestor_campanhas.erros import ErroAutenticacao
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import autenticacao, sessoes
from tests.conftest import PASSWORD_TESTE

# --- passwords ---------------------------------------------------------------


def test_hash_nao_contem_a_password():
    guardado = seguranca.gerar_hash("segredo-123")

    assert "segredo-123" not in guardado
    assert guardado.startswith("pbkdf2_sha256$")


def test_mesma_password_da_hashes_diferentes():
    assert seguranca.gerar_hash("segredo-123") != seguranca.gerar_hash("segredo-123")


def test_verificar_password_certa_e_errada():
    guardado = seguranca.gerar_hash("segredo-123")

    assert seguranca.verificar_password("segredo-123", guardado) is True
    assert seguranca.verificar_password("outra-coisa", guardado) is False


def test_verificar_password_com_hash_invalido():
    assert seguranca.verificar_password("segredo-123", "isto não é um hash") is False


# --- utilizadores ------------------------------------------------------------


def test_criar_utilizador_guarda_o_email_normalizado(ligacao):
    criado = utilizadores.criar(ligacao, "Ana", "  Ana@Agencia.PT ", "hash", modelos.ADMINISTRADOR)

    assert criado.email == "ana@agencia.pt"
    assert criado.ativo is True
    assert utilizadores.obter_por_email(ligacao, "ANA@agencia.pt") == criado
    assert utilizadores.obter_por_id(ligacao, criado.id) == criado


def test_email_nao_pode_repetir(ligacao, contas):
    with pytest.raises(sqlite3.IntegrityError):
        utilizadores.criar(ligacao, "Outra Ana", "ana@agencia.pt", "hash", modelos.CLIENTE)


def test_perfil_tem_de_ser_valido(ligacao):
    with pytest.raises(sqlite3.IntegrityError):
        utilizadores.criar(ligacao, "Zé", "ze@agencia.pt", "hash", "chefe")


def test_utilizador_que_nao_existe(ligacao):
    assert utilizadores.obter_por_email(ligacao, "ninguem@agencia.pt") is None
    assert utilizadores.obter_por_id(ligacao, 999) is None
    assert utilizadores.obter_hash(ligacao, 999) is None


# --- autenticação ------------------------------------------------------------


@pytest.mark.parametrize("perfil", [modelos.ADMINISTRADOR, modelos.MARKETEER, modelos.CLIENTE])
def test_autenticar_cada_perfil(ligacao, contas, perfil):
    esperado = contas[perfil]

    assert autenticacao.autenticar(ligacao, esperado.email, PASSWORD_TESTE) == esperado


def test_autenticar_com_password_errada(ligacao, contas):
    with pytest.raises(ErroAutenticacao, match="Email ou password incorretos"):
        autenticacao.autenticar(ligacao, "ana@agencia.pt", "errada")


def test_autenticar_com_email_desconhecido_da_a_mesma_mensagem(ligacao, contas):
    with pytest.raises(ErroAutenticacao, match="Email ou password incorretos"):
        autenticacao.autenticar(ligacao, "ninguem@agencia.pt", PASSWORD_TESTE)


def test_conta_desativada_nao_entra(ligacao, contas):
    ligacao.execute("UPDATE utilizadores SET ativo = 0 WHERE email = 'miguel@agencia.pt'")

    with pytest.raises(ErroAutenticacao, match="desativada"):
        autenticacao.autenticar(ligacao, "miguel@agencia.pt", PASSWORD_TESTE)


# --- menus -------------------------------------------------------------------


@pytest.mark.parametrize(
    ("email", "titulo"),
    [
        ("ana@agencia.pt", "Administrador — Ana Admin"),
        ("miguel@agencia.pt", "Marketeer — Miguel Marketeer"),
        ("carla@empresa.pt", "Cliente — Carla Cliente"),
    ],
)
def test_entrar_abre_o_menu_do_perfil(teclado, ligacao, contas, capsys, email, titulo):
    teclado("1", email, PASSWORD_TESTE, "0", "0")

    principal.executar(ligacao)

    saida = capsys.readouterr().out
    assert titulo in saida
    assert "Sessão terminada." in saida
    assert "Até breve!" in saida


def test_entrar_com_password_errada_volta_ao_menu_inicial(teclado, ligacao, contas, capsys):
    teclado("1", "ana@agencia.pt", "errada", "", "0")

    principal.executar(ligacao)

    saida = capsys.readouterr().out
    assert "Email ou password incorretos." in saida
    assert "Administrador — Ana Admin" not in saida
    assert saida.count("1. Entrar") == 2


def test_menu_do_perfil_executa_a_opcao_escolhida(teclado, ligacao, contas, monkeypatch, capsys):
    chamadas = []
    monkeypatch.setitem(
        perfis.OPCOES, modelos.CLIENTE, [("Opção de teste", lambda lig, utilizador: chamadas.append(utilizador))]
    )
    teclado("1", "0")

    perfis.executar(ligacao, sessoes.iniciar(ligacao, contas[modelos.CLIENTE]))

    assert chamadas == [contas[modelos.CLIENTE]]
    assert "1. Opção de teste" in capsys.readouterr().out


# --- dados de demonstração ---------------------------------------------------


def test_dados_demo_criam_uma_conta_por_perfil(ligacao):
    criadas = dados_demo.criar_contas(ligacao)

    assert len(criadas) == 3
    for conta in dados_demo.CONTAS:
        utilizador = autenticacao.autenticar(ligacao, conta["email"], conta["password"])
        assert utilizador.perfil == conta["perfil"]


def test_dados_demo_podem_ser_repetidos(ligacao):
    dados_demo.criar_contas(ligacao)

    assert dados_demo.criar_contas(ligacao) == []
    assert utilizadores.contar(ligacao) == 3
