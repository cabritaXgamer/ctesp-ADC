"""Acesso à base de dados SQLite.

Este módulo abre a ligação à base de dados e cria as tabelas.

Os restantes módulos recebem a ligação já aberta e nunca abrem ligações por
conta própria. É isso que permite usar uma base de dados em memória nos
testes, sem tocar nos dados reais.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from gestor_campanhas import config

#: Caminho especial do SQLite para uma base de dados em memória.
#: Os dados desaparecem quando a ligação é fechada, por isso é usada nos testes.
EM_MEMORIA = ":memory:"

#: Instruções SQL que criam as tabelas.
#: Usa-se ``IF NOT EXISTS`` para poderem ser executadas em todos os arranques
#: sem apagar os dados que já existem.
ESQUEMA = """
CREATE TABLE IF NOT EXISTS configuracoes (
    chave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS utilizadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK (perfil IN ('administrador', 'marketeer', 'cliente')),
    ativo INTEGER NOT NULL DEFAULT 1,
    telefone TEXT NOT NULL DEFAULT '',
    empresa TEXT NOT NULL DEFAULT '',
    nif TEXT NOT NULL DEFAULT '',
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilizador_id INTEGER NOT NULL REFERENCES utilizadores (id),
    entrada TEXT NOT NULL,
    saida TEXT,
    motivo_saida TEXT CHECK (motivo_saida IN ('logout', 'inatividade'))
);

CREATE TABLE IF NOT EXISTS recuperacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilizador_id INTEGER NOT NULL REFERENCES utilizadores (id),
    codigo_hash TEXT NOT NULL,
    expira_em TEXT NOT NULL,
    usado INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS campanhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    objetivo TEXT NOT NULL DEFAULT '',
    cliente_id INTEGER NOT NULL REFERENCES utilizadores (id),
    marketeer_id INTEGER NOT NULL REFERENCES utilizadores (id),
    budget_centimos INTEGER,
    data_inicio TEXT,
    data_fim TEXT,
    criada_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos_campanha (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL REFERENCES utilizadores (id),
    objetivo TEXT NOT NULL,
    orcamento_centimos INTEGER NOT NULL,
    prazo TEXT NOT NULL,
    plataformas TEXT NOT NULL DEFAULT '',
    estado TEXT NOT NULL DEFAULT 'pendente'
        CHECK (estado IN ('pendente', 'em_analise', 'aprovado', 'rejeitado', 'cancelado')),
    motivo_rejeicao TEXT NOT NULL DEFAULT '',
    campanha_id INTEGER REFERENCES campanhas (id) ON DELETE SET NULL,
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS criativos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campanha_id INTEGER NOT NULL REFERENCES campanhas (id),
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL DEFAULT '',
    custo_centimos INTEGER,
    prazo TEXT,
    publico_alvo TEXT NOT NULL DEFAULT '',
    plataforma TEXT NOT NULL DEFAULT '',
    estado TEXT NOT NULL DEFAULT 'em_preparacao'
        CHECK (estado IN ('em_preparacao', 'em_revisao', 'aprovado', 'rejeitado', 'publicado')),
    motivo_rejeicao TEXT NOT NULL DEFAULT '',
    ficheiro TEXT NOT NULL DEFAULT '',
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos_budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campanha_id INTEGER NOT NULL REFERENCES campanhas (id) ON DELETE CASCADE,
    budget_atual_centimos INTEGER,
    budget_pedido_centimos INTEGER NOT NULL,
    motivo TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendente'
        CHECK (estado IN ('pendente', 'em_analise', 'aprovado', 'rejeitado', 'cancelado')),
    parecer_viavel INTEGER CHECK (parecer_viavel IN (0, 1)),
    parecer_justificacao TEXT NOT NULL DEFAULT '',
    motivo_rejeicao TEXT NOT NULL DEFAULT '',
    criado_em TEXT NOT NULL,
    decidido_em TEXT
);

CREATE TABLE IF NOT EXISTS alteracoes_budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campanha_id INTEGER NOT NULL REFERENCES campanhas (id) ON DELETE CASCADE,
    budget_anterior_centimos INTEGER,
    budget_novo_centimos INTEGER NOT NULL,
    motivo TEXT NOT NULL,
    pedido_budget_id INTEGER REFERENCES pedidos_budget (id) ON DELETE SET NULL,
    alterado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    criativo_id INTEGER NOT NULL REFERENCES criativos (id) ON DELETE CASCADE,
    autor_id INTEGER NOT NULL REFERENCES utilizadores (id),
    texto TEXT NOT NULL,
    resposta_a INTEGER REFERENCES comentarios (id) ON DELETE CASCADE,
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilizador_id INTEGER NOT NULL REFERENCES utilizadores (id),
    texto TEXT NOT NULL,
    sobre TEXT NOT NULL CHECK (sobre IN ('campanha', 'pedido_budget', 'criativo')),
    item_id INTEGER NOT NULL,
    lida INTEGER NOT NULL DEFAULT 0,
    criada_em TEXT NOT NULL
);
"""


def ligar(caminho: str | Path | None = None) -> sqlite3.Connection:
    """Abre uma ligação à base de dados.

    A ligação fica configurada para:

    * devolver cada linha como :class:`sqlite3.Row`, o que permite ler as
      colunas pelo nome (``linha["chave"]``);
    * verificar as chaves estrangeiras, que o SQLite ignora por omissão.

    :param caminho: Caminho do ficheiro da base de dados. Se for ``None``,
        usa-se o caminho indicado em :func:`gestor_campanhas.config.ficheiro_bd`.
        Para uma base de dados em memória, passar :data:`EM_MEMORIA`.
    :return: Ligação aberta. Quem a pede é responsável por fechá-la.
    """
    if caminho is None:
        caminho = config.ficheiro_bd()
    if str(caminho) != EM_MEMORIA:
        # O SQLite cria o ficheiro, mas não cria a pasta onde ele fica.
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    ligacao = sqlite3.connect(str(caminho))
    ligacao.row_factory = sqlite3.Row
    ligacao.execute("PRAGMA foreign_keys = ON")
    return ligacao


def criar_tabelas(ligacao: sqlite3.Connection) -> None:
    """Cria as tabelas que ainda não existem.

    Pode ser chamada várias vezes sobre a mesma base de dados: as tabelas
    que já existem ficam como estão.

    :param ligacao: Ligação aberta à base de dados.
    """
    ligacao.executescript(ESQUEMA)
    ligacao.commit()


def iniciar_bd(caminho: str | Path | None = None) -> sqlite3.Connection:
    """Abre a ligação e garante que as tabelas existem.

    É a função usada no arranque da aplicação.

    :param caminho: Caminho do ficheiro da base de dados (ver :func:`ligar`).
    :return: Ligação aberta, com as tabelas criadas.
    """
    ligacao = ligar(caminho)
    criar_tabelas(ligacao)
    return ligacao
