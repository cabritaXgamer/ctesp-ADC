"""Data e hora atuais.

Toda a aplicação pergunta as horas a este módulo, e não diretamente ao
sistema. Assim, os testes podem substituir :func:`agora` e simular a passagem
do tempo sem terem de esperar.
"""

from datetime import datetime

#: Formato em que as datas e horas são guardadas na base de dados.
FORMATO = "%Y-%m-%d %H:%M:%S"


def agora() -> datetime:
    """Devolve a data e hora atuais, sem frações de segundo.

    :return: Data e hora do sistema.
    """
    return datetime.now().replace(microsecond=0)


def para_texto(momento: datetime) -> str:
    """Converte uma data e hora no texto que é guardado na base de dados.

    :param momento: Data e hora a converter.
    :return: Texto no formato ``AAAA-MM-DD HH:MM:SS``.
    """
    return momento.strftime(FORMATO)


def de_texto(texto: str) -> datetime:
    """Converte um texto lido da base de dados numa data e hora.

    :param texto: Texto no formato ``AAAA-MM-DD HH:MM:SS``.
    :return: Data e hora correspondentes.
    """
    return datetime.strptime(texto, FORMATO)
