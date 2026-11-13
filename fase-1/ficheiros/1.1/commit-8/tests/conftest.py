"""Peças partilhadas por todos os testes (*fixtures* do pytest)."""

import pytest

from gestor_campanhas import bd, modelos, seguranca
from gestor_campanhas.repositorios import utilizadores

#: Password de todas as contas criadas pela fixture ``contas``.
PASSWORD_TESTE = "segredo-123"


@pytest.fixture(autouse=True)
def hash_rapido(monkeypatch):
    """Reduz o trabalho do hash das passwords, para os testes serem rápidos."""
    monkeypatch.setattr(seguranca, "ITERACOES", 1000)


@pytest.fixture
def ligacao():
    """Base de dados em memória, já com as tabelas criadas.

    Cada teste recebe uma base de dados nova e vazia, por isso os testes
    não interferem uns com os outros nem tocam nos dados reais.
    """
    ligacao_teste = bd.iniciar_bd(bd.EM_MEMORIA)
    yield ligacao_teste
    ligacao_teste.close()


@pytest.fixture
def teclado(monkeypatch):
    """Simula o que o utilizador escreve no teclado.

    Devolve uma função que recebe as respostas, pela ordem em que devem ser
    dadas. Exemplo: ``teclado("x", "1")`` responde ``x`` à primeira pergunta
    e ``1`` à segunda. Quando as respostas acabam, a pergunta seguinte falha
    com :class:`EOFError`, tal como o ``input()`` verdadeiro quando a entrada
    termina.
    """

    def definir_respostas(*respostas):
        fila = iter(respostas)

        def responder(_pergunta=""):
            try:
                return next(fila)
            except StopIteration:
                raise EOFError from None

        monkeypatch.setattr("builtins.input", responder)
        # As passwords são pedidas com getpass quando há uma consola a sério.
        monkeypatch.setattr("getpass.getpass", responder)

    return definir_respostas


@pytest.fixture
def contas(ligacao):
    """Cria uma conta de cada perfil, todas com a password ``PASSWORD_TESTE``.

    Devolve um dicionário com os utilizadores, pelo nome do perfil.
    """
    dados = {
        modelos.ADMINISTRADOR: ("Ana Admin", "ana@agencia.pt"),
        modelos.MARKETEER: ("Miguel Marketeer", "miguel@agencia.pt"),
        modelos.CLIENTE: ("Carla Cliente", "carla@empresa.pt"),
    }
    return {
        perfil: utilizadores.criar(ligacao, nome, email, seguranca.gerar_hash(PASSWORD_TESTE), perfil)
        for perfil, (nome, email) in dados.items()
    }
