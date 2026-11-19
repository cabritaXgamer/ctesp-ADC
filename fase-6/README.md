# Fase 6 — Comentários, notificações, painel e relatório

A Fase 6 é a última com user stories. No fim, o Cliente comenta os criativos e o Marketeer responde; os dois recebem notificações do que lhes diz respeito, na aplicação e por email; o Administrador tem um painel para comparar o trabalho dos marketeers e ver quem está parado; e o Cliente exporta um relatório das suas campanhas para o Excel.

São nove user stories (C17, C18, C19, C20, M17, M18, A17, A18 e A19), em quatro unidades de trabalho, mais a release `v0.6.0`. Com esta fase ficam feitas as 57 user stories do projeto.

```
============================================================
As minhas notificações
============================================================
N.º  Data              Estado   Sobre           Mensagem
---  ----------------  -------  --------------  ------------------------------------------------------------
2    2026-11-19 11:03  Por ler  Criativo n.º 2  Miguel Marketeer respondeu ao seu comentário sobre o cria...
1    2026-11-19 10:58  Lida     Criativo n.º 5  Foi criado o criativo Teste das notificações, da campanha...

2 notificações, 1 por ler.
```

```
============================================================
Painel de marketeers
============================================================
N.º  Marketeer         Campanhas ativas  Ativos  Em atraso  Concluídos  Última atividade  Situação
---  ----------------  ----------------  ------  ---------  ----------  ----------------  ----------------
3    Marta Marques     1                 1       0          0           2026-11-17        Parado há 2 dias
2    Miguel Marketeer  1                 2       1          1           2026-11-19
```

| Unidade | O que traz | Quem usa |
|---|---|---|
| 6.1 | Comentários dos criativos e respostas | Cliente e Marketeer |
| 6.2 | Notificações na aplicação e por email | Marketeer e Cliente |
| 6.3 | Painel de marketeers: trabalho, carga e inatividade | Administrador |
| 6.4 | Relatório das campanhas em CSV | Cliente |

O que muda em relação à Fase 5:

- **A forma de trabalhar é a mesma.** Issues das stories, ramo, commits copiados com o `copiar.py`, pull request, revisão e merge.
- **Confirmem o `Closes #` antes de juntar.** Na Fase 5, os pull requests das unidades 5.1 e 5.4 foram juntos sem a linha `Closes #` com o número verdadeiro, e as issues C15 e A16 tiveram de ser fechadas à mão. O passo de quem revê já manda confirmar isto: não o saltem.
- **Os menus mudam de número.** O Marketeer e o Cliente ganham `4. Notificações` (unidade 6.2), e as opções da conta descem para `5` e `6`. O Administrador ganha `8. Painel de marketeers` (6.3), e as opções da conta descem para `9` e `10`. Os menus de criativos ganham uma opção no fim (6.1) e as campanhas do Cliente também (6.4). Os passos "Testa" dizem sempre o número certo para a unidade em causa.
- **Testar volta a mexer nos teus dados.** Os passos escrevem comentários, criam notificações, fazem e decidem pedidos de budget e gravam um ficheiro CSV. Os comentários e as notificações não se apagam, e isso é normal: nas unidades seguintes vais vê-los nas listas.
- **Os números dos itens variam.** Os números dos comentários, das notificações e dos criativos dependem do que cada um já fez nos seus dados. Os passos dizem sempre de que item se trata ("o número do comentário da Carla"): procura o número na primeira coluna ou na linha `N.º`.
- **Três tabelas novas.** `comentarios` (6.1), `notificacoes` (6.2) e `atividades` (6.3). São criadas sozinhas no primeiro arranque depois do merge, sem apagar nada.
- **Depois de instalares o Python de novo, instala outra vez as ferramentas.** Se o `python -m pytest` responder `No module named pytest`, corre `python -m pip install -r requirements-dev.txt` dentro da pasta `ADC-TrabGrupo`.

Decisões do grupo, que estão escritas nos critérios de aceitação:

- **Só o cliente comenta; o marketeer responde** (C18, M17). Cada comentário pode ter respostas; para continuar a conversa, o cliente escreve um comentário novo. Os comentários não se editam nem se apagam.
- **Notificações na aplicação e por email** (C17, C19, M18). As stories dizem "e/ou"; fazemos as duas. A "ligação direta ao item" é abrir a notificação: aparece logo a campanha, o pedido ou o criativo.
- **O cliente é notificado de tudo o que o marketeer faz aos seus criativos** (C19): criar, editar, eliminar, mudar o estado, anexar um ficheiro e responder a um comentário. O Administrador não recebe notificações.
- **O período da carga de trabalho é o prazo dos criativos** (A18). "Concluídos" são os aprovados e os publicados; "em atraso" são os que ainda têm trabalho por fazer e cujo prazo já passou.
- **"Sem atividade" quer dizer sem criativos ativos, ou sem mexer nos criativos há 7 dias ou mais** (A19). O número de dias muda-se no painel. A atividade só começa a ser registada nesta fase; os criativos que já existiam contam pelo dia em que foram criados.
- **O relatório é em CSV** (C20, que fala em PDF ou CSV). O CSV usa `;` e a vírgula nas casas decimais, para abrir bem no Excel em português. Fica na opção "Campanhas" do Cliente.

Os dados de demonstração ganham um comentário da Carla ao criativo `Vídeo da montra`, a partir da unidade 6.1. Para o criar, corre-se outra vez `python -m gestor_campanhas.dados_demo`, que só acrescenta o que faltar. Os passos de cada página dizem quando.

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
| 1 | Ricardo | Fazer a unidade 6.1 — Comentários dos criativos e respostas | [ricardo.md](ricardo.md), passos 1 a 10 |
| 2 | Fabio | Rever e juntar a unidade 6.1 (de Ricardo) | [fabio.md](fabio.md), passos 1 a 7 |
| 3 | Fabio | Fazer a unidade 6.2 — Notificações na aplicação e por email | [fabio.md](fabio.md), passos 8 a 17 |
| 4 | Tomas | Rever e juntar a unidade 6.2 (de Fabio) | [tomas.md](tomas.md), passos 1 a 7 |
| 5 | Tomas | Fazer a unidade 6.3 — Painel de marketeers | [tomas.md](tomas.md), passos 8 a 17 |
| 6 | Ricardo | Rever e juntar a unidade 6.3 (de Tomas) | [ricardo.md](ricardo.md), passos 11 a 17 |
| 7 | Ricardo | Fazer a unidade 6.4 — Relatório das campanhas em CSV | [ricardo.md](ricardo.md), passos 18 a 27 |
| 8 | Fabio | Rever e juntar a unidade 6.4 (de Ricardo) | [fabio.md](fabio.md), passos 18 a 24 |
| 9 | Ricardo | Preparar a release v0.6.0 | [ricardo.md](ricardo.md), passos 28 a 36 |
| 10 | Fabio | Rever a release v0.6.0 e juntá-la ao main | [fabio.md](fabio.md), passos 25 a 32 |
| 11 | Ricardo | Publicar a release v0.6.0 e pedir o regresso ao develop | [ricardo.md](ricardo.md), passos 37 a 42 |
| 12 | Fabio | Juntar a release v0.6.0 ao develop | [fabio.md](fabio.md), passos 33 a 36 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Atualiza a página "Guia de utilização" da wiki | [fabio.md](fabio.md), passo 37 |
| Tomas | Atualiza a página "Arquitetura" da wiki | [tomas.md](tomas.md), passo 18 |
| Ricardo | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | [ricardo.md](ricardo.md), passos 43 a 44 |

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-6/ficheiros/
  6.1/    Comentários dos criativos e respostas
    commit-1/    feat(bd): criar a tabela dos comentários dos criativos
    commit-2/    feat(repositorios): guardar e ler os comentários dos criativos
    commit-3/    feat(comentarios): comentar um criativo e responder aos comentários
    commit-4/    feat(cli): comentários nos menus de criativos do cliente e do marketeer
    commit-5/    feat(demo): acrescentar um comentário de demonstração
    commit-6/    docs: documentar os comentários dos criativos
  6.2/    Notificações na aplicação e por email
    commit-1/    feat(bd): criar a tabela das notificações
    commit-2/    feat(repositorios): guardar e ler as notificações
    commit-3/    feat(notificacoes): notificar na plataforma e por email
    commit-4/    feat(notificacoes): avisar o marketeer e o cliente do que lhes diz respeito
    commit-5/    feat(cli): opção Notificações e aviso das notificações por ler
    commit-6/    docs: documentar as notificações
  6.3/    Painel de marketeers
    commit-1/    feat(bd): criar a tabela da atividade dos marketeers
    commit-2/    feat(repositorios): guardar a atividade e ler os criativos de cada marketeer
    commit-3/    feat(painel): registar a atividade dos marketeers nos criativos
    commit-4/    feat(painel): carga de trabalho e inatividade dos marketeers
    commit-5/    feat(cli): painel de marketeers no menu do administrador
    commit-6/    docs: documentar o painel de marketeers
  6.4/    Relatório das campanhas em CSV
    commit-1/    feat(relatorios): gravar o relatório das campanhas de um cliente em CSV
    commit-2/    feat(cli): exportar o relatório nas campanhas do cliente
    commit-3/    docs: documentar o relatório das campanhas
  6.5/    Release v0.6.0
    commit-1/    chore(release): passar a versão para 0.6.0
    commit-2/    docs(release): registar as alterações da versão 0.6.0
    commit-3/    docs(release): atualizar o README para a versão 0.6.0
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 6.5
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 6.5.`

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `863 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] As 9 issues das user stories da fase estão fechadas, e já não há nenhuma issue de user story aberta (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aopen+label%3A%22user+story%22)
- [ ] A release `v0.6.0` está publicada e a tag está num commit do `main` (ver https://github.com/Blive77/ADC-TrabGrupo/releases e https://github.com/Blive77/ADC-TrabGrupo/tags)
- [ ] O `main` tem a versão 0.6.0 (ver https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py)
- [ ] A milestone `Fase 6 — Comentários, notificações e relatórios` está fechada
- [ ] A wiki diz `Versão atual: v0.6.0` na página inicial
- [ ] No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias
- [ ] Todos os pull requests da fase juntos, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] `verificar.py 6.5` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, Fabio diz ao Claude **"avança para a Fase 7"** e conta os problemas que o grupo teve.

## Trello

Antes de começarem, confirmem que os nove cards da Fase 6 estão em **Sprint Backlog**: C17, C18, C19, C20, M17, M18, A17, A18 e A19.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com os 57 cards do projeto: os 8 da Fase 1, os 7 da Fase 2, os 12 da Fase 3, os 15 da Fase 4, os 6 da Fase 5 e os 9 desta fase. A Fase 7 não tem user stories.

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
