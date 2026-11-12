"""Funções comuns a todos os menus.

Juntam num só sítio a forma de mostrar títulos, ler respostas e pedir
confirmações, para que todos os menus se comportem da mesma maneira.
"""

from __future__ import annotations

#: Largura, em caracteres, das linhas que delimitam os títulos.
LARGURA = 60


def titulo(texto: str) -> None:
    """Mostra um título entre duas linhas.

    :param texto: Texto do título.
    """
    print()
    print("=" * LARGURA)
    print(texto)
    print("=" * LARGURA)


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
