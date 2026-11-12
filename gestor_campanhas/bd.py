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
