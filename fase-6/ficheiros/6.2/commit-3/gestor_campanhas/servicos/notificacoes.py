"""Notificações: avisos na plataforma e por email.

Quando acontece algo que interessa a alguém (uma campanha nova, um pedido
de budget, a decisão de um pedido, um criativo novo ou alterado, um
comentário), quem está interessado recebe uma notificação. A notificação
fica guardada, para aparecer na opção "Notificações" do menu, e é também
enviada por email (para a caixa de saída, ver
:mod:`gestor_campanhas.servicos.correio`).

Cada notificação indica o item a que se refere, para se poder abri-lo
diretamente a partir da lista.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Notificacao, Utilizador
from gestor_campanhas.repositorios import notificacoes
from gestor_campanhas.servicos import correio

#: Última linha do email de cada notificação: onde se encontra o item no
#: menu de quem a recebe. A chave é o par ``(sobre, perfil)``.
ONDE = {
    (modelos.SOBRE_CAMPANHA, modelos.MARKETEER): 'Pode consultá-la na opção "Campanhas" do seu menu.',
    (modelos.SOBRE_CAMPANHA, modelos.CLIENTE): 'Pode consultá-la na opção "Campanhas" do seu menu.',
    (modelos.SOBRE_PEDIDO_BUDGET, modelos.MARKETEER): 'Pode dar o parecer na opção "Pedidos de budget" do seu menu.',
    (modelos.SOBRE_PEDIDO_BUDGET, modelos.CLIENTE): 'Pode consultá-lo na opção "Pedidos de campanha" do seu menu.',
    (modelos.SOBRE_CRIATIVO, modelos.MARKETEER): 'Pode consultá-lo na opção "Criativos" do seu menu.',
    (modelos.SOBRE_CRIATIVO, modelos.CLIENTE): 'Pode consultá-lo na opção "Criativos" do seu menu.',
}


def notificar(
    ligacao: sqlite3.Connection, destinatario: Utilizador, assunto: str, texto: str, sobre: str, item_id: int
) -> Notificacao:
    """Guarda uma notificação para um utilizador e envia-lhe o mesmo aviso por email.

    :param ligacao: Ligação aberta à base de dados.
    :param destinatario: Quem recebe a notificação.
    :param assunto: Assunto do email.
    :param texto: O que aconteceu, numa frase. É o texto da notificação e o
        corpo do email.
    :param sobre: :data:`~gestor_campanhas.modelos.SOBRE_CAMPANHA`,
        :data:`~gestor_campanhas.modelos.SOBRE_PEDIDO_BUDGET` ou
        :data:`~gestor_campanhas.modelos.SOBRE_CRIATIVO`.
    :param item_id: Número da campanha, do pedido ou do criativo.
    :return: A notificação guardada.
    """
    notificacao = notificacoes.criar(ligacao, destinatario.id, texto, sobre, item_id)
    onde = ONDE.get((sobre, destinatario.perfil), "")
    correio.enviar(destinatario.email, assunto, f"Olá, {destinatario.nome}.\n\n{texto}\n{onde}".rstrip())
    return notificacao


def listar(ligacao: sqlite3.Connection, utilizador: Utilizador) -> list[Notificacao]:
    """Lista as notificações de um utilizador, lidas e por ler.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que está a consultar.
    :return: Notificações, da mais recente para a mais antiga.
    """
    return notificacoes.listar_por_utilizador(ligacao, utilizador.id)


def contar_por_ler(ligacao: sqlite3.Connection, utilizador: Utilizador) -> int:
    """Conta as notificações que o utilizador ainda não abriu.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador a consultar.
    :return: Número de notificações por ler.
    """
    return notificacoes.contar_por_ler(ligacao, utilizador.id)


def abrir(ligacao: sqlite3.Connection, utilizador: Utilizador, identificador: int) -> Notificacao:
    """Procura uma notificação do utilizador e marca-a como lida.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que está a abrir a notificação.
    :param identificador: Número da notificação.
    :return: A notificação, já lida.
    :raises ErroValidacao: Se o utilizador não tiver nenhuma notificação com
        esse número.
    """
    notificacao = notificacoes.obter_por_id(ligacao, identificador)
    if notificacao is None or notificacao.utilizador_id != utilizador.id:
        raise ErroValidacao(f"Não tem nenhuma notificação com o número {identificador}.")
    if notificacao.lida:
        return notificacao
    return notificacoes.marcar_como_lida(ligacao, notificacao.id)


def marcar_todas_como_lidas(ligacao: sqlite3.Connection, utilizador: Utilizador) -> int:
    """Marca como lidas todas as notificações do utilizador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador cujas notificações se marcam.
    :return: Número de notificações que estavam por ler.
    """
    return notificacoes.marcar_todas_como_lidas(ligacao, utilizador.id)
