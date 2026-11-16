"""Gestão de clientes e de marketeers, no menu do Administrador.

Os ecrãs são os mesmos para os perfis geridos. O que muda de um perfil para
outro está em :data:`NOMES` (as palavras usadas nas mensagens) e em
:data:`ACOES` (as opções disponíveis).
"""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.servicos import campanhas, gestao

#: Nome de cada perfil gerido, no singular e no plural, para as mensagens.
NOMES = {
    modelos.CLIENTE: ("cliente", "clientes"),
    modelos.MARKETEER: ("marketeer", "marketeers"),
}


def estado(conta: Utilizador) -> str:
    """Escreve o estado de uma conta por palavras.

    :param conta: Conta a descrever.
    :return: ``"Ativa"`` ou ``"Desativada"``.
    """
    return "Ativa" if conta.ativo else "Desativada"


def mostrar_contas(perfil: str, contas: list[Utilizador], campanhas_ativas: dict[int, int] | None = None) -> None:
    """Mostra uma tabela de contas de um perfil, com o total no fim.

    A coluna da empresa só aparece nos clientes.

    :param perfil: Perfil das contas.
    :param contas: Contas a mostrar.
    :param campanhas_ativas: Número de campanhas ativas de cada conta, pelo
        número da conta. Quem não aparece tem zero.
    """
    singular, plural = NOMES[perfil]
    campanhas_ativas = campanhas_ativas or {}
    cabecalhos = ["N.º", "Nome", "Empresa", "Email", "Telefone", "Estado", "Campanhas ativas"]
    linhas = [
        [
            str(conta.id),
            conta.nome,
            conta.empresa,
            conta.email,
            conta.telefone,
            estado(conta),
            str(campanhas_ativas.get(conta.id, 0)),
        ]
        for conta in contas
    ]
    if perfil != modelos.CLIENTE:
        coluna = cabecalhos.index("Empresa")
        del cabecalhos[coluna]
        for linha in linhas:
            del linha[coluna]
    comum.mostrar_tabela(cabecalhos, linhas)
    print(f"\n{len(contas)} {singular if len(contas) == 1 else plural}.")


def pedir_conta(ligacao: sqlite3.Connection, perfil: str) -> Utilizador | None:
    """Pede o número de uma conta e devolve-a.

    Se o número não existir, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil que a conta tem de ter.
    :return: A conta, ou ``None`` se o pedido foi cancelado ou o número não existe.
    """
    singular, _ = NOMES[perfil]
    numero = comum.ler_numero(f"Número do {singular} (Enter para cancelar)")
    if numero is None:
        return None
    try:
        return gestao.obter(ligacao, perfil, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None


def adicionar(ligacao: sqlite3.Connection, perfil: str) -> None:
    """Pede os dados de uma conta nova e cria-a.

    As credenciais de acesso são enviadas para o email da conta. A empresa e
    o NIF só são pedidos para os clientes.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil da conta a criar.
    """
    singular, _ = NOMES[perfil]
    comum.titulo(f"Adicionar {singular}")
    nome = comum.ler_texto("Nome")
    email = comum.ler_texto("Email")
    telefone = comum.ler_texto("Telefone (opcional)", obrigatorio=False)
    empresa, nif = "", ""
    if perfil == modelos.CLIENTE:
        empresa = comum.ler_texto("Empresa (opcional)", obrigatorio=False)
        nif = comum.ler_texto("NIF (opcional)", obrigatorio=False)
    try:
        conta = gestao.criar(ligacao, perfil, nome, email, telefone, empresa, nif)
    except ErroValidacao as erro:
        print(f"\n{erro} O {singular} não foi criado.")
    else:
        print(f"\n{singular.capitalize()} criado com o número {conta.id}.")
        print(f"As credenciais de acesso foram enviadas para {conta.email}.")
    comum.pausa()


def editar(ligacao: sqlite3.Connection, perfil: str) -> None:
    """Pede o número de uma conta e deixa alterar os dados dela.

    Para cada dado é mostrado o valor atual; com Enter, o valor mantém-se.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil da conta a editar.
    """
    singular, _ = NOMES[perfil]
    comum.titulo(f"Editar {singular}")
    conta = pedir_conta(ligacao, perfil)
    if conta is None:
        return
    print(f"\nA editar {conta.nome}.")
    print("Carregue em Enter para manter o valor que está entre parênteses retos.\n")
    nome = comum.ler_texto_com_valor("Nome", conta.nome)
    email = comum.ler_texto_com_valor("Email", conta.email)
    telefone = comum.ler_texto_com_valor("Telefone", conta.telefone)
    empresa, nif = conta.empresa, conta.nif
    if perfil == modelos.CLIENTE:
        empresa = comum.ler_texto_com_valor("Empresa", conta.empresa)
        nif = comum.ler_texto_com_valor("NIF", conta.nif)
    try:
        gestao.editar(ligacao, perfil, conta.id, nome, email, telefone, empresa, nif)
    except ErroValidacao as erro:
        print(f"\n{erro} Os dados não foram alterados.")
    else:
        print("\nDados guardados.")
    comum.pausa()


def alterar_estado(ligacao: sqlite3.Connection, perfil: str) -> None:
    """Pede o número de uma conta e desativa-a ou reativa-a.

    Mostra o estado atual e pede confirmação antes de alterar.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil da conta.
    """
    singular, _ = NOMES[perfil]
    comum.titulo(f"Desativar ou reativar {singular}")
    conta = pedir_conta(ligacao, perfil)
    if conta is None:
        return
    print(f"\n{conta.nome} ({conta.email}) tem a conta {estado(conta).lower()}.")
    if conta.ativo:
        print("Com a conta desativada, deixa de poder entrar. Os dados e o histórico mantêm-se.")
    if comum.confirmar("Desativar a conta?" if conta.ativo else "Reativar a conta?"):
        gestao.definir_estado(ligacao, perfil, conta.id, not conta.ativo)
        print("\nConta desativada." if conta.ativo else "\nConta reativada.")
        print(f"Foi enviado um aviso para {conta.email}.")
    else:
        print("\nNada foi alterado.")
    comum.pausa()


#: Opções de gestão de cada perfil, além da pesquisa. Cada opção é um par
#: ``(descrição, função)``; a descrição é completada com o nome do perfil e
#: a função recebe a ligação à base de dados e o perfil.
ACOES = {
    modelos.CLIENTE: [
        ("Adicionar", adicionar),
        ("Editar", editar),
        ("Desativar ou reativar", alterar_estado),
    ],
    modelos.MARKETEER: [
        ("Adicionar", adicionar),
        ("Editar", editar),
        ("Desativar ou reativar", alterar_estado),
    ],
}


def gerir(ligacao: sqlite3.Connection, perfil: str) -> None:
    """Mostra a lista de contas de um perfil e as opções para a gerir.

    A lista volta a aparecer depois de cada opção, já com as alterações. A
    pesquisa mantém-se até ser feita outra.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil das contas a gerir.
    """
    singular, plural = NOMES[perfil]
    acoes = ACOES[perfil]
    menu = [("1", "Pesquisar por nome")]
    menu += [(str(numero), f"{descricao} {singular}") for numero, (descricao, _) in enumerate(acoes, start=2)]
    menu.append(("0", "Voltar"))
    pesquisa = ""
    while True:
        comum.titulo(f'{plural.capitalize()} com "{pesquisa}" no nome' if pesquisa else plural.capitalize())
        contas = gestao.listar(ligacao, perfil, pesquisa)
        if contas:
            mostrar_contas(perfil, contas, campanhas.contar_ativas(ligacao, perfil))
        elif pesquisa:
            print(f'Não há {plural} com "{pesquisa}" no nome.')
        else:
            print(f"Ainda não há {plural}.")
        escolha = comum.escolher_opcao(f"Gestão de {plural}", menu)
        if escolha == "0":
            return
        if escolha == "1":
            pesquisa = comum.ler_texto("Pesquisar por nome (Enter para ver todos)", obrigatorio=False)
        else:
            _, funcao = acoes[int(escolha) - 2]
            funcao(ligacao, perfil)


def clientes(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Clientes" do menu do Administrador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a consultar.
    """
    gerir(ligacao, modelos.CLIENTE)


def marketeers(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Marketeers" do menu do Administrador.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a consultar.
    """
    gerir(ligacao, modelos.MARKETEER)
