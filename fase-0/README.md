# Fase 0 — Arranque

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

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-0/ficheiros/
  0.1/    Estrutura do pacote Python
    commit-1/    chore: adicionar .gitignore e .gitattributes
    commit-2/    feat(nucleo): criar pacote gestor_campanhas com ponto de entrada
    commit-3/    feat(config): adicionar configuração dos caminhos de dados
    commit-4/    chore: adicionar pyproject.toml
  0.2/    Base de dados e menu inicial
    commit-1/    feat(bd): adicionar ligação SQLite e criação de tabelas
    commit-2/    feat(cli): adicionar funções comuns dos menus
    commit-3/    feat(cli): adicionar menu inicial
    commit-4/    feat(nucleo): ligar o ponto de entrada à base de dados e ao menu inicial
    commit-5/    fix(cli): ler e escrever acentos em UTF-8 em qualquer terminal
  0.3/    Testes automáticos e integração contínua
    commit-1/    test: configurar o pytest e as fixtures comuns
    commit-2/    test(bd): testar a ligação, as tabelas e os caminhos de dados
    commit-3/    test(cli): testar os menus e o ponto de entrada
    commit-4/    ci: correr os testes no GitHub Actions
  0.4/    Documentação base
    commit-1/    docs: configurar o Sphinx e documentar a instalação
    commit-2/    docs: descrever a arquitetura e os testes
    commit-3/    docs: gerar a referência do código a partir dos docstrings
    commit-4/    ci: gerar a documentação no GitHub Actions
    commit-5/    docs: escrever o README
    commit-6/    docs: adicionar o guia de contribuição
    commit-7/    chore: adicionar modelos de issue e de pull request
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 0.4
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 0.4.`

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

- [ ] 4 issues de tarefa fechadas (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aclosed)
- [ ] 4 pull requests juntos ao `develop`, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] 57 issues de user stories criadas, com labels e milestone
- [ ] Wiki com as páginas Home e Fluxo Git
- [ ] `verificar.py 0.4` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, Fabio diz ao Claude **"avança para a Fase 1"** e conta os problemas que o grupo teve.

## Trello

A Fase 0 não tem cards de user stories. No fim da fase, movam para **Sprint Backlog** os oito cards da Fase 1: os três de login (Administrador, Marketeer e Cliente), o registo de logins e logouts, os horários de entrada e saída, recuperar a password, alterar a password e editar a minha informação.

## Se algo correr mal

| O que aconteceu | O que fazer |
|---|---|
| O `copiar.py` responde `ERRO` | Lê a mensagem: diz o que está mal e o que fazer. Os casos mais comuns são estar no ramo errado, ter um commit anterior por gravar, ou a unidade anterior ainda não estar junta ao `develop` |
| `can't open file ... copiar.py` | As duas pastas não estão lado a lado, ou o terminal não está dentro de `ADC-TrabGrupo`. Vê o passo A4 da Preparação |
| Enganei-me num commit e ainda não fiz `push` | Corre `git reset --hard develop` (o ramo volta a ficar igual ao `develop` e os commits que fizeste nele desaparecem) e recomeça no passo "Copia e grava os commits" |
| O commit ficou com o nome ou o email errado e ainda não fiz `push` | Corrige o nome e o email (Preparação, passo A2) e corre `git commit --amend --reset-author --no-edit` |
| `fatal: not a git repository` | O terminal não está na pasta do repositório. Usa `cd` para entrar nela |
| O `git push` é recusado com `403` ou `Permission denied` | A tua conta ainda não é colaboradora do repositório oficial, ou não aceitaste o convite (Preparação, passo A3) |
| O `git push` é recusado por causa do email (`GH007`) | O GitHub está a proteger o teu email. Em GitHub → Settings → Emails copia o endereço que termina em `users.noreply.github.com`, usa-o no `git config --global user.email` e corre `git commit --amend --reset-author --no-edit` |
| O `verificar.py` responde `ERRO` | Não avancem. Copiem a mensagem e passem-na a Fabio, para a enviar ao Claude |
| Uma verificação automática fica com uma cruz vermelha | Clica em *Details* ao lado da verificação, copia o erro e passa-o a Fabio, para o enviar ao Claude |
| O `python` não é reconhecido | Experimenta `py` em vez de `python`. Se também não der, falta instalar o Python (Preparação, passo A1) |
