"""Regras dos comentários dos criativos.

O cliente comenta os criativos das suas campanhas, para dizer ao marketeer o
que quer que mude. O marketeer responsável pela campanha vê os comentários no
detalhe do criativo e responde a cada um.

Um comentário pode ter várias respostas. Uma resposta não tem respostas: para
continuar a conversa, o cliente escreve um comentário novo.

O marketeer recebe uma notificação de cada comentário novo, e o cliente de
cada resposta (ver :mod:`gestor_campanhas.servicos.notificacoes`).
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, Comentario, Criativo, Utilizador
from gestor_campanhas.repositorios import campanhas, comentarios, utilizadores
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.servicos import criativos, notificacoes


def _texto_validado(texto: str) -> str:
    """Confirma que o texto não está vazio e devolve-o sem espaços nas pontas."""
    texto = texto.strip()
    if not texto:
        raise ErroValidacao("O texto não pode ficar vazio.")
    return texto


def comentar(ligacao: sqlite3.Connection, cliente: Utilizador, criativo_id: int, texto: str) -> Comentario:
    """Guarda um comentário do cliente sobre um criativo de uma campanha dele.

    O criativo pode estar em qualquer estado. O marketeer responsável pela
    campanha é notificado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a comentar.
    :param criativo_id: Número do criativo.
    :param texto: O comentário ou a sugestão. Obrigatório.
    :return: O comentário guardado.
    :raises ErroValidacao: Se o criativo não for de uma campanha do cliente
        ou se o texto ficar vazio.
    """
    criativo = criativos.obter_do_cliente(ligacao, cliente, criativo_id)
    comentario = comentarios.criar(ligacao, criativo.id, cliente.id, _texto_validado(texto))
    campanha = campanhas.obter_por_id(ligacao, criativo.campanha_id)
    notificacoes.notificar(
        ligacao,
        utilizadores.obter_por_id(ligacao, campanha.marketeer_id),
        "Novo comentário a um criativo",
        f"{cliente.nome} comentou o criativo {criativo.nome}, da campanha {criativo.campanha_nome}: "
        f"{comentario.texto}",
        modelos.SOBRE_CRIATIVO,
        criativo.id,
    )
    return comentario


def obter_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> Comentario:
    """Procura um comentário pelo número, confirmando que é de um criativo do marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :param identificador: Número do comentário.
    :return: O comentário.
    :raises ErroValidacao: Se não houver nenhum comentário com esse número
        nos criativos das campanhas do marketeer.
    """
    comentario = comentarios.obter_por_id(ligacao, identificador)
    if comentario is not None:
        try:
            criativos.obter_do_marketeer(ligacao, marketeer, comentario.criativo_id)
        except ErroValidacao:
            pass
        else:
            return comentario
    raise ErroValidacao(f"Não há nenhum comentário com o número {identificador} nos seus criativos.")


def responder(ligacao: sqlite3.Connection, marketeer: Utilizador, comentario_id: int, texto: str) -> Comentario:
    """Guarda a resposta do marketeer a um comentário do cliente.

    Quem escreveu o comentário é notificado.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer responsável pela campanha do criativo.
    :param comentario_id: Número do comentário a que responde.
    :param texto: A resposta. Obrigatória.
    :return: A resposta guardada.
    :raises ErroValidacao: Se o comentário não for de um criativo do
        marketeer, se for ele próprio uma resposta, ou se o texto ficar vazio.
    """
    comentario = obter_do_marketeer(ligacao, marketeer, comentario_id)
    if comentario.resposta_a is not None:
        raise ErroValidacao("Só se pode responder a um comentário do cliente, e não a uma resposta.")
    resposta = comentarios.criar(ligacao, comentario.criativo_id, marketeer.id, _texto_validado(texto), comentario.id)
    criativo = criativos_bd.obter_por_id(ligacao, comentario.criativo_id)
    notificacoes.notificar(
        ligacao,
        utilizadores.obter_por_id(ligacao, comentario.autor_id),
        "Resposta ao seu comentário",
        f"{marketeer.nome} respondeu ao seu comentário sobre o criativo {criativo.nome}: {resposta.texto}",
        modelos.SOBRE_CRIATIVO,
        criativo.id,
    )
    return resposta


def conversa(ligacao: sqlite3.Connection, criativo: Criativo) -> list[tuple[Comentario, list[Comentario]]]:
    """Arruma os comentários de um criativo, cada um com as suas respostas.

    :param ligacao: Ligação aberta à base de dados.
    :param criativo: Criativo a consultar.
    :return: Lista de pares ``(comentário, respostas)``, pela ordem em que os
        comentários foram escritos; as respostas de cada um também vêm por
        ordem.
    """
    todos = comentarios.listar_por_criativo(ligacao, criativo.id)
    respostas: dict[int, list[Comentario]] = {}
    for comentario in todos:
        if comentario.resposta_a is not None:
            respostas.setdefault(comentario.resposta_a, []).append(comentario)
    return [(comentario, respostas.get(comentario.id, [])) for comentario in todos if comentario.resposta_a is None]


def por_responder(ligacao: sqlite3.Connection, campanha: Campanha) -> dict[int, int]:
    """Conta os comentários sem resposta em cada criativo de uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha: Campanha a consultar.
    :return: Dicionário do número do criativo para o número de comentários
        do cliente que ainda não têm resposta. Os criativos sem comentários
        por responder não aparecem.
    """
    totais = {}
    for criativo in criativos_bd.listar_por_campanha(ligacao, campanha.id):
        sem_resposta = sum(1 for _, respostas in conversa(ligacao, criativo) if not respostas)
        if sem_resposta:
            totais[criativo.id] = sem_resposta
    return totais

