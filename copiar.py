"""Copia para o repositório oficial os ficheiros de um commit.

Corre-se DENTRO da pasta do repositório oficial, com as duas pastas lado a lado::

    python ../ctesp-ADC/copiar.py 0.1 1

O primeiro número é a unidade de trabalho e o segundo é o commit dentro dela.
Os ficheiros estão em ``fase-N/ficheiros/<unidade>/commit-<n>``. Copiar essa
pasta à mão para dentro do repositório oficial dá o mesmo resultado.

Antes de copiar, o script confirma que estás na pasta certa, no ramo certo e
no ponto certo (ou seja, que não saltaste nenhum commit). Não faz commits: no
fim diz que comandos deves correr para gravar.

Sem argumentos, só confirma que as duas pastas estão no sítio certo.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

#: Pasta do repositório de trabalho (onde está este ficheiro).
TRABALHO = Path(__file__).resolve().parent


def configurar_saida() -> None:
    """Garante que os acentos aparecem bem em qualquer terminal."""
    for canal in (sys.stdout, sys.stderr):
        if hasattr(canal, "reconfigure"):
            canal.reconfigure(encoding="utf-8", errors="replace")


def git(*argumentos: str) -> str | None:
    """Corre um comando git na pasta atual. Devolve ``None`` se o comando falhar."""
    resultado = subprocess.run(
        ["git", "-c", "core.quotepath=false", *argumentos], capture_output=True, encoding="utf-8"
    )
    if resultado.returncode != 0:
        return None
    return resultado.stdout.strip()


def erro(mensagem: str) -> SystemExit:
    """Mostra uma mensagem de erro e devolve a exceção que termina o programa."""
    print(f"\nERRO: {mensagem}\n")
    return SystemExit(1)


def carregar_unidades() -> tuple[dict, str]:
    """Lê os manifestos de todas as fases.

    :return: As unidades por identificador (por exemplo ``"0.1"``) e o nome
        do repositório oficial.
    """
    unidades: dict = {}
    repo_oficial = ""
    for ficheiro in sorted(TRABALHO.glob("fase-*/ficheiros/manifesto.json")):
        manifesto = json.loads(ficheiro.read_text(encoding="utf-8"))
        repo_oficial = manifesto["repo_oficial"]
        for unidade in manifesto["unidades"]:
            unidade["pasta"] = ficheiro.parent / unidade["id"]
            unidades[unidade["id"]] = unidade
    if not unidades:
        raise erro(f"Não encontrei ficheiros de nenhuma fase em {TRABALHO}.")
    return unidades, repo_oficial


def confirmar_pasta_oficial(repo_oficial: str) -> Path:
    """Confirma que o comando está a ser corrido na raiz do repositório oficial."""
    aqui = Path.cwd().resolve()
    raiz = git("rev-parse", "--show-toplevel")
    if raiz is None:
        raise erro(
            f"Esta pasta não é um repositório Git:\n  {aqui}\n"
            f"Entra na pasta do repositório oficial ({repo_oficial}) e repete o comando."
        )
    raiz = Path(raiz).resolve()
    origem = git("remote", "get-url", "origin") or ""
    if raiz == TRABALHO or repo_oficial.lower() not in origem.lower():
        raise erro(
            f"Estás na pasta errada:\n  {aqui}\n"
            f"Este comando tem de ser corrido dentro da pasta do repositório oficial ({repo_oficial}).\n"
            "A pasta do repositório de trabalho é só para ler."
        )
    if aqui != raiz:
        raise erro(f"Estás numa subpasta. Volta à pasta principal do repositório:\n  cd \"{raiz}\"")
    return raiz


def descrever_ponto(arvore: str | None, unidades: dict) -> str:
    """Diz, por palavras, em que ponto do trabalho está o ramo atual."""
    if arvore is None:
        return "O repositório ainda não tem nenhum commit."
    for unidade in unidades.values():
        if unidade["commits"][0]["tree_antes"] == arvore:
            return f"Neste momento, o próximo commit a fazer no teu ramo é o commit 1 da unidade {unidade['id']}."
    for unidade in unidades.values():
        total = len(unidade["commits"])
        for commit in unidade["commits"]:
            if commit["tree_depois"] == arvore:
                if commit["numero"] == total:
                    return f"O teu ramo já tem os {total} commits da unidade {unidade['id']}. Não falta copiar nenhum."
                return (
                    f"O teu ramo já tem o commit {commit['numero']} da unidade {unidade['id']}. "
                    f"O próximo é o commit {commit['numero'] + 1}."
                )
    return (
        "O conteúdo do teu ramo não corresponde a nenhum ponto conhecido. "
        "Pode haver um ficheiro alterado ou a mais num commit anterior."
    )


def main() -> int:
    """Lê os argumentos, faz as verificações e copia os ficheiros."""
    configurar_saida()
    unidades, repo_oficial = carregar_unidades()
    raiz = confirmar_pasta_oficial(repo_oficial)

    if len(sys.argv) == 1:
        print("Pastas no sítio certo.")
        print(f"  Repositório oficial:     {raiz}")
        print(f"  Repositório de trabalho: {TRABALHO}")
        print("\nPara copiar os ficheiros de um commit:  python ../ctesp-ADC/copiar.py UNIDADE COMMIT")
        return 0
    if len(sys.argv) != 3 or not sys.argv[2].isdigit():
        raise erro("Indica a unidade e o número do commit. Exemplo:\n  python ../ctesp-ADC/copiar.py 0.1 1")

    identificador, numero = sys.argv[1], int(sys.argv[2])
    if identificador not in unidades:
        raise erro(f"Não existe a unidade {identificador}. Unidades disponíveis: {', '.join(unidades)}.")
    unidade = unidades[identificador]
    total = len(unidade["commits"])
    if not 1 <= numero <= total:
        raise erro(f"A unidade {identificador} tem {total} commits. Escolhe um número de 1 a {total}.")
    commit = unidade["commits"][numero - 1]

    ramo = git("branch", "--show-current")
    if ramo != unidade["ramo"]:
        raise erro(
            f"Estás no ramo '{ramo}'. A unidade {identificador} é feita no ramo '{unidade['ramo']}'.\n"
            f"Se já criaste esse ramo, muda para ele:  git switch {unidade['ramo']}\n"
            "Se ainda não o criaste, volta ao passo \"Atualiza as pastas e cria o ramo\"."
        )

    por_gravar = git("status", "--porcelain")
    if por_gravar:
        raise erro(
            "Tens alterações por gravar nesta pasta:\n"
            + "\n".join(f"  {linha}" for linha in por_gravar.splitlines())
            + "\n\nSe são os ficheiros do commit anterior, falta gravá-los (git add -A e git commit).\n"
            "Se não sabes o que são, corre  git status  e pede ajuda antes de continuar."
        )

    arvore = git("rev-parse", "HEAD^{tree}")
    if arvore != commit["tree_antes"]:
        raise erro(
            f"O teu ramo não está no ponto certo para o commit {numero} da unidade {identificador}.\n"
            + descrever_ponto(arvore, unidades)
            + "\n\nSe esperavas estar mais à frente, a unidade anterior pode ainda não estar junta ao develop.\n"
            "Confirma no GitHub. Depois de ela estar junta, apaga este ramo e cria-o outra vez a partir do develop atualizado."
        )

    origem = unidade["pasta"] / f"commit-{numero}"
    for relativo in commit["ficheiros"]:
        destino = raiz / relativo
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origem / relativo, destino)
    for relativo in commit["apagar"]:
        (raiz / relativo).unlink(missing_ok=True)

    print(f"\nUnidade {identificador}, commit {numero} de {total}")
    n = len(commit["ficheiros"])
    print(f"Copiados {n} ficheiro{'s' if n != 1 else ''}:")
    for relativo in commit["ficheiros"]:
        print(f"  {relativo}")
    if commit["apagar"]:
        print("Apagados:")
        for relativo in commit["apagar"]:
            print(f"  {relativo}")
    print("\nAgora grava o commit:")
    print("  git add -A")
    print(f"  git commit -m \"{commit['mensagem']}\"\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
