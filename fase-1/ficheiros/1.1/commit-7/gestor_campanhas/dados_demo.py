"""Dados de demonstração.

Cria uma conta de cada perfil, para se poder experimentar a aplicação logo a
seguir a instalá-la. Corre-se a partir da pasta do projeto com::

    python -m gestor_campanhas.dados_demo

Pode ser corrido várias vezes: as contas que já existem ficam como estão.

As passwords destas contas são públicas. Servem só para demonstração e não
devem ser usadas numa instalação a sério.
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import bd, modelos, seguranca
from gestor_campanhas.cli import comum
from gestor_campanhas.repositorios import utilizadores

#: Contas de demonstração, uma por perfil.
CONTAS = [
    {
        "nome": "Ana Administradora",
        "email": "admin@agencia.pt",
        "password": "admin12345",
        "perfil": modelos.ADMINISTRADOR,
        "telefone": "910000001",
    },
    {
        "nome": "Miguel Marketeer",
        "email": "marketeer@agencia.pt",
        "password": "marketeer12345",
        "perfil": modelos.MARKETEER,
        "telefone": "910000002",
    },
    {
        "nome": "Carla Cliente",
        "email": "cliente@empresa.pt",
        "password": "cliente12345",
        "perfil": modelos.CLIENTE,
        "telefone": "910000003",
        "empresa": "Empresa Exemplo, Lda.",
        "nif": "500000000",
    },
]


def criar_contas(ligacao: sqlite3.Connection) -> list[str]:
    """Cria as contas de demonstração que ainda não existem.

    :param ligacao: Ligação aberta à base de dados.
    :return: Emails das contas criadas nesta chamada.
    """
    criadas = []
    for conta in CONTAS:
        if utilizadores.obter_por_email(ligacao, conta["email"]) is not None:
            continue
        utilizadores.criar(
            ligacao,
            nome=conta["nome"],
            email=conta["email"],
            password_hash=seguranca.gerar_hash(conta["password"]),
            perfil=conta["perfil"],
            telefone=conta.get("telefone", ""),
            empresa=conta.get("empresa", ""),
            nif=conta.get("nif", ""),
        )
        criadas.append(conta["email"])
    return criadas


def main() -> int:
    """Cria as contas e mostra as credenciais de cada uma.

    :return: Código de saída do processo (``0`` quando termina sem erros).
    """
    comum.configurar_terminal()
    ligacao = bd.iniciar_bd()
    try:
        criadas = criar_contas(ligacao)
    finally:
        ligacao.close()
    print(f"Contas criadas: {len(criadas)} (as restantes já existiam).")
    print()
    print("Contas de demonstração:")
    for conta in CONTAS:
        perfil = modelos.NOMES_PERFIS[conta["perfil"]]
        print(f"  {perfil:<14} {conta['email']:<22} password: {conta['password']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
