"""Testes do painel de marketeers: trabalho, carga e inatividade."""

from datetime import date, datetime

import pytest

from gestor_campanhas import modelos, relogio, seguranca
from gestor_campanhas.cli import painel as menu
from gestor_campanhas.cli import perfis
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.repositorios import atividades
from gestor_campanhas.repositorios import campanhas as campanhas_bd
from gestor_campanhas.repositorios import criativos as criativos_bd
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import comentarios as servico_comentarios
from gestor_campanhas.servicos import criativos as servico_criativos
from gestor_campanhas.servicos import painel as servico
from tests.conftest import PASSWORD_TESTE


@pytest.fixture
def relogio_falso(monkeypatch):
    """Relógio que começa a 19 de novembro de 2026, às 10h00, e que os testes podem acertar.

    Devolve um dicionário: mudar ``relogio_falso["agora"]`` muda a hora atual.
    """
    estado = {"agora": datetime(2026, 11, 19, 10, 0)}
    monkeypatch.setattr(relogio, "agora", lambda: estado["agora"])
    return estado


@pytest.fixture(autouse=True)
def dia_19_de_novembro(relogio_falso):
    """Todos os testes começam a 19 de novembro de 2026, às 10h00."""
    return relogio_falso


@pytest.fixture
def miguel(contas):
    """O marketeer Miguel, da fixture ``contas``."""
    return contas[modelos.MARKETEER]


@pytest.fixture
def marta(ligacao):
    """Uma segunda marketeer."""
    return utilizadores.criar(
        ligacao, "Marta Marques", "marta@agencia.pt", seguranca.gerar_hash(PASSWORD_TESTE), modelos.MARKETEER
    )


@pytest.fixture
def natal(ligacao, contas, miguel):
    """Campanha da Carla, do Miguel, de 1 a 24 de dezembro, com um budget de 1500 €."""
    return campanhas_bd.criar(
        ligacao, "Natal 2026", "", contas[modelos.CLIENTE].id, miguel.id, date(2026, 12, 1), date(2026, 12, 24), 150000
    )


@pytest.fixture
def bicicletas(ligacao, contas, marta):
    """Campanha da Carla, da Marta, sem datas."""
    return campanhas_bd.criar(ligacao, "Bicicletas", "", contas[modelos.CLIENTE].id, marta.id)


# --- base de dados -----------------------------------------------------------


def test_repositorio_regista_e_lista_as_atividades_da_mais_recente_para_a_mais_antiga(
    ligacao, miguel, marta, relogio_falso
):
    primeira = atividades.registar(ligacao, miguel.id, "Criou o criativo Banner")
    atividades.registar(ligacao, marta.id, "De outra pessoa")
    relogio_falso["agora"] = datetime(2026, 11, 19, 11, 0)
    segunda = atividades.registar(ligacao, miguel.id, "Editou o criativo Banner")

    lista = atividades.listar_por_utilizador(ligacao, miguel.id)

    assert lista == [segunda, primeira]
    assert primeira.descricao == "Criou o criativo Banner"
    assert primeira.registada_em == datetime(2026, 11, 19, 10, 0)
    assert segunda.registada_em == datetime(2026, 11, 19, 11, 0)


def test_repositorio_lista_so_as_atividades_mais_recentes(ligacao, miguel):
    for numero in range(7):
        atividades.registar(ligacao, miguel.id, f"Atividade {numero}")

    lista = atividades.listar_por_utilizador(ligacao, miguel.id, limite=3)

    assert [atividade.descricao for atividade in lista] == ["Atividade 6", "Atividade 5", "Atividade 4"]


def test_repositorio_devolve_a_ultima_atividade_de_cada_marketeer(ligacao, miguel, marta, relogio_falso):
    atividades.registar(ligacao, miguel.id, "Antiga")
    relogio_falso["agora"] = datetime(2026, 11, 20, 9, 0)
    atividades.registar(ligacao, miguel.id, "Recente")

    assert atividades.ultima_por_utilizador(ligacao) == {miguel.id: datetime(2026, 11, 20, 9, 0)}


def test_repositorio_lista_os_criativos_das_campanhas_de_um_marketeer(ligacao, miguel, natal, bicicletas):
    banner = criativos_bd.criar(ligacao, natal.id, "Banner", "")
    criativos_bd.criar(ligacao, bicicletas.id, "Anúncio", "")
    video = criativos_bd.criar(ligacao, natal.id, "Vídeo", "")

    assert criativos_bd.listar_por_marketeer(ligacao, miguel.id) == [banner, video]


def test_repositorio_devolve_o_criativo_mais_recente_de_cada_marketeer(
    ligacao, miguel, marta, natal, bicicletas, relogio_falso
):
    criativos_bd.criar(ligacao, natal.id, "Banner", "")
    relogio_falso["agora"] = datetime(2026, 11, 21, 15, 30)
    criativos_bd.criar(ligacao, natal.id, "Vídeo", "")
    relogio_falso["agora"] = datetime(2026, 11, 20, 8, 0)
    criativos_bd.criar(ligacao, bicicletas.id, "Anúncio", "")

    assert criativos_bd.ultima_criacao_por_marketeer(ligacao) == {
        miguel.id: datetime(2026, 11, 21, 15, 30),
        marta.id: datetime(2026, 11, 20, 8, 0),
    }


# --- registo da atividade ----------------------------------------------------


def _descricoes(ligacao, marketeer):
    """Devolve as descrições das atividades de um marketeer, da mais antiga para a mais recente."""
    return [atividade.descricao for atividade in reversed(atividades.listar_por_utilizador(ligacao, marketeer.id, 20))]


def test_alteracoes_aos_criativos_ficam_na_atividade_do_marketeer(ligacao, miguel, natal, tmp_path):
    criativo = servico_criativos.criar(ligacao, miguel, natal.id, "Banner")
    servico_criativos.editar(ligacao, miguel, criativo.id, "Banner grande")
    origem = tmp_path / "banner.png"
    origem.write_bytes(b"imagem")
    servico_criativos.anexar(ligacao, miguel, criativo.id, str(origem))
    servico_criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.EM_REVISAO)
    servico_criativos.mudar_estado(ligacao, miguel, criativo.id, modelos.EM_PREPARACAO)
    servico_criativos.eliminar(ligacao, miguel, criativo.id)

    assert _descricoes(ligacao, miguel) == [
        "Criou o criativo Banner (campanha Natal 2026)",
        "Editou o criativo Banner grande (campanha Natal 2026)",
        "Anexou o ficheiro banner.png ao criativo Banner grande (campanha Natal 2026)",
        "Passou a Em revisão o criativo Banner grande (campanha Natal 2026)",
        "Passou a Em preparação o criativo Banner grande (campanha Natal 2026)",
        "Eliminou o criativo Banner grande (campanha Natal 2026)",
    ]


def test_resposta_a_um_comentario_fica_na_atividade_do_marketeer(ligacao, contas, miguel, natal):
    banner = criativos_bd.criar(ligacao, natal.id, "Banner", "")
    comentario = servico_comentarios.comentar(ligacao, contas[modelos.CLIENTE], banner.id, "Maior, por favor")

    servico_comentarios.responder(ligacao, miguel, comentario.id, "Combinado")

    assert _descricoes(ligacao, miguel) == ["Respondeu a um comentário do criativo Banner (campanha Natal 2026)"]


def test_alteracao_recusada_nao_fica_na_atividade(ligacao, miguel, natal):
    with pytest.raises(ErroValidacao):
        servico_criativos.criar(ligacao, miguel, natal.id, "")

    assert _descricoes(ligacao, miguel) == []


# --- regras do painel --------------------------------------------------------


def _criativo(ligacao, campanha, nome, estado=modelos.EM_PREPARACAO, prazo=None):
    """Cria um criativo diretamente no repositório, já no estado pedido."""
    criativo = criativos_bd.criar(ligacao, campanha.id, nome, "", prazo=prazo)
    if estado != modelos.EM_PREPARACAO:
        criativo = criativos_bd.definir_estado(ligacao, criativo.id, estado)
    return criativo


def _por_nome(lista):
    return {indicadores.marketeer.nome: indicadores for indicadores in lista}


def test_dias_sem_atividade_sao_sete_por_omissao(ligacao):
    assert servico.dias_sem_atividade(ligacao) == 7


def test_administrador_muda_os_dias_sem_atividade(ligacao):
    servico.definir_dias_sem_atividade(ligacao, 3)

    assert servico.dias_sem_atividade(ligacao) == 3


def test_dias_sem_atividade_tem_de_ser_pelo_menos_um(ligacao):
    with pytest.raises(ErroValidacao, match="O número de dias tem de ser pelo menos 1."):
        servico.definir_dias_sem_atividade(ligacao, 0)

    assert servico.dias_sem_atividade(ligacao) == 7


@pytest.mark.parametrize(
    ("estado", "prazo", "atrasado"),
    [
        (modelos.EM_PREPARACAO, date(2026, 11, 18), True),
        (modelos.EM_REVISAO, date(2026, 11, 18), True),
        (modelos.REJEITADO, date(2026, 11, 18), True),
        (modelos.EM_PREPARACAO, date(2026, 11, 19), False),
        (modelos.EM_PREPARACAO, None, False),
        (modelos.APROVADO, date(2026, 11, 18), False),
        (modelos.PUBLICADO, date(2026, 11, 18), False),
    ],
)
def test_criativo_em_atraso(ligacao, natal, estado, prazo, atrasado):
    criativo = _criativo(ligacao, natal, "Banner", estado, prazo)

    assert servico.em_atraso(criativo) is atrasado


def test_carga_conta_os_criativos_de_cada_marketeer(ligacao, miguel, marta, natal, bicicletas):
    _criativo(ligacao, natal, "Atrasado", modelos.EM_PREPARACAO, date(2026, 11, 10))
    _criativo(ligacao, natal, "Em revisão", modelos.EM_REVISAO, date(2026, 11, 30))
    _criativo(ligacao, natal, "Rejeitado", modelos.REJEITADO)
    _criativo(ligacao, natal, "Aprovado", modelos.APROVADO)
    _criativo(ligacao, natal, "Publicado", modelos.PUBLICADO, date(2026, 11, 1))
    _criativo(ligacao, bicicletas, "Anúncio")

    resultado = _por_nome(servico.carga(ligacao))

    assert list(resultado) == ["Marta Marques", "Miguel Marketeer"]
    miguel_carga = resultado["Miguel Marketeer"]
    assert (miguel_carga.campanhas_ativas, miguel_carga.ativos, miguel_carga.em_atraso, miguel_carga.concluidos) == (
        1,
        3,
        1,
        2,
    )
    marta_carga = resultado["Marta Marques"]
    assert (marta_carga.campanhas_ativas, marta_carga.ativos, marta_carga.em_atraso, marta_carga.concluidos) == (
        1,
        1,
        0,
        0,
    )


def test_carga_num_periodo_so_conta_os_criativos_com_prazo_nesse_periodo(ligacao, miguel, natal):
    _criativo(ligacao, natal, "Antes", prazo=date(2026, 10, 31))
    _criativo(ligacao, natal, "Primeiro dia", prazo=date(2026, 11, 1))
    _criativo(ligacao, natal, "Último dia", modelos.PUBLICADO, prazo=date(2026, 11, 30))
    _criativo(ligacao, natal, "Depois", prazo=date(2026, 12, 1))
    _criativo(ligacao, natal, "Sem prazo")

    (indicadores,) = servico.carga(ligacao, date(2026, 11, 1), date(2026, 11, 30))

    assert (indicadores.ativos, indicadores.concluidos) == (1, 1)


def test_carga_com_so_uma_das_datas(ligacao, miguel, natal):
    _criativo(ligacao, natal, "Antes", prazo=date(2026, 10, 31))
    _criativo(ligacao, natal, "Depois", prazo=date(2026, 12, 1))
    _criativo(ligacao, natal, "Sem prazo")

    assert servico.carga(ligacao, desde=date(2026, 11, 1))[0].ativos == 1
    assert servico.carga(ligacao, ate=date(2026, 11, 1))[0].ativos == 1


def test_carga_recusa_um_periodo_ao_contrario(ligacao, miguel):
    with pytest.raises(ErroValidacao, match="A data inicial não pode ser posterior à data final."):
        servico.carga(ligacao, date(2026, 11, 30), date(2026, 11, 1))


def test_carga_nao_inclui_marketeers_desativados(ligacao, miguel, marta):
    utilizadores.definir_ativo(ligacao, marta.id, False)

    assert [indicadores.marketeer.nome for indicadores in servico.carga(ligacao)] == ["Miguel Marketeer"]


def test_ultima_atividade_e_a_mais_recente_entre_registos_e_criativos(
    ligacao, miguel, marta, natal, bicicletas, relogio_falso
):
    _criativo(ligacao, natal, "Banner")
    relogio_falso["agora"] = datetime(2026, 11, 20, 9, 0)
    atividades.registar(ligacao, miguel.id, "Editou o criativo Banner")
    relogio_falso["agora"] = datetime(2026, 11, 21, 9, 0)
    _criativo(ligacao, bicicletas, "Anúncio")
    relogio_falso["agora"] = datetime(2026, 11, 20, 18, 0)
    atividades.registar(ligacao, marta.id, "Antes do criativo")

    resultado = _por_nome(servico.carga(ligacao))

    assert resultado["Miguel Marketeer"].ultima_atividade == datetime(2026, 11, 20, 9, 0)
    assert resultado["Marta Marques"].ultima_atividade == datetime(2026, 11, 21, 9, 0)


def test_marketeer_sem_nada_nao_tem_ultima_atividade(ligacao, marta):
    (indicadores,) = servico.carga(ligacao)

    assert indicadores.ultima_atividade is None


@pytest.mark.parametrize(
    ("ativos", "ultima", "esperado"),
    [
        (0, datetime(2026, 11, 19, 9, 0), "Sem criativos ativos"),
        (2, None, "Sem atividade registada"),
        (2, datetime(2026, 11, 12, 23, 0), "Parado há 7 dias"),
        (2, datetime(2026, 11, 18, 8, 0), "Parado há 1 dia"),
        (2, datetime(2026, 11, 13, 8, 0), ""),
        (2, datetime(2026, 11, 19, 9, 0), ""),
    ],
)
def test_situacao_de_um_marketeer(miguel, ativos, ultima, esperado):
    indicadores = servico.Carga(miguel, ativos=ativos, ultima_atividade=ultima)
    dias = 1 if esperado == "Parado há 1 dia" else 7

    assert servico.situacao(indicadores, dias) == esperado


def test_trabalho_junta_as_campanhas_aos_criativos(ligacao, contas, miguel, natal):
    vazia = campanhas_bd.criar(ligacao, "Páscoa", "", contas[modelos.CLIENTE].id, miguel.id)
    banner = _criativo(ligacao, natal, "Banner")

    assert servico.trabalho(ligacao, miguel) == [(natal, [banner]), (vazia, [])]


def test_ultimas_atividades_sao_as_cinco_mais_recentes(ligacao, miguel):
    for numero in range(6):
        atividades.registar(ligacao, miguel.id, f"Atividade {numero}")

    assert [atividade.descricao for atividade in servico.ultimas_atividades(ligacao, miguel)] == [
        "Atividade 5",
        "Atividade 4",
        "Atividade 3",
        "Atividade 2",
        "Atividade 1",
    ]


# --- menus -------------------------------------------------------------------


def test_painel_esta_no_menu_do_administrador_depois_dos_horarios():
    opcoes = [descricao for descricao, _ in perfis.OPCOES[modelos.ADMINISTRADOR]]

    assert opcoes[6:8] == ["Horários de entrada e saída dos marketeers", "Painel de marketeers"]
    assert dict(perfis.OPCOES[modelos.ADMINISTRADOR])["Painel de marketeers"] is menu.painel


def test_painel_mostra_a_carga_e_a_situacao_de_cada_marketeer(
    teclado, ligacao, contas, miguel, marta, natal, bicicletas, relogio_falso, capsys
):
    relogio_falso["agora"] = datetime(2026, 11, 10, 9, 0)
    _criativo(ligacao, bicicletas, "Anúncio")
    relogio_falso["agora"] = datetime(2026, 11, 19, 10, 0)
    _criativo(ligacao, natal, "Banner", prazo=date(2026, 11, 15))
    _criativo(ligacao, natal, "Vídeo", modelos.PUBLICADO)
    teclado("0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert (
        "N.º  Marketeer         Campanhas ativas  Ativos  Em atraso  Concluídos  Última atividade  Situação\n"
        "---  ----------------  ----------------  ------  ---------  ----------  ----------------  ----------------\n"
        f"{marta.id}    Marta Marques     1                 1       0          0           2026-11-10        "
        "Parado há 9 dias\n"
        f"{miguel.id}    Miguel Marketeer  1                 1       1          1           2026-11-19\n"
    ) in saida
    assert "Sem atividade: sem criativos ativos, ou sem mexer nos criativos há 7 dias ou mais." in saida
    assert "Marketeers sem atividade: 1 (Marta Marques)." in saida
    assert "1. Ver o trabalho de um marketeer" in saida
    assert "2. Comparar num período" in saida
    assert "3. Mudar os dias sem atividade" in saida


def test_painel_sem_marketeers_parados(teclado, ligacao, contas, miguel, natal, capsys):
    _criativo(ligacao, natal, "Banner")
    teclado("0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Nenhum marketeer está sem atividade." in capsys.readouterr().out


def test_ver_o_trabalho_de_um_marketeer(teclado, ligacao, contas, miguel, natal, capsys):
    campanhas_bd.criar(ligacao, "Páscoa", "", contas[modelos.CLIENTE].id, miguel.id)
    atrasado = _criativo(ligacao, natal, "Banner", prazo=date(2026, 11, 15))
    publicado = _criativo(ligacao, natal, "Vídeo", modelos.PUBLICADO, prazo=date(2026, 11, 15))
    atividades.registar(ligacao, miguel.id, "Criou o criativo Banner (campanha Natal 2026)")
    teclado("1", str(miguel.id), "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Trabalho de Miguel Marketeer" in saida
    assert f"Campanha n.º {natal.id}: Natal 2026 (Carla Cliente), Por começar" in saida
    assert f"{atrasado.id}    Banner    Em preparação  2026-11-15  Em atraso" in saida
    assert f"{publicado.id}    Vídeo     Publicado      2026-11-15\n" in saida
    assert "Páscoa (Carla Cliente), Em curso\n  Ainda não tem criativos." in saida
    assert "Últimas atividades\n  2026-11-19 10:00  Criou o criativo Banner (campanha Natal 2026)" in saida


def test_ver_o_trabalho_de_um_marketeer_sem_campanhas(teclado, ligacao, contas, marta, capsys):
    teclado("1", str(marta.id), "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Não é responsável por nenhuma campanha." in saida
    assert "Últimas atividades: nenhuma registada." in saida


def test_ver_o_trabalho_so_aceita_marketeers(teclado, ligacao, contas, capsys):
    teclado("1", str(contas[modelos.CLIENTE].id), "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    assert f"Não existe nenhum marketeer com o número {contas[modelos.CLIENTE].id}." in capsys.readouterr().out


def test_comparar_num_periodo(teclado, ligacao, contas, miguel, marta, natal, capsys):
    _criativo(ligacao, natal, "Em novembro", prazo=date(2026, 11, 15))
    _criativo(ligacao, natal, "Publicado em novembro", modelos.PUBLICADO, prazo=date(2026, 11, 20))
    _criativo(ligacao, natal, "Em dezembro", prazo=date(2026, 12, 5))
    teclado("2", "2026-11-01", "2026-11-30", "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Contam os criativos com o prazo dentro do período." in saida
    assert "Carga de trabalho de 2026-11-01 a 2026-11-30" in saida
    assert (
        "N.º  Marketeer         Criativos  Ativos  Em atraso  Concluídos\n"
        "---  ----------------  ---------  ------  ---------  ----------\n"
        f"{marta.id}    Marta Marques     0          0       0          0\n"
        f"{miguel.id}    Miguel Marketeer  2          1       1          1\n"
    ) in saida


@pytest.mark.parametrize(
    ("desde", "ate", "titulo"),
    [
        ("2026-11-01", "", "Carga de trabalho a partir de 2026-11-01"),
        ("", "2026-11-30", "Carga de trabalho até 2026-11-30"),
        ("", "", "Carga de trabalho sem limite de datas"),
    ],
)
def test_comparar_com_periodo_aberto(teclado, ligacao, contas, miguel, desde, ate, titulo, capsys):
    teclado("2", desde, ate, "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    assert titulo in capsys.readouterr().out


def test_comparar_recusa_um_periodo_ao_contrario(teclado, ligacao, contas, miguel, capsys):
    teclado("2", "2026-11-30", "2026-11-01", "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    assert "A data inicial não pode ser posterior à data final." in capsys.readouterr().out


def test_mudar_os_dias_sem_atividade(teclado, ligacao, contas, miguel, natal, relogio_falso, capsys):
    relogio_falso["agora"] = datetime(2026, 11, 17, 9, 0)
    _criativo(ligacao, natal, "Banner")
    relogio_falso["agora"] = datetime(2026, 11, 19, 10, 0)
    teclado("3", "2", "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Um marketeer fica sem atividade ao fim de 7 dias sem mexer nos criativos." in saida
    assert "Guardado. Um marketeer fica sem atividade ao fim de 2 dias." in saida
    assert "Marketeers sem atividade: 1 (Miguel Marketeer)." in saida
    assert "Parado há 2 dias" in saida
    assert servico.dias_sem_atividade(ligacao) == 2


def test_mudar_os_dias_recusa_zero(teclado, ligacao, contas, capsys):
    teclado("3", "0", "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    assert "O número de dias tem de ser pelo menos 1. Nada foi alterado." in capsys.readouterr().out
    assert servico.dias_sem_atividade(ligacao) == 7


def test_mudar_os_dias_com_enter_mantem(teclado, ligacao, contas, capsys):
    teclado("3", "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    assert "Guardado" not in capsys.readouterr().out


def test_com_um_dia_o_painel_escreve_no_singular(teclado, ligacao, contas, miguel, capsys):
    servico.definir_dias_sem_atividade(ligacao, 1)
    teclado("3", "", "0")

    menu.painel(ligacao, contas[modelos.ADMINISTRADOR])

    saida = capsys.readouterr().out
    assert "Sem atividade: sem criativos ativos, ou sem mexer nos criativos há 1 dia ou mais." in saida
    assert "Um marketeer fica sem atividade ao fim de 1 dia sem mexer nos criativos." in saida
