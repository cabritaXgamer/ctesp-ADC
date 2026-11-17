"""Criativos, nos menus do Marketeer e do Cliente.

O marketeer escolhe uma das suas campanhas e vê os criativos dela, com o
custo, o prazo, o público-alvo e a plataforma de cada um. A partir daí pode
criar, editar, consultar e eliminar criativos, atualizar o estado de cada
um e anexar o ficheiro do criativo.

O cliente vê os criativos de todas as suas campanhas, numa só lista, pode
filtrá-los e pesquisá-los, aprova ou rejeita os que estão em revisão, e
pré-visualiza e descarrega os ficheiros.
"""

from __future__ import annotations

import sqlite3
import subprocess
from datetime import date
from pathlib import Path

from gestor_campanhas import dinheiro, modelos
from gestor_campanhas.cli import campanhas as menu_campanhas
from gestor_campanhas.cli import comum
from gestor_campanhas.cli.pedidos import resumir
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, Criativo, Utilizador
from gestor_campanhas.servicos import campanhas, criativos, ficheiros


#: O que se escreve para apagar um valor quando se edita um criativo.
APAGAR = "-"

#: O que aparece no menu "Atualizar estado" para cada estado de destino.
DESCRICOES_ESTADOS = {
    modelos.EM_REVISAO: "Enviar ao cliente para revisão",
    modelos.EM_PREPARACAO: "Voltar a pôr em preparação",
    modelos.PUBLICADO: "Marcar como publicado",
}

#: Número máximo de caracteres do público-alvo que cabem na lista.
LARGURA_PUBLICO = 25


def custo(criativo: Criativo) -> str:
    """Escreve o custo de um criativo como é mostrado nas listas.

    :param criativo: Criativo a descrever.
    :return: O valor em euros, ou ``"Por definir"`` se ainda não foi indicado.
    """
    if criativo.custo_centimos is None:
        return "Por definir"
    return dinheiro.formatar(criativo.custo_centimos)


def mostrar_criativos(lista: list[Criativo]) -> None:
    """Mostra uma tabela de criativos, com o total no fim.

    :param lista: Criativos a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Nome", "Custo", "Prazo", "Público-alvo", "Plataforma", "Estado"],
        [
            [
                str(criativo.id),
                criativo.nome,
                custo(criativo),
                menu_campanhas.data(criativo.prazo),
                resumir(criativo.publico_alvo, LARGURA_PUBLICO) or "-",
                criativo.plataforma or "-",
                criativo.nome_estado,
            ]
            for criativo in lista
        ],
    )
    print(f"\n{len(lista)} {'criativo' if len(lista) == 1 else 'criativos'}.")


def mostrar_detalhes(criativo: Criativo) -> None:
    """Mostra todos os dados de um criativo, um por linha.

    :param criativo: Criativo a mostrar.
    """
    print(f"Criativo n.º {criativo.id}")
    print(f"  Nome:        {criativo.nome}")
    print(f"  Campanha:    {criativo.campanha_nome}")
    print(f"  Descrição:   {criativo.descricao or '-'}")
    print(f"  Custo:       {custo(criativo)}")
    print(f"  Prazo:       {menu_campanhas.data(criativo.prazo)}")
    print(f"  Público:     {criativo.publico_alvo or '-'}")
    print(f"  Plataforma:  {criativo.plataforma or '-'}")
    print(f"  Estado:      {criativo.nome_estado}")
    if criativo.estado == modelos.REJEITADO:
        print(f"  Motivo:      {criativo.motivo_rejeicao}")
    print(f"  Ficheiro:    {criativo.ficheiro or '-'}")


def pedir_criativo(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> Criativo | None:
    """Pede o número de um criativo da campanha e devolve-o.

    Se o número não for de um criativo desta campanha, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a usar o menu.
    :param campanha: Campanha que está a ser vista.
    :return: O criativo, ou ``None`` se o pedido foi cancelado ou o número não serve.
    """
    numero = comum.ler_numero("Número do criativo (Enter para cancelar)")
    if numero is None:
        return None
    try:
        criativo = criativos.obter_do_marketeer(ligacao, marketeer, numero)
        if criativo.campanha_id != campanha.id:
            raise ErroValidacao(f"Esta campanha não tem nenhum criativo com o número {numero}.")
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None
    return criativo


def ler_plataforma(atual: str | None = None) -> str:
    """Mostra as plataformas numeradas e pede o número de uma delas.

    Repete a pergunta enquanto a resposta não for o número de uma plataforma.

    :param atual: Plataforma que o criativo já tem, quando se está a editar.
        Com ``None`` (ao criar), Enter deixa o criativo sem plataforma; ao
        editar, Enter mantém a atual e :data:`APAGAR` apaga-a.
    :return: Nome da plataforma escolhida, ou ``""`` se ficar sem plataforma.
    """
    print("Plataformas:")
    for numero, nome in enumerate(modelos.PLATAFORMAS, start=1):
        print(f"  {numero}. {nome}")
    if atual is None:
        pergunta = "Número da plataforma (Enter para escolher mais tarde)"
    else:
        pergunta = f"Número da plataforma [{atual or 'nenhuma'}]"
    while True:
        resposta = input(f"{pergunta}: ").strip()
        if not resposta:
            return atual or ""
        if resposta == APAGAR and atual is not None:
            return ""
        if resposta.isdigit() and 1 <= int(resposta) <= len(modelos.PLATAFORMAS):
            return modelos.PLATAFORMAS[int(resposta) - 1]
        print(f"Escreva um número entre 1 e {len(modelos.PLATAFORMAS)}.")


def criar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede os dados de um criativo novo e cria-o na campanha.

    Só o nome é obrigatório: o custo, o prazo, o público-alvo e a plataforma
    podem ser indicados mais tarde, em "Editar criativo".

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a criar o criativo.
    :param campanha: Campanha onde o criativo fica.
    """
    comum.titulo("Criar criativo")
    nome = comum.ler_texto("Nome do criativo")
    descricao = comum.ler_texto("Descrição (opcional)", obrigatorio=False)
    valor = comum.ler_texto("Custo estimado em euros (por exemplo 400 ou 399,90, opcional)", obrigatorio=False)
    prazo = comum.ler_texto("Prazo (AAAA-MM-DD, opcional)", obrigatorio=False)
    publico = comum.ler_texto("Público-alvo (opcional)", obrigatorio=False)
    plataforma = ler_plataforma()
    try:
        criativo = criativos.criar(ligacao, marketeer, campanha.id, nome, descricao, valor, prazo, publico, plataforma)
    except ErroValidacao as erro:
        print(f"\n{erro} O criativo não foi criado.")
    else:
        print(f"\nCriativo criado com o número {criativo.id}.")
    comum.pausa()


def _ler_com_valor(pergunta: str, atual: str, vazio: str) -> str:
    """Pede um valor, mostrando o atual (ou ``vazio`` se não houver).

    Enter mantém o valor atual e :data:`APAGAR` apaga-o.
    """
    resposta = comum.ler_texto_com_valor(pergunta, atual or vazio)
    return "" if resposta in (APAGAR, vazio) else resposta


def _texto_do_prazo(prazo: date | None) -> str:
    """Escreve o prazo como é pedido ao editar, ou ``""`` se não houver."""
    return prazo.isoformat() if prazo else ""


def editar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e deixa alterar todos os dados dele.

    Para cada dado é mostrado o valor atual; com Enter, o valor mantém-se, e
    com :data:`APAGAR` o valor é apagado.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a editar.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Editar criativo")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is None:
        return
    if criativo.estado not in criativos.EDITAVEIS:
        print(f"\nSó se pode editar um criativo em preparação ou rejeitado. Este criativo está {criativo.nome_estado}.")
        comum.pausa()
        return
    print(f"\nA editar o criativo {criativo.nome}.")
    print("Carregue em Enter para manter o valor que está entre parênteses retos.")
    print(f"Para apagar um valor, escreva {APAGAR}\n")
    nome = comum.ler_texto_com_valor("Nome", criativo.nome)
    descricao = _ler_com_valor("Descrição", criativo.descricao, "sem descrição")
    valor = _ler_com_valor("Custo estimado em euros", custo(criativo), "Por definir")
    prazo = _ler_com_valor("Prazo (AAAA-MM-DD)", _texto_do_prazo(criativo.prazo), "sem prazo")
    publico = _ler_com_valor("Público-alvo", criativo.publico_alvo, "sem público-alvo")
    plataforma = ler_plataforma(criativo.plataforma)
    try:
        criativos.editar(ligacao, marketeer, criativo.id, nome, descricao, valor, prazo, publico, plataforma)
    except ErroValidacao as erro:
        print(f"\n{erro} O criativo não foi alterado.")
    else:
        print("\nCriativo guardado.")
    comum.pausa()


def ver(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e mostra todos os dados dele.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Ver criativo")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is None:
        return
    print()
    mostrar_detalhes(criativo)
    comum.pausa()


def eliminar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e elimina-o, depois de pedir confirmação.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a eliminar.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Eliminar criativo")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is None:
        return
    print()
    mostrar_detalhes(criativo)
    print("\nUm criativo eliminado não pode ser recuperado.")
    if comum.confirmar("Eliminar este criativo?"):
        try:
            criativos.eliminar(ligacao, marketeer, criativo.id)
        except ErroValidacao as erro:
            print(f"\n{erro}")
        else:
            print(f"\nO criativo {criativo.nome} foi eliminado.")
    else:
        print("\nNada foi alterado.")
    comum.pausa()


def atualizar_estado(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e muda o estado dele.

    Mostra só as mudanças permitidas a partir do estado atual (ver
    :data:`gestor_campanhas.servicos.criativos.PROXIMOS_ESTADOS`).

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a usar o menu.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Atualizar estado")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is None:
        return
    print(f"\nO criativo {criativo.nome} está {criativo.nome_estado}.")
    if criativo.estado == modelos.REJEITADO:
        print(f"Motivo da rejeição: {criativo.motivo_rejeicao}")
    proximos = criativos.PROXIMOS_ESTADOS[criativo.estado]
    if criativo.estado == modelos.EM_REVISAO:
        print("Está à espera de que o cliente o aprove ou rejeite.")
    if not proximos:
        print("O estado de um criativo publicado já não muda.")
        comum.pausa()
        return
    opcoes = [(str(numero), DESCRICOES_ESTADOS[estado]) for numero, estado in enumerate(proximos, start=1)]
    opcoes.append(("0", "Deixar como está"))
    escolha = comum.escolher_opcao("Novo estado", opcoes)
    if escolha == "0":
        return
    criativo = criativos.mudar_estado(ligacao, marketeer, criativo.id, proximos[int(escolha) - 1])
    print(f"\nO criativo passou a {criativo.nome_estado}.")
    if criativo.estado == modelos.EM_REVISAO:
        print("O cliente já o pode aprovar ou rejeitar, na opção \"Criativos\" do menu dele.")
    comum.pausa()


def anexar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e o caminho de um ficheiro, e anexa-o.

    O ficheiro é copiado para a pasta de ficheiros da aplicação. Se o criativo
    já tinha um ficheiro, fica o novo.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a anexar.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Anexar ficheiro")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is None:
        return
    if criativo.ficheiro:
        print(f"\nO criativo {criativo.nome} já tem o ficheiro {criativo.ficheiro}, que vai ser substituído.")
    print("\nNo Windows, pode clicar no ficheiro com o botão direito, escolher \"Copiar como caminho\"")
    print("e colar aqui com o botão direito do rato.")
    origem = comum.ler_texto("Caminho do ficheiro (Enter para cancelar)", obrigatorio=False)
    if not origem:
        return
    try:
        criativo = criativos.anexar(ligacao, marketeer, criativo.id, origem)
    except ErroValidacao as erro:
        print(f"\n{erro} O ficheiro não foi anexado.")
    else:
        print(f"\nFicheiro {criativo.ficheiro} anexado ao criativo {criativo.nome}.")
    comum.pausa()


def pre_visualizar_ficheiro(criativo: Criativo) -> None:
    """Mostra o nome, o tipo e o tamanho do ficheiro de um criativo e oferece-se para o abrir.

    O ficheiro abre-se no programa predefinido do sistema (por exemplo, o
    visualizador de imagens). Mostra uma mensagem se o criativo não tiver
    ficheiro.

    :param criativo: Criativo cujo ficheiro se quer ver.
    """
    try:
        caminho = criativos.ficheiro_de(criativo)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return
    dados = ficheiros.descrever(caminho)
    print(f"\nFicheiro do criativo {criativo.nome}")
    print(f"  Nome:     {dados['nome']}")
    print(f"  Tipo:     {dados['tipo']}")
    print(f"  Tamanho:  {dados['tamanho']}")
    print()
    if comum.confirmar("Abrir o ficheiro no programa predefinido?"):
        try:
            ficheiros.abrir(caminho)
        except (OSError, subprocess.CalledProcessError) as erro:
            print(f"\nNão foi possível abrir o ficheiro: {erro}")
        else:
            print("\nO ficheiro foi aberto noutra janela.")
    comum.pausa()


def pre_visualizar(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Pede o número de um criativo e mostra o ficheiro dele (ver :func:`pre_visualizar_ficheiro`).

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :param campanha: Campanha que está a ser vista.
    """
    comum.titulo("Pré-visualizar ficheiro")
    criativo = pedir_criativo(ligacao, marketeer, campanha)
    if criativo is not None:
        pre_visualizar_ficheiro(criativo)


#: Opções do menu de criativos de uma campanha. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados, o
#: marketeer e a campanha.
ACOES = [
    ("Criar criativo", criar),
    ("Editar criativo", editar),
    ("Ver criativo", ver),
    ("Eliminar criativo", eliminar),
    ("Atualizar estado", atualizar_estado),
    ("Anexar ficheiro", anexar),
    ("Pré-visualizar ficheiro", pre_visualizar),
]


def da_campanha(ligacao: sqlite3.Connection, marketeer: Utilizador, campanha: Campanha) -> None:
    """Mostra os criativos de uma campanha e as opções para os gerir.

    A lista volta a aparecer depois de cada opção, já com as alterações.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a usar o menu.
    :param campanha: Campanha escolhida.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo(f"Criativos da campanha {campanha.nome} ({campanha.cliente_nome})")
        lista = criativos.listar_da_campanha(ligacao, campanha)
        if lista:
            mostrar_criativos(lista)
        else:
            print("Esta campanha ainda não tem criativos.")
        escolha = comum.escolher_opcao("Criativos", menu)
        if escolha == "0":
            return
        _, funcao = ACOES[int(escolha) - 1]
        funcao(ligacao, marketeer, campanha)


def do_marketeer(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Criativos" do menu do Marketeer.

    Mostra as campanhas do marketeer e pede o número de uma delas. Depois
    mostra os criativos dessa campanha (ver :func:`da_campanha`).

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Marketeer que está a usar o menu.
    """
    while True:
        comum.titulo("Criativos — escolher a campanha")
        lista = campanhas.listar_do_marketeer(ligacao, utilizador)
        if not lista:
            print('Ainda não tem campanhas. Crie uma na opção "Campanhas".')
            comum.pausa()
            return
        menu_campanhas.mostrar_campanhas(lista)
        print()
        numero = comum.ler_numero("Número da campanha (Enter para voltar)")
        if numero is None:
            return
        try:
            campanha = campanhas.obter_do_marketeer(ligacao, utilizador, numero)
        except ErroValidacao as erro:
            print(f"\n{erro}")
            comum.pausa()
            continue
        da_campanha(ligacao, utilizador, campanha)


def mostrar_do_cliente(lista: list[Criativo]) -> None:
    """Mostra uma tabela com os criativos de um cliente, com o total no fim.

    Tem as mesmas colunas da lista do marketeer e mais a campanha de cada criativo.

    :param lista: Criativos a mostrar.
    """
    comum.mostrar_tabela(
        ["N.º", "Nome", "Campanha", "Custo", "Prazo", "Público-alvo", "Plataforma", "Estado"],
        [
            [
                str(criativo.id),
                criativo.nome,
                criativo.campanha_nome,
                custo(criativo),
                menu_campanhas.data(criativo.prazo),
                resumir(criativo.publico_alvo, LARGURA_PUBLICO) or "-",
                criativo.plataforma or "-",
                criativo.nome_estado,
            ]
            for criativo in lista
        ],
    )
    print(f"\n{len(lista)} {'criativo' if len(lista) == 1 else 'criativos'}.")


def pedir_criativo_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> Criativo | None:
    """Pede o número de um criativo do cliente e devolve-o.

    Se o número não for de um criativo dele, mostra o erro e espera por Enter.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a usar o menu.
    :return: O criativo, ou ``None`` se o pedido foi cancelado ou o número não serve.
    """
    numero = comum.ler_numero("Número do criativo (Enter para cancelar)")
    if numero is None:
        return None
    try:
        return criativos.obter_do_cliente(ligacao, cliente, numero)
    except ErroValidacao as erro:
        print(f"\n{erro}")
        comum.pausa()
        return None


def ver_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um criativo do cliente e mostra todos os dados dele.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    """
    comum.titulo("Ver criativo")
    criativo = pedir_criativo_do_cliente(ligacao, cliente)
    if criativo is None:
        return
    print()
    mostrar_detalhes(criativo)
    comum.pausa()


def escolher_da_lista(titulo_lista: str, nomes: list[str], pergunta: str) -> int | None:
    """Mostra uma lista numerada e pede o número de um dos elementos.

    Repete a pergunta enquanto a resposta não for um dos números mostrados.

    :param titulo_lista: Texto mostrado por cima da lista, por exemplo ``"Plataformas:"``.
    :param nomes: Elementos da lista, pela ordem em que aparecem.
    :param pergunta: Texto da pergunta.
    :return: A posição do elemento escolhido (a contar do zero), ou ``None``
        se a resposta ficou vazia.
    """
    print(titulo_lista)
    for numero, nome in enumerate(nomes, start=1):
        print(f"  {numero}. {nome}")
    while True:
        resposta = input(f"{pergunta}: ").strip()
        if not resposta:
            return None
        if resposta.isdigit() and 1 <= int(resposta) <= len(nomes):
            return int(resposta) - 1
        print(f"Escreva um número entre 1 e {len(nomes)}, ou Enter.")


def filtrar(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede os filtros e mostra os criativos do cliente que os respeitam.

    São pedidos, por esta ordem, o texto a pesquisar, a campanha, a
    plataforma e o estado. Com Enter, a pergunta não filtra nada.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    """
    comum.titulo("Filtrar e pesquisar")
    print("Carregue em Enter nas perguntas que não quer usar.\n")
    pesquisa = comum.ler_texto("Texto a procurar no nome, na descrição e no público-alvo", obrigatorio=False)
    lista_campanhas = campanhas.listar_do_cliente(ligacao, cliente)
    posicao = escolher_da_lista(
        "\nCampanhas:", [campanha.nome for campanha in lista_campanhas], "Número da campanha (Enter para todas)"
    )
    campanha_id = None if posicao is None else lista_campanhas[posicao].id
    posicao = escolher_da_lista(
        "\nPlataformas:", list(modelos.PLATAFORMAS), "Número da plataforma (Enter para todas)"
    )
    plataforma = "" if posicao is None else modelos.PLATAFORMAS[posicao]
    estados = list(modelos.NOMES_ESTADOS_CRIATIVO)
    posicao = escolher_da_lista(
        "\nEstados:", list(modelos.NOMES_ESTADOS_CRIATIVO.values()), "Número do estado (Enter para todos)"
    )
    estado = "" if posicao is None else estados[posicao]

    escolhidos = criativos.filtrar(
        criativos.listar_do_cliente(ligacao, cliente), pesquisa, campanha_id, plataforma, estado
    )
    comum.titulo("Criativos encontrados")
    if escolhidos:
        mostrar_do_cliente(escolhidos)
    else:
        print("Nenhum criativo corresponde aos filtros.")
    comum.pausa()


def decidir(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um criativo em revisão e deixa aprová-lo ou rejeitá-lo.

    Para rejeitar, é obrigatório escrever o motivo. Também se pode deixar a
    decisão para mais tarde: o criativo continua em revisão.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a decidir.
    """
    comum.titulo("Aprovar ou rejeitar criativo")
    criativo = pedir_criativo_do_cliente(ligacao, cliente)
    if criativo is None:
        return
    print()
    mostrar_detalhes(criativo)
    if criativo.estado != modelos.EM_REVISAO:
        print(f"\nSó se pode aprovar ou rejeitar um criativo em revisão. Este criativo está {criativo.nome_estado}.")
        comum.pausa()
        return
    escolha = comum.escolher_opcao(
        "Decisão", [("1", "Aprovar"), ("2", "Rejeitar"), ("0", "Decidir mais tarde")]
    )
    if escolha == "0":
        return
    try:
        if escolha == "1":
            criativos.aprovar(ligacao, cliente, criativo.id)
            print("\nCriativo aprovado. O marketeer já o pode publicar.")
        else:
            motivo = comum.ler_texto("Motivo da rejeição (o que quer que mude)")
            criativos.rejeitar(ligacao, cliente, criativo.id, motivo)
            print("\nCriativo rejeitado. O marketeer vai ver o motivo e preparar uma versão nova.")
    except ErroValidacao as erro:
        print(f"\n{erro}")
    comum.pausa()


def pre_visualizar_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um criativo do cliente e mostra o ficheiro dele.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    """
    comum.titulo("Pré-visualizar ficheiro")
    criativo = pedir_criativo_do_cliente(ligacao, cliente)
    if criativo is not None:
        pre_visualizar_ficheiro(criativo)


def pasta_transferencias() -> Path:
    """Devolve a pasta onde os ficheiros são guardados quando não se indica outra.

    :return: A pasta ``Downloads`` (Transferências) da pasta pessoal do utilizador.
    """
    return Path.home() / "Downloads"


def descarregar(ligacao: sqlite3.Connection, cliente: Utilizador) -> None:
    """Pede o número de um criativo do cliente e guarda uma cópia do ficheiro dele.

    A cópia vai para a pasta indicada, ou para a pasta Transferências se a
    resposta ficar vazia. Nenhum ficheiro que já lá esteja é apagado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a descarregar.
    """
    comum.titulo("Descarregar ficheiro")
    criativo = pedir_criativo_do_cliente(ligacao, cliente)
    if criativo is None:
        return
    try:
        caminho = criativos.ficheiro_de(criativo)
        pasta = comum.ler_texto(
            f"Pasta onde guardar a cópia (Enter para {pasta_transferencias()})", obrigatorio=False
        )
        copia = ficheiros.copiar_para(caminho, pasta or str(pasta_transferencias()))
    except ErroValidacao as erro:
        print(f"\n{erro}")
    else:
        print(f"\nCópia guardada em {copia}")
    comum.pausa()


#: Opções do menu de criativos do Cliente. Cada opção é um par
#: ``(descrição, função)``; a função recebe a ligação à base de dados e o
#: cliente.
ACOES_DO_CLIENTE = [
    ("Filtrar e pesquisar", filtrar),
    ("Ver criativo", ver_do_cliente),
    ("Aprovar ou rejeitar criativo", decidir),
    ("Pré-visualizar ficheiro", pre_visualizar_do_cliente),
    ("Descarregar ficheiro", descarregar),
]


def do_cliente(ligacao: sqlite3.Connection, utilizador: Utilizador) -> None:
    """Opção "Criativos" do menu do Cliente.

    Mostra os criativos de todas as campanhas do cliente, quantos estão à
    espera de aprovação e as opções para os filtrar, consultar, aprovar e
    rejeitar, e para ver e descarregar os ficheiros. A lista completa volta a aparecer depois de cada opção.

    :param ligacao: Ligação aberta à base de dados.
    :param utilizador: Cliente que está a usar o menu.
    """
    menu = [(str(numero), descricao) for numero, (descricao, _) in enumerate(ACOES_DO_CLIENTE, start=1)]
    menu.append(("0", "Voltar"))
    while True:
        comum.titulo("Os meus criativos")
        lista = criativos.listar_do_cliente(ligacao, utilizador)
        if lista:
            mostrar_do_cliente(lista)
            em_revisao = len(criativos.filtrar(lista, estado=modelos.EM_REVISAO))
            if em_revisao == 1:
                print("Há 1 criativo à espera da sua aprovação.")
            elif em_revisao:
                print(f"Há {em_revisao} criativos à espera da sua aprovação.")
        else:
            print("Ainda não há criativos nas suas campanhas.")
        escolha = comum.escolher_opcao("Criativos", menu)
        if escolha == "0":
            return
        _, funcao = ACOES_DO_CLIENTE[int(escolha) - 1]
        funcao(ligacao, utilizador)
