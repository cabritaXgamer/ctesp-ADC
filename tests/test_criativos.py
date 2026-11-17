"""Testes dos criativos."""

from gestor_campanhas import modelos
from gestor_campanhas.modelos import Criativo


# --- classe Criativo ---------------------------------------------------------


def test_criativo_novo_esta_em_preparacao():
    criativo = Criativo(id=1, campanha_id=1, nome="Banner")

    assert criativo.estado == modelos.EM_PREPARACAO
    assert criativo.nome_estado == "Em preparação"


def test_todos_os_estados_tem_nome():
    nomes = [Criativo(1, 1, "Banner", estado=estado).nome_estado for estado in modelos.NOMES_ESTADOS_CRIATIVO]

    assert nomes == ["Em preparação", "Em revisão", "Aprovado", "Rejeitado", "Publicado"]
