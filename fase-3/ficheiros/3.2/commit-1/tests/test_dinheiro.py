"""Testes da conversão de valores em euros."""

import pytest

from gestor_campanhas import dinheiro
from gestor_campanhas.erros import ErroValidacao


@pytest.mark.parametrize(
    ("escrito", "centimos"),
    [
        ("1500", 150000),
        ("1500,50", 150050),
        ("1500.5", 150050),
        ("0,05", 5),
        (" 1 500,50 € ", 150050),
        ("0", 0),
    ],
)
def test_para_centimos_aceita_as_formas_habituais(escrito, centimos):
    assert dinheiro.para_centimos(escrito) == centimos


@pytest.mark.parametrize("escrito", ["", "mil", "-5", "1,2,3", "10,999", "1.500,50", ",50"])
def test_para_centimos_recusa_o_que_nao_e_um_valor(escrito):
    with pytest.raises(ErroValidacao, match="O valor não é válido"):
        dinheiro.para_centimos(escrito)


@pytest.mark.parametrize(
    ("centimos", "texto"),
    [(0, "0,00 €"), (5, "0,05 €"), (150050, "1 500,50 €"), (99999, "999,99 €"), (123456789, "1 234 567,89 €")],
)
def test_formatar_separa_os_milhares_e_mostra_dois_decimais(centimos, texto):
    assert dinheiro.formatar(centimos) == texto


def test_formatar_e_para_centimos_sao_inversos():
    assert dinheiro.para_centimos(dinheiro.formatar(150050)) == 150050
