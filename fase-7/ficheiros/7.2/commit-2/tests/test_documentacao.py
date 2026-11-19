"""Testes da documentação do código.

A referência da documentação (Sphinx) é gerada a partir dos docstrings. Estes
testes confirmam que nenhum módulo, classe ou função fica sem docstring, que
as funções públicas descrevem todos os parâmetros e o que devolvem, e que
todos os módulos aparecem na página de referência.
"""

import ast
import re
from pathlib import Path

import pytest

from gestor_campanhas import config

#: Pasta do código da aplicação.
PACOTE = config.PASTA_PROJETO / "gestor_campanhas"

#: Página da documentação com a referência do código.
REFERENCIA = config.PASTA_PROJETO / "docs" / "referencia.rst"

#: Ficheiros do código da aplicação, incluindo os dos subpacotes.
FICHEIROS = sorted(PACOTE.rglob("*.py"))


def nome_do_modulo(ficheiro: Path) -> str:
    """Converte o caminho de um ficheiro no nome do módulo, por exemplo ``gestor_campanhas.cli.comum``."""
    partes = ficheiro.relative_to(config.PASTA_PROJETO).with_suffix("").parts
    if partes[-1] == "__init__":
        partes = partes[:-1]
    return ".".join(partes)


def arvore(ficheiro: Path) -> ast.Module:
    """Lê um ficheiro de código e devolve a sua árvore sintática."""
    return ast.parse(ficheiro.read_text(encoding="utf-8"))


def funcoes_e_classes(modulo: ast.Module):
    """Percorre todas as funções e classes de um módulo, incluindo as que estão dentro de outras."""
    for no in ast.walk(modulo):
        if isinstance(no, (ast.FunctionDef, ast.ClassDef)):
            yield no


def funcoes_publicas(modulo: ast.Module):
    """Percorre as funções públicas do módulo e os métodos públicos das suas classes.

    As funções definidas dentro de outras funções ficam de fora: servem só
    a função onde estão e não aparecem na documentação.
    """
    for no in modulo.body:
        corpo = no.body if isinstance(no, ast.ClassDef) else [no]
        for funcao in corpo:
            if isinstance(funcao, ast.FunctionDef) and not funcao.name.startswith("_"):
                yield funcao


def e_propriedade(funcao: ast.FunctionDef) -> bool:
    """Diz se uma função é uma propriedade (``@property``), que se documenta só com uma frase."""
    return any(isinstance(d, ast.Name) and d.id == "property" for d in funcao.decorator_list)


@pytest.mark.parametrize("ficheiro", FICHEIROS, ids=nome_do_modulo)
def test_modulo_classes_e_funcoes_tem_docstring(ficheiro):
    modulo = arvore(ficheiro)

    em_falta = [no.name for no in funcoes_e_classes(modulo) if not ast.get_docstring(no)]

    assert ast.get_docstring(modulo), "o módulo não tem docstring"
    assert em_falta == []


@pytest.mark.parametrize("ficheiro", FICHEIROS, ids=nome_do_modulo)
def test_funcoes_publicas_descrevem_os_parametros_e_o_resultado(ficheiro):
    problemas = []
    for no in funcoes_publicas(arvore(ficheiro)):
        if e_propriedade(no):
            continue
        docstring = ast.get_docstring(no) or ""
        parametros = [a.arg for a in no.args.args + no.args.kwonlyargs if a.arg not in ("self", "cls")]
        for parametro in parametros:
            if f":param {parametro}:" not in docstring:
                problemas.append(f"{no.name}: falta :param {parametro}:")
        devolve_nada = no.returns is None or (isinstance(no.returns, ast.Constant) and no.returns.value is None)
        if not devolve_nada and ":return:" not in docstring:
            problemas.append(f"{no.name}: falta :return:")

    assert problemas == []


def test_referencia_inclui_todos_os_modulos():
    na_referencia = set(re.findall(r"^\.\. automodule:: (\S+)$", REFERENCIA.read_text(encoding="utf-8"), re.MULTILINE))

    assert {nome_do_modulo(ficheiro) for ficheiro in FICHEIROS} == na_referencia
