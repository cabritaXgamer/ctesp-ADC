"""Funções comuns a todos os menus.

Juntam num só sítio a forma de mostrar títulos, ler respostas e pedir
confirmações, para que todos os menus se comportem da mesma maneira.
"""

from __future__ import annotations

import getpass
import sys
from datetime import date, datetime

#: Largura, em caracteres, das linhas que delimitam os títulos.
LARGURA = 60


def configurar_terminal() -> None:
    """Garante que os acentos são lidos e escritos em UTF-8.

    Numa consola do Windows o Python já trata bem os acentos. Quando o texto
    passa por outro programa (por exemplo no terminal Git Bash), o Python usa
    a codificação antiga do Windows e os acentos aparecem trocados. Esta
    função força o UTF-8 nos três canais: teclado, saída e erros.
    """
    for canal in (sys.stdin, sys.stdout, sys.stderr):
        # Durante os testes os canais são substituídos por objetos que podem
        # não ter "reconfigure"; nesse caso não há nada a fazer.
        if hasattr(canal, "reconfigure"):
            canal.reconfigure(encoding="utf-8", errors="replace")


def titulo(texto: str) -> None:
    """Mostra um título entre duas linhas.

    :param texto: Texto do título.
    """
    print()
    print("=" * LARGURA)
    print(texto)
    print("=" * LARGURA)


def ler_password(pergunta: str = "Password") -> str:
    """Pede uma password sem a mostrar no ecrã.

    Numa consola normal, o que se escreve não aparece. Quando a aplicação não
    está ligada diretamente a uma consola (por exemplo no terminal Git Bash,
    ou nos testes), não é possível esconder o texto e a password é lida como
    qualquer outra resposta.

    :param pergunta: Texto mostrado antes da resposta.
    :return: Password introduzida, tal como foi escrita.
    """
    if sys.stdin is not None and sys.stdin.isatty():
        return getpass.getpass(f"{pergunta}: ")
    return input(f"{pergunta}: ")


def ler_texto(pergunta: str, obrigatorio: bool = True) -> str:
    """Pede um texto ao utilizador.

    :param pergunta: Texto mostrado antes da resposta.
    :param obrigatorio: Se for ``True``, repete a pergunta até haver resposta.
    :return: Resposta sem espaços no início e no fim. Só pode ser vazia
        quando ``obrigatorio`` é ``False``.
    """
    while True:
        resposta = input(f"{pergunta}: ").strip()
        if resposta or not obrigatorio:
            return resposta
        print("Este campo é obrigatório.")


def confirmar(pergunta: str) -> bool:
    """Pede uma confirmação de sim ou não.

    Repete a pergunta até a resposta ser válida.

    :param pergunta: Texto mostrado antes da resposta.
    :return: ``True`` se a resposta for sim, ``False`` se for não.
    """
    while True:
        resposta = input(f"{pergunta} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Responda 's' ou 'n'.")


def escolher_opcao(titulo_menu: str, opcoes: list[tuple[str, str]]) -> str:
    """Mostra um menu e devolve a opção escolhida.

    Repete o pedido até ser escolhida uma das opções do menu.

    :param titulo_menu: Título mostrado por cima das opções.
    :param opcoes: Lista de pares ``(chave, descrição)``, pela ordem em que
        devem aparecer. A chave é o que o utilizador escreve, por exemplo ``"1"``.
    :return: Chave da opção escolhida.
    """
    titulo(titulo_menu)
    for chave, descricao in opcoes:
        print(f"  {chave}. {descricao}")
    chaves = [chave for chave, _ in opcoes]
    while True:
        escolha = input("Opção: ").strip()
        if escolha in chaves:
            return escolha
        print("Opção inválida.")


def pausa() -> None:
    """Espera que o utilizador prima Enter antes de continuar."""
    input("\nPrima Enter para continuar...")


def ler_data(pergunta: str) -> date | None:
    """Pede uma data no formato ``AAAA-MM-DD``. A resposta pode ficar vazia.

    Repete a pergunta enquanto a resposta não for uma data válida.

    :param pergunta: Texto mostrado antes da resposta.
    :return: A data introduzida, ou ``None`` se a resposta ficou vazia.
    """
    while True:
        resposta = input(f"{pergunta} (AAAA-MM-DD, Enter para não filtrar): ").strip()
        if not resposta:
            return None
        try:
            return datetime.strptime(resposta, "%Y-%m-%d").date()
        except ValueError:
            print("Data inválida. Exemplo de uma data válida: 2026-11-13.")


def mostrar_tabela(cabecalhos: list[str], linhas: list[list[str]]) -> None:
    """Mostra uma tabela de texto, com as colunas alinhadas.

    A largura de cada coluna é a do texto mais comprido que lá aparece.

    :param cabecalhos: Título de cada coluna.
    :param linhas: Linhas da tabela; cada linha tem um texto por coluna.
    """
    larguras = [len(cabecalho) for cabecalho in cabecalhos]
    for linha in linhas:
        for indice, celula in enumerate(linha):
            larguras[indice] = max(larguras[indice], len(celula))

    def formatar(celulas: list[str]) -> str:
        return "  ".join(celula.ljust(largura) for celula, largura in zip(celulas, larguras)).rstrip()

    print(formatar(cabecalhos))
    print("  ".join("-" * largura for largura in larguras))
    for linha in linhas:
        print(formatar(linha))
