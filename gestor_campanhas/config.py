"""Configuração da aplicação.

Reúne num só sítio os caminhos usados pela aplicação.

Por omissão, os dados ficam na pasta ``dados`` dentro da pasta do projeto.
Para usar outra pasta (por exemplo numa demonstração ou nos testes), basta
definir a variável de ambiente ``GESTOR_CAMPANHAS_DADOS`` antes de arrancar
a aplicação.
"""

import os
from pathlib import Path

#: Nome da variável de ambiente que indica a pasta de dados.
VARIAVEL_PASTA_DADOS = "GESTOR_CAMPANHAS_DADOS"

#: Pasta raiz do projeto (a que contém o pacote ``gestor_campanhas``).
PASTA_PROJETO = Path(__file__).resolve().parent.parent

#: Nome do ficheiro da base de dados, dentro da pasta de dados.
NOME_FICHEIRO_BD = "app.db"


def pasta_dados() -> Path:
    """Devolve a pasta onde a aplicação guarda os seus dados.

    A variável de ambiente ``GESTOR_CAMPANHAS_DADOS`` tem prioridade. Se não
    estiver definida, usa-se a pasta ``dados`` dentro da pasta do projeto.

    :return: Caminho da pasta de dados. A pasta pode ainda não existir.
    """
    definida = os.environ.get(VARIAVEL_PASTA_DADOS)
    if definida:
        return Path(definida)
    return PASTA_PROJETO / "dados"


def ficheiro_bd() -> Path:
    """Devolve o caminho do ficheiro da base de dados SQLite.

    :return: Caminho do ficheiro ``app.db`` dentro da pasta de dados.
    """
    return pasta_dados() / NOME_FICHEIRO_BD
