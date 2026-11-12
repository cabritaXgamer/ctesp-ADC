# Fase 0 — Arranque

> **Atenção:** ainda não sei o endereço do vosso repositório oficial. Onde aparecer `https://github.com/DONO/REPOSITORIO-OFICIAL`, usa o endereço verdadeiro.

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

## Páginas de cada um

Cada pessoa segue a sua página, do primeiro ao último passo.

| Pessoa | Página |
|---|---|
| Fabio | [fabio.md](fabio.md) |
| Tomas | [tomas.md](tomas.md) |
| Ricardo | [ricardo.md](ricardo.md) |

Antes da primeira fase, todos fazem a [Preparação](../preparacao.md). Os termos usados estão explicados em [O que é o quê](../conceitos.md).

## Ordem de trabalho

As unidades assentam umas nas outras, por isso o trabalho é feito à vez, por esta ordem. Cada linha só começa quando a anterior acabou.

| Vez | Quem | O que faz | Onde está explicado |
|---|---|---|---|
| 1 | Fabio | Fazer a unidade 0.1 — Estrutura do pacote Python | [fabio.md](fabio.md), passos 1 a 10 |
| 2 | Tomas | Rever e juntar a unidade 0.1 (de Fabio) | [tomas.md](tomas.md), passos 1 a 7 |
| 3 | Tomas | Fazer a unidade 0.2 — Base de dados e menu inicial | [tomas.md](tomas.md), passos 8 a 17 |
| 4 | Ricardo | Rever e juntar a unidade 0.2 (de Tomas) | [ricardo.md](ricardo.md), passos 1 a 7 |
| 5 | Ricardo | Fazer a unidade 0.3 — Testes automáticos e integração contínua | [ricardo.md](ricardo.md), passos 8 a 17 |
| 6 | Fabio | Rever e juntar a unidade 0.3 (de Ricardo) | [fabio.md](fabio.md), passos 11 a 17 |
| 7 | Fabio | Fazer a unidade 0.4 — Documentação base | [fabio.md](fabio.md), passos 18 a 27 |
| 8 | Tomas | Rever e juntar a unidade 0.4 (de Fabio) | [tomas.md](tomas.md), passos 18 a 24 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Cria as 19 issues do perfil Administrador | [fabio.md](fabio.md), passo 28 |
| Tomas | Cria as 18 issues do perfil Marketeer; Cria a página "Fluxo Git" da wiki | [tomas.md](tomas.md), passos 25 a 26 |
| Ricardo | Cria as 20 issues do perfil Cliente; Cria a página inicial da wiki | [ricardo.md](ricardo.md), passos 18 a 19 |

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao de trabalho.

```bash
git switch develop
git pull
git fetch trabalho
git diff --stat trabalho/develop develop
```

O último comando não deve mostrar nada. Segunda confirmação:

```bash
git rev-parse "develop^{tree}"
```

O resultado tem de ser exatamente:

```text
e90209e7d8085e3d7d2be163df305ec58f9cdf82
```

Este código identifica o conteúdo de todos os ficheiros. Se for igual, os dois repositórios têm exatamente os mesmos ficheiros.

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `20 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] 4 issues de tarefa fechadas (ver https://github.com/DONO/REPOSITORIO-OFICIAL/issues?q=is%3Aissue+is%3Aclosed)
- [ ] 4 pull requests juntos ao `develop`, cada um aprovado por outra pessoa do grupo (ver https://github.com/DONO/REPOSITORIO-OFICIAL/pulls?q=is%3Apr+is%3Amerged)
- [ ] 57 issues de user stories criadas, com labels e milestone
- [ ] Wiki com as páginas Home e Fluxo Git
- [ ] `git diff --stat trabalho/develop develop` não mostra nada
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, digam-me **"avança para a Fase 1"** e contem-me os problemas que tiveram.

## Trello

A Fase 0 não tem cards de user stories. No fim da fase, movam para **Sprint Backlog** os oito cards da Fase 1: os três de login (Administrador, Marketeer e Cliente), o registo de logins e logouts, os horários de entrada e saída, recuperar a password, alterar a password e editar a minha informação.

## Se algo correr mal

| O que aconteceu | O que fazer |
|---|---|
| O `git cherry-pick -n` mostra `CONFLICT` | O teu ramo não está igual ao esperado, quase sempre porque a unidade anterior ainda não foi junta ou porque saltaste um commit. Corre `git reset --hard` para desfazer a tentativa e diz-me o que apareceu |
| Enganei-me num commit e ainda não fiz `push` | Corre `git reset --hard develop` (o ramo volta a ficar igual ao `develop`) e recomeça no passo "Copia os commits" |
| O commit ficou com o nome ou o email errado e ainda não fiz `push` | Corrige o nome e o email (Preparação, passo A2) e corre `git commit --amend --reset-author --no-edit` |
| `fatal: not a git repository` | O terminal não está na pasta do repositório. Usa `cd` para entrar nela |
| `error: pathspec ... did not match` ou `bad revision` no `cherry-pick` | Falta ir buscar os commits: corre `git fetch trabalho` e repete |
| O `git push` é recusado com `403` ou `Permission denied` | A tua conta ainda não é colaboradora do repositório oficial, ou não aceitaste o convite |
| O `git push` é recusado por causa do email (`GH007`) | O GitHub está a proteger o teu email. Em GitHub → Settings → Emails copia o endereço que termina em `users.noreply.github.com`, usa-o no `git config --global user.email` e corre `git commit --amend --reset-author --no-edit` |
| O `git diff --stat` de confirmação mostra ficheiros | Não avancem. Digam-me que ficheiros aparecem |
| Uma verificação automática fica com uma cruz vermelha | Clica em *Details* ao lado da verificação, copia o erro e envia-mo |
| O `python` não é reconhecido | Experimenta `py` em vez de `python`. Se também não der, falta instalar o Python (Preparação, passo A1) |
