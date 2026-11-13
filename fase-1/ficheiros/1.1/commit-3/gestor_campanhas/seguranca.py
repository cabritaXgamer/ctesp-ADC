"""Proteção das passwords.

A aplicação nunca guarda uma password. Guarda um *hash*: o resultado de uma
conta que se faz num só sentido, a partir do qual não é possível recuperar a
password. Para confirmar uma password, repete-se a conta e comparam-se os
resultados.

Cada hash usa um *salt*, um valor aleatório diferente para cada conta. Por
causa dele, duas pessoas com a mesma password ficam com hashes diferentes.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

#: Nome do algoritmo, guardado junto do hash.
ALGORITMO = "pbkdf2_sha256"

#: Número de repetições da conta. Quanto maior, mais lento é adivinhar
#: passwords por tentativas. Os testes usam um valor baixo para serem rápidos.
ITERACOES = 200_000

#: Número mínimo de caracteres de uma password.
TAMANHO_MINIMO = 8


def gerar_hash(password: str) -> str:
    """Calcula o hash de uma password, com um salt novo.

    :param password: Password em texto.
    :return: Texto no formato ``algoritmo$iterações$salt$hash``, pronto a
        guardar na base de dados.
    """
    salt = secrets.token_hex(16)
    resumo = _calcular(password, salt, ITERACOES)
    return f"{ALGORITMO}${ITERACOES}${salt}${resumo}"


def verificar_password(password: str, guardado: str) -> bool:
    """Confirma se uma password corresponde a um hash guardado.

    :param password: Password introduzida.
    :param guardado: Texto devolvido por :func:`gerar_hash`.
    :return: ``True`` se a password estiver certa.
    """
    try:
        algoritmo, iteracoes, salt, resumo = guardado.split("$")
    except ValueError:
        return False
    if algoritmo != ALGORITMO or not iteracoes.isdigit():
        return False
    calculado = _calcular(password, salt, int(iteracoes))
    # compare_digest demora sempre o mesmo tempo, quer os textos sejam
    # parecidos quer não, para não dar pistas a quem tenta adivinhar.
    return hmac.compare_digest(calculado, resumo)


def _calcular(password: str, salt: str, iteracoes: int) -> str:
    """Faz a conta do hash e devolve o resultado em hexadecimal."""
    dados = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iteracoes)
    return dados.hex()
