"""Cria no GitHub as issues das user stories, a partir de ``issues.json``.

É opcional: as issues também podem ser criadas à mão, copiando de ``issues.md``.

Precisa do GitHub CLI (``gh``) instalado e com sessão iniciada na conta de quem
vai ficar como autor das issues::

    winget install GitHub.cli
    gh auth login

As labels e as milestones têm de existir antes (ver ``fase-0.md``).

Utilização::

    python criar_issues.py --repo DONO/REPO --perfil Administrador --simular
    python criar_issues.py --repo DONO/REPO --perfil Administrador

Com ``--simular`` o script só mostra o que faria, sem criar nada.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

FICHEIRO = Path(__file__).resolve().parent / "issues.json"
PERFIS = ["Administrador", "Marketeer", "Cliente"]


def main() -> int:
    """Lê os argumentos e cria as issues do perfil escolhido."""
    analisador = argparse.ArgumentParser(description="Cria as issues das user stories no GitHub.")
    analisador.add_argument("--repo", required=True, help="repositório de destino, no formato DONO/REPO")
    analisador.add_argument("--perfil", required=True, choices=PERFIS, help="perfil das issues a criar")
    analisador.add_argument("--simular", action="store_true", help="mostrar o que seria criado, sem criar")
    argumentos = analisador.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    todas = json.loads(FICHEIRO.read_text(encoding="utf-8"))
    escolhidas = [issue for issue in todas if issue["perfil"] == argumentos.perfil]
    print(f"{len(escolhidas)} issues do perfil {argumentos.perfil} para {argumentos.repo}")

    for issue in escolhidas:
        comando = [
            "gh", "issue", "create",
            "--repo", argumentos.repo,
            "--title", issue["titulo"],
            "--body", issue["corpo"],
            "--milestone", issue["milestone"],
        ]
        for label in issue["labels"]:
            comando += ["--label", label]
        if argumentos.simular:
            print(f"[simulação] {issue['titulo']}")
            print(f"            labels: {', '.join(issue['labels'])} | milestone: {issue['milestone']}")
            continue
        resultado = subprocess.run(comando, capture_output=True, encoding="utf-8")
        if resultado.returncode != 0:
            print(f"ERRO em {issue['id']}: {resultado.stderr.strip()}")
            print("As issues anteriores já foram criadas. Corrigir o problema e criar as restantes à mão.")
            return 1
        print(f"{issue['id']} criada: {resultado.stdout.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
