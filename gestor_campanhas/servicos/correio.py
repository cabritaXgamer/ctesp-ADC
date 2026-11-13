"""Envio de emails, simulado com ficheiros de texto.

A aplicação corre na linha de comandos e não tem servidor de email. Em vez de
enviar a mensagem, escreve-a num ficheiro da pasta ``caixa_saida``, dentro da
pasta de dados. Quem quiser "ler o email" abre esse ficheiro.
"""

from __future__ import annotations

import re
from pathlib import Path

from gestor_campanhas import config, relogio


def enviar(destinatario: str, assunto: str, corpo: str) -> Path:
    """Escreve um email na caixa de saída.

    O nome do ficheiro tem a data, a hora e o destinatário, para os emails
    ficarem por ordem e ser fácil encontrar o de cada pessoa.

    :param destinatario: Email de quem recebe.
    :param assunto: Assunto da mensagem.
    :param corpo: Texto da mensagem.
    :return: Caminho do ficheiro criado.
    """
    pasta = config.pasta_caixa_saida()
    pasta.mkdir(parents=True, exist_ok=True)
    agora = relogio.agora()
    # No nome do ficheiro ficam só letras, algarismos, pontos e hífenes.
    nome_seguro = re.sub(r"[^A-Za-z0-9.-]", "_", destinatario)
    base = f"{agora.strftime('%Y%m%d-%H%M%S')}-{nome_seguro}"
    ficheiro = pasta / f"{base}.txt"
    numero = 2
    while ficheiro.exists():
        ficheiro = pasta / f"{base}-{numero}.txt"
        numero += 1
    texto = f"Para: {destinatario}\nData: {relogio.para_texto(agora)}\nAssunto: {assunto}\n\n{corpo}\n"
    ficheiro.write_text(texto, encoding="utf-8")
    return ficheiro
