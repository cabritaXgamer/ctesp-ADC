"""Preenche o modelo de um guia de fase com os dados reais do Git.

O texto de cada guia é escrito à mão em ``modelos/fase-N.md``. Os dados que
vêm do repositório (SHA dos commits, ficheiros tocados, comandos a executar)
são inseridos por este script, para nunca ficarem trocados.

Utilização, a partir da pasta ``_guias``::

    python ferramentas/gerar_guia.py modelos/fase-0.md fase-0.md

Marcadores reconhecidos no modelo:

``{{COMMITS:<ramo>}}``
    Tabela com os commits do ramo, pela ordem em que devem ser replicados.
``{{COMANDOS:<ramo>}}``
    Bloco de comandos para replicar o ramo no Repo B.
``{{MERGE:<ramo>}}``
    Commit de merge do ramo em ``develop``, para comparar depois de cada unidade.
``{{TREE}}``
    Identificador do conteúdo do ramo ``develop`` (``git rev-parse develop^{tree}``).
``{{HEAD}}``
    Commit atual do ramo ``develop``.
``{{INICIAL}}``
    Primeiro commit do ramo ``develop``.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

#: Pasta do repositório de código (a pasta acima de ``_guias``).
REPO = Path(__file__).resolve().parent.parent.parent

#: Ramo de integração onde as unidades são fundidas.
RAMO_INTEGRACAO = "develop"


def git(*argumentos: str) -> str:
    """Executa um comando git no repositório de código e devolve a saída."""
    resultado = subprocess.run(
        ["git", "-c", "core.quotepath=false", *argumentos],
        cwd=REPO,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return resultado.stdout.strip()


def merge_do_ramo(ramo: str) -> str:
    """Devolve o commit de merge que fundiu um ramo em ``develop``.

    :param ramo: Nome do ramo, por exemplo ``feature/0.1-estrutura-pacote``.
    :return: SHA completo do commit de merge.
    """
    ponta = git("rev-parse", ramo)
    for merge in git("rev-list", "--first-parent", "--merges", RAMO_INTEGRACAO).split():
        if git("rev-parse", f"{merge}^2") == ponta:
            return merge
    raise SystemExit(f"O ramo {ramo} não foi fundido em {RAMO_INTEGRACAO}.")


def commits_do_ramo(ramo: str) -> list[tuple[str, str, list[str]]]:
    """Devolve os commits de um ramo já fundido em ``develop``.

    :param ramo: Nome do ramo, por exemplo ``feature/0.1-estrutura-pacote``.
    :return: Lista de ``(sha curto, mensagem, ficheiros)``, do mais antigo
        para o mais recente.
    """
    merge = merge_do_ramo(ramo)
    commits = []
    for sha in git("rev-list", "--reverse", "--no-merges", f"{merge}^1..{merge}^2").split():
        curto = git("rev-parse", "--short", sha)
        mensagem = git("log", "-1", "--format=%s", sha)
        ficheiros = git("show", "--name-only", "--format=", sha).split("\n")
        commits.append((curto, mensagem, [f for f in ficheiros if f]))
    return commits


def tabela_commits(ramo: str) -> str:
    """Gera a tabela Markdown com os commits de um ramo."""
    linhas = ["| # | SHA | Mensagem | Ficheiros |", "|---|---|---|---|"]
    for numero, (sha, mensagem, ficheiros) in enumerate(commits_do_ramo(ramo), start=1):
        lista = "<br>".join(f"`{f}`" for f in ficheiros)
        linhas.append(f"| {numero} | `{sha}` | `{mensagem}` | {lista} |")
    return "\n".join(linhas)


def comandos(ramo: str) -> str:
    """Gera o bloco de comandos que replica um ramo no Repo B."""
    linhas = [
        "```bash",
        "git fetch trabalho",
        f"git switch {RAMO_INTEGRACAO}",
        "git pull",
        f"git switch -c {ramo}",
    ]
    for sha, mensagem, _ in commits_do_ramo(ramo):
        if '"' in mensagem:
            raise SystemExit(f"A mensagem do commit {sha} tem aspas: {mensagem}")
        linhas += ["", f"git cherry-pick -n {sha}", f'git commit -m "{mensagem}"']
    linhas += ["", f"git push -u origin {ramo}", "```"]
    return "\n".join(linhas)


def preencher(texto: str) -> str:
    """Substitui todos os marcadores de um modelo."""
    texto = re.sub(r"\{\{COMMITS:([^}]+)\}\}", lambda m: tabela_commits(m.group(1)), texto)
    texto = re.sub(r"\{\{COMANDOS:([^}]+)\}\}", lambda m: comandos(m.group(1)), texto)
    texto = re.sub(
        r"\{\{MERGE:([^}]+)\}\}",
        lambda m: git("rev-parse", "--short", merge_do_ramo(m.group(1))),
        texto,
    )
    texto = texto.replace("{{TREE}}", git("rev-parse", f"{RAMO_INTEGRACAO}^{{tree}}"))
    texto = texto.replace("{{HEAD}}", git("rev-parse", "--short", RAMO_INTEGRACAO))
    inicial = git("rev-list", "--max-parents=0", RAMO_INTEGRACAO)
    texto = texto.replace("{{INICIAL}}", git("rev-parse", "--short", inicial))
    por_preencher = re.findall(r"\{\{[^}]*\}\}", texto)
    if por_preencher:
        raise SystemExit(f"Marcadores desconhecidos: {por_preencher}")
    return texto


def main() -> int:
    """Lê o modelo, preenche os marcadores e escreve o guia."""
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    modelo, destino = Path(sys.argv[1]), Path(sys.argv[2])
    guia = preencher(modelo.read_text(encoding="utf-8"))
    destino.write_text(guia, encoding="utf-8", newline="\n")
    print(f"Guia escrito em {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
