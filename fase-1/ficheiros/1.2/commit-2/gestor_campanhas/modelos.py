"""Classes de dados da aplicação.

Cada classe representa uma linha de uma tabela da base de dados, já com os
valores nos tipos certos do Python.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

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
