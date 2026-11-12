"""Ponto de entrada da aplicação.

Permite arrancar a aplicação a partir da pasta do projeto com::

    python -m gestor_campanhas
"""

from gestor_campanhas import bd
from gestor_campanhas.cli import principal


def main() -> int:
    """Arranca a aplicação.

    Abre a base de dados, mostra o menu inicial e, no fim, fecha a ligação.
    Se o utilizador interromper o programa com Ctrl+C, a aplicação termina
    sem mostrar um erro.

    :return: Código de saída do processo (``0`` quando termina sem erros).
    """
    ligacao = bd.iniciar_bd()
    try:
        principal.executar(ligacao)
    except (KeyboardInterrupt, EOFError):
        print("\nA sair...")
    finally:
        ligacao.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
