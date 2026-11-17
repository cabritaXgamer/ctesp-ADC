"""Testes dos criativos."""

from datetime import date

import pytest

from gestor_campanhas import modelos
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Criativo
from gestor_campanhas.repositorios import campanhas as repositorio_campanhas
from gestor_campanhas.repositorios import criativos as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import criativos as servico


@pytest.fixture
def natal(ligacao, contas):
    """Uma campanha da Carla, do Miguel, com budget de 1500 €."""
    return repositorio_campanhas.criar(
        ligacao,
        "Natal",
        "Vender mais",
        contas[modelos.CLIENTE].id,
        contas[modelos.MARKETEER].id,
        date(2026, 12, 1),
        date(2026, 12, 24),
        150000,
    )


@pytest.fixture
def saldos(ligacao, contas):
    """Outra campanha da Carla, do Miguel, sem budget."""
    return repositorio_campanhas.criar(ligacao, "Saldos", "", contas[modelos.CLIENTE].id, contas[modelos.MARKETEER].id)


@pytest.fixture
def marta(ligacao, contas):
    """Um segundo marketeer, sem campanhas."""
    return utilizadores.criar(ligacao, "Marta Marques", "marta@agencia.pt", "x", modelos.MARKETEER)


def nomes(lista):
    return [criativo.nome for criativo in lista]


# --- classe Criativo ---------------------------------------------------------


def test_criativo_novo_esta_em_preparacao():
    criativo = Criativo(id=1, campanha_id=1, nome="Banner")

    assert criativo.estado == modelos.EM_PREPARACAO
    assert criativo.nome_estado == "Em preparação"


def test_todos_os_estados_tem_nome():
    nomes_estados = [Criativo(1, 1, "Banner", estado=estado).nome_estado for estado in modelos.NOMES_ESTADOS_CRIATIVO]

    assert nomes_estados == ["Em preparação", "Em revisão", "Aprovado", "Rejeitado", "Publicado"]


# --- base de dados -----------------------------------------------------------


def test_repositorio_guarda_e_le_um_criativo(ligacao, natal):
    criativo = repositorio.criar(ligacao, natal.id, "Banner de Natal", "Árvore e presentes")

    assert criativo == repositorio.obter_por_id(ligacao, criativo.id)
    assert criativo.campanha_id == natal.id
    assert criativo.nome == "Banner de Natal"
    assert criativo.descricao == "Árvore e presentes"
    assert criativo.estado == modelos.EM_PREPARACAO
    assert criativo.campanha_nome == "Natal"


def test_repositorio_devolve_none_quando_o_criativo_nao_existe(ligacao):
    assert repositorio.obter_por_id(ligacao, 999) is None


def test_repositorio_lista_so_os_criativos_da_campanha(ligacao, natal, saldos):
    repositorio.criar(ligacao, natal.id, "Banner", "")
    repositorio.criar(ligacao, saldos.id, "Cartaz", "")
    repositorio.criar(ligacao, natal.id, "Vídeo", "")

    assert nomes(repositorio.listar_por_campanha(ligacao, natal.id)) == ["Banner", "Vídeo"]
    assert nomes(repositorio.listar_por_campanha(ligacao, saldos.id)) == ["Cartaz"]


def test_repositorio_atualiza_o_nome_e_a_descricao(ligacao, natal):
    criativo = repositorio.criar(ligacao, natal.id, "Banner", "")

    alterado = repositorio.atualizar(ligacao, criativo.id, "Banner grande", "Com o logótipo")

    assert alterado.nome == "Banner grande"
    assert alterado.descricao == "Com o logótipo"
    assert repositorio.obter_por_id(ligacao, criativo.id) == alterado


def test_repositorio_elimina_e_conta_criativos(ligacao, natal, saldos):
    banner = repositorio.criar(ligacao, natal.id, "Banner", "")
    repositorio.criar(ligacao, natal.id, "Vídeo", "")

    repositorio.eliminar(ligacao, banner.id)

    assert repositorio.obter_por_id(ligacao, banner.id) is None
    assert repositorio.contar_por_campanha(ligacao, natal.id) == 1
    assert repositorio.contar_por_campanha(ligacao, saldos.id) == 0


# --- regras ------------------------------------------------------------------


def test_marketeer_cria_um_criativo_na_sua_campanha(ligacao, contas, natal):
    criativo = servico.criar(ligacao, contas[modelos.MARKETEER], natal.id, "  Banner  ", "  Árvore  ")

    assert criativo.nome == "Banner"
    assert criativo.descricao == "Árvore"
    assert criativo.estado == modelos.EM_PREPARACAO
    assert servico.listar_da_campanha(ligacao, natal) == [criativo]


def test_criativo_tem_de_ter_nome(ligacao, contas, natal):
    with pytest.raises(ErroValidacao, match="O nome não pode ficar vazio."):
        servico.criar(ligacao, contas[modelos.MARKETEER], natal.id, "   ")

    assert servico.listar_da_campanha(ligacao, natal) == []


def test_marketeer_nao_cria_criativos_em_campanhas_de_outro(ligacao, natal, marta):
    with pytest.raises(ErroValidacao, match=f"Não tem nenhuma campanha com o número {natal.id}."):
        servico.criar(ligacao, marta, natal.id, "Banner")


def test_nao_cria_criativos_numa_campanha_que_nao_existe(ligacao, contas):
    with pytest.raises(ErroValidacao, match="Não tem nenhuma campanha com o número 999."):
        servico.criar(ligacao, contas[modelos.MARKETEER], 999, "Banner")


def test_marketeer_edita_o_seu_criativo(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner")

    alterado = servico.editar(ligacao, miguel, criativo.id, "Banner grande", "Com o logótipo")

    assert alterado.nome == "Banner grande"
    assert alterado.descricao == "Com o logótipo"


def test_editar_com_nome_vazio_nao_altera_nada(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner", "Árvore")

    with pytest.raises(ErroValidacao):
        servico.editar(ligacao, miguel, criativo.id, "", "Outra")

    assert repositorio.obter_por_id(ligacao, criativo.id) == criativo


def test_marketeer_nao_mexe_em_criativos_de_outro(ligacao, contas, natal, marta):
    criativo = servico.criar(ligacao, contas[modelos.MARKETEER], natal.id, "Banner")

    with pytest.raises(ErroValidacao, match=f"Não tem nenhum criativo com o número {criativo.id}."):
        servico.editar(ligacao, marta, criativo.id, "Meu")
    with pytest.raises(ErroValidacao, match="Não tem nenhum criativo"):
        servico.eliminar(ligacao, marta, criativo.id)

    assert repositorio.obter_por_id(ligacao, criativo.id) == criativo


def test_nao_encontra_um_criativo_que_nao_existe(ligacao, contas):
    with pytest.raises(ErroValidacao, match="Não tem nenhum criativo com o número 999."):
        servico.obter_do_marketeer(ligacao, contas[modelos.MARKETEER], 999)


def test_marketeer_elimina_o_seu_criativo(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    banner = servico.criar(ligacao, miguel, natal.id, "Banner")
    video = servico.criar(ligacao, miguel, natal.id, "Vídeo")

    eliminado = servico.eliminar(ligacao, miguel, banner.id)

    assert eliminado == banner
    assert servico.listar_da_campanha(ligacao, natal) == [video]
