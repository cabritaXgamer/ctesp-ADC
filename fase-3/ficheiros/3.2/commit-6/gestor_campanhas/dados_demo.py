"""Dados de demonstração.

Cria um administrador, dois marketeers, três clientes e três campanhas, para
se poder experimentar a aplicação logo a seguir a instalá-la. Corre-se a
partir da pasta do projeto com::

    python -m gestor_campanhas.dados_demo

Pode ser corrido várias vezes: o que já existe fica como está.

As passwords destas contas são públicas. Servem só para demonstração e não
devem ser usadas numa instalação a sério.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from gestor_campanhas import bd, modelos, seguranca
from gestor_campanhas.cli import comum
from gestor_campanhas.repositorios import campanhas, utilizadores

#: Contas de demonstração: pelo menos uma de cada perfil.
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
        "nome": "Marta Marques",
        "email": "marta@agencia.pt",
        "password": "marta12345",
        "perfil": modelos.MARKETEER,
        "telefone": "910000006",
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
    {
        "nome": "José Padeiro",
        "email": "jose@padaria.pt",
        "password": "jose12345",
        "perfil": modelos.CLIENTE,
        "telefone": "910000004",
        "empresa": "Padaria Central, Lda.",
        "nif": "500000001",
    },
    {
        "nome": "Beatriz Lopes",
        "email": "beatriz@bicicletas.pt",
        "password": "beatriz12345",
        "perfil": modelos.CLIENTE,
        "telefone": "910000005",
        "empresa": "Bicicletas do Sul, Lda.",
        "nif": "500000002",
    },
]

#: Campanhas de demonstração. O cliente e o marketeer são indicados pelo email
#: das contas de :data:`CONTAS`. O budget está em cêntimos.
CAMPANHAS = [
    {
        "nome": "Natal 2026",
        "objetivo": "Aumentar as vendas de dezembro",
        "cliente": "cliente@empresa.pt",
        "marketeer": "marketeer@agencia.pt",
        "inicio": date(2026, 12, 1),
        "fim": date(2026, 12, 24),
        "budget": 150000,
    },
    {
        "nome": "Regresso às aulas",
        "objetivo": "Divulgar os lanches para a escola",
        "cliente": "jose@padaria.pt",
        "marketeer": "marketeer@agencia.pt",
        "inicio": date(2026, 9, 1),
        "fim": date(2026, 9, 30),
        "budget": 80000,
    },
    {
        "nome": "Bicicletas de primavera",
        "objetivo": "",
        "cliente": "beatriz@bicicletas.pt",
        "marketeer": "marta@agencia.pt",
        "inicio": None,
        "fim": None,
        "budget": None,
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


def criar_campanhas(ligacao: sqlite3.Connection) -> list[str]:
    """Cria as campanhas de demonstração que ainda não existem.

    As contas de demonstração têm de existir (ver :func:`criar_contas`). Uma
    campanha já existe quando o marketeer dela tem uma campanha com o mesmo nome.

    :param ligacao: Ligação aberta à base de dados.
    :return: Nomes das campanhas criadas nesta chamada.
    """
    criadas = []
    for campanha in CAMPANHAS:
        cliente = utilizadores.obter_por_email(ligacao, campanha["cliente"])
        marketeer = utilizadores.obter_por_email(ligacao, campanha["marketeer"])
        existentes = [existente.nome for existente in campanhas.listar_por_marketeer(ligacao, marketeer.id)]
        if campanha["nome"] in existentes:
            continue
        campanhas.criar(
            ligacao,
            campanha["nome"],
            campanha["objetivo"],
            cliente.id,
            marketeer.id,
            campanha["inicio"],
            campanha["fim"],
            campanha["budget"],
        )
        criadas.append(campanha["nome"])
    return criadas


def main() -> int:
    """Cria as contas e as campanhas e mostra as credenciais de cada conta.

    :return: Código de saída do processo (``0`` quando termina sem erros).
    """
    comum.configurar_terminal()
    ligacao = bd.iniciar_bd()
    try:
        criadas = criar_contas(ligacao)
        campanhas_criadas = criar_campanhas(ligacao)
    finally:
        ligacao.close()
    print(f"Contas criadas: {len(criadas)} (as restantes já existiam).")
    print(f"Campanhas criadas: {len(campanhas_criadas)} (as restantes já existiam).")
    print()
    print("Contas de demonstração:")
    for conta in CONTAS:
        perfil = modelos.NOMES_PERFIS[conta["perfil"]]
        print(f"  {perfil:<14} {conta['email']:<22} password: {conta['password']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
