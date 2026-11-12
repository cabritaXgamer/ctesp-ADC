"""Configuração do Sphinx para a documentação do Gestor de Campanhas.

Gerar a documentação HTML a partir da pasta do projeto::

    python -m sphinx -b html docs docs/_build/html

Lista completa das opções de configuração:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys

# -- Localização do código ----------------------------------------------------
# O autodoc importa os módulos para ler os docstrings. Como este ficheiro está
# na pasta "docs", é preciso acrescentar a pasta do projeto (a pasta acima) à
# lista de sítios onde o Python procura módulos.
sys.path.insert(0, os.path.abspath(".."))

import gestor_campanhas  # noqa: E402  (tem de vir depois de alterar o sys.path)

# -- Informação do projeto ----------------------------------------------------
project = "Gestor de Campanhas"
author = "Fabio Felgueiras, Tomas Paulo, Ricardo Cabrita"
copyright = f"2026, {author}"
# A versão é lida do próprio código, para nunca ficar desatualizada.
release = gestor_campanhas.__version__
version = release

# -- Configuração geral -------------------------------------------------------
extensions = [
    # Gera a referência do código a partir dos docstrings.
    "sphinx.ext.autodoc",
    # Acrescenta a cada função uma ligação para o respetivo código-fonte.
    "sphinx.ext.viewcode",
]

# Ficheiros e pastas que não fazem parte da documentação.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Língua dos textos gerados pelo Sphinx ("Índice", "Pesquisar", ...).
language = "pt_PT"

# -- Opções do autodoc --------------------------------------------------------
# Mostra os membros pela ordem em que aparecem no código, e não por ordem
# alfabética.
autodoc_member_order = "bysource"

# Opções aplicadas a todas as diretivas "automodule".
autodoc_default_options = {
    # Documenta as funções, classes e constantes de cada módulo.
    "members": True,
    # Inclui também os membros sem docstring, para se notar quando falta um.
    "undoc-members": True,
    # Mostra de que classe herda cada classe.
    "show-inheritance": True,
}

# Mostra os tipos dos parâmetros na descrição e não na assinatura da função,
# que assim fica mais curta e mais fácil de ler.
autodoc_typehints = "description"

# -- Opções da saída HTML -----------------------------------------------------
html_theme = "alabaster"
html_title = f"{project} {release}"
html_theme_options = {
    "description": "Gestão de campanhas de marketing em linha de comandos.",
    "fixed_sidebar": True,
}
