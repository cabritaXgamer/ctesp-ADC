"""Sessões: registo de entradas e saídas, e saída automática por inatividade.

Cada vez que alguém entra na aplicação fica registada uma sessão, com a hora
de entrada. Quando sai, fica registada a hora de saída e o motivo: porque
terminou a sessão, ou porque esteve demasiado tempo sem fazer nada.

Numa aplicação de linha de comandos, o programa fica parado à espera de que o
utilizador escreva. Por isso a inatividade só é detetada quando ele volta a
escrever: nesse momento, se passou mais tempo do que o limite, a sessão é
dada como terminada na hora em que o limite foi atingido.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

from gestor_campanhas import config, modelos, relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.repositorios import configuracoes, sessoes

#: Nome da definição que guarda o limite de inatividade, em minutos.
CHAVE_MINUTOS_INATIVIDADE = "minutos_inatividade"


@dataclass
class SessaoAtiva:
    """A sessão do utilizador que está a usar a aplicação neste momento.

    :param id: Identificador da sessão na base de dados.
    :param utilizador: Utilizador que entrou.
    :param limite: Tempo máximo sem atividade.
    :param ultima_atividade: Momento da última ação do utilizador.
    :param aberta: ``False`` depois de a saída ter sido registada.
    """

    id: int
    utilizador: Utilizador
    limite: timedelta
    ultima_atividade: datetime
    aberta: bool = True

    @property
    def momento_de_expiracao(self) -> datetime:
        """Momento em que a sessão expira se não houver mais atividade."""
        return self.ultima_atividade + self.limite

    def expirou(self) -> bool:
        """Diz se já passou mais tempo sem atividade do que o limite."""
        return relogio.agora() > self.momento_de_expiracao

    def registar_atividade(self) -> None:
        """Marca que o utilizador acabou de fazer alguma coisa."""
        self.ultima_atividade = relogio.agora()


def minutos_de_inatividade(ligacao: sqlite3.Connection) -> int:
    """Devolve o limite de inatividade em vigor, em minutos.

    :param ligacao: Ligação aberta à base de dados.
    :return: O valor guardado na tabela ``configuracoes`` ou, se não houver,
        :data:`gestor_campanhas.config.MINUTOS_INATIVIDADE`.
    """
    guardado = configuracoes.obter(ligacao, CHAVE_MINUTOS_INATIVIDADE)
    return int(guardado) if guardado else config.MINUTOS_INATIVIDADE


def definir_minutos_de_inatividade(ligacao: sqlite3.Connection, minutos: int) -> None:
    """Altera o limite de inatividade.

    :param ligacao: Ligação aberta à base de dados.
    :param minutos: Novo limite, em minutos.
    :raises ErroValidacao: Se o valor não for pelo menos 1.
    """
    if minutos < 1:
        raise ErroValidacao("O limite de inatividade tem de ser de pelo menos 1 minuto.")
    configuracoes.definir(ligacao, CHAVE_MINUTOS_INATIVIDADE, str(minutos))


def iniciar(ligacao: sqlite3.Connection, utilizador: Utilizador) -> SessaoAtiva:
    """Regista a entrada de um utilizador e devolve a sessão ativa.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Utilizador que acabou de se autenticar.
    :return: A sessão ativa, com o limite de inatividade em vigor.
    """
    agora = relogio.agora()
    registo = sessoes.abrir(ligacao, utilizador.id, agora)
    return SessaoAtiva(
        id=registo.id,
        utilizador=utilizador,
        limite=timedelta(minutes=minutos_de_inatividade(ligacao)),
        ultima_atividade=agora,
    )


def terminar(ligacao: sqlite3.Connection, sessao: SessaoAtiva, motivo: str = modelos.LOGOUT) -> None:
    """Regista a saída de uma sessão.

    Quando o motivo é a inatividade, a hora de saída é a hora em que o limite
    foi atingido, e não a hora em que isso foi detetado. Chamar esta função
    para uma sessão que já terminou não faz nada.

    :param ligacao: Ligação aberta à base de dados.
    :param sessao: Sessão a terminar.
    :param motivo: :data:`gestor_campanhas.modelos.LOGOUT` ou
        :data:`gestor_campanhas.modelos.INATIVIDADE`.
    """
    if not sessao.aberta:
        return
    saida = sessao.momento_de_expiracao if motivo == modelos.INATIVIDADE else relogio.agora()
    sessoes.fechar(ligacao, sessao.id, saida, motivo)
    sessao.aberta = False
