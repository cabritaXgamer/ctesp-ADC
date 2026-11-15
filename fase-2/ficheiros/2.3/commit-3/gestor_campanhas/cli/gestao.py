"""Gestão de clientes e de marketeers, no menu do Administrador."""

from __future__ import annotations

import sqlite3

from gestor_campanhas import modelos
from gestor_campanhas.cli import comum
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.servicos import gestao

#: Opções mostradas por baixo da lista de clientes.
OPCOES_CLIENTES = [
    ("1", "Pesquisar por nome"),
    ("2", "Adicionar cliente"),
    ("3", "Editar cliente"),
    ("4", "Desativar ou reativar cliente"),
    ("0", "Voltar"),
]


def estado(conta: Utilizador) -> str:
    """Escreve o estado de uma conta por palavras.

    :param conta: Conta a descrever.
    :return: ``"Ativa"`` ou ``"Desativada"``.
    """
    return "Ativa" if conta.ativo else "Desativada"


def mostrar_clientes(contas: list[Utilizador]) -> None:
    """Mostra uma tabela de clientes, com o total no fim.

    :param contas: Clientes a mostrar.
    """
    linhas = [
        [str(conta.id), conta.nome, conta.empresa, conta.email, conta.telefone, estado(conta)] for conta in contas
    ]
    comum.mostrar_tabela(["N.º", "Nome", "Empresa", "Email", "Telefone", "Estado"], linhas)
    print(f"\n{len(contas)} {'cliente' if len(contas) == 1 else 'clientes'}.")


def clientes(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Mostra a lista de clientes e as opções para a gerir.

    A lista volta a aparecer depois de cada opção, já com as alterações. A
    pesquisa mantém-se até ser feita outra.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Administrador que está a consultar.
    """
    pesquisa = ""
    while True:
        comum.titulo(f'Clientes com "{pesquisa}" no nome' if pesquisa else "Clientes")
        contas = gestao.listar(ligacao, modelos.CLIENTE, pesquisa)
        if contas:
            mostrar_clientes(contas)
        elif pesquisa:
            print(f'Não há clientes com "{pesquisa}" no nome.')
        else:
            print("Ainda não há clientes.")
        escolha = comum.escolher_opcao("Gestão de clientes", OPCOES_CLIENTES)
        if escolha == "0":
            return
        if escolha == "1":
            pesquisa = comum.ler_texto("Pesquisar por nome (Enter para ver todos)", obrigatorio=False)
        elif escolha == "2":
            adicionar_cliente(ligacao)
        elif escolha == "3":
            editar_cliente(ligacao)
        elif escolha == "4":
            alterar_estado_cliente(ligacao)


def adicionar_cliente(ligacao: sqlite3.Connection) -> None:
    """Pede os dados de um cliente novo e cria a conta.

    As credenciais de acesso são enviadas para o email do cliente.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Adicionar cliente")
    nome = comum.ler_texto("Nome")
    email = comum.ler_texto("Email")
    telefone = comum.ler_texto("Telefone (opcional)", obrigatorio=False)
    empresa = comum.ler_texto("Empresa (opcional)", obrigatorio=False)
    nif = comum.ler_texto("NIF (opcional)", obrigatorio=False)
    try:
        conta = gestao.criar(ligacao, modelos.CLIENTE, nome, email, telefone, empresa, nif)
    except ErroValidacao as erro:
        print(f"\n{erro} O cliente não foi criado.")
    else:
        print(f"\nCliente criado com o número {conta.id}.")
        print(f"As credenciais de acesso foram enviadas para {conta.email}.")
    comum.pausa()


def editar_cliente(ligacao: sqlite3.Connection) -> None:
    """Pede o número de um cliente e deixa alterar os dados dele.

    Para cada dado é mostrado o valor atual; com Enter, o valor mantém-se.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Editar cliente")
    numero = comum.ler_numero("Número do cliente (Enter para cancelar)")
    if numero is None:
        return
    try:
        conta = gestao.obter(ligacao, modelos.CLIENTE, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    print(f"\nA editar {conta.nome}.")
    print("Carregue em Enter para manter o valor que está entre parênteses retos.\n")
    nome = comum.ler_texto_com_valor("Nome", conta.nome)
    email = comum.ler_texto_com_valor("Email", conta.email)
    telefone = comum.ler_texto_com_valor("Telefone", conta.telefone)
    empresa = comum.ler_texto_com_valor("Empresa", conta.empresa)
    nif = comum.ler_texto_com_valor("NIF", conta.nif)
    try:
        gestao.editar(ligacao, modelos.CLIENTE, conta.id, nome, email, telefone, empresa, nif)
    except ErroValidacao as erro:
        print(f"\n{erro} Os dados não foram alterados.")
    else:
        print("\nDados guardados.")
    comum.pausa()


def alterar_estado_cliente(ligacao: sqlite3.Connection) -> None:
    """Pede o número de um cliente e desativa ou reativa a conta dele.

    Mostra o estado atual e pede confirmação antes de alterar.

    :param ligacao: Ligação aberta à base de dados.
    """
    comum.titulo("Desativar ou reativar cliente")
    numero = comum.ler_numero("Número do cliente (Enter para cancelar)")
    if numero is None:
        return
    try:
        conta = gestao.obter(ligacao, modelos.CLIENTE, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    print(f"\n{conta.nome} ({conta.email}) tem a conta {estado(conta).lower()}.")
    if conta.ativo:
        print("Com a conta desativada, deixa de poder entrar. Os dados e o histórico mantêm-se.")
    if comum.confirmar("Desativar a conta?" if conta.ativo else "Reativar a conta?"):
        gestao.definir_estado(ligacao, modelos.CLIENTE, conta.id, not conta.ativo)
        print("\nConta desativada." if conta.ativo else "\nConta reativada.")
    else:
        print("\nNada foi alterado.")
    comum.pausa()
