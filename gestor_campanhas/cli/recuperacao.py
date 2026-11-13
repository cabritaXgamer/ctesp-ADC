"""Recuperação da password, a partir do menu inicial."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import config
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.servicos import recuperacao


def recuperar(ligacao: sqlite3.Connection) -> None:
    """Pede o email, envia o código e, com o código, define uma password nova.

    A mensagem depois de pedir o código é sempre a mesma, exista ou não uma
    conta com esse email. Quem não tiver o código pode sair deixando-o em
    branco.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Recuperar a password")
    email = comum.ler_texto("Email da conta")
    recuperacao.pedir_codigo(ligacao, email)
    print("\nSe existir uma conta com esse email, foi enviado um código de 6 algarismos.")
    print(f"O código é válido durante {config.MINUTOS_VALIDADE_CODIGO} minutos.")
    print(f"Nesta aplicação os emails são ficheiros de texto na pasta:\n  {config.pasta_caixa_saida()}\n")
    codigo = comum.ler_texto("Código (Enter para desistir)", obrigatorio=False)
    if not codigo:
        print("A password não foi alterada.")
        comum.pausa()
        return
    nova = comum.ler_password("Password nova")
    confirmacao = comum.ler_password("Repita a password nova")
    try:
        recuperacao.repor_password(ligacao, email, codigo, nova, confirmacao)
    except ErroValidacao as erro:
        print(f"\n{erro} A password não foi alterada.")
    else:
        print("\nPassword alterada. Já pode entrar com a password nova.")
    comum.pausa()
