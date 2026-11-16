"""Validação dos dados escritos pelo utilizador.

Cada função recebe um valor tal como foi escrito, confirma que respeita as
regras e devolve-o já arrumado (sem espaços a mais). Se não respeitar, lança
:class:`~gestor_campanhas.erros.ErroValidacao` com a mensagem a mostrar.

As mesmas regras valem quando é o próprio a alterar os seus dados e quando é
o Administrador a criar ou a editar uma conta. As datas são usadas nas
campanhas.
"""

from __future__ import annotations

import re
from datetime import date, datetime

from gestor_campanhas.erros import ErroValidacao

#: Forma mínima de um email: texto, ``@``, texto, ponto, texto, sem espaços.
_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def nome(valor: str) -> str:
    """Valida um nome.

    :param valor: Nome escrito.
    :return: O nome, sem espaços no início e no fim.
    :raises ErroValidacao: Se ficar vazio.
    """
    valor = valor.strip()
    if not valor:
        raise ErroValidacao("O nome não pode ficar vazio.")
    return valor


def email(valor: str) -> str:
    """Valida um email.

    :param valor: Email escrito.
    :return: O email, sem espaços à volta e em minúsculas.
    :raises ErroValidacao: Se não tiver a forma ``nome@dominio.algo``.
    """
    valor = valor.strip().lower()
    if not _EMAIL.fullmatch(valor):
        raise ErroValidacao("O email não é válido. Exemplo de um email válido: nome@empresa.pt.")
    return valor


def telefone(valor: str) -> str:
    """Valida um telefone. Pode ficar vazio.

    :param valor: Telefone escrito, com ou sem espaços.
    :return: O telefone sem espaços.
    :raises ErroValidacao: Se não estiver vazio nem tiver 9 a 15 algarismos,
        com ou sem ``+`` no início.
    """
    valor = valor.replace(" ", "")
    algarismos = valor[1:] if valor.startswith("+") else valor
    if valor and not (algarismos.isdigit() and 9 <= len(algarismos) <= 15):
        raise ErroValidacao("O telefone tem de ter entre 9 e 15 algarismos.")
    return valor


def nif(valor: str) -> str:
    """Valida um número de contribuinte. Pode ficar vazio.

    :param valor: NIF escrito, com ou sem espaços.
    :return: O NIF sem espaços.
    :raises ErroValidacao: Se não estiver vazio nem tiver 9 algarismos.
    """
    valor = valor.replace(" ", "")
    if valor and not (valor.isdigit() and len(valor) == 9):
        raise ErroValidacao("O NIF tem de ter 9 algarismos.")
    return valor


def data(valor: str, campo: str = "data") -> date | None:
    """Valida uma data escrita no formato ``AAAA-MM-DD``. Pode ficar vazia.

    :param valor: Data escrita.
    :param campo: Nome do campo, para a mensagem de erro (por exemplo ``"data de fim"``).
    :return: A data, ou ``None`` se o valor estiver vazio.
    :raises ErroValidacao: Se não estiver vazio nem for uma data que existe.
    """
    valor = valor.strip()
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        raise ErroValidacao(f"A {campo} não é válida. Exemplo de uma data válida: 2026-11-30.") from None


def periodo(inicio: date | None, fim: date | None) -> None:
    """Confirma que um período não acaba antes de começar.

    :param inicio: Primeiro dia, ou ``None``.
    :param fim: Último dia, ou ``None``.
    :raises ErroValidacao: Se as duas datas existirem e a de fim for anterior à de início.
    """
    if inicio and fim and fim < inicio:
        raise ErroValidacao("A data de fim não pode ser anterior à data de início.")
