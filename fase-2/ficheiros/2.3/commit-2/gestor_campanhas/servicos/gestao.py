"""Gestão das contas de clientes e de marketeers, feita pelo Administrador."""

from __future__ import annotations

import secrets
import sqlite3
import unicodedata

from gestor_campanhas import modelos, seguranca
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import correio, validacao

#: Perfis cujas contas o Administrador pode gerir.
PERFIS_GERIDOS = (modelos.CLIENTE, modelos.MARKETEER)

#: Mensagem mostrada quando o email indicado já pertence a outra conta.
MENSAGEM_EMAIL_REPETIDO = "Já existe uma conta com este email."


def simplificar(texto: str) -> str:
    """Prepara um texto para ser comparado sem contar acentos nem maiúsculas.

    ``"José"`` e ``"jose"`` ficam iguais depois de simplificados.

    :param texto: Texto original.
    :return: O texto em minúsculas, sem acentos e sem espaços à volta.
    """
    # A forma NFD separa cada letra do seu acento ("é" passa a "e" + "´").
    # Os acentos ficam na categoria "Mn" e são deixados de fora.
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acentos = "".join(letra for letra in decomposto if unicodedata.category(letra) != "Mn")
    return sem_acentos.casefold().strip()


def listar(ligacao: sqlite3.Connection, perfil: str, pesquisa: str = "") -> list[Utilizador]:
    """Lista as contas de um perfil, com pesquisa opcional por nome.

    A pesquisa encontra os nomes que contêm o texto indicado, em qualquer
    posição, sem distinguir maiúsculas nem acentos.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil das contas a listar.
    :param pesquisa: Parte do nome a procurar. Vazio para listar todas.
    :return: Contas encontradas, por ordem alfabética do nome. Inclui as
        desativadas.
    """
    contas = utilizadores.listar_por_perfil(ligacao, perfil)
    procurado = simplificar(pesquisa)
    if procurado:
        contas = [conta for conta in contas if procurado in simplificar(conta.nome)]
    # A ordenação é feita aqui, e não no SQL, porque o SQLite põe as letras
    # com acento depois do "z": "Álvaro" ficaria no fim da lista.
    return sorted(contas, key=lambda conta: simplificar(conta.nome))


def gerar_password_inicial() -> str:
    """Gera a password com que uma conta nova começa.

    :return: Password aleatória de 12 caracteres (letras, algarismos, ``-`` e ``_``).
    """
    return secrets.token_urlsafe(9)


def _dados_validados(perfil: str, nome: str, email: str, telefone: str, empresa: str, nif: str) -> tuple:
    """Valida os dados de uma conta e devolve-os arrumados, pela mesma ordem.

    A empresa e o NIF só existem nos clientes; nos outros perfis ficam vazios.
    """
    if perfil not in PERFIS_GERIDOS:
        raise ValueError(f"O perfil {perfil!r} não é gerido pelo Administrador.")
    nome, email, telefone = validacao.nome(nome), validacao.email(email), validacao.telefone(telefone)
    if perfil == modelos.CLIENTE:
        empresa, nif = empresa.strip(), validacao.nif(nif)
    else:
        empresa, nif = "", ""
    return nome, email, telefone, empresa, nif


def criar(
    ligacao: sqlite3.Connection,
    perfil: str,
    nome: str,
    email: str,
    telefone: str = "",
    empresa: str = "",
    nif: str = "",
) -> Utilizador:
    """Cria uma conta e envia as credenciais de acesso para o email dela.

    A conta começa com uma password aleatória, que só aparece no email. Quem
    a recebe deve trocá-la na primeira vez que entrar.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil da conta: um dos :data:`PERFIS_GERIDOS`.
    :param nome: Nome da pessoa. Obrigatório.
    :param email: Email, usado para entrar. Obrigatório e único.
    :param telefone: Telefone: vazio, ou 9 a 15 algarismos.
    :param empresa: Nome da empresa (só clientes).
    :param nif: Número de contribuinte: vazio ou 9 algarismos (só clientes).
    :return: A conta criada.
    :raises ErroValidacao: Se algum dos valores não respeitar as regras ou
        se já existir uma conta com o mesmo email.
    """
    nome, email, telefone, empresa, nif = _dados_validados(perfil, nome, email, telefone, empresa, nif)
    if utilizadores.obter_por_email(ligacao, email) is not None:
        raise ErroValidacao(MENSAGEM_EMAIL_REPETIDO)
    password = gerar_password_inicial()
    conta = utilizadores.criar(
        ligacao, nome, email, seguranca.gerar_hash(password), perfil, telefone=telefone, empresa=empresa, nif=nif
    )
    correio.enviar(
        conta.email,
        "A sua conta no Gestor de Campanhas",
        f"Olá, {conta.nome}.\n\n"
        f"Foi criada uma conta de {conta.nome_perfil} para si no Gestor de Campanhas.\n\n"
        f"Email: {conta.email}\n"
        f"Password: {password}\n\n"
        'Por segurança, altere a password na primeira vez que entrar (opção "Alterar a password").',
    )
    return conta


def obter(ligacao: sqlite3.Connection, perfil: str, identificador: int) -> Utilizador:
    """Procura uma conta pelo número, confirmando que é do perfil esperado.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil que a conta tem de ter.
    :param identificador: Número da conta, mostrado na primeira coluna das listas.
    :return: A conta.
    :raises ErroValidacao: Se não existir uma conta desse perfil com esse número.
    """
    conta = utilizadores.obter_por_id(ligacao, identificador)
    if conta is None or conta.perfil != perfil:
        raise ErroValidacao(f"Não existe nenhum {modelos.NOMES_PERFIS[perfil].lower()} com o número {identificador}.")
    return conta


def editar(
    ligacao: sqlite3.Connection,
    perfil: str,
    identificador: int,
    nome: str,
    email: str,
    telefone: str,
    empresa: str = "",
    nif: str = "",
) -> Utilizador:
    """Altera os dados de uma conta. A password e o estado não são alterados.

    Nada é guardado se algum dos valores não for válido.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil da conta: um dos :data:`PERFIS_GERIDOS`.
    :param identificador: Número da conta a alterar.
    :param nome: Nome novo. Obrigatório.
    :param email: Email novo. Obrigatório e único.
    :param telefone: Telefone novo: vazio, ou 9 a 15 algarismos.
    :param empresa: Nome da empresa (só clientes).
    :param nif: Número de contribuinte: vazio ou 9 algarismos (só clientes).
    :return: A conta, já com os dados novos.
    :raises ErroValidacao: Se a conta não existir, se algum dos valores não
        respeitar as regras ou se o email já for de outra conta.
    """
    conta = obter(ligacao, perfil, identificador)
    nome, email, telefone, empresa, nif = _dados_validados(perfil, nome, email, telefone, empresa, nif)
    if email != conta.email:
        if utilizadores.obter_por_email(ligacao, email) is not None:
            raise ErroValidacao(MENSAGEM_EMAIL_REPETIDO)
        utilizadores.atualizar_email(ligacao, conta.id, email)
    return utilizadores.atualizar_dados(ligacao, conta.id, nome, telefone, empresa, nif)


def definir_estado(ligacao: sqlite3.Connection, perfil: str, identificador: int, ativo: bool) -> Utilizador:
    """Desativa ou reativa uma conta.

    Quem tem a conta desativada deixa de poder entrar e de poder recuperar a
    password. A conta não é apagada: os dados e o histórico mantêm-se, e
    pode ser reativada mais tarde.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil da conta: um dos :data:`PERFIS_GERIDOS`.
    :param identificador: Número da conta.
    :param ativo: ``False`` para desativar, ``True`` para reativar.
    :return: A conta, já com o estado novo.
    :raises ErroValidacao: Se a conta não existir ou já estiver nesse estado.
    """
    if perfil not in PERFIS_GERIDOS:
        raise ValueError(f"O perfil {perfil!r} não é gerido pelo Administrador.")
    conta = obter(ligacao, perfil, identificador)
    if conta.ativo == ativo:
        raise ErroValidacao("Esta conta já está ativa." if ativo else "Esta conta já está desativada.")
    return utilizadores.definir_ativo(ligacao, conta.id, ativo)
