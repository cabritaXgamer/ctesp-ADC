"""Regras dos criativos.

Um criativo pertence a uma campanha. Só o marketeer responsável pela
campanha pode criar, alterar ou eliminar os criativos dela.

Além do nome e da descrição, o marketeer indica o custo estimado, o prazo,
o público-alvo e a plataforma. Todos estes dados são opcionais quando o
criativo é criado, porque podem ainda não ser conhecidos.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import dinheiro, modelos
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


def custo_validado(valor: str) -> int | None:
    """Converte um custo escrito em euros. Pode ficar vazio.

    :param valor: Custo tal como foi escrito, por exemplo ``"400"`` ou ``"399,90"``.
    :return: O custo em cêntimos, ou ``None`` se o valor estiver vazio.
    :raises ErroValidacao: Se não estiver vazio nem for um valor em euros.
    """
    if not valor.strip():
        return None
    return dinheiro.para_centimos(valor)


def plataforma_validada(valor: str) -> str:
    """Confirma que a plataforma é uma das previstas. Pode ficar vazia.

    :param valor: Nome da plataforma, por exemplo ``"Instagram"``.
    :return: O nome da plataforma, ou ``""`` se estiver vazio.
    :raises ErroValidacao: Se não estiver vazio nem for uma das plataformas
        de :data:`~gestor_campanhas.modelos.PLATAFORMAS`.
    """
    valor = valor.strip()
    if valor and valor not in modelos.PLATAFORMAS:
        raise ErroValidacao(f"A plataforma tem de ser uma destas: {', '.join(modelos.PLATAFORMAS)}.")
    return valor


def prazo_validado(valor: str, campanha: Campanha) -> date | None:
    """Valida o prazo de um criativo. Pode ficar vazio.

    :param valor: Prazo escrito, no formato ``AAAA-MM-DD``.
    :param campanha: Campanha do criativo.
    :return: O prazo, ou ``None`` se o valor estiver vazio.
    :raises ErroValidacao: Se não for uma data válida ou se for depois do fim
        da campanha.
    """
    prazo = validacao.data(valor, "data do prazo")
    if prazo and campanha.data_fim and prazo > campanha.data_fim:
        raise ErroValidacao(
            f"O prazo não pode ser depois do fim da campanha ({campanha.data_fim.isoformat()})."
        )
    return prazo


def _dados_validados(
    campanha: Campanha, nome: str, descricao: str, custo: str, prazo: str, publico_alvo: str, plataforma: str
) -> tuple:
    """Valida os dados de um criativo e devolve-os arrumados, pela mesma ordem."""
    return (
        validacao.nome(nome),
        descricao.strip(),
        custo_validado(custo),
        prazo_validado(prazo, campanha),
        publico_alvo.strip(),
        plataforma_validada(plataforma),
    )


def criar(
    ligacao: sqlite3.Connection,
    marketeer: Utilizador,
    campanha_id: int,
    nome: str,
    descricao: str = "",
    custo: str = "",
    prazo: str = "",
    publico_alvo: str = "",
    plataforma: str = "",
) -> Criativo:
    """Cria um criativo numa campanha do marketeer. O criativo começa em preparação.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a criar o criativo.
    :param campanha_id: Número da campanha.
    :param nome: Nome do criativo. Obrigatório.
    :param descricao: O que o criativo mostra ou diz. Pode ficar vazio.
    :param custo: Custo estimado em euros, ou vazio.
    :param prazo: Dia em que deve estar pronto (``AAAA-MM-DD``), ou vazio.
    :param publico_alvo: A quem se destina, ou vazio.
    :param plataforma: Plataforma onde vai ser publicado, ou vazio.
    :return: O criativo criado.
    :raises ErroValidacao: Se a campanha não for do marketeer ou se algum dos
        valores não respeitar as regras.
    """
    campanha = campanhas.obter_por_id(ligacao, campanha_id)
    if campanha is None or campanha.marketeer_id != marketeer.id:
        raise ErroValidacao(f"Não tem nenhuma campanha com o número {campanha_id}.")
    dados = _dados_validados(campanha, nome, descricao, custo, prazo, publico_alvo, plataforma)
    return criativos.criar(ligacao, campanha.id, *dados)


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
    ligacao: sqlite3.Connection,
    marketeer: Utilizador,
    identificador: int,
    nome: str,
    descricao: str = "",
    custo: str = "",
    prazo: str = "",
    publico_alvo: str = "",
    plataforma: str = "",
) -> Criativo:
    """Altera os dados de um criativo do marketeer.

    Nada é guardado se algum dos valores não for válido. Um valor vazio
    apaga o que estava guardado.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a editar.
    :param identificador: Número do criativo.
    :param nome: Nome novo. Obrigatório.
    :param descricao: Descrição nova. Pode ficar vazia.
    :param custo: Custo novo em euros, ou vazio.
    :param prazo: Prazo novo (``AAAA-MM-DD``), ou vazio.
    :param publico_alvo: Público-alvo novo, ou vazio.
    :param plataforma: Plataforma nova, ou vazio.
    :return: O criativo, já com os dados novos.
    :raises ErroValidacao: Se o criativo não for do marketeer ou se algum dos
        valores não respeitar as regras.
    """
    criativo = obter_do_marketeer(ligacao, marketeer, identificador)
    campanha = campanhas.obter_por_id(ligacao, criativo.campanha_id)
    dados = _dados_validados(campanha, nome, descricao, custo, prazo, publico_alvo, plataforma)
    return criativos.atualizar(ligacao, criativo.id, *dados)


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
