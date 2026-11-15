"""Gestão das contas de clientes e de marketeers, feita pelo Administrador."""

from __future__ import annotations

import sqlite3
import unicodedata

from gestor_campanhas.modelos import Utilizador
from gestor_campanhas.repositorios import utilizadores


def simplificar(texto: str) -> str:
    """Prepara um texto para ser comparado sem contar acentos nem maiúsculas.

    ``"José"`` e ``"jose"`` ficam iguais depois de simplificados.

    :param texto: Texto original.
    :return: O texto em minúsculas, sem acentos e sem espaços à volta.
    """
    # A forma NFD separa cada letra do seu acento ("é" passa a "e" + "´").
    # Os acentos ficam na categoria "Mn" e são deixados de fora.
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acentos = "".join(letra for letra in decomposto if unicodedata.category(letra) != "Mn")
    return sem_acentos.casefold().strip()


def listar(ligacao: sqlite3.Connection, perfil: str, pesquisa: str = "") -> list[Utilizador]:
    """Lista as contas de um perfil, com pesquisa opcional por nome.

    A pesquisa encontra os nomes que contêm o texto indicado, em qualquer
    posição, sem distinguir maiúsculas nem acentos.

    :param ligacao: Ligação aberta à base de dados.
    :param perfil: Perfil das contas a listar.
    :param pesquisa: Parte do nome a procurar. Vazio para listar todas.
    :return: Contas encontradas, por ordem alfabética do nome. Inclui as
        desativadas.
    """
    contas = utilizadores.listar_por_perfil(ligacao, perfil)
    procurado = simplificar(pesquisa)
    if procurado:
        contas = [conta for conta in contas if procurado in simplificar(conta.nome)]
    # A ordenação é feita aqui, e não no SQL, porque o SQLite põe as letras
    # com acento depois do "z": "Álvaro" ficaria no fim da lista.
    return sorted(contas, key=lambda conta: simplificar(conta.nome))
