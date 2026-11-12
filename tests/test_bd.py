"""Testes do módulo :mod:`gestor_campanhas.bd` e dos caminhos de dados."""

import sqlite3

import pytest

from gestor_campanhas import bd, config


def test_pasta_dados_por_omissao_fica_no_projeto(monkeypatch):
    monkeypatch.delenv(config.VARIAVEL_PASTA_DADOS, raising=False)

    assert config.pasta_dados() == config.PASTA_PROJETO / "dados"


def test_pasta_dados_segue_variavel_de_ambiente(monkeypatch, tmp_path):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))

    assert config.pasta_dados() == tmp_path
    assert config.ficheiro_bd() == tmp_path / "app.db"


def test_ligar_cria_a_pasta_e_o_ficheiro(tmp_path):
    caminho = tmp_path / "nova_pasta" / "app.db"

    ligacao = bd.ligar(caminho)
    ligacao.close()

    assert caminho.exists()


def test_ligar_sem_caminho_usa_a_pasta_de_dados(monkeypatch, tmp_path):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))

    ligacao = bd.ligar()
    ligacao.close()

    assert (tmp_path / "app.db").exists()


def test_ligacao_verifica_chaves_estrangeiras(ligacao):
    ativo = ligacao.execute("PRAGMA foreign_keys").fetchone()[0]

    assert ativo == 1


def test_linhas_podem_ser_lidas_pelo_nome_da_coluna(ligacao):
    ligacao.execute("INSERT INTO configuracoes (chave, valor) VALUES ('cor', 'azul')")

    linha = ligacao.execute("SELECT chave, valor FROM configuracoes").fetchone()

    assert linha["chave"] == "cor"
    assert linha["valor"] == "azul"


def test_criar_tabelas_cria_a_tabela_configuracoes(ligacao):
    tabelas = [
        linha["name"]
        for linha in ligacao.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    ]

    assert "configuracoes" in tabelas


def test_criar_tabelas_pode_ser_repetida_sem_perder_dados(ligacao):
    ligacao.execute("INSERT INTO configuracoes (chave, valor) VALUES ('cor', 'azul')")

    bd.criar_tabelas(ligacao)

    total = ligacao.execute("SELECT COUNT(*) FROM configuracoes").fetchone()[0]
    assert total == 1


def test_chave_de_configuracao_nao_pode_repetir(ligacao):
    ligacao.execute("INSERT INTO configuracoes (chave, valor) VALUES ('cor', 'azul')")

    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute("INSERT INTO configuracoes (chave, valor) VALUES ('cor', 'verde')")
