"""Ponto de entrada da aplicação.

Permite arrancar a aplicação a partir da pasta do projeto com::

    python -m gestor_campanhas
"""

from gestor_campanhas import __version__


def main() -> int:
    """Arranca a aplicação.

    :return: Código de saída do processo (``0`` quando termina sem erros).
    """
    print(f"Gestor de Campanhas v{__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
