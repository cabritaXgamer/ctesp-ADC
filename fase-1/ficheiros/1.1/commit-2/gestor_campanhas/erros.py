"""Erros próprios da aplicação.

As regras de negócio assinalam um problema lançando um destes erros. Os menus
apanham-nos e mostram a mensagem ao utilizador, em vez de o programa parar.
"""


class ErroAplicacao(Exception):
    """Erro esperado, com uma mensagem que pode ser mostrada ao utilizador."""


class ErroAutenticacao(ErroAplicacao):
    """O email ou a password não estão corretos, ou a conta não pode entrar."""


class ErroValidacao(ErroAplicacao):
    """Os dados introduzidos não respeitam as regras."""
