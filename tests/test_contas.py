"""Testes das alterações à própria conta: password e dados."""

import pytest

from gestor_campanhas import modelos
from gestor_campanhas.cli import conta, perfis
from gestor_campanhas.erros import ErroAutenticacao, ErroValidacao
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import autenticacao
from gestor_campanhas.servicos import contas as servico
from tests.conftest import PASSWORD_TESTE

NOVA = "outra-password-456"


@pytest.fixture
def cliente(contas):
    """A conta de cliente criada pela fixture ``contas``."""
    return contas[modelos.CLIENTE]


# --- alterar a password ------------------------------------------------------


def test_alterar_password_passa_a_valer_a_nova(ligacao, cliente):
    servico.alterar_password(ligacao, cliente, PASSWORD_TESTE, NOVA, NOVA)

    assert autenticacao.autenticar(ligacao, cliente.email, NOVA) == cliente
    with pytest.raises(ErroAutenticacao):
        autenticacao.autenticar(ligacao, cliente.email, PASSWORD_TESTE)


@pytest.mark.parametrize(
    ("atual", "nova", "confirmacao", "mensagem"),
    [
        ("errada", NOVA, NOVA, "password atual não está correta"),
        (PASSWORD_TESTE, "curta", "curta", "pelo menos 8 caracteres"),
        (PASSWORD_TESTE, PASSWORD_TESTE, PASSWORD_TESTE, "diferente da atual"),
        (PASSWORD_TESTE, NOVA, NOVA + "x", "confirmação não é igual"),
    ],
)
def test_alterar_password_recusada(ligacao, cliente, atual, nova, confirmacao, mensagem):
    with pytest.raises(ErroValidacao, match=mensagem):
        servico.alterar_password(ligacao, cliente, atual, nova, confirmacao)

    # A password antiga continua a valer.
    assert autenticacao.autenticar(ligacao, cliente.email, PASSWORD_TESTE) == cliente


# --- editar os dados ---------------------------------------------------------


def test_cliente_altera_contactos_e_dados_da_empresa(ligacao, cliente):
    servico.atualizar_dados(ligacao, cliente, " Carla Costa ", "912 345 678", "Costa, Lda.", "501 234 567")

    guardado = utilizadores.obter_por_id(ligacao, cliente.id)
    assert (guardado.nome, guardado.telefone) == ("Carla Costa", "912345678")
    assert (guardado.empresa, guardado.nif) == ("Costa, Lda.", "501234567")
    assert cliente == guardado


def test_telefone_internacional_e_campos_vazios_sao_aceites(ligacao, cliente):
    servico.atualizar_dados(ligacao, cliente, "Carla", "+351912345678", "", "")

    assert cliente.telefone == "+351912345678"
    assert cliente.nif == ""


@pytest.mark.parametrize(
    ("nome", "telefone", "nif", "mensagem"),
    [
        ("   ", "912345678", "501234567", "nome não pode ficar vazio"),
        ("Carla", "12345", "501234567", "telefone tem de ter entre 9 e 15 algarismos"),
        ("Carla", "91234567a", "501234567", "telefone tem de ter entre 9 e 15 algarismos"),
        ("Carla", "912345678", "1234", "NIF tem de ter 9 algarismos"),
    ],
)
def test_dados_invalidos_sao_recusados(ligacao, cliente, nome, telefone, nif, mensagem):
    with pytest.raises(ErroValidacao, match=mensagem):
        servico.atualizar_dados(ligacao, cliente, nome, telefone, "Empresa", nif)

    assert utilizadores.obter_por_id(ligacao, cliente.id).nome == "Carla Cliente"


def test_quem_nao_e_cliente_nao_fica_com_dados_de_empresa(ligacao, contas):
    marketeer = contas[modelos.MARKETEER]

    servico.atualizar_dados(ligacao, marketeer, "Miguel M.", "910000002", "Não devia ficar", "123456789")

    assert marketeer.nome == "Miguel M."
    assert (marketeer.empresa, marketeer.nif) == ("", "")


# --- menus -------------------------------------------------------------------


def test_menu_editar_dados_mantem_o_que_fica_em_branco(teclado, ligacao, cliente, capsys):
    teclado("", "913000000", "Nova Empresa", "", "")

    conta.editar_dados(ligacao, cliente)

    assert cliente.nome == "Carla Cliente"
    assert cliente.telefone == "913000000"
    assert cliente.empresa == "Nova Empresa"
    saida = capsys.readouterr().out
    assert "carla@empresa.pt (não pode ser alterado)" in saida
    assert "Dados guardados." in saida


def test_menu_editar_dados_mostra_o_erro(teclado, ligacao, cliente, capsys):
    teclado("", "123", "", "", "")

    conta.editar_dados(ligacao, cliente)

    assert "Os dados não foram alterados." in capsys.readouterr().out


def test_menu_editar_dados_nao_pede_empresa_a_quem_nao_e_cliente(teclado, ligacao, contas):
    teclado("Ana A.", "", "")  # nome, telefone, pausa: não há perguntas sobre a empresa

    conta.editar_dados(ligacao, contas[modelos.ADMINISTRADOR])

    assert contas[modelos.ADMINISTRADOR].nome == "Ana A."


def test_menu_alterar_password(teclado, ligacao, cliente, capsys):
    teclado(PASSWORD_TESTE, NOVA, NOVA, "")

    conta.alterar_password(ligacao, cliente)

    assert "Password alterada." in capsys.readouterr().out
    assert autenticacao.autenticar(ligacao, cliente.email, NOVA)


def test_menu_alterar_password_mostra_o_erro(teclado, ligacao, cliente, capsys):
    teclado("errada", NOVA, NOVA, "")

    conta.alterar_password(ligacao, cliente)

    assert "A password não foi alterada." in capsys.readouterr().out


def test_opcoes_da_conta_existem_em_todos_os_perfis():
    for opcoes in perfis.OPCOES.values():
        descricoes = [descricao for descricao, _ in opcoes]
        assert "Editar os meus dados" in descricoes
        assert "Alterar a password" in descricoes
