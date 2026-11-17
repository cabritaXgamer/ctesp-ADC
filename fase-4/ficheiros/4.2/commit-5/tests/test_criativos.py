"""Testes dos criativos."""

from datetime import date

import pytest

from gestor_campanhas import dados_demo, modelos
from gestor_campanhas.cli import criativos as menu
from gestor_campanhas.cli import perfis
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Criativo
from gestor_campanhas.repositorios import campanhas as repositorio_campanhas
from gestor_campanhas.repositorios import criativos as repositorio
from gestor_campanhas.repositorios import utilizadores
from gestor_campanhas.servicos import campanhas as servico_campanhas
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


def test_repositorio_guarda_o_custo_o_prazo_o_publico_e_a_plataforma(ligacao, natal):
    criativo = repositorio.criar(
        ligacao, natal.id, "Banner", "", 40000, date(2026, 11, 25), "Famílias com filhos", "Facebook"
    )

    lido = repositorio.obter_por_id(ligacao, criativo.id)
    assert lido.custo_centimos == 40000
    assert lido.prazo == date(2026, 11, 25)
    assert lido.publico_alvo == "Famílias com filhos"
    assert lido.plataforma == "Facebook"


def test_repositorio_aceita_criativo_sem_custo_nem_prazo(ligacao, natal):
    criativo = repositorio.criar(ligacao, natal.id, "Banner", "")

    assert criativo.custo_centimos is None
    assert criativo.prazo is None
    assert criativo.publico_alvo == ""
    assert criativo.plataforma == ""


def test_repositorio_atualiza_todos_os_dados(ligacao, natal):
    criativo = repositorio.criar(ligacao, natal.id, "Banner", "", 40000, date(2026, 11, 25), "Famílias", "Facebook")

    alterado = repositorio.atualizar(ligacao, criativo.id, "Banner", "", None, None, "", "Instagram")

    assert alterado.custo_centimos is None
    assert alterado.prazo is None
    assert alterado.publico_alvo == ""
    assert alterado.plataforma == "Instagram"


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


# --- menu do marketeer -------------------------------------------------------


def test_opcao_criativos_esta_no_menu_do_marketeer():
    opcoes = dict(perfis.OPCOES[modelos.MARKETEER])

    assert opcoes["Criativos"] is menu.do_marketeer
    assert [descricao for descricao, _ in perfis.OPCOES[modelos.MARKETEER]][:2] == ["Campanhas", "Criativos"]


def test_menu_sem_campanhas_avisa_e_volta(teclado, ligacao, marta, capsys):
    teclado("")

    menu.do_marketeer(ligacao, marta)

    assert 'Ainda não tem campanhas. Crie uma na opção "Campanhas".' in capsys.readouterr().out


def test_menu_mostra_as_campanhas_e_os_criativos_da_escolhida(teclado, ligacao, contas, natal, saldos, capsys):
    miguel = contas[modelos.MARKETEER]
    servico.criar(ligacao, miguel, natal.id, "Banner de Natal")
    servico.criar(ligacao, miguel, saldos.id, "Cartaz dos saldos")
    teclado(str(natal.id), "0", "")

    menu.do_marketeer(ligacao, miguel)

    saida = capsys.readouterr().out
    assert "Criativos — escolher a campanha" in saida
    assert "2 campanhas." in saida
    assert "Criativos da campanha Natal (Carla Cliente)" in saida
    assert "Banner de Natal  Por definir  -      -             -           Em preparação" in saida
    assert "1 criativo." in saida
    assert "Cartaz dos saldos" not in saida


def test_menu_recusa_campanha_de_outro_marketeer(teclado, ligacao, contas, natal, marta, capsys):
    servico_campanhas.criar(ligacao, marta, "Da Marta", "", contas[modelos.CLIENTE].id)
    teclado(str(natal.id), "", "")

    menu.do_marketeer(ligacao, marta)

    assert f"Não tem nenhuma campanha com o número {natal.id}." in capsys.readouterr().out


def test_campanha_sem_criativos(teclado, ligacao, contas, natal, capsys):
    teclado(str(natal.id), "0", "")

    menu.do_marketeer(ligacao, contas[modelos.MARKETEER])

    assert "Esta campanha ainda não tem criativos." in capsys.readouterr().out


def test_menu_cria_um_criativo(teclado, ligacao, contas, natal, capsys):
    teclado("1", "Banner de Natal", "Árvore e presentes", "", "", "", "", "", "0")

    menu.da_campanha(ligacao, contas[modelos.MARKETEER], natal)

    saida = capsys.readouterr().out
    (criativo,) = servico.listar_da_campanha(ligacao, natal)
    assert f"Criativo criado com o número {criativo.id}." in saida
    assert criativo.nome == "Banner de Natal"
    assert criativo.descricao == "Árvore e presentes"


def test_menu_edita_um_criativo_mantendo_o_que_fica_vazio(teclado, ligacao, contas, natal, capsys):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner", "Árvore")
    teclado("2", str(criativo.id), "Banner grande", "", "", "", "", "", "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    assert "Criativo guardado." in capsys.readouterr().out
    alterado = repositorio.obter_por_id(ligacao, criativo.id)
    assert alterado.nome == "Banner grande"
    assert alterado.descricao == "Árvore"


def test_menu_nao_aceita_criativo_de_outra_campanha(teclado, ligacao, contas, natal, saldos, capsys):
    miguel = contas[modelos.MARKETEER]
    cartaz = servico.criar(ligacao, miguel, saldos.id, "Cartaz")
    teclado("2", str(cartaz.id), "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    assert f"Esta campanha não tem nenhum criativo com o número {cartaz.id}." in capsys.readouterr().out


def test_menu_elimina_depois_de_confirmar(teclado, ligacao, contas, natal, capsys):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner")
    teclado("4", str(criativo.id), "s", "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    saida = capsys.readouterr().out
    assert "Um criativo eliminado não pode ser recuperado." in saida
    assert "O criativo Banner foi eliminado." in saida
    assert repositorio.obter_por_id(ligacao, criativo.id) is None


def test_menu_nao_elimina_sem_confirmacao(teclado, ligacao, contas, natal, capsys):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner")
    teclado("4", str(criativo.id), "n", "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    assert "Nada foi alterado." in capsys.readouterr().out
    assert repositorio.obter_por_id(ligacao, criativo.id) == criativo


# --- custo, prazo, público-alvo e plataforma ---------------------------------


def test_cria_um_criativo_com_todos_os_dados(ligacao, contas, natal):
    criativo = servico.criar(
        ligacao, contas[modelos.MARKETEER], natal.id, "Banner", "", "399,90", "2026-11-25", " Famílias ", "Facebook"
    )

    assert criativo.custo_centimos == 39990
    assert criativo.prazo == date(2026, 11, 25)
    assert criativo.publico_alvo == "Famílias"
    assert criativo.plataforma == "Facebook"


@pytest.mark.parametrize(
    ("custo", "esperado"),
    [("", None), ("0", 0), ("400", 40000), ("1 500,50 €", 150050)],
)
def test_custo_em_euros(custo, esperado):
    assert servico.custo_validado(custo) == esperado


def test_custo_tem_de_ser_um_valor_em_euros(ligacao, contas, natal):
    with pytest.raises(ErroValidacao, match="O valor não é válido"):
        servico.criar(ligacao, contas[modelos.MARKETEER], natal.id, "Banner", custo="quatrocentos")


def test_plataforma_tem_de_ser_uma_das_previstas(ligacao, contas, natal):
    with pytest.raises(ErroValidacao, match="A plataforma tem de ser uma destas: Facebook, Instagram"):
        servico.criar(ligacao, contas[modelos.MARKETEER], natal.id, "Banner", plataforma="Myspace")

    assert servico.plataforma_validada("") == ""
    assert servico.plataforma_validada("TikTok") == "TikTok"


def test_prazo_tem_de_ser_uma_data(ligacao, contas, natal):
    with pytest.raises(ErroValidacao, match="A data do prazo não é válida."):
        servico.criar(ligacao, contas[modelos.MARKETEER], natal.id, "Banner", prazo="25/11/2026")


def test_prazo_nao_pode_passar_o_fim_da_campanha(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]

    with pytest.raises(ErroValidacao, match=r"O prazo não pode ser depois do fim da campanha \(2026-12-24\)."):
        servico.criar(ligacao, miguel, natal.id, "Banner", prazo="2026-12-25")

    assert servico.criar(ligacao, miguel, natal.id, "Banner", prazo="2026-12-24").prazo == date(2026, 12, 24)


def test_campanha_sem_data_de_fim_aceita_qualquer_prazo(ligacao, contas, saldos):
    criativo = servico.criar(ligacao, contas[modelos.MARKETEER], saldos.id, "Cartaz", prazo="2027-06-30")

    assert criativo.prazo == date(2027, 6, 30)


def test_editar_altera_e_apaga_os_dados(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner", "", "400", "2026-11-25", "Famílias", "Facebook")

    alterado = servico.editar(ligacao, miguel, criativo.id, "Banner", "", "450", "", "", "Instagram")

    assert alterado.custo_centimos == 45000
    assert alterado.prazo is None
    assert alterado.publico_alvo == ""
    assert alterado.plataforma == "Instagram"


def test_editar_com_um_valor_errado_nao_altera_nada(ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner", "", "400")

    with pytest.raises(ErroValidacao):
        servico.editar(ligacao, miguel, criativo.id, "Banner novo", "", "400", "2027-01-01")

    assert repositorio.obter_por_id(ligacao, criativo.id) == criativo


def test_menu_cria_um_criativo_com_todos_os_dados(teclado, ligacao, contas, natal, capsys):
    teclado("1", "Banner", "", "400", "2026-11-25", "Famílias com filhos", "1", "", "0")

    menu.da_campanha(ligacao, contas[modelos.MARKETEER], natal)

    saida = capsys.readouterr().out
    assert "N.º  Nome    Custo     Prazo       Público-alvo         Plataforma  Estado" in saida
    assert "Banner  400,00 €  2026-11-25  Famílias com filhos  Facebook    Em preparação" in saida


def test_menu_mostra_o_erro_e_nao_cria(teclado, ligacao, contas, natal, capsys):
    teclado("1", "Banner", "", "400", "2026-12-31", "", "", "", "0")

    menu.da_campanha(ligacao, contas[modelos.MARKETEER], natal)

    saida = capsys.readouterr().out
    assert "O prazo não pode ser depois do fim da campanha (2026-12-24). O criativo não foi criado." in saida
    assert servico.listar_da_campanha(ligacao, natal) == []


def test_menu_repete_a_plataforma_ate_ser_um_numero_valido(teclado, ligacao, contas, natal, capsys):
    teclado("1", "Banner", "", "", "", "", "9", "x", "2", "", "0")

    menu.da_campanha(ligacao, contas[modelos.MARKETEER], natal)

    assert "Escreva um número entre 1 e 6." in capsys.readouterr().out
    assert servico.listar_da_campanha(ligacao, natal)[0].plataforma == "Instagram"


def test_menu_edita_e_apaga_valores(teclado, ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner", "Árvore", "400", "2026-11-25", "Famílias", "Facebook")
    teclado("2", str(criativo.id), "", "-", "450", "-", "", "-", "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    alterado = repositorio.obter_por_id(ligacao, criativo.id)
    assert alterado.nome == "Banner"
    assert alterado.descricao == ""
    assert alterado.custo_centimos == 45000
    assert alterado.prazo is None
    assert alterado.publico_alvo == "Famílias"
    assert alterado.plataforma == ""


def test_menu_editar_mantem_tudo_com_enter(teclado, ligacao, contas, natal, capsys):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner", "Árvore", "400", "2026-11-25", "Famílias", "Facebook")
    teclado("2", str(criativo.id), "", "", "", "", "", "", "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    assert "Criativo guardado." in capsys.readouterr().out
    assert repositorio.obter_por_id(ligacao, criativo.id) == criativo


def test_menu_editar_sem_valores_mantem_o_criativo_vazio(teclado, ligacao, contas, natal):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(ligacao, miguel, natal.id, "Banner")
    teclado("2", str(criativo.id), "", "", "", "", "", "", "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    assert repositorio.obter_por_id(ligacao, criativo.id) == criativo


def test_custo_por_palavras():
    assert menu.custo(Criativo(1, 1, "Banner")) == "Por definir"
    assert menu.custo(Criativo(1, 1, "Banner", custo_centimos=0)) == "0,00 €"


def test_menu_mostra_os_detalhes_de_um_criativo(teclado, ligacao, contas, natal, capsys):
    miguel = contas[modelos.MARKETEER]
    criativo = servico.criar(
        ligacao, miguel, natal.id, "Banner", "Árvore e presentes", "400", "2026-11-25", "Famílias", "Facebook"
    )
    teclado("3", str(criativo.id), "", "0")

    menu.da_campanha(ligacao, miguel, natal)

    saida = capsys.readouterr().out
    assert f"Criativo n.º {criativo.id}" in saida
    assert "  Campanha:    Natal" in saida
    assert "  Descrição:   Árvore e presentes" in saida
    assert "  Custo:       400,00 €" in saida
    assert "  Prazo:       2026-11-25" in saida
    assert "  Público:     Famílias" in saida
    assert "  Plataforma:  Facebook" in saida
    assert "  Estado:      Em preparação" in saida


def test_detalhes_mostram_tracos_quando_faltam_dados(ligacao, contas, natal, capsys):
    criativo = servico.criar(ligacao, contas[modelos.MARKETEER], natal.id, "Banner")

    menu.mostrar_detalhes(criativo)

    saida = capsys.readouterr().out
    assert "  Descrição:   -" in saida
    assert "  Custo:       Por definir" in saida
    assert "  Prazo:       -" in saida
    assert "  Plataforma:  -" in saida


def test_menu_tem_as_opcoes_pela_ordem_certa():
    assert [descricao for descricao, _ in menu.ACOES] == [
        "Criar criativo",
        "Editar criativo",
        "Ver criativo",
        "Eliminar criativo",
    ]


# --- dados de demonstração ---------------------------------------------------


def test_dados_demo_criam_criativos_nas_campanhas(ligacao):
    dados_demo.criar_contas(ligacao)
    dados_demo.criar_campanhas(ligacao)

    criados = dados_demo.criar_criativos(ligacao)

    assert criados == ["Banner de Natal", "Vídeo da montra", "Cartaz dos lanches", "Anúncio da bicicleta elétrica"]
    natal = next(c for c in repositorio_campanhas.listar_todas(ligacao) if c.nome == "Natal 2026")
    banner, video = repositorio.listar_por_campanha(ligacao, natal.id)
    assert banner.custo_centimos == 40000
    assert banner.plataforma == "Facebook"
    assert video.prazo == date(2026, 11, 28)


def test_dados_demo_nao_repetem_criativos(ligacao):
    dados_demo.criar_contas(ligacao)
    dados_demo.criar_campanhas(ligacao)
    dados_demo.criar_criativos(ligacao)

    assert dados_demo.criar_criativos(ligacao) == []


def test_criativos_de_demonstracao_respeitam_as_regras():
    campanhas_demo = {campanha["nome"]: campanha for campanha in dados_demo.CAMPANHAS}
    for criativo in dados_demo.CRIATIVOS:
        campanha = campanhas_demo[criativo["campanha"]]
        assert criativo["plataforma"] in ("", *modelos.PLATAFORMAS)
        if criativo["prazo"] and campanha["fim"]:
            assert criativo["prazo"] <= campanha["fim"]
