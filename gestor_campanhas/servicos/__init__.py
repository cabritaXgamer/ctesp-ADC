"""Regras de negócio da aplicação.

Cada módulo deste pacote trata de um assunto (autenticação, sessões, ...).
As funções decidem o que é permitido e o que acontece, usando os
repositórios para ler e guardar dados. Não escrevem no ecrã nem leem do
teclado: quando algo não é permitido, lançam um erro de
:mod:`gestor_campanhas.erros`, que os menus mostram ao utilizador.
"""
