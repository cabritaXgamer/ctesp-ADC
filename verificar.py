"""Confirma que o repositório oficial está igual ao original no fim de uma unidade.

Corre-se DENTRO da pasta do repositório oficial, com as duas pastas lado a lado::

    python ../ctesp-ADC/verificar.py 0.1

Compara o conteúdo do ramo em que estás com o conteúdo que a unidade indicada
deve ter depois do último commit. Não altera nada.
"""

from __future__ import annotations

import sys

from copiar import carregar_unidades, configurar_saida, confirmar_pasta_oficial, descrever_ponto, erro, git


def main() -> int:
    """Lê o argumento e compara o ramo atual com o original."""
    configurar_saida()
    unidades, repo_oficial = carregar_unidades()
    confirmar_pasta_oficial(repo_oficial)

    if len(sys.argv) != 2:
        raise erro("Indica a unidade. Exemplo:\n  python ../ctesp-ADC/verificar.py 0.1")
    identificador = sys.argv[1]
    if identificador not in unidades:
        raise erro(f"Não existe a unidade {identificador}. Unidades disponíveis: {', '.join(unidades)}.")
    unidade = unidades[identificador]

    ramo = git("branch", "--show-current")
    por_gravar = git("status", "--porcelain")
    arvore = git("rev-parse", "HEAD^{tree}")
    esperado = unidade["commits"][-1]["tree_depois"]

    if arvore == esperado and not por_gravar:
        print(f"\nTudo certo: o ramo '{ramo}' está igual ao original no fim da unidade {identificador}.\n")
        return 0

    print(f"\nERRO: o ramo '{ramo}' NÃO está igual ao original no fim da unidade {identificador}.\n")
    if por_gravar:
        print("Tens alterações por gravar:")
        for linha in por_gravar.splitlines():
            print(f"  {linha}")
        print()
    if arvore != esperado:
        print(descrever_ponto(arvore, unidades))
        atuais = {}
        for linha in (git("ls-tree", "-r", "HEAD") or "").splitlines():
            dados, caminho = linha.split("\t", 1)
            atuais[caminho] = dados.split()[2]
        finais = unidade["ficheiros_finais"]
        diferentes = sorted(c for c in finais if c in atuais and atuais[c] != finais[c])
        em_falta = sorted(c for c in finais if c not in atuais)
        a_mais = sorted(c for c in atuais if c not in finais)
        for titulo, lista in (("Diferentes do original", diferentes), ("Em falta", em_falta), ("A mais", a_mais)):
            if lista:
                print(f"\n{titulo}:")
                for caminho in lista:
                    print(f"  {caminho}")
        print()
    print("Não avances. Copia esta mensagem e pede ajuda.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
