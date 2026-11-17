"""Regras dos criativos.

Um criativo pertence a uma campanha. Só o marketeer responsável pela
campanha pode criar, alterar ou eliminar os criativos dela.

Além do nome e da descrição, o marketeer indica o custo estimado, o prazo,
o público-alvo e a plataforma. Todos estes dados são opcionais quando o
criativo é criado, porque podem ainda não ser conhecidos.

O cliente vê os criativos de todas as suas campanhas e pode filtrá-los e
pesquisá-los.

Um criativo passa por vários estados. O marketeer muda-o de estado seguindo
:data:`PROXIMOS_ESTADOS`; o cliente aprova ou rejeita os que estão em
revisão. Um criativo só pode ser editado enquanto está em preparação ou
depois de ser rejeitado, e um criativo publicado não pode ser eliminado.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import dinheiro, modelos
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, Criativo, Utilizador
from gestor_campanhas.repositorios import campanhas, criativos
from gestor_campanhas.servicos import gestao, validacao

#: Estados para onde o marketeer pode mudar um criativo, a partir de cada
#: estado. Os estados :data:`~gestor_campanhas.modelos.APROVADO` e
#: :data:`~gestor_campanhas.modelos.REJEITADO` são decididos pelo cliente,
#: por isso só aparecem como ponto de partida.
PROXIMOS_ESTADOS = {
    modelos.EM_PREPARACAO: (modelos.EM_REVISAO,),
    modelos.EM_REVISAO: (modelos.EM_PREPARACAO,),
    modelos.REJEITADO: (modelos.EM_PREPARACAO, modelos.EM_REVISAO),
    modelos.APROVADO: (modelos.PUBLICADO,),
    modelos.PUBLICADO: (),
}

#: Estados em que o marketeer pode editar um criativo.
EDITAVEIS = (modelos.EM_PREPARACAO, modelos.REJEITADO)


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
    :raises ErroValidacao: Se o criativo não for do marketeer, se não estiver
        num dos estados de :data:`EDITAVEIS` ou se algum dos valores não
        respeitar as regras.
    """
    criativo = obter_do_marketeer(ligacao, marketeer, identificador)
    if criativo.estado not in EDITAVEIS:
        raise ErroValidacao(
            f"Só se pode editar um criativo em preparação ou rejeitado. Este criativo está {criativo.nome_estado}."
        )
    campanha = campanhas.obter_por_id(ligacao, criativo.campanha_id)
    dados = _dados_validados(campanha, nome, descricao, custo, prazo, publico_alvo, plataforma)
    return criativos.atualizar(ligacao, criativo.id, *dados)


def eliminar(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> Criativo:
    """Elimina um criativo do marketeer. Não pode ser desfeito.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a eliminar.
    :param identificador: Número do criativo.
    :return: O criativo que foi eliminado, para se poder mostrar o nome.
    :raises ErroValidacao: Se o criativo não for do marketeer ou se já tiver
        sido publicado.
    """
    criativo = obter_do_marketeer(ligacao, marketeer, identificador)
    if criativo.estado == modelos.PUBLICADO:
        raise ErroValidacao("Um criativo publicado não pode ser eliminado.")
    criativos.eliminar(ligacao, criativo.id)
    return criativo


def listar_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> list[Criativo]:
    """Lista os criativos de todas as campanhas de um cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :return: Criativos das campanhas do cliente, agrupados por campanha.
    """
    return criativos.listar_por_cliente(ligacao, cliente.id)


def obter_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> Criativo:
    """Procura um criativo pelo número, confirmando que é de uma campanha do cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :param identificador: Número do criativo, mostrado na primeira coluna da lista.
    :return: O criativo.
    :raises ErroValidacao: Se não houver nenhum criativo com esse número nas
        campanhas do cliente.
    """
    criativo = criativos.obter_por_id(ligacao, identificador)
    if criativo is not None:
        campanha = campanhas.obter_por_id(ligacao, criativo.campanha_id)
        if campanha.cliente_id == cliente.id:
            return criativo
    raise ErroValidacao(f"Não tem nenhum criativo com o número {identificador}.")


def filtrar(
    lista: list[Criativo],
    pesquisa: str = "",
    campanha_id: int | None = None,
    plataforma: str = "",
    estado: str = "",
) -> list[Criativo]:
    """Escolhe, de uma lista de criativos, os que respeitam todos os filtros.

    Um filtro vazio (ou ``None``) não exclui nenhum criativo.

    :param lista: Criativos a filtrar.
    :param pesquisa: Texto a procurar no nome, na descrição e no público-alvo,
        em qualquer posição. Não distingue maiúsculas nem acentos.
    :param campanha_id: Número da campanha.
    :param plataforma: Nome da plataforma.
    :param estado: Estado do criativo, por exemplo
        :data:`~gestor_campanhas.modelos.EM_PREPARACAO`.
    :return: Os criativos que respeitam os filtros, pela mesma ordem.
    """
    procura = gestao.simplificar(pesquisa.strip())
    escolhidos = []
    for criativo in lista:
        texto = gestao.simplificar(f"{criativo.nome} {criativo.descricao} {criativo.publico_alvo}")
        if procura and procura not in texto:
            continue
        if campanha_id is not None and criativo.campanha_id != campanha_id:
            continue
        if plataforma and criativo.plataforma != plataforma:
            continue
        if estado and criativo.estado != estado:
            continue
        escolhidos.append(criativo)
    return escolhidos


def mudar_estado(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int, estado: str) -> Criativo:
    """Muda o estado de um criativo do marketeer.

    Só são permitidas as mudanças de :data:`PROXIMOS_ESTADOS`. Enviar o
    criativo para revisão é o que permite ao cliente aprová-lo ou rejeitá-lo.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a mudar o estado.
    :param identificador: Número do criativo.
    :param estado: Estado novo.
    :return: O criativo, já com o estado novo.
    :raises ErroValidacao: Se o criativo não for do marketeer ou se a mudança
        não for permitida.
    """
    criativo = obter_do_marketeer(ligacao, marketeer, identificador)
    if estado not in PROXIMOS_ESTADOS[criativo.estado]:
        novo = modelos.NOMES_ESTADOS_CRIATIVO.get(estado, estado)
        raise ErroValidacao(f"Um criativo {criativo.nome_estado} não pode passar a {novo}.")
    return criativos.definir_estado(ligacao, criativo.id, estado)


def _em_revisao_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> Criativo:
    """Procura um criativo do cliente e confirma que está em revisão."""
    criativo = obter_do_cliente(ligacao, cliente, identificador)
    if criativo.estado != modelos.EM_REVISAO:
        raise ErroValidacao(
            f"Só se pode aprovar ou rejeitar um criativo em revisão. Este criativo está {criativo.nome_estado}."
        )
    return criativo


def aprovar(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> Criativo:
    """Aprova um criativo em revisão. A partir daqui, o marketeer pode publicá-lo.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a decidir.
    :param identificador: Número do criativo.
    :return: O criativo, já aprovado.
    :raises ErroValidacao: Se o criativo não for do cliente ou não estiver em revisão.
    """
    criativo = _em_revisao_do_cliente(ligacao, cliente, identificador)
    return criativos.definir_estado(ligacao, criativo.id, modelos.APROVADO)


def rejeitar(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int, motivo: str) -> Criativo:
    """Rejeita um criativo em revisão, com o motivo, para o marketeer saber o que mudar.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a decidir.
    :param identificador: Número do criativo.
    :param motivo: O que o cliente quer que mude. Obrigatório.
    :return: O criativo, já rejeitado.
    :raises ErroValidacao: Se o criativo não for do cliente, se não estiver em
        revisão ou se o motivo estiver vazio.
    """
    criativo = _em_revisao_do_cliente(ligacao, cliente, identificador)
    motivo = motivo.strip()
    if not motivo:
        raise ErroValidacao("Indique o motivo da rejeição, para o marketeer saber o que mudar.")
    return criativos.definir_estado(ligacao, criativo.id, modelos.REJEITADO, motivo)


def contar_por_estado(ligacao: sqlite3.Connection, campanha: Campanha) -> dict[str, int]:
    """Conta os criativos de uma campanha em cada estado.

    :param ligacao: Ligação aberta à base de dados.
    :param campanha: Campanha a consultar.
    :return: Dicionário do estado para o número de criativos nesse estado,
        pela ordem de :data:`~gestor_campanhas.modelos.NOMES_ESTADOS_CRIATIVO`.
        Os estados sem criativos não aparecem.
    """
    totais = {estado: 0 for estado in modelos.NOMES_ESTADOS_CRIATIVO}
    for criativo in criativos.listar_por_campanha(ligacao, campanha.id):
        totais[criativo.estado] += 1
    return {estado: total for estado, total in totais.items() if total}
