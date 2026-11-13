"""Testes da recuperação da password e do envio simulado de emails."""

import re
from datetime import datetime, timedelta

import pytest

from gestor_campanhas import config, modelos, relogio
from gestor_campanhas.cli import principal
from gestor_campanhas.cli import recuperacao as menu
from gestor_campanhas.erros import ErroAutenticacao, ErroValidacao
from gestor_campanhas.servicos import autenticacao, correio, recuperacao
from tests.conftest import PASSWORD_TESTE

NOVA = "outra-password-456"
EMAIL = "carla@empresa.pt"


@pytest.fixture(autouse=True)
def pasta_de_dados(monkeypatch, tmp_path):
    """Põe a pasta de dados numa pasta temporária, para os emails não irem para a verdadeira."""
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))
    return tmp_path


@pytest.fixture
def agora(monkeypatch):
    """Relógio controlado pelos testes. ``agora.avancar(minutes=...)`` faz passar o tempo."""

    class Relogio:
        valor = datetime(2026, 11, 13, 10, 0, 0)

        def avancar(self, **tempo):
            self.valor += timedelta(**tempo)

    falso = Relogio()
    monkeypatch.setattr(relogio, "agora", lambda: falso.valor)
    return falso


def emails():
    """Ficheiros da caixa de saída, por ordem."""
    pasta = config.pasta_caixa_saida()
    return sorted(pasta.glob("*.txt")) if pasta.exists() else []


def codigo_do_ultimo_email():
    texto = emails()[-1].read_text(encoding="utf-8")
    return re.search(r"é: (\d{6})", texto).group(1)


# --- envio simulado de emails ------------------------------------------------


def test_email_fica_num_ficheiro_da_caixa_de_saida(agora):
    ficheiro = correio.enviar("ana@agencia.pt", "Olá", "Texto da mensagem.")

    assert ficheiro.parent == config.pasta_caixa_saida()
    assert ficheiro.name == "20261113-100000-ana_agencia.pt.txt"
    texto = ficheiro.read_text(encoding="utf-8")
    assert "Para: ana@agencia.pt" in texto
    assert "Assunto: Olá" in texto
    assert "Texto da mensagem." in texto


def test_dois_emails_no_mesmo_segundo_nao_se_substituem(agora):
    correio.enviar("ana@agencia.pt", "Primeiro", "1")
    correio.enviar("ana@agencia.pt", "Segundo", "2")

    assert len(emails()) == 2


# --- regras ------------------------------------------------------------------


def test_codigo_tem_seis_algarismos():
    assert re.fullmatch(r"\d{6}", recuperacao.gerar_codigo())


def test_pedir_codigo_envia_email_ao_dono_da_conta(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, "  CARLA@empresa.pt ")

    (ficheiro,) = emails()
    texto = ficheiro.read_text(encoding="utf-8")
    assert "Para: carla@empresa.pt" in texto
    assert "Carla Cliente" in texto
    assert re.search(r"é: \d{6}", texto)


def test_o_codigo_nao_fica_guardado_na_base_de_dados(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, EMAIL)

    (linha,) = ligacao.execute("SELECT codigo_hash FROM recuperacoes").fetchall()
    assert codigo_do_ultimo_email() not in linha["codigo_hash"]


def test_email_sem_conta_nao_envia_nada_nem_da_erro(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, "ninguem@empresa.pt")

    assert emails() == []


def test_conta_desativada_nao_recebe_codigo(ligacao, contas, agora):
    ligacao.execute("UPDATE utilizadores SET ativo = 0 WHERE email = ?", (EMAIL,))

    recuperacao.pedir_codigo(ligacao, EMAIL)

    assert emails() == []


def test_repor_password_com_o_codigo_certo(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, EMAIL)

    recuperacao.repor_password(ligacao, EMAIL, codigo_do_ultimo_email(), NOVA, NOVA)

    assert autenticacao.autenticar(ligacao, EMAIL, NOVA) == contas[modelos.CLIENTE]
    with pytest.raises(ErroAutenticacao):
        autenticacao.autenticar(ligacao, EMAIL, PASSWORD_TESTE)


def test_codigo_errado_e_recusado(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, EMAIL)
    errado = "000000" if codigo_do_ultimo_email() != "000000" else "111111"

    with pytest.raises(ErroValidacao, match="não é válido"):
        recuperacao.repor_password(ligacao, EMAIL, errado, NOVA, NOVA)


def test_codigo_so_vale_durante_o_prazo(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, EMAIL)
    codigo = codigo_do_ultimo_email()
    agora.avancar(minutes=config.MINUTOS_VALIDADE_CODIGO, seconds=1)

    with pytest.raises(ErroValidacao, match="passou do prazo"):
        recuperacao.repor_password(ligacao, EMAIL, codigo, NOVA, NOVA)


def test_codigo_so_pode_ser_usado_uma_vez(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, EMAIL)
    codigo = codigo_do_ultimo_email()
    recuperacao.repor_password(ligacao, EMAIL, codigo, NOVA, NOVA)

    with pytest.raises(ErroValidacao, match="não é válido"):
        recuperacao.repor_password(ligacao, EMAIL, codigo, "mais-uma-password", "mais-uma-password")


def test_pedido_novo_anula_o_codigo_anterior(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, EMAIL)
    primeiro = codigo_do_ultimo_email()
    agora.avancar(minutes=1)
    recuperacao.pedir_codigo(ligacao, EMAIL)
    segundo = codigo_do_ultimo_email()

    if primeiro != segundo:
        with pytest.raises(ErroValidacao):
            recuperacao.repor_password(ligacao, EMAIL, primeiro, NOVA, NOVA)
    recuperacao.repor_password(ligacao, EMAIL, segundo, NOVA, NOVA)


def test_codigo_de_outra_conta_nao_serve(ligacao, contas, agora):
    recuperacao.pedir_codigo(ligacao, EMAIL)

    with pytest.raises(ErroValidacao, match="não é válido"):
        recuperacao.repor_password(ligacao, "miguel@agencia.pt", codigo_do_ultimo_email(), NOVA, NOVA)


@pytest.mark.parametrize(
    ("nova", "confirmacao", "mensagem"),
    [("curta", "curta", "pelo menos 8 caracteres"), (NOVA, NOVA + "x", "confirmação não é igual")],
)
def test_password_nova_invalida_nao_gasta_o_codigo(ligacao, contas, agora, nova, confirmacao, mensagem):
    recuperacao.pedir_codigo(ligacao, EMAIL)
    codigo = codigo_do_ultimo_email()

    with pytest.raises(ErroValidacao, match=mensagem):
        recuperacao.repor_password(ligacao, EMAIL, codigo, nova, confirmacao)

    recuperacao.repor_password(ligacao, EMAIL, codigo, NOVA, NOVA)


# --- menus -------------------------------------------------------------------


def test_menu_recuperar_ate_ao_fim(ligacao, contas, agora, monkeypatch, capsys):
    respostas = iter([EMAIL, None, NOVA, NOVA, ""])

    def responder(_pergunta=""):
        resposta = next(respostas)
        # O código só existe depois de o email ter sido "enviado".
        return codigo_do_ultimo_email() if resposta is None else resposta

    monkeypatch.setattr("builtins.input", responder)
    monkeypatch.setattr("getpass.getpass", responder)

    menu.recuperar(ligacao)

    saida = capsys.readouterr().out
    assert "foi enviado um código" in saida
    assert str(config.pasta_caixa_saida()) in saida
    assert "Password alterada." in saida
    assert autenticacao.autenticar(ligacao, EMAIL, NOVA)


def test_menu_da_a_mesma_resposta_a_um_email_sem_conta(teclado, ligacao, contas, agora, capsys):
    teclado("ninguem@empresa.pt", "", "")

    menu.recuperar(ligacao)

    saida = capsys.readouterr().out
    assert "Se existir uma conta com esse email, foi enviado um código" in saida
    assert "A password não foi alterada." in saida


def test_menu_com_codigo_errado(teclado, ligacao, contas, agora, capsys):
    teclado(EMAIL, "abc", NOVA, NOVA, "")

    menu.recuperar(ligacao)

    assert "O código não é válido ou já passou do prazo. A password não foi alterada." in capsys.readouterr().out
    assert autenticacao.autenticar(ligacao, EMAIL, PASSWORD_TESTE)


def test_menu_inicial_tem_a_opcao_de_recuperar(teclado, ligacao, contas, agora, capsys):
    teclado("2", EMAIL, "", "", "0")

    principal.executar(ligacao)

    saida = capsys.readouterr().out
    assert "2. Recuperar a password" in saida
    assert len(emails()) == 1
