"""Testes dos menus: funções comuns, menu inicial e ponto de entrada."""

from gestor_campanhas import __main__, config
from gestor_campanhas.cli import comum, principal

OPCOES = [("1", "Primeira"), ("0", "Sair")]


def test_escolher_opcao_devolve_a_chave_escolhida(teclado, capsys):
    teclado("1")

    assert comum.escolher_opcao("Menu de teste", OPCOES) == "1"

    saida = capsys.readouterr().out
    assert "Menu de teste" in saida
    assert "1. Primeira" in saida
    assert "0. Sair" in saida


def test_escolher_opcao_repete_ate_a_opcao_ser_valida(teclado, capsys):
    teclado("9", "", "0")

    assert comum.escolher_opcao("Menu de teste", OPCOES) == "0"
    assert capsys.readouterr().out.count("Opção inválida.") == 2


def test_escolher_opcao_ignora_espacos(teclado):
    teclado("  1  ")

    assert comum.escolher_opcao("Menu de teste", OPCOES) == "1"


def test_confirmar_aceita_sim_e_nao(teclado):
    teclado("s", "SIM", "n", "não")

    assert comum.confirmar("Tem a certeza?") is True
    assert comum.confirmar("Tem a certeza?") is True
    assert comum.confirmar("Tem a certeza?") is False
    assert comum.confirmar("Tem a certeza?") is False


def test_confirmar_repete_ate_a_resposta_ser_valida(teclado, capsys):
    teclado("talvez", "s")

    assert comum.confirmar("Tem a certeza?") is True
    assert "Responda 's' ou 'n'." in capsys.readouterr().out


def test_ler_texto_obrigatorio_repete_ate_haver_resposta(teclado, capsys):
    teclado("", "   ", "  Ana  ")

    assert comum.ler_texto("Nome") == "Ana"
    assert capsys.readouterr().out.count("Este campo é obrigatório.") == 2


def test_ler_texto_opcional_aceita_resposta_vazia(teclado):
    teclado("")

    assert comum.ler_texto("Observações", obrigatorio=False) == ""


def test_menu_inicial_termina_com_a_opcao_sair(teclado, ligacao, capsys):
    teclado("0")

    principal.executar(ligacao)

    assert "Até breve!" in capsys.readouterr().out


def test_menu_inicial_volta_a_aparecer_depois_de_entrar(teclado, ligacao, capsys):
    teclado("1", "", "0")

    principal.executar(ligacao)

    saida = capsys.readouterr().out
    assert "ainda não está disponível" in saida
    assert saida.count("1. Entrar") == 2


def test_main_cria_a_base_de_dados_e_devolve_zero(teclado, monkeypatch, tmp_path):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))
    teclado("0")

    assert __main__.main() == 0
    assert (tmp_path / "app.db").exists()


def test_main_termina_sem_erro_quando_a_entrada_acaba(teclado, monkeypatch, tmp_path, capsys):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))
    teclado()  # sem respostas: a primeira pergunta fica sem resposta

    assert __main__.main() == 0
    assert "A sair..." in capsys.readouterr().out
