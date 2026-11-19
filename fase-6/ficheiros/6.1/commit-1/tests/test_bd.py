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


def test_campanha_tem_de_ter_um_cliente_que_existe(ligacao):
    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute(
            "INSERT INTO campanhas (nome, cliente_id, marketeer_id, criada_em) "
            "VALUES ('Natal', 999, 999, '2026-11-16 10:00:00')"
        )


def test_pedido_de_campanha_so_aceita_os_estados_previstos(ligacao, contas):
    cliente = contas["cliente"]

    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute(
            "INSERT INTO pedidos_campanha (cliente_id, objetivo, orcamento_centimos, prazo, estado, criado_em) "
            "VALUES (?, 'Vender', 1000, '2026-12-01', 'perdido', '2026-11-16 10:00:00')",
            (cliente.id,),
        )


def test_criativo_tem_de_ter_uma_campanha_que_existe(ligacao):
    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute(
            "INSERT INTO criativos (campanha_id, nome, criado_em) VALUES (999, 'Banner', '2026-11-17 10:00:00')"
        )


def test_campanha_com_criativos_nao_pode_ser_apagada(ligacao, contas):
    cursor = ligacao.execute(
        "INSERT INTO campanhas (nome, cliente_id, marketeer_id, criada_em) VALUES ('Natal', ?, ?, '2026-11-17')",
        (contas["cliente"].id, contas["marketeer"].id),
    )
    ligacao.execute(
        "INSERT INTO criativos (campanha_id, nome, criado_em) VALUES (?, 'Banner', '2026-11-17 10:00:00')",
        (cursor.lastrowid,),
    )

    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute("DELETE FROM campanhas WHERE id = ?", (cursor.lastrowid,))


def test_criativo_comeca_em_preparacao(ligacao, contas):
    cursor = ligacao.execute(
        "INSERT INTO campanhas (nome, cliente_id, marketeer_id, criada_em) VALUES ('Natal', ?, ?, '2026-11-17')",
        (contas["cliente"].id, contas["marketeer"].id),
    )
    ligacao.execute(
        "INSERT INTO criativos (campanha_id, nome, criado_em) VALUES (?, 'Banner', '2026-11-17 10:00:00')",
        (cursor.lastrowid,),
    )

    linha = ligacao.execute("SELECT estado, custo_centimos, ficheiro FROM criativos").fetchone()
    assert tuple(linha) == ("em_preparacao", None, "")


def test_pasta_dos_ficheiros_fica_na_pasta_de_dados(monkeypatch, tmp_path):
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(tmp_path))

    assert config.pasta_ficheiros() == tmp_path / "ficheiros"


def _campanha(ligacao, contas):
    """Cria uma campanha sem budget e devolve o número dela."""
    cursor = ligacao.execute(
        "INSERT INTO campanhas (nome, cliente_id, marketeer_id, criada_em) VALUES ('Natal', ?, ?, '2026-11-18')",
        (contas["cliente"].id, contas["marketeer"].id),
    )
    return cursor.lastrowid


def test_pedido_de_budget_comeca_pendente_e_sem_parecer(ligacao, contas):
    campanha_id = _campanha(ligacao, contas)
    ligacao.execute(
        "INSERT INTO pedidos_budget (campanha_id, budget_pedido_centimos, motivo, criado_em) "
        "VALUES (?, 200000, 'Mais anúncios', '2026-11-18 10:00:00')",
        (campanha_id,),
    )

    linha = ligacao.execute(
        "SELECT estado, budget_atual_centimos, parecer_viavel, parecer_justificacao, decidido_em FROM pedidos_budget"
    ).fetchone()
    assert tuple(linha) == ("pendente", None, None, "", None)


def test_pedido_de_budget_tem_de_ter_uma_campanha_que_existe(ligacao):
    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute(
            "INSERT INTO pedidos_budget (campanha_id, budget_pedido_centimos, motivo, criado_em) "
            "VALUES (999, 200000, 'Mais anúncios', '2026-11-18 10:00:00')"
        )


@pytest.mark.parametrize(("coluna", "valor"), [("estado", "perdido"), ("parecer_viavel", 2)])
def test_pedido_de_budget_so_aceita_valores_previstos(ligacao, contas, coluna, valor):
    campanha_id = _campanha(ligacao, contas)

    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute(
            f"INSERT INTO pedidos_budget (campanha_id, budget_pedido_centimos, motivo, criado_em, {coluna}) "
            "VALUES (?, 200000, 'Mais anúncios', '2026-11-18 10:00:00', ?)",
            (campanha_id, valor),
        )


def test_apagar_uma_campanha_apaga_os_pedidos_de_budget_dela(ligacao, contas):
    campanha_id = _campanha(ligacao, contas)
    ligacao.execute(
        "INSERT INTO pedidos_budget (campanha_id, budget_pedido_centimos, motivo, criado_em) "
        "VALUES (?, 200000, 'Mais anúncios', '2026-11-18 10:00:00')",
        (campanha_id,),
    )

    ligacao.execute("DELETE FROM campanhas WHERE id = ?", (campanha_id,))

    assert ligacao.execute("SELECT COUNT(*) FROM pedidos_budget").fetchone()[0] == 0


def test_alteracao_de_budget_pode_nao_ter_valor_anterior_nem_pedido(ligacao, contas):
    campanha_id = _campanha(ligacao, contas)
    ligacao.execute(
        "INSERT INTO alteracoes_budget (campanha_id, budget_novo_centimos, motivo, alterado_em) "
        "VALUES (?, 150000, 'Budget inicial', '2026-11-18 10:00:00')",
        (campanha_id,),
    )

    linha = ligacao.execute("SELECT budget_anterior_centimos, pedido_budget_id FROM alteracoes_budget").fetchone()
    assert tuple(linha) == (None, None)


def test_alteracao_de_budget_tem_de_ter_uma_campanha_que_existe(ligacao):
    with pytest.raises(sqlite3.IntegrityError):
        ligacao.execute(
            "INSERT INTO alteracoes_budget (campanha_id, budget_novo_centimos, motivo, alterado_em) "
            "VALUES (999, 150000, 'Budget inicial', '2026-11-18 10:00:00')"
        )


def test_apagar_uma_campanha_apaga_o_historico_do_budget_dela(ligacao, contas):
    campanha_id = _campanha(ligacao, contas)
    ligacao.execute(
        "INSERT INTO alteracoes_budget (campanha_id, budget_novo_centimos, motivo, alterado_em) "
        "VALUES (?, 150000, 'Budget inicial', '2026-11-18 10:00:00')",
        (campanha_id,),
    )

    ligacao.execute("DELETE FROM campanhas WHERE id = ?", (campanha_id,))

    assert ligacao.execute("SELECT COUNT(*) FROM alteracoes_budget").fetchone()[0] == 0


def _criativo(ligacao, contas):
    """Cria uma campanha com um criativo e devolve o número do criativo."""
    cursor = ligacao.execute(
        "INSERT INTO criativos (campanha_id, nome, criado_em) VALUES (?, 'Banner', '2026-11-19 10:00:00')",
        (_campanha(ligacao, contas),),
    )
    return cursor.lastrowid


def _comentar(ligacao, criativo_id, autor_id, resposta_a=None):
    """Acrescenta um comentário a um criativo e devolve o número do comentário."""
    cursor = ligacao.execute(
        "INSERT INTO comentarios (criativo_id, autor_id, texto, resposta_a, criado_em) "
        "VALUES (?, ?, 'O logótipo devia ser maior', ?, '2026-11-19 10:00:00')",
        (criativo_id, autor_id, resposta_a),
    )
    return cursor.lastrowid


def test_comentario_tem_de_ter_um_criativo_que_existe(ligacao, contas):
    with pytest.raises(sqlite3.IntegrityError):
        _comentar(ligacao, 999, contas["cliente"].id)


def test_comentario_tem_de_ter_um_autor_que_existe(ligacao, contas):
    criativo_id = _criativo(ligacao, contas)

    with pytest.raises(sqlite3.IntegrityError):
        _comentar(ligacao, criativo_id, 999)


def test_apagar_um_criativo_apaga_os_comentarios_e_as_respostas(ligacao, contas):
    criativo_id = _criativo(ligacao, contas)
    comentario_id = _comentar(ligacao, criativo_id, contas["cliente"].id)
    _comentar(ligacao, criativo_id, contas["marketeer"].id, resposta_a=comentario_id)

    ligacao.execute("DELETE FROM criativos WHERE id = ?", (criativo_id,))

    assert ligacao.execute("SELECT COUNT(*) FROM comentarios").fetchone()[0] == 0
