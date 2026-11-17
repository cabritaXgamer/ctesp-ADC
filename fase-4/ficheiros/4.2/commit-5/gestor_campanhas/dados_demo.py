"""Dados de demonstração.

Cria um administrador, dois marketeers, três clientes, três campanhas, dois
pedidos de campanha e quatro criativos, para se poder experimentar a
aplicação logo a seguir a instalá-la. Corre-se a partir da pasta do projeto
com::

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
from gestor_campanhas.repositorios import campanhas, criativos, pedidos, utilizadores

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

#: Pedidos de campanha de demonstração, todos pendentes. O cliente é indicado
#: pelo email da conta de :data:`CONTAS`. O orçamento está em cêntimos.
PEDIDOS = [
    {
        "cliente": "jose@padaria.pt",
        "objetivo": "Divulgar o bolo-rei no Natal",
        "orcamento": 60000,
        "prazo": date(2026, 12, 15),
        "plataformas": ["Facebook", "Instagram"],
    },
    {
        "cliente": "beatriz@bicicletas.pt",
        "objetivo": "Dar a conhecer a loja nova de Faro",
        "orcamento": 120000,
        "prazo": date(2027, 2, 28),
        "plataformas": ["Instagram", "Google Ads"],
    },
]


#: Criativos de demonstração. A campanha é indicada pelo nome, e tem de ser
#: uma das de :data:`CAMPANHAS`. O custo está em cêntimos.
CRIATIVOS = [
    {
        "campanha": "Natal 2026",
        "nome": "Banner de Natal",
        "descricao": "Árvore de Natal com os produtos da loja",
        "custo": 40000,
        "prazo": date(2026, 11, 25),
        "publico": "Famílias da região de Lisboa",
        "plataforma": "Facebook",
    },
    {
        "campanha": "Natal 2026",
        "nome": "Vídeo da montra",
        "descricao": "Vídeo curto da montra decorada",
        "custo": 90000,
        "prazo": date(2026, 11, 28),
        "publico": "Jovens adultos, 18 a 35 anos",
        "plataforma": "Instagram",
    },
    {
        "campanha": "Regresso às aulas",
        "nome": "Cartaz dos lanches",
        "descricao": "Lanches para levar para a escola",
        "custo": 30000,
        "prazo": date(2026, 8, 25),
        "publico": "Pais de alunos do básico",
        "plataforma": "Facebook",
    },
    {
        "campanha": "Bicicletas de primavera",
        "nome": "Anúncio da bicicleta elétrica",
        "descricao": "",
        "custo": None,
        "prazo": None,
        "publico": "",
        "plataforma": "",
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


def criar_pedidos(ligacao: sqlite3.Connection) -> list[str]:
    """Cria os pedidos de campanha de demonstração que ainda não existem.

    As contas de demonstração têm de existir (ver :func:`criar_contas`). Um
    pedido já existe quando o cliente dele tem um pedido com o mesmo objetivo.

    :param ligacao: Ligação aberta à base de dados.
    :return: Objetivos dos pedidos criados nesta chamada.
    """
    criados = []
    for pedido in PEDIDOS:
        cliente = utilizadores.obter_por_email(ligacao, pedido["cliente"])
        existentes = [existente.objetivo for existente in pedidos.listar_por_cliente(ligacao, cliente.id)]
        if pedido["objetivo"] in existentes:
            continue
        pedidos.criar(
            ligacao, cliente.id, pedido["objetivo"], pedido["orcamento"], pedido["prazo"], pedido["plataformas"]
        )
        criados.append(pedido["objetivo"])
    return criados


def criar_criativos(ligacao: sqlite3.Connection) -> list[str]:
    """Cria os criativos de demonstração que ainda não existem.

    As campanhas de demonstração têm de existir (ver :func:`criar_campanhas`).
    Um criativo já existe quando a campanha dele tem um criativo com o mesmo nome.

    :param ligacao: Ligação aberta à base de dados.
    :return: Nomes dos criativos criados nesta chamada.
    """
    criados = []
    por_nome = {campanha.nome: campanha for campanha in campanhas.listar_todas(ligacao)}
    for criativo in CRIATIVOS:
        campanha = por_nome[criativo["campanha"]]
        existentes = [existente.nome for existente in criativos.listar_por_campanha(ligacao, campanha.id)]
        if criativo["nome"] in existentes:
            continue
        criativos.criar(
            ligacao,
            campanha.id,
            criativo["nome"],
            criativo["descricao"],
            criativo["custo"],
            criativo["prazo"],
            criativo["publico"],
            criativo["plataforma"],
        )
        criados.append(criativo["nome"])
    return criados


def main() -> int:
    """Cria as contas, as campanhas, os pedidos e os criativos e mostra as credenciais de cada conta.

    :return: Código de saída do processo (``0`` quando termina sem erros).
    """
    comum.configurar_terminal()
    ligacao = bd.iniciar_bd()
    try:
        criadas = criar_contas(ligacao)
        campanhas_criadas = criar_campanhas(ligacao)
        pedidos_criados = criar_pedidos(ligacao)
        criativos_criados = criar_criativos(ligacao)
    finally:
        ligacao.close()
    print(f"Contas criadas: {len(criadas)} (as restantes já existiam).")
    print(f"Campanhas criadas: {len(campanhas_criadas)} (as restantes já existiam).")
    print(f"Pedidos de campanha criados: {len(pedidos_criados)} (os restantes já existiam).")
    print(f"Criativos criados: {len(criativos_criados)} (os restantes já existiam).")
    print()
    print("Contas de demonstração:")
    for conta in CONTAS:
        perfil = modelos.NOMES_PERFIS[conta["perfil"]]
        print(f"  {perfil:<14} {conta['email']:<22} password: {conta['password']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
