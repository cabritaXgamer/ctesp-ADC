"""Regras dos pedidos de nova campanha.

Um cliente pede uma campanha indicando o objetivo, o orçamento, o prazo e as
plataformas. O pedido começa no estado pendente; enquanto estiver pendente, o
cliente pode cancelá-lo.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import dinheiro, modelos, relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import PedidoCampanha, Utilizador
from gestor_campanhas.repositorios import pedidos
from gestor_campanhas.servicos import validacao


def _plataformas_validadas(escolhidas: list[str]) -> list[str]:
    """Confirma as plataformas escolhidas e devolve-as sem repetições, pela ordem dos menus."""
    desconhecidas = [nome for nome in escolhidas if nome not in modelos.PLATAFORMAS]
    if desconhecidas:
        raise ErroValidacao(f"A plataforma {desconhecidas[0]} não existe.")
    if not escolhidas:
        raise ErroValidacao("Escolha pelo menos uma plataforma.")
    return [nome for nome in modelos.PLATAFORMAS if nome in escolhidas]


def criar(
    ligacao: sqlite3.Connection,
    cliente: Utilizador,
    objetivo: str,
    orcamento: str,
    prazo: str,
    plataformas: list[str],
) -> PedidoCampanha:
    """Regista um pedido de nova campanha, no estado pendente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    :param objetivo: O que pretende com a campanha. Obrigatório.
    :param orcamento: Quanto quer investir, em euros, tal como foi escrito
        (por exemplo ``"1500"`` ou ``"1500,50"``). Tem de ser maior do que zero.
    :param prazo: Dia até ao qual quer a campanha, no formato ``AAAA-MM-DD``.
        Obrigatório; não pode ser um dia que já passou.
    :param plataformas: Nomes das plataformas onde quer anunciar, de
        :data:`~gestor_campanhas.modelos.PLATAFORMAS`. Pelo menos uma.
    :return: O pedido criado.
    :raises ErroValidacao: Se algum dos valores não respeitar as regras.
    """
    objetivo = objetivo.strip()
    if not objetivo:
        raise ErroValidacao("O objetivo não pode ficar vazio.")
    centimos = dinheiro.para_centimos(orcamento)
    if centimos <= 0:
        raise ErroValidacao("O orçamento tem de ser maior do que zero.")
    dia = validacao.data(prazo, "data do prazo")
    if dia is None:
        raise ErroValidacao("O prazo não pode ficar vazio.")
    if dia < relogio.hoje():
        raise ErroValidacao("O prazo não pode ser um dia que já passou.")
    return pedidos.criar(ligacao, cliente.id, objetivo, centimos, dia, _plataformas_validadas(plataformas))


def listar_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> list[PedidoCampanha]:
    """Lista os pedidos feitos por um cliente, em qualquer estado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :return: Pedidos desse cliente, do mais recente para o mais antigo.
    """
    return pedidos.listar_por_cliente(ligacao, cliente.id)


def obter_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoCampanha:
    """Procura um pedido pelo número, confirmando que é do cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :param identificador: Número do pedido, mostrado na primeira coluna da lista.
    :return: O pedido.
    :raises ErroValidacao: Se o cliente não tiver nenhum pedido com esse número.
    """
    pedido = pedidos.obter_por_id(ligacao, identificador)
    if pedido is None or pedido.cliente_id != cliente.id:
        raise ErroValidacao(f"Não tem nenhum pedido com o número {identificador}.")
    return pedido


def cancelar(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoCampanha:
    """Cancela um pedido do cliente que ainda esteja pendente.

    O pedido não é apagado: fica na lista, com o estado cancelado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a cancelar.
    :param identificador: Número do pedido.
    :return: O pedido, já cancelado.
    :raises ErroValidacao: Se o pedido não for do cliente ou já não estiver pendente.
    """
    pedido = obter_do_cliente(ligacao, cliente, identificador)
    if pedido.estado != modelos.PENDENTE:
        raise ErroValidacao(
            f"Só é possível cancelar um pedido pendente. Este pedido está no estado {pedido.nome_estado}."
        )
    return pedidos.definir_estado(ligacao, pedido.id, modelos.CANCELADO)
