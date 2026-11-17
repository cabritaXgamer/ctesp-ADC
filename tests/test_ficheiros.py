"""Testes dos ficheiros anexados aos criativos."""

from pathlib import Path

import pytest

from gestor_campanhas import config
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.servicos import ficheiros


@pytest.fixture
def pasta_dados(monkeypatch, tmp_path):
    """Põe a pasta de dados numa pasta temporária."""
    pasta = tmp_path / "dados"
    monkeypatch.setenv(config.VARIAVEL_PASTA_DADOS, str(pasta))
    return pasta


@pytest.fixture
def banner(tmp_path):
    """Um ficheiro de imagem pequeno, fora da pasta de dados."""
    ficheiro = tmp_path / "originais" / "banner.png"
    ficheiro.parent.mkdir()
    ficheiro.write_bytes(b"x" * 2048)
    return ficheiro


def test_limpar_caminho_tira_aspas_e_espacos():
    assert ficheiros.limpar_caminho('  "C:/Imagens/banner.png"  ') == Path("C:/Imagens/banner.png")
    assert ficheiros.limpar_caminho("'banner.png'") == Path("banner.png")


def test_guardar_copia_para_a_pasta_do_criativo(pasta_dados, banner):
    nome = ficheiros.guardar(str(banner), 7)

    assert nome == "banner.png"
    copia = ficheiros.caminho(7, nome)
    assert copia == pasta_dados / "ficheiros" / "7" / "banner.png"
    assert copia.read_bytes() == banner.read_bytes()


def test_guardar_aceita_o_caminho_entre_aspas(pasta_dados, banner):
    assert ficheiros.guardar(f'"{banner}"', 7) == "banner.png"


def test_guardar_substitui_o_ficheiro_anterior(pasta_dados, banner, tmp_path):
    ficheiros.guardar(str(banner), 7)
    outro = tmp_path / "originais" / "video.mp4"
    outro.write_bytes(b"v")

    ficheiros.guardar(str(outro), 7)

    assert [ficheiro.name for ficheiro in ficheiros.pasta_do_criativo(7).iterdir()] == ["video.mp4"]


def test_guardar_recusa_um_ficheiro_que_nao_existe(pasta_dados, tmp_path):
    with pytest.raises(ErroValidacao, match="Não existe nenhum ficheiro em"):
        ficheiros.guardar(str(tmp_path / "nada.png"), 7)
    with pytest.raises(ErroValidacao, match="Indique o caminho do ficheiro."):
        ficheiros.guardar("   ", 7)


def test_guardar_recusa_uma_pasta(pasta_dados, tmp_path):
    with pytest.raises(ErroValidacao, match="Não existe nenhum ficheiro em"):
        ficheiros.guardar(str(tmp_path), 7)


def test_apagar_remove_a_pasta_e_nao_falha_se_nao_existir(pasta_dados, banner):
    ficheiros.guardar(str(banner), 7)

    ficheiros.apagar(7)
    ficheiros.apagar(7)

    assert not ficheiros.pasta_do_criativo(7).exists()


@pytest.mark.parametrize(
    ("nome", "esperado"),
    [
        ("banner.png", "Imagem (image/png)"),
        ("video.mp4", "Vídeo (video/mp4)"),
        ("texto.txt", "Texto (text/plain)"),
        ("briefing.pdf", "PDF (application/pdf)"),
        ("sem_extensao", "Desconhecido"),
    ],
)
def test_tipo_a_partir_da_extensao(nome, esperado):
    assert ficheiros.tipo(Path(nome)) == esperado


@pytest.mark.parametrize(
    ("bytes_", "esperado"),
    [(0, "0 bytes"), (512, "512 bytes"), (1536, "1,5 KB"), (2 * 1024 * 1024, "2,0 MB")],
)
def test_tamanho_legivel(bytes_, esperado):
    assert ficheiros.tamanho(bytes_) == esperado


def test_descrever_um_ficheiro(banner):
    assert ficheiros.descrever(banner) == {"nome": "banner.png", "tipo": "Imagem (image/png)", "tamanho": "2,0 KB"}


def test_copiar_para_uma_pasta(banner, tmp_path):
    destino = tmp_path / "transferencias"
    destino.mkdir()

    copia = ficheiros.copiar_para(banner, str(destino))

    assert copia == destino / "banner.png"
    assert copia.read_bytes() == banner.read_bytes()


def test_copiar_nao_apaga_um_ficheiro_com_o_mesmo_nome(banner, tmp_path):
    destino = tmp_path / "transferencias"
    destino.mkdir()
    (destino / "banner.png").write_bytes(b"antigo")

    primeira = ficheiros.copiar_para(banner, str(destino))
    segunda = ficheiros.copiar_para(banner, str(destino))

    assert primeira.name == "banner (1).png"
    assert segunda.name == "banner (2).png"
    assert (destino / "banner.png").read_bytes() == b"antigo"


def test_copiar_para_uma_pasta_que_nao_existe(banner, tmp_path):
    with pytest.raises(ErroValidacao, match="A pasta .* não existe."):
        ficheiros.copiar_para(banner, str(tmp_path / "nao_existe"))
