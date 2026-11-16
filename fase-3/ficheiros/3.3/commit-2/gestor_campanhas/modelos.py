"""Classes de dados da aplicação.

Cada classe representa uma linha de uma tabela da base de dados, já com os
valores nos tipos certos do Python.

Os valores em dinheiro são guardados em cêntimos, como números inteiros, para
as contas darem sempre certo: ``150050`` são 1500,50 €.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

#: Perfil de quem gere a plataforma.
ADMINISTRADOR = "administrador"
#: Perfil de quem cria campanhas e criativos.
MARKETEER = "marketeer"
#: Perfil de quem pede campanhas e acompanha o trabalho.
CLIENTE = "cliente"

#: Motivo de saída de uma sessão terminada pelo próprio utilizador.
LOGOUT = "logout"
#: Motivo de saída de uma sessão terminada por falta de atividade.
INATIVIDADE = "inatividade"

#: Estado de uma campanha cuja data de início ainda não chegou.
POR_COMECAR = "Por começar"
#: Estado de uma campanha que está a decorrer.
EM_CURSO = "Em curso"
#: Estado de uma campanha cuja data de fim já passou.
TERMINADA = "Terminada"

#: Estado de um pedido que ainda ninguém analisou. É o único que o cliente pode cancelar.
PENDENTE = "pendente"
#: Estado de um pedido que o Administrador já abriu, mas ainda não decidiu.
EM_ANALISE = "em_analise"
#: Estado de um pedido aceite, que deu origem a uma campanha.
APROVADO = "aprovado"
#: Estado de um pedido recusado pelo Administrador.
REJEITADO = "rejeitado"
#: Estado de um pedido de que o cliente desistiu.
CANCELADO = "cancelado"

#: Todos os estados de um pedido, com o nome que é mostrado nas listas.
NOMES_ESTADOS_PEDIDO = {
    PENDENTE: "Pendente",
    EM_ANALISE: "Em análise",
    APROVADO: "Aprovado",
    REJEITADO: "Rejeitado",
    CANCELADO: "Cancelado",
}

#: Plataformas onde se pode anunciar, pela ordem em que aparecem nos menus.
PLATAFORMAS = ("Facebook", "Instagram", "Google Ads", "LinkedIn", "TikTok", "YouTube")

#: Todos os perfis, com o nome que é mostrado nos menus.
NOMES_PERFIS = {
    ADMINISTRADOR: "Administrador",
    MARKETEER: "Marketeer",
    CLIENTE: "Cliente",
}


@dataclass
class Utilizador:
    """Uma conta de acesso à aplicação.

    :param id: Identificador na base de dados.
    :param nome: Nome da pessoa.
    :param email: Email, usado para entrar. É único.
    :param perfil: :data:`ADMINISTRADOR`, :data:`MARKETEER` ou :data:`CLIENTE`.
    :param ativo: ``False`` quando a conta foi desativada e já não pode entrar.
    :param telefone: Contacto telefónico. Pode estar vazio.
    :param empresa: Nome da empresa. Só se usa nos clientes.
    :param nif: Número de contribuinte da empresa. Só se usa nos clientes.
    """

    id: int
    nome: str
    email: str
    perfil: str
    ativo: bool = True
    telefone: str = ""
    empresa: str = ""
    nif: str = ""

    @property
    def nome_perfil(self) -> str:
        """Nome do perfil tal como aparece nos menus, por exemplo ``"Marketeer"``."""
        return NOMES_PERFIS[self.perfil]


@dataclass
class Sessao:
    """Um período em que um utilizador esteve dentro da aplicação.

    :param id: Identificador na base de dados.
    :param utilizador_id: Identificador do utilizador que entrou.
    :param entrada: Data e hora em que entrou.
    :param saida: Data e hora em que saiu, ou ``None`` se ainda não saiu.
    :param motivo_saida: :data:`LOGOUT` ou :data:`INATIVIDADE`; ``None``
        enquanto a sessão está aberta.
    """

    id: int
    utilizador_id: int
    entrada: datetime
    saida: datetime | None = None
    motivo_saida: str | None = None


@dataclass
class Campanha:
    """Uma campanha de marketing de um cliente.

    :param id: Identificador na base de dados.
    :param nome: Nome da campanha.
    :param objetivo: O que se pretende com a campanha. Pode estar vazio.
    :param cliente_id: Identificador do cliente a quem a campanha pertence.
    :param marketeer_id: Identificador do marketeer responsável.
    :param budget_centimos: Budget atribuído, em cêntimos, ou ``None`` se o
        Administrador ainda não o definiu.
    :param data_inicio: Primeiro dia da campanha, ou ``None`` se não foi indicado.
    :param data_fim: Último dia da campanha, ou ``None`` se não foi indicado.
    :param cliente_nome: Nome do cliente, para mostrar nas listas.
    :param marketeer_nome: Nome do marketeer responsável, para mostrar nas listas.
    """

    id: int
    nome: str
    objetivo: str
    cliente_id: int
    marketeer_id: int
    budget_centimos: int | None = None
    data_inicio: date | None = None
    data_fim: date | None = None
    cliente_nome: str = ""
    marketeer_nome: str = ""


@dataclass
class PedidoCampanha:
    """Um pedido de nova campanha, feito por um cliente.

    :param id: Identificador na base de dados.
    :param cliente_id: Identificador do cliente que fez o pedido.
    :param objetivo: O que o cliente pretende com a campanha.
    :param orcamento_centimos: Quanto o cliente quer investir, em cêntimos.
    :param prazo: Dia até ao qual o cliente quer a campanha.
    :param plataformas: Nomes das plataformas onde quer anunciar.
    :param estado: :data:`PENDENTE`, :data:`EM_ANALISE`, :data:`APROVADO`,
        :data:`REJEITADO` ou :data:`CANCELADO`.
    :param criado_em: Data e hora em que o pedido foi feito.
    :param motivo_rejeicao: Motivo indicado pelo Administrador. Só existe
        nos pedidos rejeitados.
    :param campanha_id: Identificador da campanha criada a partir do pedido.
        Só existe nos pedidos aprovados.
    :param cliente_nome: Nome do cliente, para mostrar nas listas.
    """

    id: int
    cliente_id: int
    objetivo: str
    orcamento_centimos: int
    prazo: date
    plataformas: list[str] = field(default_factory=list)
    estado: str = PENDENTE
    criado_em: datetime | None = None
    motivo_rejeicao: str = ""
    campanha_id: int | None = None
    cliente_nome: str = ""

    @property
    def nome_estado(self) -> str:
        """Nome do estado tal como aparece nas listas, por exemplo ``"Em análise"``."""
        return NOMES_ESTADOS_PEDIDO[self.estado]
