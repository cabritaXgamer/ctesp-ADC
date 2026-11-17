"""Regras dos criativos.

Um criativo pertence a uma campanha. Só o marketeer responsável pela
campanha pode criar, alterar ou eliminar os criativos dela.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, Criativo, Utilizador
from gestor_campanhas.repositorios import campanhas, criativos
from gestor_campanhas.servicos import validacao


def listar_da_campanha(ligacao: sqlite3.Connection, campanha: Campanha) -> list[Criativo]:
    """Lista os criativos de uma campanha.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha: Campanha a consultar.
    :return: Criativos da campanha, pela ordem em que foram criados.
    """
    return criativos.listar_por_campanha(ligacao, campanha.id)


def criar(
    ligacao: sqlite3.Connection, marketeer: Utilizador, campanha_id: int, nome: str, descricao: str = ""
) -> Criativo:
    """Cria um criativo numa campanha do marketeer. O criativo começa em preparação.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a criar o criativo.
    :param campanha_id: Número da campanha.
    :param nome: Nome do criativo. Obrigatório.
    :param descricao: O que o criativo mostra ou diz. Pode ficar vazio.
    :return: O criativo criado.
    :raises ErroValidacao: Se a campanha não for do marketeer ou se o nome estiver vazio.
    """
    campanha = campanhas.obter_por_id(ligacao, campanha_id)
    if campanha is None or campanha.marketeer_id != marketeer.id:
        raise ErroValidacao(f"Não tem nenhuma campanha com o número {campanha_id}.")
    return criativos.criar(ligacao, campanha.id, validacao.nome(nome), descricao.strip())


def obter_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> Criativo:
    """Procura um criativo pelo número, confirmando que é de uma campanha do marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :param identificador: Número do criativo, mostrado na primeira coluna da lista.
    :return: O criativo.
    :raises ErroValidacao: Se não houver nenhum criativo com esse número nas
        campanhas do marketeer.
    """
    criativo = criativos.obter_por_id(ligacao, identificador)
    if criativo is not None:
        campanha = campanhas.obter_por_id(ligacao, criativo.campanha_id)
        if campanha.marketeer_id == marketeer.id:
            return criativo
    raise ErroValidacao(f"Não tem nenhum criativo com o número {identificador}.")


def editar(
    ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int, nome: str, descricao: str = ""
) -> Criativo:
    """Altera o nome e a descrição de um criativo do marketeer.

    Nada é guardado se algum dos valores não for válido.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a editar.
    :param identificador: Número do criativo.
    :param nome: Nome novo. Obrigatório.
    :param descricao: Descrição nova. Pode ficar vazia.
    :return: O criativo, já com os dados novos.
    :raises ErroValidacao: Se o criativo não for do marketeer ou se o nome estiver vazio.
    """
    criativo = obter_do_marketeer(ligacao, marketeer, identificador)
    return criativos.atualizar(ligacao, criativo.id, validacao.nome(nome), descricao.strip())


def eliminar(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> Criativo:
    """Elimina um criativo do marketeer. Não pode ser desfeito.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a eliminar.
    :param identificador: Número do criativo.
    :return: O criativo que foi eliminado, para se poder mostrar o nome.
    :raises ErroValidacao: Se o criativo não for do marketeer.
    """
    criativo = obter_do_marketeer(ligacao, marketeer, identificador)
    criativos.eliminar(ligacao, criativo.id)
    return criativo
