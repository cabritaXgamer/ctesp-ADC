"""Testes das validações dos dados escritos pelo utilizador."""

from datetime import date

import pytest

from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.servicos import validacao


def test_nome_fica_sem_espacos_a_volta():
    assert validacao.nome("  Ana Silva ") == "Ana Silva"


def test_nome_vazio_da_erro():
    with pytest.raises(ErroValidacao, match="nome não pode ficar vazio"):
        validacao.nome("   ")


@pytest.mark.parametrize(
    ("escrito", "esperado"),
    [
        ("ana@empresa.pt", "ana@empresa.pt"),
        ("  Ana.Silva@Empresa.PT ", "ana.silva@empresa.pt"),
        ("ana+campanhas@sub.empresa.com", "ana+campanhas@sub.empresa.com"),
    ],
)
def test_email_valido_fica_em_minusculas(escrito, esperado):
    assert validacao.email(escrito) == esperado


@pytest.mark.parametrize("escrito", ["", "ana", "ana@empresa", "@empresa.pt", "ana silva@empresa.pt", "ana@@empresa.pt"])
def test_email_invalido_da_erro(escrito):
    with pytest.raises(ErroValidacao, match="email não é válido"):
        validacao.email(escrito)


@pytest.mark.parametrize(
    ("escrito", "esperado"),
    [("", ""), ("912 345 678", "912345678"), ("+351912345678", "+351912345678")],
)
def test_telefone_valido_fica_sem_espacos(escrito, esperado):
    assert validacao.telefone(escrito) == esperado


@pytest.mark.parametrize("escrito", ["12345", "91234567a", "1234567890123456", "+"])
def test_telefone_invalido_da_erro(escrito):
    with pytest.raises(ErroValidacao, match="entre 9 e 15 algarismos"):
        validacao.telefone(escrito)


def test_nif_vazio_ou_com_nove_algarismos():
    assert validacao.nif("") == ""
    assert validacao.nif("500 000 000") == "500000000"


@pytest.mark.parametrize("escrito", ["12345678", "1234567890", "50000000A"])
def test_nif_invalido_da_erro(escrito):
    with pytest.raises(ErroValidacao, match="9 algarismos"):
        validacao.nif(escrito)


def test_data_valida_e_convertida():
    assert validacao.data(" 2026-12-24 ") == date(2026, 12, 24)


def test_data_vazia_fica_sem_valor():
    assert validacao.data("   ") is None


@pytest.mark.parametrize("escrito", ["24-12-2026", "2026/12/24", "2026-02-30", "amanhã"])
def test_data_invalida_da_erro_com_o_nome_do_campo(escrito):
    with pytest.raises(ErroValidacao, match="A data de fim não é válida"):
        validacao.data(escrito, "data de fim")


def test_periodo_aceita_datas_iguais_e_datas_em_falta():
    validacao.periodo(date(2026, 12, 1), date(2026, 12, 1))
    validacao.periodo(None, date(2026, 12, 1))
    validacao.periodo(date(2026, 12, 1), None)


def test_periodo_que_acaba_antes_de_comecar_da_erro():
    with pytest.raises(ErroValidacao, match="não pode ser anterior"):
        validacao.periodo(date(2026, 12, 2), date(2026, 12, 1))
