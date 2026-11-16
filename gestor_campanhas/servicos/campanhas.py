"""Regras das campanhas.

Uma campanha pertence a um cliente e tem um marketeer responsável. O
marketeer que cria a campanha fica responsável por ela e só pode mexer nas
suas campanhas.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, Utilizador
from gestor_campanhas.repositorios import campanhas, utilizadores
from gestor_campanhas.servicos import gestao, validacao


def clientes_disponiveis(ligacao: sqlite3.Connection) -> list[Utilizador]:
    """Lista os clientes para quem se pode criar uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :return: Clientes com a conta ativa, por ordem alfabética do nome.
    """
    return [cliente for cliente in gestao.listar(ligacao, modelos.CLIENTE) if cliente.ativo]


def listar_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador) -> list[Campanha]:
    """Lista as campanhas de que um marketeer é responsável.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :return: Campanhas desse marketeer, pela ordem em que foram criadas.
    """
    return campanhas.listar_por_marketeer(ligacao, marketeer.id)


def _dados_validados(nome: str, objetivo: str, data_inicio: str, data_fim: str) -> tuple:
    """Valida o nome, o objetivo e as datas e devolve-os arrumados, pela mesma ordem."""
    nome = validacao.nome(nome)
    inicio = validacao.data(data_inicio, "data de início")
    fim = validacao.data(data_fim, "data de fim")
    validacao.periodo(inicio, fim)
    return nome, objetivo.strip(), inicio, fim


def criar(
    ligacao: sqlite3.Connection,
    marketeer: Utilizador,
    nome: str,
    objetivo: str,
    cliente_id: int,
    data_inicio: str = "",
    data_fim: str = "",
) -> Campanha:
    """Cria uma campanha para um cliente. Quem a cria fica responsável por ela.

    A campanha começa sem budget: é o Administrador que o define.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a criar a campanha.
    :param nome: Nome da campanha. Obrigatório.
    :param objetivo: O que se pretende com a campanha. Pode ficar vazio.
    :param cliente_id: Número do cliente a quem a campanha pertence.
    :param data_inicio: Primeiro dia, no formato ``AAAA-MM-DD``, ou vazio.
    :param data_fim: Último dia, no formato ``AAAA-MM-DD``, ou vazio.
    :return: A campanha criada.
    :raises ErroValidacao: Se o cliente não existir ou tiver a conta
        desativada, ou se algum dos valores não respeitar as regras.
    """
    cliente = utilizadores.obter_por_id(ligacao, cliente_id)
    if cliente is None or cliente.perfil != modelos.CLIENTE:
        raise ErroValidacao(f"Não existe nenhum cliente com o número {cliente_id}.")
    if not cliente.ativo:
        raise ErroValidacao("Este cliente tem a conta desativada.")
    nome, objetivo, inicio, fim = _dados_validados(nome, objetivo, data_inicio, data_fim)
    return campanhas.criar(ligacao, nome, objetivo, cliente.id, marketeer.id, inicio, fim)


def obter_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> Campanha:
    """Procura uma campanha pelo número, confirmando que é do marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :param identificador: Número da campanha, mostrado na primeira coluna da lista.
    :return: A campanha.
    :raises ErroValidacao: Se o marketeer não for responsável por nenhuma
        campanha com esse número.
    """
    campanha = campanhas.obter_por_id(ligacao, identificador)
    if campanha is None or campanha.marketeer_id != marketeer.id:
        raise ErroValidacao(f"Não tem nenhuma campanha com o número {identificador}.")
    return campanha


def editar(
    ligacao: sqlite3.Connection,
    marketeer: Utilizador,
    identificador: int,
    nome: str,
    objetivo: str,
    data_inicio: str = "",
    data_fim: str = "",
) -> Campanha:
    """Altera o nome, o objetivo e as datas de uma campanha do marketeer.

    O cliente e o budget não são alterados: o budget é definido pelo
    Administrador. Nada é guardado se algum dos valores não for válido.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a editar.
    :param identificador: Número da campanha.
    :param nome: Nome novo. Obrigatório.
    :param objetivo: Objetivo novo. Pode ficar vazio.
    :param data_inicio: Primeiro dia novo (``AAAA-MM-DD``), ou vazio para ficar sem data.
    :param data_fim: Último dia novo (``AAAA-MM-DD``), ou vazio para ficar sem data.
    :return: A campanha, já com os dados novos.
    :raises ErroValidacao: Se a campanha não for do marketeer ou se algum dos
        valores não respeitar as regras.
    """
    campanha = obter_do_marketeer(ligacao, marketeer, identificador)
    nome, objetivo, inicio, fim = _dados_validados(nome, objetivo, data_inicio, data_fim)
    return campanhas.atualizar(ligacao, campanha.id, nome, objetivo, inicio, fim)
