"""Testes da gestão de clientes e de marketeers pelo Administrador."""

import re

import pytest

from gestor_campanhas import config, modelos, seguranca
from gestor_campanhas.cli import gestao as menu
from gestor_campanhas.cli import perfis
from gestor_campanhas.erros import ErroAutenticacao, ErroValidacao
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import autenticacao, gestao
from tests.conftest import PASSWORD_TESTE


@pytest.fixture(autouse=True)
def pasta_de_dados(monkeypatch, tmp_path):
    """Põe a pasta de dados numa pasta temporária, para os emails não irem para a verdadeira."""
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))
    return tmp_path


def emails():
    """Texto dos emails da caixa de saída, por ordem."""
    pasta = config.pasta_caixa_saida()
    if not pasta.exists():
        return []
    return [ficheiro.read_text(encoding="utf-8") for ficheiro in sorted(pasta.glob("*.txt"))]


@pytest.fixture
def clientes(ligacao, contas):
    """Mais três clientes, além da ``Carla Cliente`` da fixture ``contas``."""
    dados = [
        ("José Padeiro", "jose@padaria.pt", "910000004", "Padaria Central, Lda."),
        ("beatriz lopes", "beatriz@bicicletas.pt", "", "Bicicletas do Sul, Lda."),
        ("Álvaro Josué", "alvaro@oficina.pt", "910000006", ""),
    ]
    palavra_passe = seguranca.gerar_hash(PASSWORD_TESTE)
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


# --- adicionar ---------------------------------------------------------------


def test_criar_cliente_guarda_os_dados_arrumados(ligacao):
    conta = gestao.criar(
        ligacao, modelos.CLIENTE, "  Rita Reis ", " Rita@Loja.PT ", "912 345 678", " Loja da Rita ", "500 000 009"
    )

    assert conta == utilizadores.obter_por_email(ligacao, "rita@loja.pt")
    assert (conta.nome, conta.email, conta.telefone) == ("Rita Reis", "rita@loja.pt", "912345678")
    assert (conta.empresa, conta.nif) == ("Loja da Rita", "500000009")
    assert conta.perfil == modelos.CLIENTE
    assert conta.ativo


def test_criar_cliente_envia_as_credenciais_e_a_password_do_email_funciona(ligacao):
    conta = gestao.criar(ligacao, modelos.CLIENTE, "Rita Reis", "rita@loja.pt")

    (email,) = emails()
    assert "Para: rita@loja.pt" in email
    assert "Assunto: A sua conta no Gestor de Campanhas" in email
    assert "conta de Cliente" in email
    password = re.search(r"Password: (.+)", email).group(1)
    assert autenticacao.autenticar(ligacao, "rita@loja.pt", password) == conta


def test_cada_conta_nova_recebe_uma_password_diferente():
    passwords = {gestao.gerar_password_inicial() for _ in range(20)}

    assert len(passwords) == 20
    assert all(len(password) >= seguranca.TAMANHO_MINIMO for password in passwords)


@pytest.mark.parametrize(
    ("dados", "mensagem"),
    [
        (("", "rita@loja.pt", "", "", ""), "nome não pode ficar vazio"),
        (("Rita", "rita", "", "", ""), "email não é válido"),
        (("Rita", "rita@loja.pt", "123", "", ""), "entre 9 e 15 algarismos"),
        (("Rita", "rita@loja.pt", "", "", "123"), "9 algarismos"),
        (("Rita", "CARLA@empresa.pt", "", "", ""), "Já existe uma conta com este email"),
    ],
)
def test_criar_cliente_com_dados_invalidos_nao_cria_nada(ligacao, contas, dados, mensagem):
    with pytest.raises(ErroValidacao, match=mensagem):
        gestao.criar(ligacao, modelos.CLIENTE, *dados)

    assert utilizadores.contar(ligacao) == 3
    assert emails() == []


def test_so_se_criam_contas_dos_perfis_geridos(ligacao):
    with pytest.raises(ValueError, match="não é gerido"):
        gestao.criar(ligacao, modelos.ADMINISTRADOR, "Outro Admin", "outro@agencia.pt")


# --- editar ------------------------------------------------------------------


def test_obter_confirma_o_numero_e_o_perfil(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    assert gestao.obter(ligacao, modelos.CLIENTE, cliente.id) == cliente
    with pytest.raises(ErroValidacao, match="Não existe nenhum cliente com o número 999"):
        gestao.obter(ligacao, modelos.CLIENTE, 999)
    with pytest.raises(ErroValidacao, match="Não existe nenhum cliente"):
        gestao.obter(ligacao, modelos.CLIENTE, contas[modelos.MARKETEER].id)


def test_editar_cliente_altera_todos_os_dados(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    novo = gestao.editar(
        ligacao, modelos.CLIENTE, cliente.id, "Carla Costa", "Carla@Nova.pt", "+351 912 345 678", "Nova, Lda.", "500000009"
    )

    assert novo == utilizadores.obter_por_id(ligacao, cliente.id)
    assert (novo.nome, novo.email, novo.telefone) == ("Carla Costa", "carla@nova.pt", "+351912345678")
    assert (novo.empresa, novo.nif) == ("Nova, Lda.", "500000009")


def test_editar_cliente_mantem_a_password_e_o_estado(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    gestao.editar(ligacao, modelos.CLIENTE, cliente.id, "Carla Costa", "carla@nova.pt", "")

    assert autenticacao.autenticar(ligacao, "carla@nova.pt", PASSWORD_TESTE).nome == "Carla Costa"
    with pytest.raises(ErroAutenticacao):
        autenticacao.autenticar(ligacao, "carla@empresa.pt", PASSWORD_TESTE)


def test_editar_cliente_pode_manter_o_mesmo_email(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    novo = gestao.editar(ligacao, modelos.CLIENTE, cliente.id, "Carla Costa", cliente.email, "")

    assert novo.email == cliente.email


@pytest.mark.parametrize(
    ("dados", "mensagem"),
    [
        (("", "carla@empresa.pt", "", "", ""), "nome não pode ficar vazio"),
        (("Carla", "carla", "", "", ""), "email não é válido"),
        (("Carla", "miguel@agencia.pt", "", "", ""), "Já existe uma conta com este email"),
        (("Carla", "carla@nova.pt", "123", "", ""), "entre 9 e 15 algarismos"),
        (("Carla", "carla@nova.pt", "", "", "123"), "9 algarismos"),
    ],
)
def test_editar_cliente_com_dados_invalidos_nao_altera_nada(ligacao, contas, dados, mensagem):
    cliente = contas[modelos.CLIENTE]

    with pytest.raises(ErroValidacao, match=mensagem):
        gestao.editar(ligacao, modelos.CLIENTE, cliente.id, *dados)

    assert utilizadores.obter_por_id(ligacao, cliente.id) == cliente


# --- menus de adicionar e editar ---------------------------------------------


def test_menu_adicionar_cliente(teclado, ligacao, contas, capsys):
    teclado("2", "Rita Reis", "rita@loja.pt", "", "Loja da Rita", "", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    conta = utilizadores.obter_por_email(ligacao, "rita@loja.pt")
    assert f"Cliente criado com o número {conta.id}." in saida
    assert "As credenciais de acesso foram enviadas para rita@loja.pt." in saida
    assert "2 clientes." in saida
    assert len(emails()) == 1


def test_menu_adicionar_cliente_mostra_o_erro(teclado, ligacao, contas, capsys):
    teclado("2", "Rita Reis", "carla@empresa.pt", "", "", "", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Já existe uma conta com este email. O cliente não foi criado." in capsys.readouterr().out
    assert utilizadores.contar(ligacao) == 3


def test_menu_editar_cliente_com_enter_mantem_os_valores(teclado, ligacao, contas, capsys):
    cliente = contas[modelos.CLIENTE]
    teclado("3", str(cliente.id), "", "", "912345678", "Empresa Nova", "", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    novo = utilizadores.obter_por_id(ligacao, cliente.id)
    assert "A editar Carla Cliente." in saida
    assert "Dados guardados." in saida
    assert (novo.nome, novo.email) == (cliente.nome, cliente.email)
    assert (novo.telefone, novo.empresa) == ("912345678", "Empresa Nova")


def test_menu_editar_cliente_mostra_o_erro(teclado, ligacao, contas, capsys):
    cliente = contas[modelos.CLIENTE]
    teclado("3", str(cliente.id), "", "miguel@agencia.pt", "", "", "", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Já existe uma conta com este email. Os dados não foram alterados." in capsys.readouterr().out
    assert utilizadores.obter_por_id(ligacao, cliente.id) == cliente


def test_menu_editar_cliente_com_numero_que_nao_existe(teclado, ligacao, contas, capsys):
    teclado("3", "abc", "999", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Escreva um número." in saida
    assert "Não existe nenhum cliente com o número 999." in saida


def test_menu_editar_cliente_pode_ser_cancelado(teclado, ligacao, contas, capsys):
    teclado("3", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    assert "A editar" not in capsys.readouterr().out


# --- desativar e reativar ----------------------------------------------------


def test_cliente_desativado_deixa_de_poder_entrar(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    desativado = gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, False)

    assert not desativado.ativo
    with pytest.raises(ErroAutenticacao, match="Esta conta está desativada"):
        autenticacao.autenticar(ligacao, cliente.email, PASSWORD_TESTE)


def test_cliente_desativado_mantem_os_dados_e_continua_na_lista(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, False)

    (na_lista,) = gestao.listar(ligacao, modelos.CLIENTE)
    assert (na_lista.nome, na_lista.email, na_lista.ativo) == (cliente.nome, cliente.email, False)


def test_cliente_reativado_volta_a_entrar_com_a_mesma_password(ligacao, contas):
    cliente = contas[modelos.CLIENTE]
    gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, False)

    gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, True)

    assert autenticacao.autenticar(ligacao, cliente.email, PASSWORD_TESTE) == cliente


def test_nao_se_desativa_nem_reativa_duas_vezes(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    with pytest.raises(ErroValidacao, match="já está ativa"):
        gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, True)
    gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, False)
    with pytest.raises(ErroValidacao, match="já está desativada"):
        gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, False)


def test_so_se_altera_o_estado_de_contas_do_perfil_indicado(ligacao, contas):
    with pytest.raises(ErroValidacao, match="Não existe nenhum cliente"):
        gestao.definir_estado(ligacao, modelos.CLIENTE, contas[modelos.MARKETEER].id, False)
    with pytest.raises(ValueError, match="não é gerido"):
        gestao.definir_estado(ligacao, modelos.ADMINISTRADOR, contas[modelos.ADMINISTRADOR].id, False)

    assert utilizadores.obter_por_id(ligacao, contas[modelos.MARKETEER].id).ativo
    assert utilizadores.obter_por_id(ligacao, contas[modelos.ADMINISTRADOR].id).ativo


def test_menu_desativar_cliente_pede_confirmacao(teclado, ligacao, contas, capsys):
    cliente = contas[modelos.CLIENTE]
    teclado("4", str(cliente.id), "s", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Carla Cliente (carla@empresa.pt) tem a conta ativa." in saida
    assert "Conta desativada." in saida
    assert "carla@empresa.pt            Desativada" in saida
    assert not utilizadores.obter_por_id(ligacao, cliente.id).ativo


def test_menu_desativar_cliente_sem_confirmar_nao_altera_nada(teclado, ligacao, contas, capsys):
    cliente = contas[modelos.CLIENTE]
    teclado("4", str(cliente.id), "n", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Nada foi alterado." in capsys.readouterr().out
    assert utilizadores.obter_por_id(ligacao, cliente.id).ativo


def test_menu_reativar_cliente(teclado, ligacao, contas, capsys):
    cliente = contas[modelos.CLIENTE]
    gestao.definir_estado(ligacao, modelos.CLIENTE, cliente.id, False)
    teclado("4", str(cliente.id), "s", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "tem a conta desativada." in saida
    assert "Conta reativada." in saida
    assert utilizadores.obter_por_id(ligacao, cliente.id).ativo


def test_menu_estado_com_numero_que_nao_existe_ou_cancelado(teclado, ligacao, contas, capsys):
    teclado("4", "999", "", "4", "", "0")

    menu.clientes(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Não existe nenhum cliente com o número 999." in capsys.readouterr().out


# --- marketeers --------------------------------------------------------------


def test_criar_marketeer_ignora_a_empresa_e_o_nif(ligacao):
    conta = gestao.criar(ligacao, modelos.MARKETEER, "Marta Marques", "marta@agencia.pt", "910000006", "Empresa", "500000009")

    assert conta.perfil == modelos.MARKETEER
    assert (conta.nome, conta.email, conta.telefone) == ("Marta Marques", "marta@agencia.pt", "910000006")
    assert (conta.empresa, conta.nif) == ("", "")


def test_criar_marketeer_envia_as_credenciais(ligacao):
    conta = gestao.criar(ligacao, modelos.MARKETEER, "Marta Marques", "marta@agencia.pt")

    (email,) = emails()
    assert "conta de Marketeer" in email
    password = re.search(r"Password: (.+)", email).group(1)
    assert autenticacao.autenticar(ligacao, "marta@agencia.pt", password) == conta


def test_email_de_um_marketeer_novo_nao_pode_ser_o_de_um_cliente(ligacao, contas):
    with pytest.raises(ErroValidacao, match="Já existe uma conta com este email"):
        gestao.criar(ligacao, modelos.MARKETEER, "Carla", "carla@empresa.pt")


def test_editar_marketeer_altera_o_nome_o_email_e_o_telefone(ligacao, contas):
    marketeer = contas[modelos.MARKETEER]

    novo = gestao.editar(ligacao, modelos.MARKETEER, marketeer.id, "Miguel Matos", "matos@agencia.pt", "912345678", "X", "1")

    assert (novo.nome, novo.email, novo.telefone) == ("Miguel Matos", "matos@agencia.pt", "912345678")
    assert (novo.empresa, novo.nif) == ("", "")
    assert autenticacao.autenticar(ligacao, "matos@agencia.pt", PASSWORD_TESTE) == novo


def test_o_numero_de_um_cliente_nao_serve_para_editar_um_marketeer(ligacao, contas):
    cliente = contas[modelos.CLIENTE]

    with pytest.raises(ErroValidacao, match="Não existe nenhum marketeer com o número"):
        gestao.editar(ligacao, modelos.MARKETEER, cliente.id, "Outro Nome", "outro@agencia.pt", "")

    assert utilizadores.obter_por_id(ligacao, cliente.id) == cliente


def test_menu_marketeers_mostra_a_lista_sem_a_coluna_da_empresa(teclado, ligacao, contas, capsys):
    teclado("0")

    menu.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "N.º  Nome              Email              Telefone  Estado" in saida
    assert "Miguel Marketeer  miguel@agencia.pt            Ativa" in saida
    assert "Carla Cliente" not in saida
    assert "1 marketeer." in saida


def test_menu_marketeers_pesquisa_por_nome(teclado, ligacao, contas, capsys):
    gestao.criar(ligacao, modelos.MARKETEER, "Marta Marques", "marta@agencia.pt")
    teclado("1", "MARTA", "0")

    menu.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    _, depois_da_pesquisa = capsys.readouterr().out.split('Marketeers com "MARTA" no nome')
    assert "Marta Marques" in depois_da_pesquisa
    assert "Miguel Marketeer" not in depois_da_pesquisa


def test_menu_adicionar_marketeer_nao_pede_empresa_nem_nif(teclado, ligacao, contas, capsys):
    teclado("2", "Marta Marques", "marta@agencia.pt", "910000006", "", "0")

    menu.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    conta = utilizadores.obter_por_email(ligacao, "marta@agencia.pt")
    assert f"Marketeer criado com o número {conta.id}." in saida
    assert "As credenciais de acesso foram enviadas para marta@agencia.pt." in saida
    assert "2 marketeers." in saida


def test_menu_adicionar_marketeer_mostra_o_erro(teclado, ligacao, contas, capsys):
    teclado("2", "Marta Marques", "marta", "", "", "0")

    menu.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    assert "O marketeer não foi criado." in capsys.readouterr().out
    assert utilizadores.contar(ligacao) == 3


def test_menu_editar_marketeer(teclado, ligacao, contas, capsys):
    marketeer = contas[modelos.MARKETEER]
    teclado("3", str(marketeer.id), "Miguel Matos", "", "912345678", "", "0")

    menu.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    novo = utilizadores.obter_por_id(ligacao, marketeer.id)
    assert "A editar Miguel Marketeer." in saida
    assert "Dados guardados." in saida
    assert (novo.nome, novo.email, novo.telefone) == ("Miguel Matos", marketeer.email, "912345678")


def test_menu_editar_marketeer_com_o_numero_de_um_cliente(teclado, ligacao, contas, capsys):
    teclado("3", str(contas[modelos.CLIENTE].id), "", "0")

    menu.marketeers(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Não existe nenhum marketeer com o número" in capsys.readouterr().out


def test_opcao_marketeers_so_existe_no_menu_do_administrador():
    descricoes = {perfil: [descricao for descricao, _ in opcoes] for perfil, opcoes in perfis.OPCOES.items()}

    assert "Marketeers" in descricoes[modelos.ADMINISTRADOR]
    assert "Marketeers" not in descricoes[modelos.MARKETEER]
    assert "Marketeers" not in descricoes[modelos.CLIENTE]
