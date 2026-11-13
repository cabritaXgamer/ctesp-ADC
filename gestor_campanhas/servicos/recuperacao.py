"""Recuperação da password por quem a esqueceu.

Faz-se em dois passos. Primeiro pede-se um código, que é enviado para o email
da conta. Depois, com o email e o código, define-se uma password nova.

Numa aplicação web seria enviado um link. Na linha de comandos não há onde
clicar, por isso o link é substituído por um código de seis algarismos, com o
mesmo efeito: prova que quem pede tem acesso ao email da conta, e só vale
durante algum tempo.
"""

from __future__ import annotations

import secrets
import sqlite3
from datetime import timedelta

from gestor_campanhas import config, relogio, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import recuperacoes, utilizadores
from gestor_campanhas.servicos import contas, correio

#: Mensagem mostrada quando o código não pode ser usado. É sempre a mesma,
#: para não revelar se o email tem conta nem porque é que o código falhou.
MENSAGEM_CODIGO = "O código não é válido ou já passou do prazo."


def gerar_codigo() -> str:
    """Gera um código aleatório de seis algarismos.

    :return: O código, como texto, com zeros à esquerda se for preciso.
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def pedir_codigo(ligacao: sqlite3.Connection, email: str) -> None:
    """Envia um código de recuperação para o email indicado, se tiver conta ativa.

    Não devolve nada nem lança erros: quem pede não fica a saber se o email
    tem conta. Um pedido novo anula os códigos anteriores da mesma conta.

    :param ligacao: Ligação aberta à base de dados.
    :param email: Email da conta a recuperar.
    """
    utilizador = utilizadores.obter_por_email(ligacao, email)
    if utilizador is None or not utilizador.ativo:
        return
    codigo = gerar_codigo()
    expira_em = relogio.agora() + timedelta(minutes=config.MINUTOS_VALIDADE_CODIGO)
    recuperacoes.criar(ligacao, utilizador.id, seguranca.gerar_hash(codigo), expira_em)
    correio.enviar(
        utilizador.email,
        "Recuperação da password",
        f"Olá, {utilizador.nome}.\n\n"
        f"O código para definir uma password nova é: {codigo}\n\n"
        f"O código é válido durante {config.MINUTOS_VALIDADE_CODIGO} minutos e só pode ser usado uma vez.\n"
        "Se não pediu a recuperação da password, ignore esta mensagem.",
    )


def repor_password(ligacao: sqlite3.Connection, email: str, codigo: str, nova: str, confirmacao: str) -> None:
    """Define uma password nova, depois de confirmar o código recebido por email.

    :param ligacao: Ligação aberta à base de dados.
    :param email: Email da conta.
    :param codigo: Código recebido por email.
    :param nova: Password nova.
    :param confirmacao: Password nova, escrita segunda vez.
    :raises ErroValidacao: Se o código não for válido ou estiver fora de
        prazo, se a password não respeitar as regras ou se a confirmação for
        diferente.
    """
    utilizador = utilizadores.obter_por_email(ligacao, email)
    pedido = recuperacoes.obter_ativa(ligacao, utilizador.id, relogio.agora()) if utilizador else None
    if pedido is None:
        raise ErroValidacao(MENSAGEM_CODIGO)
    identificador, codigo_hash = pedido
    if not seguranca.verificar_password(codigo.strip(), codigo_hash):
        raise ErroValidacao(MENSAGEM_CODIGO)
    contas.validar_password(nova)
    if nova != confirmacao:
        raise ErroValidacao("A confirmação não é igual à password nova.")
    utilizadores.atualizar_password(ligacao, utilizador.id, seguranca.gerar_hash(nova))
    recuperacoes.marcar_usada(ligacao, identificador)
