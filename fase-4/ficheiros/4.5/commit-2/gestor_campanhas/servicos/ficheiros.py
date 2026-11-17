"""Ficheiros anexados aos criativos.

Quando o marketeer anexa um ficheiro, a aplicação faz uma cópia dele para a
pasta de ficheiros (ver :func:`gestor_campanhas.config.pasta_ficheiros`),
numa pasta com o número do criativo. Assim, o ficheiro continua disponível
mesmo que o original seja apagado ou mudado de sítio.

Este módulo só trata dos ficheiros: copia-os, descreve-os, abre-os e apaga-os.
Não sabe nada de criativos nem de quem pode fazer o quê.
"""

from __future__ import annotations

import mimetypes
import os
import shutil
import subprocess
import sys
from pathlib import Path

from gestor_campanhas import config
from gestor_campanhas.erros import ErroValidacao

#: Nome dado a cada tipo principal de ficheiro, a primeira parte do tipo MIME.
NOMES_TIPOS = {
    "image": "Imagem",
    "video": "Vídeo",
    "audio": "Áudio",
    "text": "Texto",
}


def limpar_caminho(texto: str) -> Path:
    """Converte um caminho escrito pelo utilizador num :class:`~pathlib.Path`.

    Tira os espaços e as aspas à volta. No Windows, a opção "Copiar como
    caminho" do Explorador de Ficheiros põe o caminho entre aspas.

    :param texto: Caminho tal como foi escrito ou colado.
    :return: O caminho, sem aspas.
    """
    return Path(texto.strip().strip('"').strip("'"))


def pasta_do_criativo(criativo_id: int) -> Path:
    """Devolve a pasta onde fica o ficheiro de um criativo.

    :param criativo_id: Número do criativo.
    :return: Caminho da pasta. Pode ainda não existir.
    """
    return config.pasta_ficheiros() / str(criativo_id)


def guardar(origem: str, criativo_id: int) -> str:
    """Copia um ficheiro para a pasta de um criativo.

    O ficheiro que o criativo já tinha, se houver, é apagado: cada criativo
    tem um só ficheiro.

    :param origem: Caminho do ficheiro a copiar, tal como foi escrito.
    :param criativo_id: Número do criativo.
    :return: Nome do ficheiro copiado, por exemplo ``"banner.png"``.
    :raises ErroValidacao: Se o caminho estiver vazio ou não for de um
        ficheiro que existe.
    """
    if not origem.strip():
        raise ErroValidacao("Indique o caminho do ficheiro.")
    caminho = limpar_caminho(origem)
    if not caminho.is_file():
        raise ErroValidacao(f"Não existe nenhum ficheiro em {caminho}.")
    apagar(criativo_id)
    pasta = pasta_do_criativo(criativo_id)
    pasta.mkdir(parents=True)
    shutil.copy2(caminho, pasta / caminho.name)
    return caminho.name


def caminho(criativo_id: int, nome: str) -> Path:
    """Devolve o caminho da cópia de um ficheiro anexado.

    :param criativo_id: Número do criativo.
    :param nome: Nome do ficheiro, tal como foi devolvido por :func:`guardar`.
    :return: Caminho do ficheiro.
    """
    return pasta_do_criativo(criativo_id) / nome


def apagar(criativo_id: int) -> None:
    """Apaga a pasta de um criativo, com o ficheiro que lá estiver.

    Não faz nada se a pasta não existir.

    :param criativo_id: Número do criativo.
    """
    shutil.rmtree(pasta_do_criativo(criativo_id), ignore_errors=True)


def tipo(ficheiro: Path) -> str:
    """Diz que tipo de ficheiro é, a partir da extensão.

    :param ficheiro: Caminho do ficheiro.
    :return: Por exemplo ``"Imagem (image/png)"``, ``"PDF (application/pdf)"``
        ou ``"Desconhecido"``.
    """
    mime, _ = mimetypes.guess_type(ficheiro.name)
    if mime is None:
        return "Desconhecido"
    if mime == "application/pdf":
        return f"PDF ({mime})"
    return f"{NOMES_TIPOS.get(mime.split('/')[0], 'Outro')} ({mime})"


def tamanho(bytes_: int) -> str:
    """Escreve um tamanho de ficheiro de forma legível.

    :param bytes_: Tamanho em bytes.
    :return: Por exemplo ``"512 bytes"``, ``"1,5 KB"`` ou ``"2,0 MB"``.
    """
    if bytes_ < 1024:
        return f"{bytes_} bytes"
    if bytes_ < 1024 * 1024:
        return f"{bytes_ / 1024:.1f} KB".replace(".", ",")
    return f"{bytes_ / (1024 * 1024):.1f} MB".replace(".", ",")


def descrever(ficheiro: Path) -> dict[str, str]:
    """Junta o nome, o tipo e o tamanho de um ficheiro, para a pré-visualização.

    :param ficheiro: Caminho do ficheiro.
    :return: Dicionário com as chaves ``"nome"``, ``"tipo"`` e ``"tamanho"``.
    """
    return {"nome": ficheiro.name, "tipo": tipo(ficheiro), "tamanho": tamanho(ficheiro.stat().st_size)}


def abrir(ficheiro: Path) -> None:
    """Abre um ficheiro no programa predefinido do sistema.

    No Windows usa ``os.startfile``; no macOS, o comando ``open``; no Linux,
    o comando ``xdg-open``.

    :param ficheiro: Caminho do ficheiro.
    :raises OSError: Se o sistema não conseguir abrir o ficheiro.
    """
    if sys.platform.startswith("win"):
        os.startfile(ficheiro)  # esta função só existe no Windows
    elif sys.platform == "darwin":
        subprocess.run(["open", str(ficheiro)], check=True)
    else:
        subprocess.run(["xdg-open", str(ficheiro)], check=True)


def copiar_para(ficheiro: Path, destino: str) -> Path:
    """Copia um ficheiro para uma pasta, sem apagar nenhum ficheiro que lá esteja.

    Se já existir um ficheiro com o mesmo nome, a cópia fica com um número
    entre parênteses, por exemplo ``banner (1).png``.

    :param ficheiro: Caminho do ficheiro a copiar.
    :param destino: Pasta de destino, tal como foi escrita.
    :return: Caminho da cópia.
    :raises ErroValidacao: Se a pasta de destino não existir.
    """
    pasta = limpar_caminho(destino)
    if not pasta.is_dir():
        raise ErroValidacao(f"A pasta {pasta} não existe.")
    copia = pasta / ficheiro.name
    numero = 1
    while copia.exists():
        copia = pasta / f"{ficheiro.stem} ({numero}){ficheiro.suffix}"
        numero += 1
    shutil.copy2(ficheiro, copia)
    return copia
