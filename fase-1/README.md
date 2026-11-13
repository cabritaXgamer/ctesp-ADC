# Fase 1 — Autenticação e sessões

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

## Páginas de cada um

Cada pessoa segue a sua página, do primeiro ao último passo.

| Pessoa | Página |
|---|---|
| Fabio | [fabio.md](fabio.md) |
| Tomas | [tomas.md](tomas.md) |
| Ricardo | [ricardo.md](ricardo.md) |

Os termos usados estão explicados em [O que é o quê](../conceitos.md).

## Ordem de trabalho

As unidades assentam umas nas outras, por isso o trabalho é feito à vez, por esta ordem. Cada linha só começa quando a anterior acabou.

| Vez | Quem | O que faz | Onde está explicado |
|---|---|---|---|
| 1 | Tomas | Fazer a unidade 1.1 — Login e logout dos três perfis | [tomas.md](tomas.md), passos 1 a 10 |
| 2 | Ricardo | Rever e juntar a unidade 1.1 (de Tomas) | [ricardo.md](ricardo.md), passos 1 a 7 |
| 3 | Ricardo | Fazer a unidade 1.2 — Registo de sessões e saída por inatividade | [ricardo.md](ricardo.md), passos 8 a 17 |
| 4 | Fabio | Rever e juntar a unidade 1.2 (de Ricardo) | [fabio.md](fabio.md), passos 1 a 7 |
| 5 | Fabio | Fazer a unidade 1.3 — Horários de entrada e saída dos marketeers | [fabio.md](fabio.md), passos 8 a 17 |
| 6 | Tomas | Rever e juntar a unidade 1.3 (de Fabio) | [tomas.md](tomas.md), passos 11 a 17 |
| 7 | Tomas | Fazer a unidade 1.4 — Alterar a password e editar os meus dados | [tomas.md](tomas.md), passos 18 a 27 |
| 8 | Ricardo | Rever e juntar a unidade 1.4 (de Tomas) | [ricardo.md](ricardo.md), passos 18 a 24 |
| 9 | Ricardo | Fazer a unidade 1.5 — Recuperar a password | [ricardo.md](ricardo.md), passos 25 a 34 |
| 10 | Fabio | Rever e juntar a unidade 1.5 (de Ricardo) | [fabio.md](fabio.md), passos 18 a 24 |
| 11 | Fabio | Preparar a release v0.1.0 | [fabio.md](fabio.md), passos 25 a 33 |
| 12 | Tomas | Rever a release v0.1.0 e juntá-la ao main | [tomas.md](tomas.md), passos 28 a 34 |
| 13 | Fabio | Publicar a release v0.1.0 e pedir o regresso ao develop | [fabio.md](fabio.md), passos 34 a 37 |
| 14 | Tomas | Juntar a release v0.1.0 ao develop | [tomas.md](tomas.md), passos 35 a 38 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Cria a página "Guia de utilização" da wiki; Atualiza a página inicial da wiki | [fabio.md](fabio.md), passos 38 a 39 |
| Tomas | Cria a página "Arquitetura" da wiki | [tomas.md](tomas.md), passo 39 |
| Ricardo | Cria a página "Registo das fases" da wiki | [ricardo.md](ricardo.md), passo 35 |

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-1/ficheiros/
  1.1/    Login e logout dos três perfis
    commit-1/    feat(bd): adicionar a tabela de utilizadores
    commit-2/    feat(modelos): adicionar utilizador, perfis, erros e relógio
    commit-3/    feat(seguranca): guardar as passwords com hash e salt
    commit-4/    feat(utilizadores): adicionar o repositório de utilizadores
    commit-5/    feat(auth): autenticar por email e password
    commit-6/    feat(cli): entrar na aplicação e mostrar o menu do perfil
    commit-7/    feat(dados): criar contas de demonstração
    commit-8/    test(auth): testar passwords, utilizadores, autenticação e menus
    commit-9/    docs(auth): documentar a entrada na aplicação e a arquitetura em camadas
  1.2/    Registo de sessões e saída por inatividade
    commit-1/    feat(bd): adicionar a tabela de sessões
    commit-2/    feat(modelos): adicionar a sessão e o limite de inatividade por omissão
    commit-3/    feat(config): ler e guardar definições na base de dados
    commit-4/    feat(sessoes): adicionar o repositório de sessões
    commit-5/    feat(sessoes): registar entradas e saídas e detetar inatividade
    commit-6/    feat(cli): abrir sessão ao entrar e terminá-la por logout ou inatividade
    commit-7/    test(sessoes): testar o registo de sessões e a inatividade
    commit-8/    docs(sessoes): documentar as sessões e a inatividade
  1.3/    Horários de entrada e saída dos marketeers
    commit-1/    feat(cli): ler datas e mostrar tabelas de texto
    commit-2/    feat(sessoes): listar as sessões dos utilizadores de um perfil
    commit-3/    feat(sessoes): consultar os horários dos marketeers por período
    commit-4/    feat(admin): mostrar os horários de entrada e saída dos marketeers
    commit-5/    test(horarios): testar a consulta de horários e a tabela
    commit-6/    docs(horarios): documentar a consulta de horários
  1.4/    Alterar a password e editar os meus dados
    commit-1/    feat(utilizadores): atualizar a password e os dados de um utilizador
    commit-2/    feat(conta): validar e aplicar alterações à própria conta
    commit-3/    feat(cli): editar os meus dados e alterar a password em todos os perfis
    commit-4/    test(conta): testar a alteração da password e dos dados
    commit-5/    docs(conta): documentar as opções da conta
  1.5/    Recuperar a password
    commit-1/    feat(bd): adicionar a tabela de códigos de recuperação e a caixa de saída
    commit-2/    feat(correio): simular o envio de emails com ficheiros de texto
    commit-3/    feat(recuperacao): guardar os códigos de recuperação
    commit-4/    feat(recuperacao): pedir um código e repor a password
    commit-5/    feat(cli): recuperar a password a partir do menu inicial
    commit-6/    test(recuperacao): testar a recuperação da password e os emails
    commit-7/    docs(recuperacao): documentar a recuperação da password e os emails simulados
  1.6/    Release v0.1.0
    commit-1/    chore(release): passar a versão para 0.1.0
    commit-2/    docs(release): criar o registo de alterações
    commit-3/    docs(release): atualizar o README para a versão 0.1.0
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 1.6
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 1.6.`

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `104 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] As 8 issues das user stories da fase estão fechadas (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- [ ] A release `v0.1.0` está publicada (ver https://github.com/Blive77/ADC-TrabGrupo/releases)
- [ ] A milestone `Fase 1 — Autenticação e sessões` está fechada
- [ ] A wiki tem as páginas Guia de utilização, Arquitetura e Registo das fases
- [ ] Todos os pull requests da fase juntos, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] `verificar.py 1.6` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, Fabio diz ao Claude **"avança para a Fase 2"** e conta os problemas que o grupo teve.

## Trello

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um.

No fim da fase, movam para **Sprint Backlog** os sete cards da Fase 2: ver a lista de clientes, adicionar, editar e remover clientes, e adicionar, editar e remover marketeers.

## Se algo correr mal

| O que aconteceu | O que fazer |
|---|---|
| O `copiar.py` responde `ERRO` | Lê a mensagem: diz o que está mal e o que fazer. Os casos mais comuns são estar no ramo errado, ter um commit anterior por gravar, ou a unidade anterior ainda não estar junta ao `develop` |
| `can't open file ... copiar.py` | As duas pastas não estão lado a lado, ou o terminal não está dentro de `ADC-TrabGrupo`. Vê o passo A4 da Preparação |
| O `copiar.py` diz que não existe a unidade | A pasta do repositório de trabalho está desatualizada. Corre `git -C ../ctesp-ADC pull` e repete |
| Enganei-me num commit e ainda não fiz `push` | Corre `git reset --hard develop` (o ramo volta a ficar igual ao `develop` e os commits que fizeste nele desaparecem) e recomeça no passo "Copia e grava os commits" |
| O commit ficou com o nome ou o email errado e ainda não fiz `push` | Corrige o nome e o email (Preparação, passo A2) e corre `git commit --amend --reset-author --no-edit` |
| `fatal: not a git repository` | O terminal não está na pasta do repositório. Usa `cd` para entrar nela |
| O `git push` é recusado com `403` ou `Permission denied` | A tua conta não é colaboradora do repositório oficial, ou não aceitaste o convite (Preparação, passo A3) |
| O `verificar.py` responde `ERRO` | Não avancem. Copiem a mensagem e passem-na a Fabio, para a enviar ao Claude |
| Uma verificação automática fica com uma cruz vermelha | Clica em *Details* ao lado da verificação, copia o erro e passa-o a Fabio, para o enviar ao Claude |
| O `python` não é reconhecido | Experimenta `py` em vez de `python` |
