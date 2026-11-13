---
numero: 1
titulo: Autenticação e sessões
testes: 104
---

@@ entrega
A Fase 1 põe a aplicação a funcionar com contas. No fim, cada pessoa entra com o seu email e a sua password, vê o menu do seu perfil, pode alterar os seus dados e a password, e recuperar a password se a esquecer. Todas as entradas e saídas ficam registadas, e o Administrador consulta as dos marketeers.

São oito user stories (A01, A02, A03, M01, C01, C02, C03 e C04), em cinco unidades de trabalho, mais a primeira release: a `v0.1.0`.

```
============================================================
Gestor de Campanhas v0.1.0
============================================================
  1. Entrar
  2. Recuperar a password
  0. Sair
Opção:
```

O que muda em relação à Fase 0:

- **As issues já existem.** Em vez de criar uma issue, quem faz a unidade fica com as issues das suas user stories e escreve nelas os critérios de aceitação.
- **Há uma release no fim.** É uma unidade diferente das outras: o pull request vai para o `main`, publica-se a versão com uma tag, e depois leva-se a release de volta ao `develop`.

Para experimentar a aplicação a partir da unidade 1.1, criam-se as contas de demonstração com `python -m gestor_campanhas.dados_demo`. As credenciais aparecem no ecrã.

@@ verificacao
- As 8 issues das user stories da fase estão fechadas (ver {{REPO_B}}/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- A release `v0.1.0` está publicada (ver {{REPO_B}}/releases)
- A milestone `Fase 1 — Autenticação e sessões` está fechada
- A wiki tem as páginas Guia de utilização, Arquitetura e Registo das fases

@@ trello
Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um.

No fim da fase, movam para **Sprint Backlog** os sete cards da Fase 2: ver a lista de clientes, adicionar, editar e remover clientes, e adicionar, editar e remover marketeers.
