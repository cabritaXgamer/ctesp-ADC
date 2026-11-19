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

#: Estado de um criativo em que o marketeer ainda está a trabalhar. É o estado
#: de um criativo acabado de criar.
EM_PREPARACAO = "em_preparacao"
#: Estado de um criativo que o marketeer enviou ao cliente para ser revisto.
EM_REVISAO = "em_revisao"
#: Estado de um criativo que já foi publicado na plataforma.
PUBLICADO = "publicado"

#: Todos os estados de um criativo, com o nome que é mostrado nas listas.
#: Um criativo usa também os estados :data:`APROVADO` e :data:`REJEITADO`,
#: quando o cliente o aprova ou rejeita.
NOMES_ESTADOS_CRIATIVO = {
    EM_PREPARACAO: "Em preparação",
    EM_REVISAO: "Em revisão",
    APROVADO: "Aprovado",
    REJEITADO: "Rejeitado",
    PUBLICADO: "Publicado",
}

#: Plataformas onde se pode anunciar, pela ordem em que aparecem nos menus.
PLATAFORMAS = ("Facebook", "Instagram", "Google Ads", "LinkedIn", "TikTok", "YouTube")

#: Notificação sobre uma campanha.
SOBRE_CAMPANHA = "campanha"
#: Notificação sobre um pedido de alteração de budget.
SOBRE_PEDIDO_BUDGET = "pedido_budget"
#: Notificação sobre um criativo (incluindo os comentários dele).
SOBRE_CRIATIVO = "criativo"

#: Assuntos de uma notificação, com o nome que é mostrado nas listas.
NOMES_SOBRE = {
    SOBRE_CAMPANHA: "Campanha",
    SOBRE_PEDIDO_BUDGET: "Pedido de budget",
    SOBRE_CRIATIVO: "Criativo",
}

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

    def terminada(self, hoje: date) -> bool:
        """Diz se a campanha já terminou.

        :param hoje: Dia de referência.
        :return: ``True`` se a campanha tem data de fim e essa data já passou.
        """
        return self.data_fim is not None and self.data_fim < hoje


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


@dataclass
class Criativo:
    """Uma peça de uma campanha: uma imagem, um vídeo ou um texto a publicar.

    :param id: Identificador na base de dados.
    :param campanha_id: Identificador da campanha a que o criativo pertence.
    :param nome: Nome do criativo, por exemplo ``"Banner de Natal"``.
    :param descricao: O que o criativo mostra ou diz. Pode estar vazio.
    :param custo_centimos: Custo estimado, em cêntimos, ou ``None`` se ainda
        não foi indicado.
    :param prazo: Dia em que o criativo deve estar pronto, ou ``None``.
    :param publico_alvo: A quem o criativo se destina. Pode estar vazio.
    :param plataforma: Plataforma onde vai ser publicado, uma das de
        :data:`PLATAFORMAS`, ou vazio se ainda não foi escolhida.
    :param estado: :data:`EM_PREPARACAO`, :data:`EM_REVISAO`, :data:`APROVADO`,
        :data:`REJEITADO` ou :data:`PUBLICADO`.
    :param motivo_rejeicao: Motivo indicado pelo cliente quando rejeita o
        criativo. Só existe nos criativos rejeitados.
    :param ficheiro: Nome do ficheiro anexado, ou vazio se ainda não há.
    :param campanha_nome: Nome da campanha, para mostrar nas listas.
    """

    id: int
    campanha_id: int
    nome: str
    descricao: str = ""
    custo_centimos: int | None = None
    prazo: date | None = None
    publico_alvo: str = ""
    plataforma: str = ""
    estado: str = EM_PREPARACAO
    motivo_rejeicao: str = ""
    ficheiro: str = ""
    campanha_nome: str = ""

    @property
    def nome_estado(self) -> str:
        """Nome do estado tal como aparece nas listas, por exemplo ``"Em preparação"``."""
        return NOMES_ESTADOS_CRIATIVO[self.estado]


@dataclass
class PedidoBudget:
    """Um pedido de alteração do budget de uma campanha, feito pelo cliente dela.

    Usa os mesmos estados de um :class:`PedidoCampanha`.

    :param id: Identificador na base de dados.
    :param campanha_id: Identificador da campanha cujo budget se quer alterar.
    :param budget_atual_centimos: Budget da campanha quando o pedido foi
        feito, em cêntimos, ou ``None`` se ainda não tinha budget.
    :param budget_pedido_centimos: Budget que o cliente pretende, em cêntimos.
    :param motivo: Porque é que o cliente quer alterar o budget.
    :param estado: :data:`PENDENTE`, :data:`EM_ANALISE`, :data:`APROVADO`,
        :data:`REJEITADO` ou :data:`CANCELADO`.
    :param criado_em: Data e hora em que o pedido foi feito.
    :param parecer_viavel: Parecer do marketeer: ``True`` se o pedido é
        viável, ``False`` se não é, ``None`` enquanto não houver parecer.
    :param parecer_justificacao: Justificação do parecer do marketeer.
    :param motivo_rejeicao: Motivo indicado pelo Administrador. Só existe
        nos pedidos rejeitados.
    :param decidido_em: Data e hora em que o Administrador decidiu o pedido,
        ou ``None`` se ainda não o decidiu.
    :param campanha_nome: Nome da campanha, para mostrar nas listas.
    :param cliente_id: Identificador do cliente da campanha.
    :param cliente_nome: Nome do cliente, para mostrar nas listas.
    :param marketeer_id: Identificador do marketeer responsável pela campanha.
    :param marketeer_nome: Nome do marketeer responsável, para mostrar nas listas.
    """

    id: int
    campanha_id: int
    budget_atual_centimos: int | None
    budget_pedido_centimos: int
    motivo: str
    estado: str = PENDENTE
    criado_em: datetime | None = None
    parecer_viavel: bool | None = None
    parecer_justificacao: str = ""
    motivo_rejeicao: str = ""
    decidido_em: datetime | None = None
    campanha_nome: str = ""
    cliente_id: int | None = None
    cliente_nome: str = ""
    marketeer_id: int | None = None
    marketeer_nome: str = ""

    @property
    def nome_estado(self) -> str:
        """Nome do estado tal como aparece nas listas, por exemplo ``"Em análise"``."""
        return NOMES_ESTADOS_PEDIDO[self.estado]

    @property
    def nome_parecer(self) -> str:
        """Parecer do marketeer tal como aparece nas listas: ``"Viável"``, ``"Não viável"`` ou ``"Por dar"``."""
        if self.parecer_viavel is None:
            return "Por dar"
        return "Viável" if self.parecer_viavel else "Não viável"


@dataclass
class AlteracaoBudget:
    """Uma alteração do budget de uma campanha, registada no histórico.

    :param id: Identificador na base de dados.
    :param campanha_id: Identificador da campanha.
    :param budget_anterior_centimos: Budget antes da alteração, em cêntimos,
        ou ``None`` se a campanha ainda não tinha budget.
    :param budget_novo_centimos: Budget depois da alteração, em cêntimos.
    :param motivo: Porque é que o budget mudou.
    :param alterado_em: Data e hora da alteração.
    :param pedido_budget_id: Identificador do pedido de alteração de budget
        que deu origem à alteração, ou ``None`` se o Administrador alterou o
        budget sem pedido.
    """

    id: int
    campanha_id: int
    budget_anterior_centimos: int | None
    budget_novo_centimos: int
    motivo: str
    alterado_em: datetime
    pedido_budget_id: int | None = None


@dataclass
class Comentario:
    """Um comentário sobre um criativo, ou a resposta a um comentário.

    O cliente comenta os criativos das suas campanhas; o marketeer responde
    a cada comentário. Uma resposta é um comentário que indica, em
    ``resposta_a``, o comentário a que responde.

    :param id: Identificador na base de dados.
    :param criativo_id: Identificador do criativo comentado.
    :param autor_id: Identificador de quem escreveu.
    :param texto: O que foi escrito.
    :param criado_em: Data e hora em que foi escrito.
    :param resposta_a: Identificador do comentário a que esta resposta
        responde, ou ``None`` se for um comentário do cliente.
    :param autor_nome: Nome de quem escreveu, para mostrar no ecrã.
    :param autor_perfil: Perfil de quem escreveu (:data:`CLIENTE` ou
        :data:`MARKETEER`).
    """

    id: int
    criativo_id: int
    autor_id: int
    texto: str
    criado_em: datetime
    resposta_a: int | None = None
    autor_nome: str = ""
    autor_perfil: str = ""


@dataclass
class Notificacao:
    """Um aviso para um utilizador, sobre algo que aconteceu na plataforma.

    A notificação indica o item a que se refere (uma campanha, um pedido de
    alteração de budget ou um criativo), para se poder abrir esse item
    diretamente a partir da lista de notificações.

    :param id: Identificador na base de dados.
    :param utilizador_id: Identificador de quem recebe a notificação.
    :param texto: O que aconteceu, numa frase.
    :param sobre: :data:`SOBRE_CAMPANHA`, :data:`SOBRE_PEDIDO_BUDGET` ou
        :data:`SOBRE_CRIATIVO`.
    :param item_id: Identificador da campanha, do pedido ou do criativo.
    :param criada_em: Data e hora da notificação.
    :param lida: ``True`` depois de o utilizador a abrir.
    """

    id: int
    utilizador_id: int
    texto: str
    sobre: str
    item_id: int
    criada_em: datetime
    lida: bool = False

    @property
    def nome_item(self) -> str:
        """O item da notificação tal como aparece nas listas, por exemplo ``"Criativo n.º 3"``."""
        return f"{NOMES_SOBRE[self.sobre]} n.º {self.item_id}"
