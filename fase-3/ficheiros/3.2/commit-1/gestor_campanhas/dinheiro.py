"""Valores em euros.

A aplicação guarda o dinheiro em cêntimos, como números inteiros. Com números
decimais as contas podem dar resultados inesperados (em Python,
``0.1 + 0.2`` não dá exatamente ``0.3``); com cêntimos inteiros dão sempre
certo.

Este módulo converte o que o utilizador escreve em cêntimos e os cêntimos no
texto que é mostrado.
"""

from __future__ import annotations

import re

from gestor_campanhas.erros import ErroValidacao

#: Forma de um valor: euros e, opcionalmente, uma vírgula ou um ponto seguido
#: de um ou dois algarismos dos cêntimos.
_VALOR = re.compile(r"(\d+)(?:[.,](\d{1,2}))?")


def para_centimos(texto: str) -> int:
    """Converte um valor escrito em euros no número de cêntimos.

    Aceita ``1500``, ``1500,5``, ``1500.50``, ``1 500,50`` e ``1500 €``.

    :param texto: Valor tal como foi escrito.
    :return: O valor em cêntimos. ``"1500,50"`` dá ``150050``.
    :raises ErroValidacao: Se o texto não for um valor em euros.
    """
    limpo = texto.replace("€", "").replace(" ", "")
    encontrado = _VALOR.fullmatch(limpo)
    if not encontrado:
        raise ErroValidacao("O valor não é válido. Exemplos de valores válidos: 1500 ou 1500,50.")
    euros, centimos = encontrado.groups()
    # "1500,5" são 50 cêntimos, e não 5: completa-se com um zero à direita.
    return int(euros) * 100 + int((centimos or "0").ljust(2, "0"))


def formatar(centimos: int) -> str:
    """Escreve um valor em cêntimos como é mostrado ao utilizador.

    :param centimos: Valor em cêntimos.
    :return: O valor em euros, com os milhares separados por um espaço e duas
        casas decimais. ``150050`` dá ``"1 500,50 €"``.
    """
    euros, resto = divmod(centimos, 100)
    milhares = f"{euros:,}".replace(",", " ")
    return f"{milhares},{resto:02d} €"
