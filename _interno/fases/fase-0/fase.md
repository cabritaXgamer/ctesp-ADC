---
numero: 0
titulo: Arranque
fechada: sim
testes: 20
---

@@ entrega
A Fase 0 monta a base do projeto, ainda sem user stories. No fim, a aplicação arranca, cria a base de dados e mostra o menu inicial. Ficam também os testes automáticos, a documentação Sphinx e as regras de trabalho do repositório.

```
python -m gestor_campanhas

============================================================
Gestor de Campanhas v0.0.0
============================================================
  1. Entrar
  0. Sair
Opção:
```

Nesta fase ninguém escreve código à mão. Cada pessoa copia para o repositório oficial os commits que estão preparados no repositório de trabalho, grava-os em seu nome, e passa pelo ciclo completo: issue, ramo, commits, pull request, revisão e merge.

São quatro unidades de trabalho e não há release. A primeira release é a `v0.1.0`, no fim da Fase 1.

@@ verificacao
- 57 issues de user stories criadas, com labels e milestone
- Wiki com as páginas Home e Fluxo Git

@@ trello
A Fase 0 não tem cards de user stories. No fim da fase, movam para **Sprint Backlog** os oito cards da Fase 1: os três de login (Administrador, Marketeer e Cliente), o registo de logins e logouts, os horários de entrada e saída, recuperar a password, alterar a password e editar a minha informação.
