"""Gera os guias passo a passo de cada fase, uma página por pessoa.

O texto próprio de cada unidade de trabalho (issue, pull request, como testar,
explicação do código) é escrito à mão em ``fases/fase-N/``. Tudo o que se
repete de unidade para unidade (criar o ramo, copiar os commits, abrir o pull
request, rever, juntar) é escrito aqui uma só vez. Os dados que vêm do Git
(código de cada commit, ficheiros, comandos) são lidos do repositório, para
nunca ficarem trocados.

Utilização, a partir da pasta ``_guias``::

    python ferramentas/gerar_guias.py

Ficheiros lidos:

``config.json``
    Endereço dos dois repositórios e nomes dos membros.
``fases/fase-N/fase.md``
    Dados da fase. Secções: ``entrega``, ``trello``.
``fases/fase-N/<id>.md``
    Uma unidade de trabalho. Cabeçalho com ``id``, ``titulo``, ``ramo``,
    ``quem``, ``revisor``, ``milestone``. Secções: ``issue``, ``pr``,
    ``testar``, ``verificar``, ``explicacao``.
``fases/fase-N/extra-<pessoa>.md``
    Passos adicionais de uma pessoa. Cada secção ``passo: Título`` é um passo.
``modelos/*.md``
    Páginas soltas com marcadores ``{{REPO_A}}``, ``{{REPO_B}}``, ``{{INICIAL}}``.

Ficheiros escritos: ``fase-N/README.md``, ``fase-N/<pessoa>.md`` e uma página
por cada ficheiro de ``modelos``.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

#: Pasta ``_guias``.
GUIAS = Path(__file__).resolve().parent.parent

#: Pasta do repositório de código (a pasta acima de ``_guias``).
REPO = GUIAS.parent

#: Ramo de integração onde as unidades são fundidas.
RAMO_INTEGRACAO = "develop"

#: Endereço mostrado enquanto não se souber o do repositório oficial.
REPO_B_POR_DEFINIR = "https://github.com/DONO/REPOSITORIO-OFICIAL"


# --------------------------------------------------------------------------
# Leitura do Git
# --------------------------------------------------------------------------


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
    """Devolve o commit de merge que fundiu um ramo em ``develop``."""
    ponta = git("rev-parse", ramo)
    for merge in git("rev-list", "--first-parent", "--merges", RAMO_INTEGRACAO).split():
        if git("rev-parse", f"{merge}^2") == ponta:
            return merge
    raise SystemExit(f"O ramo {ramo} não foi fundido em {RAMO_INTEGRACAO}.")


def commits_do_ramo(ramo: str) -> list[dict]:
    """Devolve os commits de um ramo, do mais antigo para o mais recente.

    Cada commit é um dicionário com ``sha`` (curto), ``mensagem``,
    ``ficheiros`` e ``resumo`` (a linha "N files changed, ...").
    """
    merge = merge_do_ramo(ramo)
    commits = []
    for sha in git("rev-list", "--reverse", "--no-merges", f"{merge}^1..{merge}^2").split():
        mensagem = git("log", "-1", "--format=%s", sha)
        if '"' in mensagem:
            raise SystemExit(f"A mensagem do commit {sha} tem aspas: {mensagem}")
        commits.append(
            {
                "sha": git("rev-parse", "--short", sha),
                "mensagem": mensagem,
                "ficheiros": [f for f in git("show", "--name-only", "--format=", sha).split("\n") if f],
                "resumo": git("show", "--shortstat", "--format=", sha).strip(),
            }
        )
    return commits


# --------------------------------------------------------------------------
# Leitura dos ficheiros escritos à mão
# --------------------------------------------------------------------------


def ler_ficheiro(caminho: Path) -> tuple[dict, list[tuple[str, str]]]:
    """Lê um ficheiro com cabeçalho e secções.

    O cabeçalho fica entre duas linhas ``---`` e tem pares ``chave: valor``.
    Cada secção começa numa linha ``@@ nome`` e vai até à secção seguinte.

    :return: O cabeçalho e a lista de ``(nome, texto)`` das secções, por ordem.
    """
    texto = caminho.read_text(encoding="utf-8")
    cabecalho: dict = {}
    if texto.startswith("---\n"):
        bloco, texto = texto[4:].split("\n---\n", 1)
        for linha in bloco.splitlines():
            chave, _, valor = linha.partition(":")
            cabecalho[chave.strip()] = valor.strip()
    seccoes: list[tuple[str, str]] = []
    nome, linhas = None, []
    for linha in texto.splitlines():
        if linha.startswith("@@ "):
            if nome is not None:
                seccoes.append((nome, "\n".join(linhas).strip()))
            nome, linhas = linha[3:].strip(), []
        else:
            linhas.append(linha)
    if nome is not None:
        seccoes.append((nome, "\n".join(linhas).strip()))
    return cabecalho, seccoes


def sem_acentos(texto: str) -> str:
    """Devolve o texto em minúsculas e sem acentos, para nomes de ficheiros."""
    normal = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in normal if unicodedata.category(c) != "Mn")


def bloco(texto: str, linguagem: str = "") -> str:
    """Envolve um texto num bloco de código Markdown."""
    return f"```{linguagem}\n{texto}\n```"


# --------------------------------------------------------------------------
# Textos comuns
# --------------------------------------------------------------------------


def aviso_repo_b(config: dict) -> str:
    """Aviso mostrado enquanto o endereço do repositório oficial não é conhecido."""
    if config["repo_b"] != REPO_B_POR_DEFINIR:
        return ""
    return (
        "> **Atenção:** ainda não sei o endereço do vosso repositório oficial. "
        f"Onde aparecer `{REPO_B_POR_DEFINIR}`, usa o endereço verdadeiro.\n\n"
    )


def passos_autor(u: dict, anterior: dict | None, config: dict, ref_revisor: str) -> list[tuple[str, str]]:
    """Passos de quem faz uma unidade de trabalho."""
    b = config["repo_b"]
    ramo, n = u["ramo"], len(u["commits"])
    passos = []

    if anterior is None:
        corpo = (
            "Antes do primeiro passo tens de ter feito a [Preparação](../preparacao.md), "
            "e o repositório oficial já tem de ter o ramo `develop` (Parte B da Preparação)."
        )
    else:
        corpo = (
            f"Esta unidade assenta na anterior. O pull request **{anterior['titulo']}** "
            f"(unidade {anterior['id']}) tem de estar junto ao `develop`.\n\n"
            f"Abre {b}/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo "
            "**Merged**. Se não estiver, espera: ainda não podes começar."
        )
    passos.append(("Confirma que podes começar", corpo))

    passos.append(
        (
            f"Cria a issue da unidade {u['id']}",
            "A issue é o registo, no GitHub, do trabalho que vai ser feito. "
            "O pull request que vais abrir mais à frente fecha-a sozinho.\n\n"
            f"**a)** Abre {b}/issues e clica no botão verde **New issue**. "
            "Se aparecer uma lista de modelos, escolhe **Blank issue**.\n\n"
            "**b)** No campo do título, cola:\n\n"
            + bloco(f"[{u['id']}] {u['titulo']}", "text")
            + "\n\n**c)** Na caixa grande de texto, cola:\n\n"
            + bloco(u["issue"], "markdown")
            + "\n\n**d)** Na coluna da direita, escolhe:\n\n"
            "- **Assignees:** tu (clica em *assign yourself*)\n"
            "- **Labels:** `tarefa`\n"
            f"- **Milestone:** `{u['milestone']}`\n\n"
            "**e)** Clica no botão verde **Create** (em alguns ecrãs chama-se *Submit new issue*).\n\n"
            "**f)** Repara no número que aparece a seguir ao título, por exemplo `#3`. "
            "Aponta-o: vais precisar dele quando abrires o pull request.",
        )
    )

    passos.append(
        (
            "Atualiza o teu computador e cria o ramo",
            "Abre o terminal na pasta do repositório oficial e corre:\n\n"
            + bloco(f"git fetch origin\ngit fetch trabalho\ngit switch develop\ngit pull\ngit switch -c {ramo}", "bash")
            + "\n\n| Comando | O que faz |\n|---|---|\n"
            "| `git fetch origin` | Vai ver o que há de novo no repositório oficial. Não mexe nos teus ficheiros |\n"
            "| `git fetch trabalho` | Vai buscar ao repositório de trabalho os commits que lá estão. Também não mexe nos teus ficheiros |\n"
            "| `git switch develop` | Muda para o ramo `develop` |\n"
            "| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |\n"
            f"| `git switch -c {ramo}` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |\n\n"
            f"**Deves ver**, na última linha: `Switched to a new branch '{ramo}'`.",
        )
    )

    linhas = [
        f"São {n} commits. Para cada um há dois comandos:\n\n"
        "| Comando | O que faz |\n|---|---|\n"
        "| `git cherry-pick -n <código>` | Copia para a tua pasta as alterações de um commit do repositório de trabalho, "
        "sem as gravar. O `-n` quer dizer \"ainda não faças commit\". Se correr bem, não mostra nada |\n"
        "| `git commit -m \"mensagem\"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |\n\n"
        "Faz um commit de cada vez, pela ordem em que estão aqui. Cola as duas linhas, carrega em Enter e "
        "confirma o que aparece antes de passares ao seguinte.\n"
    ]
    for i, c in enumerate(u["commits"], start=1):
        ficheiros = ", ".join(f"`{f}`" for f in c["ficheiros"])
        linhas.append(
            f"**Commit {i} de {n}** — {ficheiros}\n\n"
            + bloco(f"git cherry-pick -n {c['sha']}\ngit commit -m \"{c['mensagem']}\"", "bash")
            + f"\n\n**Deves ver** uma linha a terminar em `{c['resumo']}`.\n"
        )
    linhas.append(
        "Se o `git cherry-pick` mostrar a palavra `CONFLICT`, para. "
        "Vê a secção \"Se algo correr mal\" na [página da fase](README.md)."
    )
    passos.append((f"Copia os {n} commits", "\n".join(linhas)))

    mensagens = "\n".join(f"xxxxxxx {c['mensagem']}" for c in reversed(u["commits"]))
    passos.append(
        (
            "Confirma que ficou igual ao original",
            bloco(f"git status\ngit diff --stat trabalho/{ramo}\ngit log --oneline -{n}", "bash")
            + "\n\n| Comando | O que deves ver |\n|---|---|\n"
            "| `git status` | `nothing to commit, working tree clean`: não ficou nada por gravar |\n"
            f"| `git diff --stat trabalho/{ramo}` | Nada. Este comando compara o teu ramo com o do repositório de trabalho; "
            "se não mostra nada, estão iguais |\n"
            f"| `git log --oneline -{n}` | Os teus {n} commits, do mais recente para o mais antigo |\n\n"
            "A lista do `git log` deve ser esta. Os códigos à esquerda vão ser diferentes dos do repositório "
            "de trabalho, porque os commits agora são teus:\n\n" + bloco(mensagens, "text"),
        )
    )

    passos.append(("Experimenta o que copiaste", u["testar"]))

    passos.append(
        (
            "Envia o ramo para o GitHub",
            bloco(f"git push -u origin {ramo}", "bash")
            + "\n\nO `push` envia o teu ramo e os teus commits para o repositório oficial. "
            "O `-u` liga o ramo do teu computador ao do GitHub, para os próximos `push` e `pull` não precisarem de mais nada.\n\n"
            "Na primeira vez pode abrir-se uma janela a pedir para entrares na tua conta do GitHub. Entra e volta ao terminal.\n\n"
            f"**Deves ver**, perto do fim: `* [new branch]      {ramo} -> {ramo}`.",
        )
    )

    passos.append(
        (
            "Abre o pull request",
            f"O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que {u['revisor']} vai rever o teu trabalho.\n\n"
            f"**a)** Abre {b}/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão "
            "**Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, "
            f"em *compare*, escolhe `{ramo}`.\n\n"
            f"**b)** Confirma, no topo, que está **base: develop** e **compare: {ramo}**. "
            "Se a base for `main`, muda para `develop`.\n\n"
            "**c)** No título, cola:\n\n"
            + bloco(u["titulo"], "text")
            + "\n\n**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. "
            "Troca `#N` pelo número da issue que apontaste:\n\n"
            + bloco(u["pr"], "markdown")
            + "\n\n**e)** Na coluna da direita, escolhe:\n\n"
            f"- **Reviewers:** {u['revisor']} (no GitHub, `{config['utilizadores'][u['revisor']]}`)\n"
            "- **Assignees:** tu\n"
            "- **Labels:** `tarefa`\n"
            f"- **Milestone:** `{u['milestone']}`\n\n"
            "**f)** Clica no botão verde **Create pull request**.\n\n"
            "**g)** Se aparecerem verificações automáticas no fundo da página (*Testes*, *Documentação*), "
            "espera um ou dois minutos até ficarem com um visto verde.",
        )
    )

    passos.append(
        (
            f"Avisa {u['revisor']}",
            f"Diz a {u['revisor']} que o pull request da unidade {u['id']} está pronto para rever. "
            f"A partir daqui é a vez de {u['revisor']}: {ref_revisor}.",
        )
    )

    passos.append(
        (
            f"Quando {u['revisor']} disser que juntou, arruma o teu computador",
            bloco(f"git switch develop\ngit pull\ngit branch -d {ramo}", "bash")
            + "\n\n| Comando | O que faz |\n|---|---|\n"
            "| `git switch develop` | Volta ao ramo `develop` |\n"
            "| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |\n"
            f"| `git branch -d {ramo}` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |",
        )
    )
    return passos


def passos_revisor(u: dict, config: dict, ref_autor: str, ref_seguinte: str) -> list[tuple[str, str]]:
    """Passos de quem revê e junta uma unidade de trabalho."""
    b = config["repo_b"]
    ramo, autor = u["ramo"], u["quem"]
    passos = []

    passos.append(
        (
            f"Abre o pull request de {autor}",
            f"Faz este passo quando {autor} te avisar que o pull request da unidade {u['id']} está pronto.\n\n"
            f"Abre {b}/pulls e clica em **{u['titulo']}**.",
        )
    )

    passos.append(
        (
            "Lê as alterações",
            "Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.\n\n"
            "Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a "
            "descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número "
            "da linha, clica no `+` azul e escreve a pergunta.",
        )
    )

    passos.append(
        (
            "Experimenta no teu computador",
            f"Traz para o teu computador o ramo de {autor}:\n\n"
            + bloco(f"git fetch origin\ngit switch --track origin/{ramo}", "bash")
            + "\n\n| Comando | O que faz |\n|---|---|\n"
            f"| `git fetch origin` | Vai buscar ao repositório oficial os ramos novos, incluindo o de {autor} |\n"
            f"| `git switch --track origin/{ramo}` | Cria no teu computador uma cópia desse ramo e muda para ela |\n\n"
            "Agora experimenta:\n\n" + u["testar"] + "\n\nConfirma também:\n\n" + u["verificar"],
        )
    )

    passos.append(
        (
            "Aprova",
            "**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** "
            "(em alguns ecrãs chama-se *Submit review*).\n\n"
            "**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que "
            "experimentaste e o que viste.\n\n"
            "**c)** Escolhe **Approve** e clica em **Submit review**.\n\n"
            "Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e "
            f"avisa {autor}. Não avances para o passo seguinte.",
        )
    )

    passos.append(
        (
            "Junta o pull request ao develop (merge)",
            "**a)** Volta ao separador **Conversation** e desce até ao fundo da página.\n\n"
            "**b)** Confirma que as verificações automáticas, se existirem, têm um visto verde.\n\n"
            "**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou "
            "*Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.\n\n"
            "**d)** Clica em **Merge pull request** e depois em **Confirm merge**.\n\n"
            "**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.\n\n"
            "**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da unidade fica fechada sozinha.",
        )
    )

    passos.append(
        (
            "Atualiza o teu computador e confirma o resultado",
            bloco(
                f"git switch develop\ngit pull\ngit branch -d {ramo}\ngit fetch trabalho\ngit diff --stat {u['merge']} develop",
                "bash",
            )
            + "\n\n| Comando | O que faz |\n|---|---|\n"
            "| `git switch develop` | Volta ao ramo `develop` |\n"
            "| `git pull` | Traz do GitHub o `develop` com o pull request já junto |\n"
            f"| `git branch -d {ramo}` | Apaga a cópia do ramo que criaste para experimentar |\n"
            "| `git fetch trabalho` | Atualiza a informação do repositório de trabalho |\n"
            f"| `git diff --stat {u['merge']} develop` | Compara o vosso `develop` com o do repositório de trabalho "
            "neste mesmo ponto |\n\n"
            "**Deves ver:** o último comando não mostra nada. Se mostrar nomes de ficheiros, os dois repositórios "
            "ficaram diferentes: não avancem e digam-me que ficheiros aparecem.",
        )
    )

    passos.append(
        (
            "Avisa o grupo",
            f"Diz a {autor} que o pull request está junto e que já pode arrumar o computador ({ref_autor}).\n\n"
            + ref_seguinte,
        )
    )
    return passos


# --------------------------------------------------------------------------
# Montagem das páginas
# --------------------------------------------------------------------------


def carregar_fase(pasta: Path) -> dict:
    """Lê os ficheiros de uma fase e junta-lhes os dados do Git."""
    cabecalho, seccoes = ler_ficheiro(pasta / "fase.md")
    fase = {**cabecalho, **dict(seccoes), "pasta": pasta.name, "unidades": [], "extras": {}}
    for ficheiro in sorted(pasta.glob("[0-9]*.md")):
        cabecalho, seccoes = ler_ficheiro(ficheiro)
        unidade = {**cabecalho, **dict(seccoes)}
        unidade["commits"] = commits_do_ramo(unidade["ramo"])
        unidade["merge"] = git("rev-parse", "--short", merge_do_ramo(unidade["ramo"]))
        fase["unidades"].append(unidade)
    for ficheiro in sorted(pasta.glob("extra-*.md")):
        _, seccoes = ler_ficheiro(ficheiro)
        pessoa = ficheiro.stem.removeprefix("extra-")
        fase["extras"][pessoa] = [(nome.removeprefix("passo:").strip(), texto) for nome, texto in seccoes]
    return fase


def planear_vezes(fase: dict, config: dict) -> list[dict]:
    """Calcula a ordem das vezes e os números dos passos de cada pessoa.

    Cada unidade dá origem a duas vezes: a de quem a faz e a de quem a revê.
    Os passos de cada pessoa são numerados de seguida, pela ordem das vezes.
    """
    vezes = []
    for unidade in fase["unidades"]:
        vezes.append({"pessoa": unidade["quem"], "papel": "autor", "unidade": unidade})
        vezes.append({"pessoa": unidade["revisor"], "papel": "revisor", "unidade": unidade})
    proximo = {pessoa: 1 for pessoa in config["membros"]}
    for vez in vezes:
        total = 10 if vez["papel"] == "autor" else 7
        vez["primeiro"] = proximo[vez["pessoa"]]
        vez["ultimo"] = vez["primeiro"] + total - 1
        proximo[vez["pessoa"]] += total
    for pessoa in config["membros"]:
        extras = fase["extras"].get(sem_acentos(pessoa), [])
        if extras:
            vezes.append(
                {
                    "pessoa": pessoa,
                    "papel": "extra",
                    "passos": extras,
                    "primeiro": proximo[pessoa],
                    "ultimo": proximo[pessoa] + len(extras) - 1,
                }
            )
    return vezes


def descricao_vez(vez: dict) -> str:
    """Descrição curta de uma vez, para as tabelas de resumo."""
    if vez["papel"] == "extra":
        return "; ".join(titulo for titulo, _ in vez["passos"])
    u = vez["unidade"]
    if vez["papel"] == "autor":
        return f"Fazer a unidade {u['id']} — {u['titulo']}"
    return f"Rever e juntar a unidade {u['id']} (de {u['quem']})"


def quando_vez(vez: dict, vezes: list[dict]) -> str:
    """Diz quando é que uma vez pode começar."""
    if vez["papel"] == "extra":
        return "Em qualquer altura depois da Preparação"
    indice = vezes.index(vez)
    if indice == 0:
        return "Logo a seguir à Preparação"
    anterior = vezes[indice - 1]
    if anterior["pessoa"] == vez["pessoa"]:
        return "A seguir ao teu passo anterior"
    if vez["papel"] == "revisor":
        return f"Quando {anterior['pessoa']} avisar que o pull request está aberto"
    return f"Quando {anterior['pessoa']} avisar que juntou a unidade {anterior['unidade']['id']}"


def pagina(pessoa: str) -> str:
    """Nome do ficheiro da página de uma pessoa."""
    return f"{sem_acentos(pessoa)}.md"


def passos_texto(vez: dict) -> str:
    """Texto "passo N" ou "passos N a M" de uma vez."""
    if vez["primeiro"] == vez["ultimo"]:
        return f"passo {vez['primeiro']}"
    return f"passos {vez['primeiro']} a {vez['ultimo']}"


def gerar_pagina_pessoa(pessoa: str, fase: dict, vezes: list[dict], config: dict) -> str:
    """Gera a página passo a passo de uma pessoa."""
    minhas = [v for v in vezes if v["pessoa"] == pessoa]
    partes = [
        f"# Fase {fase['numero']} — Passo a passo de {pessoa}\n",
        aviso_repo_b(config)
        + f"Esta página tem tudo o que **{pessoa}** faz na Fase {fase['numero']} ({fase['titulo']}), por ordem. "
        "Cada passo diz o que fazer, onde, e o que deves ver no fim. "
        "Não saltes passos e não avances se o resultado não for o esperado.\n",
        "Se algum termo não for claro, vê [O que é o quê](../conceitos.md). "
        "A ordem geral da fase está na [página da fase](README.md).\n",
        "## Os teus passos\n",
        "| Passos | O que fazes | Quando |\n|---|---|---|",
    ]
    for vez in minhas:
        intervalo = f"{vez['primeiro']} a {vez['ultimo']}" if vez["ultimo"] > vez["primeiro"] else str(vez["primeiro"])
        partes[-1] += f"\n| {intervalo} | {descricao_vez(vez)} | {quando_vez(vez, vezes)} |"
    partes.append(
        "\nOs comandos são para colar no terminal, dentro da pasta do repositório oficial. "
        "Funcionam no terminal do VS Code, no PowerShell e no Git Bash.\n"
    )

    for vez in minhas:
        if vez["papel"] == "extra":
            partes.append("---\n\n## Outras tarefas desta fase\n")
            passos = vez["passos"]
        else:
            u = vez["unidade"]
            indice = vezes.index(vez)
            if vez["papel"] == "autor":
                partes.append(f"---\n\n## Fazer a unidade {u['id']} — {u['titulo']}\n\n{u['resumo']}\n")
                anterior = fase["unidades"][fase["unidades"].index(u) - 1] if fase["unidades"].index(u) > 0 else None
                revisao = vezes[indice + 1]
                ref_revisor = f"[página de {revisao['pessoa']}]({pagina(revisao['pessoa'])}), {passos_texto(revisao)}"
                passos = passos_autor(u, anterior, config, ref_revisor)
            else:
                partes.append(
                    f"---\n\n## Rever e juntar a unidade {u['id']} — {u['titulo']}\n\n"
                    f"Quem fez: {u['quem']}. Tu confirmas que funciona e juntas o trabalho ao `develop`.\n"
                )
                autoria = vezes[indice - 1]
                ref_autor = f"passo {autoria['ultimo']} da [página de {autoria['pessoa']}]({pagina(autoria['pessoa'])})"
                seguintes = [v for v in vezes[indice + 1 :] if v["papel"] == "autor"]
                if not seguintes:
                    ref_seguinte = (
                        "Esta era a última unidade da fase. Falta o fecho, descrito na [página da fase](README.md)."
                    )
                elif seguintes[0]["pessoa"] == pessoa:
                    ref_seguinte = f"A unidade seguinte é tua: continua no passo {seguintes[0]['primeiro']}."
                else:
                    s = seguintes[0]
                    ref_seguinte = (
                        f"Diz também a {s['pessoa']} que já pode começar a unidade {s['unidade']['id']} "
                        f"([página de {s['pessoa']}]({pagina(s['pessoa'])}), passo {s['primeiro']})."
                    )
                passos = passos_revisor(u, config, ref_autor, ref_seguinte)
            assert len(passos) == vez["ultimo"] - vez["primeiro"] + 1, (pessoa, u["id"], len(passos))
        for numero, (titulo, corpo) in enumerate(passos, start=vez["primeiro"]):
            partes.append(f"### Passo {numero} — {titulo}\n\n{corpo}\n")

    explicadas = [v["unidade"] for v in minhas if v["papel"] == "autor"]
    if explicadas:
        partes.append(
            "---\n\n## O código que gravaste, explicado\n\n"
            "Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. "
            "Lê com os ficheiros abertos ao lado.\n"
        )
        for u in explicadas:
            partes.append(f"### Unidade {u['id']} — {u['titulo']}\n\n{u['explicacao']}\n")
    return "\n".join(partes).replace("{{REPO_A}}", config["repo_a"]).replace("{{REPO_B}}", config["repo_b"])


def gerar_pagina_fase(fase: dict, vezes: list[dict], config: dict) -> str:
    """Gera a página de entrada de uma fase."""
    b = config["repo_b"]
    partes = [
        f"# Fase {fase['numero']} — {fase['titulo']}\n",
        aviso_repo_b(config) + fase["entrega"] + "\n",
        "## Páginas de cada um\n",
        "Cada pessoa segue a sua página, do primeiro ao último passo.\n",
        "| Pessoa | Página |\n|---|---|",
    ]
    for pessoa in config["membros"]:
        partes[-1] += f"\n| {pessoa} | [{pagina(pessoa)}]({pagina(pessoa)}) |"
    partes.append(
        "\nAntes da primeira fase, todos fazem a [Preparação](../preparacao.md). "
        "Os termos usados estão explicados em [O que é o quê](../conceitos.md).\n"
    )
    partes.append("## Ordem de trabalho\n")
    partes.append(
        "As unidades assentam umas nas outras, por isso o trabalho é feito à vez, por esta ordem. "
        "Cada linha só começa quando a anterior acabou.\n"
    )
    partes.append("| Vez | Quem | O que faz | Onde está explicado |\n|---|---|---|---|")
    numero = 0
    for vez in vezes:
        if vez["papel"] == "extra":
            continue
        numero += 1
        partes[-1] += (
            f"\n| {numero} | {vez['pessoa']} | {descricao_vez(vez)} | "
            f"[{pagina(vez['pessoa'])}]({pagina(vez['pessoa'])}), {passos_texto(vez)} |"
        )
    extras = [v for v in vezes if v["papel"] == "extra"]
    if extras:
        partes.append("\nTarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:\n")
        partes.append("| Quem | O que faz | Onde está explicado |\n|---|---|---|")
        for vez in extras:
            partes[-1] += (
                f"\n| {vez['pessoa']} | {descricao_vez(vez)} | "
                f"[{pagina(vez['pessoa'])}]({pagina(vez['pessoa'])}), {passos_texto(vez)} |"
            )

    n_testes = fase.get("testes", "")
    partes.append(
        "\n## Fecho da fase\n\n"
        "Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou "
        "igual ao de trabalho.\n\n"
        + bloco("git switch develop\ngit pull\ngit fetch trabalho\ngit diff --stat trabalho/develop develop", "bash")
        + "\n\nO último comando não deve mostrar nada. Segunda confirmação:\n\n"
        + bloco('git rev-parse "develop^{tree}"', "bash")
        + f"\n\nO resultado tem de ser exatamente:\n\n"
        + bloco(git("rev-parse", f"{RAMO_INTEGRACAO}^{{tree}}"), "text")
        + "\n\nEste código identifica o conteúdo de todos os ficheiros. Se for igual, os dois repositórios têm "
        "exatamente os mesmos ficheiros.\n\n"
        "Depois, confirma que tudo funciona:\n\n"
        + bloco("python -m pytest", "bash")
        + f"\n\nDeve terminar com `{n_testes} passed`.\n\n"
        + bloco("python -m sphinx -W -b html docs docs/_build/html", "bash")
        + "\n\nDeve terminar com `build succeeded.`\n\n"
        + bloco("python -m gestor_campanhas", "bash")
        + "\n\nDeve aparecer o menu inicial.\n"
    )
    partes.append("### Lista de verificação\n")
    lista = [
        f"{len(fase['unidades'])} issues de tarefa fechadas (ver {b}/issues?q=is%3Aissue+is%3Aclosed)",
        f"{len(fase['unidades'])} pull requests juntos ao `develop`, cada um aprovado por outra pessoa do grupo (ver {b}/pulls?q=is%3Apr+is%3Amerged)",
    ]
    lista += [linha.strip()[2:] for linha in fase.get("verificacao", "").splitlines() if linha.strip().startswith("- ")]
    lista += ["`git diff --stat trabalho/develop develop` não mostra nada", "Testes a passar e documentação gerada sem avisos"]
    partes.append("\n".join(f"- [ ] {item}" for item in lista) + "\n")
    partes.append(
        f"Quando estiver tudo, digam-me **\"avança para a Fase {int(fase['numero']) + 1}\"** e contem-me os "
        "problemas que tiveram.\n"
    )
    if fase.get("trello"):
        partes.append("## Trello\n\n" + fase["trello"] + "\n")
    partes.append(
        "## Se algo correr mal\n\n"
        "| O que aconteceu | O que fazer |\n|---|---|\n"
        "| O `git cherry-pick -n` mostra `CONFLICT` | O teu ramo não está igual ao esperado, quase sempre porque a unidade anterior "
        "ainda não foi junta ou porque saltaste um commit. Corre `git reset --hard` para desfazer a tentativa e diz-me o que apareceu |\n"
        "| Enganei-me num commit e ainda não fiz `push` | Corre `git reset --hard develop` (o ramo volta a ficar igual ao `develop`) "
        "e recomeça no passo \"Copia os commits\" |\n"
        "| O commit ficou com o nome ou o email errado e ainda não fiz `push` | Corrige o nome e o email (Preparação, passo A2) "
        "e corre `git commit --amend --reset-author --no-edit` |\n"
        "| `fatal: not a git repository` | O terminal não está na pasta do repositório. Usa `cd` para entrar nela |\n"
        "| `error: pathspec ... did not match` ou `bad revision` no `cherry-pick` | Falta ir buscar os commits: corre `git fetch trabalho` e repete |\n"
        "| O `git push` é recusado com `403` ou `Permission denied` | A tua conta ainda não é colaboradora do repositório oficial, "
        "ou não aceitaste o convite |\n"
        "| O `git push` é recusado por causa do email (`GH007`) | O GitHub está a proteger o teu email. Em GitHub → Settings → Emails "
        "copia o endereço que termina em `users.noreply.github.com`, usa-o no `git config --global user.email` e corre "
        "`git commit --amend --reset-author --no-edit` |\n"
        "| O `git diff --stat` de confirmação mostra ficheiros | Não avancem. Digam-me que ficheiros aparecem |\n"
        "| Uma verificação automática fica com uma cruz vermelha | Clica em *Details* ao lado da verificação, copia o erro e envia-mo |\n"
        "| O `python` não é reconhecido | Experimenta `py` em vez de `python`. Se também não der, falta instalar o Python (Preparação, passo A1) |\n"
    )
    return "\n".join(partes).replace("{{REPO_A}}", config["repo_a"]).replace("{{REPO_B}}", b)


def main() -> int:
    """Gera todas as páginas."""
    config = json.loads((GUIAS / "config.json").read_text(encoding="utf-8"))
    config["repo_b"] = config.get("repo_b") or REPO_B_POR_DEFINIR
    inicial = git("rev-parse", "--short", git("rev-list", "--max-parents=0", RAMO_INTEGRACAO))

    escritos = []
    for modelo in sorted((GUIAS / "modelos").glob("*.md")):
        texto = modelo.read_text(encoding="utf-8")
        texto = texto.replace("{{AVISO_REPO_B}}", aviso_repo_b(config))
        texto = texto.replace("{{REPO_A}}", config["repo_a"]).replace("{{REPO_B}}", config["repo_b"])
        texto = texto.replace("{{INICIAL}}", inicial)
        escritos.append((GUIAS / modelo.name, texto))

    for pasta in sorted((GUIAS / "fases").glob("fase-*")):
        fase = carregar_fase(pasta)
        vezes = planear_vezes(fase, config)
        destino = GUIAS / pasta.name
        escritos.append((destino / "README.md", gerar_pagina_fase(fase, vezes, config)))
        for pessoa in config["membros"]:
            escritos.append((destino / pagina(pessoa), gerar_pagina_pessoa(pessoa, fase, vezes, config)))

    for caminho, texto in escritos:
        por_preencher = re.findall(r"\{\{[A-Z_:]+\}\}", texto)
        if por_preencher:
            raise SystemExit(f"{caminho}: marcadores por preencher: {sorted(set(por_preencher))}")
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(texto.rstrip("\n") + "\n", encoding="utf-8", newline="\n")
        print(f"escrito: {caminho.relative_to(GUIAS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
