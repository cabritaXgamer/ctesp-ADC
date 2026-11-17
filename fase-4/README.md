# Fase 4 — Criativos

A Fase 4 traz os criativos: as peças de cada campanha (uma imagem, um vídeo, um texto a publicar). No fim, o Marketeer cria os criativos das suas campanhas, com custo, prazo, público-alvo, plataforma e um ficheiro anexado, e envia-os ao cliente. O Cliente vê-os, procura-os, aprova-os ou rejeita-os e descarrega os ficheiros. As listas de campanhas passam a mostrar quanto já se gastou do budget.

São quinze user stories (M06 a M15 e C10 a C14), em seis unidades de trabalho, mais a release `v0.4.0`.

```
============================================================
Criativos da campanha Natal 2026 (Carla Cliente)
============================================================
N.º  Nome             Custo     Prazo       Público-alvo               Plataforma  Estado
---  ---------------  --------  ----------  -------------------------  ----------  -------------
1    Banner de Natal  400,00 €  2026-11-25  Famílias da região de...   Facebook    Em preparação
2    Vídeo da montra  900,00 €  2026-11-28  Jovens adultos, 18 a 3...  Instagram   Em preparação

2 criativos.
Custo dos criativos: 1 300,00 €. Budget da campanha: 1 500,00 €.

============================================================
Criativos
============================================================
  1. Criar criativo
  2. Editar criativo
  3. Ver criativo
  4. Eliminar criativo
  5. Atualizar estado
  6. Anexar ficheiro
  7. Pré-visualizar ficheiro
  0. Voltar
Opção:
```

Um criativo passa por estes estados:

```
Em preparação --> Em revisão --> Aprovado --> Publicado
                       |
                       +-------> Rejeitado --> Em preparação ou Em revisão
```

O Marketeer envia o criativo para revisão e, depois de aprovado, marca-o como publicado. Quem aprova ou rejeita é o Cliente.

| Unidade | O que traz | Quem usa |
|---|---|---|
| 4.1 | Criar, editar e eliminar criativos | Marketeer |
| 4.2 | Custo, prazo, público-alvo e plataforma; ver um criativo | Marketeer |
| 4.3 | Lista dos criativos, com pesquisa e filtros | Cliente |
| 4.4 | Estados do criativo; aprovar ou rejeitar | Marketeer e Cliente |
| 4.5 | Anexar, pré-visualizar e descarregar o ficheiro | Marketeer e Cliente |
| 4.6 | Despesa face ao budget e aviso de budget ultrapassado | Marketeer e Cliente |

**A ordem das unidades mudou em relação ao plano.** No plano, os ficheiros vinham na unidade 4.3 e a lista do cliente na 4.5. Trocaram de lugar: a aprovação (4.4) e o descarregar (4.5) acontecem no menu de criativos do cliente, por isso esse menu tem de existir primeiro. Quem faz cada número de unidade não mudou: Tomas faz a 4.1 e a 4.4, Ricardo a 4.2 e a 4.5, Fabio a 4.3, a 4.6 e a release.

O que muda em relação à Fase 3:

- **A forma de trabalhar é a mesma.** Issues das stories, ramo, commits copiados com o `copiar.py`, pull request, revisão e merge.
- **O passo "Atualiza as duas pastas e cria o ramo" diz o que fazer se o ramo já existir.** Na Fase 3, um ramo criado antes do tempo deu o erro `a branch named ... already exists`. O passo explica agora como ver se o ramo tem commits e como o apagar e criar de novo.
- **Testar volta a mexer nos teus dados.** Os passos "Testa" criam criativos, mudam estados e anexam ficheiros na tua pasta `dados`. No fim de alguns testes, o passo pede para eliminares o que criaste, para os números das unidades seguintes baterem certo. A pasta `dados` não vai para o Git.
- **Há ficheiros de verdade.** A unidade 4.5 copia ficheiros para `dados/ficheiros`. Para experimentar, o projeto traz o ficheiro `exemplos/banner-natal.svg`.

Partes de stories que ficaram de fora, por decisão do grupo, e que estão escritas nos critérios de aceitação:

- **Uma plataforma por criativo** (M12 fala em "uma ou mais"). O mesmo anúncio no Facebook e no Instagram tem formatos diferentes, por isso são dois criativos.
- **Um só prazo** (M10 fala na data de entrega e na data de publicação). O prazo é a data de entrega; a publicação fica registada quando o marketeer marca o criativo como publicado.
- **A rejeição tem um estado próprio** (C13 diz que volta para "Em produção"). O criativo fica `Rejeitado`, com o motivo à vista, e o marketeer decide quando o põe de novo em preparação.
- **A pesquisa do cliente não filtra por intervalo de datas** (C11). Filtra por texto, campanha, plataforma e estado.
- **Não se guarda a data da última alteração** (M07).

As duas partes que tinham ficado da Fase 3 fecham-se nesta fase: o número de criativos por estado (M04) entra na unidade 4.4, o budget restante (M04) na 4.6, e a regra "só se eliminam campanhas sem criativos" (M05) na 4.1.

Os pedidos de alteração de budget (C06 e C08) continuam para a Fase 5.

Os dados de demonstração ganham quatro criativos, a partir da unidade 4.2. Para os criar, corre-se outra vez `python -m gestor_campanhas.dados_demo`, que só acrescenta o que faltar. Os passos de cada página dizem quando.

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
| 1 | Tomas | Fazer a unidade 4.1 — Criar, editar e eliminar criativos | [tomas.md](tomas.md), passos 1 a 10 |
| 2 | Ricardo | Rever e juntar a unidade 4.1 (de Tomas) | [ricardo.md](ricardo.md), passos 1 a 7 |
| 3 | Ricardo | Fazer a unidade 4.2 — Custo, prazo, público-alvo e plataforma | [ricardo.md](ricardo.md), passos 8 a 17 |
| 4 | Fabio | Rever e juntar a unidade 4.2 (de Ricardo) | [fabio.md](fabio.md), passos 1 a 7 |
| 5 | Fabio | Fazer a unidade 4.3 — Criativos do cliente, com pesquisa e filtros | [fabio.md](fabio.md), passos 8 a 17 |
| 6 | Tomas | Rever e juntar a unidade 4.3 (de Fabio) | [tomas.md](tomas.md), passos 11 a 17 |
| 7 | Tomas | Fazer a unidade 4.4 — Estados do criativo e aprovação pelo cliente | [tomas.md](tomas.md), passos 18 a 27 |
| 8 | Fabio | Rever e juntar a unidade 4.4 (de Tomas) | [fabio.md](fabio.md), passos 18 a 24 |
| 9 | Ricardo | Fazer a unidade 4.5 — Ficheiros dos criativos | [ricardo.md](ricardo.md), passos 18 a 27 |
| 10 | Tomas | Rever e juntar a unidade 4.5 (de Ricardo) | [tomas.md](tomas.md), passos 28 a 34 |
| 11 | Fabio | Fazer a unidade 4.6 — Despesa face ao budget e aviso de budget ultrapassado | [fabio.md](fabio.md), passos 25 a 34 |
| 12 | Ricardo | Rever e juntar a unidade 4.6 (de Fabio) | [ricardo.md](ricardo.md), passos 28 a 34 |
| 13 | Fabio | Preparar a release v0.4.0 | [fabio.md](fabio.md), passos 35 a 43 |
| 14 | Ricardo | Rever a release v0.4.0 e juntá-la ao main | [ricardo.md](ricardo.md), passos 35 a 42 |
| 15 | Fabio | Publicar a release v0.4.0 e pedir o regresso ao develop | [fabio.md](fabio.md), passos 44 a 49 |
| 16 | Ricardo | Juntar a release v0.4.0 ao develop | [ricardo.md](ricardo.md), passos 43 a 46 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | [fabio.md](fabio.md), passos 50 a 51 |
| Tomas | Atualiza a página "Guia de utilização" da wiki | [tomas.md](tomas.md), passo 35 |
| Ricardo | Atualiza a página "Arquitetura" da wiki | [ricardo.md](ricardo.md), passo 47 |

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-4/ficheiros/
  4.1/    Criar, editar e eliminar criativos
    commit-1/    feat(bd): criar a tabela dos criativos
    commit-2/    feat(modelos): acrescentar a classe Criativo e os estados de um criativo
    commit-3/    feat(repositorios): guardar, ler e eliminar criativos
    commit-4/    feat(criativos): criar, editar e eliminar criativos de uma campanha
    commit-5/    feat(cli): menu de criativos do marketeer
    commit-6/    feat(campanhas): só eliminar campanhas sem criativos
    commit-7/    docs: documentar os criativos do marketeer
  4.2/    Custo, prazo, público-alvo e plataforma
    commit-1/    feat(repositorios): guardar o custo, o prazo, o público-alvo e a plataforma
    commit-2/    feat(criativos): validar o custo, o prazo, o público-alvo e a plataforma
    commit-3/    feat(cli): pedir e mostrar o custo, o prazo, o público-alvo e a plataforma
    commit-4/    feat(cli): ver os detalhes de um criativo
    commit-5/    feat(demo): acrescentar criativos de demonstração
    commit-6/    docs: documentar o custo, o prazo, o público-alvo e a plataforma dos criativos
  4.3/    Criativos do cliente, com pesquisa e filtros
    commit-1/    feat(repositorios): listar os criativos de um cliente
    commit-2/    feat(criativos): criativos do cliente, com filtros e pesquisa
    commit-3/    feat(cli): lista dos criativos do cliente
    commit-4/    feat(cli): filtrar e pesquisar os criativos do cliente
    commit-5/    docs: documentar os criativos vistos pelo cliente
  4.4/    Estados do criativo e aprovação pelo cliente
    commit-1/    feat(repositorios): mudar o estado de um criativo
    commit-2/    feat(criativos): mudar o estado de um criativo
    commit-3/    feat(cli): atualizar o estado de um criativo no menu do marketeer
    commit-4/    feat(criativos): aprovar ou rejeitar um criativo em revisão
    commit-5/    feat(cli): aprovar ou rejeitar criativos no menu do cliente
    commit-6/    feat(campanhas): mostrar os criativos por estado de cada campanha
    commit-7/    docs: documentar os estados dos criativos e a aprovação pelo cliente
  4.5/    Ficheiros dos criativos
    commit-1/    feat(config): pasta dos ficheiros dos criativos
    commit-2/    feat(ficheiros): copiar, descrever e abrir ficheiros
    commit-3/    feat(criativos): anexar um ficheiro a um criativo
    commit-4/    feat(cli): anexar e pré-visualizar ficheiros no menu do marketeer
    commit-5/    feat(cli): pré-visualizar e descarregar ficheiros no menu do cliente
    commit-6/    docs: documentar os ficheiros dos criativos
  4.6/    Despesa face ao budget e aviso de budget ultrapassado
    commit-1/    feat(dinheiro): escrever valores negativos
    commit-2/    feat(criativos): calcular a despesa e o budget restante de uma campanha
    commit-3/    feat(cli): despesa e budget restante nas campanhas do marketeer
    commit-4/    feat(cli): despesa face ao budget nas campanhas do cliente
    commit-5/    feat(cli): avisar quando o custo dos criativos ultrapassa o budget
    commit-6/    docs: documentar a despesa e o aviso de budget ultrapassado
  4.7/    Release v0.4.0
    commit-1/    chore(release): passar a versão para 0.4.0
    commit-2/    docs(release): registar as alterações da versão 0.4.0
    commit-3/    docs(release): atualizar o README para a versão 0.4.0
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 4.7
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 4.7.`

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `566 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] As 15 issues das user stories da fase estão fechadas (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- [ ] A release `v0.4.0` está publicada e a tag está num commit do `main` (ver https://github.com/Blive77/ADC-TrabGrupo/releases e https://github.com/Blive77/ADC-TrabGrupo/tags)
- [ ] O `main` tem a versão 0.4.0 (ver https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py)
- [ ] A milestone `Fase 4 — Criativos` está fechada
- [ ] A wiki diz `Versão atual: v0.4.0` na página inicial
- [ ] No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias
- [ ] Todos os pull requests da fase juntos, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] `verificar.py 4.7` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, Fabio diz ao Claude **"avança para a Fase 5"** e conta os problemas que o grupo teve.

## Trello

Antes de começarem, confirmem que os quinze cards da Fase 4 estão em **Sprint Backlog**: M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, C10, C11, C12, C13 e C14.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com 42 cards: os 8 da Fase 1, os 7 da Fase 2, os 12 da Fase 3 e os 15 desta fase.

Depois, movam para **Sprint Backlog** os seis cards da Fase 5: C15, M16, A14, A15, C16 e A16.

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
