"""Painel de marketeers, para o Administrador.

Mostra em que está a trabalhar cada marketeer e compara a carga de trabalho
entre eles. Os criativos contam-se em três grupos:

* **ativos**: em preparação, em revisão ou rejeitados, ou seja, ainda com
  trabalho por fazer (ver :data:`ATIVOS`);
* **em atraso**: os ativos cujo prazo já passou;
* **concluídos**: aprovados ou publicados (ver :data:`CONCLUIDOS`).

Um marketeer está **sem atividade** quando não tem criativos ativos, ou
quando não mexe nos criativos há :func:`dias_sem_atividade` dias ou mais. A
última atividade é a mais recente das alterações registadas (ver
:mod:`gestor_campanhas.repositorios.atividades`) e da criação dos criativos
das campanhas dele, que conta para os criativos que já existiam antes de a
atividade começar a ser registada.

Só entram no painel os marketeers com a conta ativa.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, datetime

from gestor_campanhas import config, modelos, relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Atividade, Campanha, Criativo, Utilizador
from gestor_campanhas.repositorios import atividades, configuracoes
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.servicos import campanhas

#: Estados dos criativos que ainda têm trabalho por fazer.
ATIVOS = (modelos.EM_PREPARACAO, modelos.EM_REVISAO, modelos.REJEITADO)

#: Estados dos criativos cujo trabalho está feito.
CONCLUIDOS = (modelos.APROVADO, modelos.PUBLICADO)

#: Nome da definição que guarda o número de dias sem atividade.
CHAVE_DIAS_SEM_ATIVIDADE = "dias_sem_atividade"


@dataclass
class Carga:
    """Indicadores da carga de trabalho de um marketeer.

    :param marketeer: O marketeer.
    :param campanhas_ativas: Campanhas dele que ainda não terminaram.
    :param ativos: Criativos ativos (ver :data:`ATIVOS`).
    :param em_atraso: Criativos ativos com o prazo já passado.
    :param concluidos: Criativos concluídos (ver :data:`CONCLUIDOS`).
    :param ultima_atividade: Data e hora da última alteração aos criativos,
        ou ``None`` se não houver nenhuma.
    """

    marketeer: Utilizador
    campanhas_ativas: int = 0
    ativos: int = 0
    em_atraso: int = 0
    concluidos: int = 0
    ultima_atividade: datetime | None = None


def dias_sem_atividade(ligacao: sqlite3.Connection) -> int:
    """Devolve o número de dias sem atividade em vigor.

    :param ligacao: Ligação aberta à base de dados.
    :return: O valor guardado na tabela ``configuracoes`` ou, se não houver,
        :data:`gestor_campanhas.config.DIAS_SEM_ATIVIDADE`.
    """
    guardado = configuracoes.obter(ligacao, CHAVE_DIAS_SEM_ATIVIDADE)
    return int(guardado) if guardado else config.DIAS_SEM_ATIVIDADE


def definir_dias_sem_atividade(ligacao: sqlite3.Connection, dias: int) -> None:
    """Altera o número de dias sem atividade.

    :param ligacao: Ligação aberta à base de dados.
    :param dias: Número de dias novo.
    :raises ErroValidacao: Se o valor não for pelo menos 1.
    """
    if dias < 1:
        raise ErroValidacao("O número de dias tem de ser pelo menos 1.")
    configuracoes.definir(ligacao, CHAVE_DIAS_SEM_ATIVIDADE, str(dias))


def em_atraso(criativo: Criativo, hoje: date | None = None) -> bool:
    """Diz se um criativo está em atraso: ainda ativo e com o prazo já passado.

    :param criativo: Criativo a avaliar.
    :param hoje: Dia de referência. Se for ``None``, usa-se o dia atual.
    :return: ``True`` se estiver em atraso. Um criativo sem prazo nunca está.
    """
    hoje = hoje or relogio.hoje()
    return criativo.estado in ATIVOS and criativo.prazo is not None and criativo.prazo < hoje


def _no_periodo(criativo: Criativo, desde: date | None, ate: date | None) -> bool:
    """Diz se o prazo de um criativo está no período. Sem período, todos os criativos contam."""
    if desde is None and ate is None:
        return True
    if criativo.prazo is None:
        return False
    return (desde is None or criativo.prazo >= desde) and (ate is None or criativo.prazo <= ate)


def carga(ligacao: sqlite3.Connection, desde: date | None = None, ate: date | None = None) -> list[Carga]:
    """Calcula os indicadores de cada marketeer com a conta ativa.

    :param ligacao: Ligação aberta à base de dados.
    :param desde: Primeiro dia do período. Com um período, só contam os
        criativos com o prazo dentro dele; ``None`` para não limitar.
    :param ate: Último dia do período; ``None`` para não limitar.
    :return: Um :class:`Carga` por marketeer, por ordem alfabética do nome.
    :raises ErroValidacao: Se a data inicial for posterior à data final.
    """
    if desde is not None and ate is not None and desde > ate:
        raise ErroValidacao("A data inicial não pode ser posterior à data final.")
    hoje = relogio.hoje()
    ativas = campanhas.contar_ativas(ligacao, modelos.MARKETEER)
    registadas = atividades.ultima_por_utilizador(ligacao)
    criados = criativos_bd.ultima_criacao_por_marketeer(ligacao)
    resultado = []
    for marketeer in campanhas.marketeers_disponiveis(ligacao):
        indicadores = Carga(marketeer, campanhas_ativas=ativas.get(marketeer.id, 0))
        for criativo in criativos_bd.listar_por_marketeer(ligacao, marketeer.id):
            if not _no_periodo(criativo, desde, ate):
                continue
            if criativo.estado in ATIVOS:
                indicadores.ativos += 1
                if em_atraso(criativo, hoje):
                    indicadores.em_atraso += 1
            else:
                indicadores.concluidos += 1
        datas = [data for data in (registadas.get(marketeer.id), criados.get(marketeer.id)) if data]
        indicadores.ultima_atividade = max(datas) if datas else None
        resultado.append(indicadores)
    return resultado


def situacao(indicadores: Carga, dias: int, hoje: date | None = None) -> str:
    """Diz se um marketeer está sem atividade, e porquê.

    :param indicadores: Indicadores do marketeer, calculados sem período.
    :param dias: Número de dias sem atividade (ver :func:`dias_sem_atividade`).
    :param hoje: Dia de referência. Se for ``None``, usa-se o dia atual.
    :return: ``"Sem criativos ativos"``, ``"Parado há N dias"`` ou
        ``"Sem atividade registada"``; ``""`` se o marketeer estiver ativo.
    """
    hoje = hoje or relogio.hoje()
    if indicadores.ativos == 0:
        return "Sem criativos ativos"
    if indicadores.ultima_atividade is None:
        return "Sem atividade registada"
    parado = (hoje - indicadores.ultima_atividade.date()).days
    if parado >= dias:
        return f"Parado há {parado} {'dia' if parado == 1 else 'dias'}"
    return ""


def trabalho(ligacao: sqlite3.Connection, marketeer: Utilizador) -> list[tuple[Campanha, list[Criativo]]]:
    """Junta as campanhas de um marketeer aos criativos de cada uma.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer a consultar.
    :return: Lista de pares ``(campanha, criativos)``, pela ordem em que as
        campanhas foram criadas. As campanhas sem criativos também aparecem.
    """
    lista = campanhas_bd.listar_por_marketeer(ligacao, marketeer.id)
    return [(campanha, criativos_bd.listar_por_campanha(ligacao, campanha.id)) for campanha in lista]


def ultimas_atividades(ligacao: sqlite3.Connection, marketeer: Utilizador) -> list[Atividade]:
    """Devolve as cinco alterações mais recentes de um marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer a consultar.
    :return: Atividades, da mais recente para a mais antiga.
    """
    return atividades.listar_por_utilizador(ligacao, marketeer.id)
