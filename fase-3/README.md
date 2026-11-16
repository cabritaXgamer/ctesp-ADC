# Fase 3 — Campanhas e pedidos

A Fase 3 traz as campanhas, que são o centro da aplicação. No fim, o Marketeer cria e gere campanhas, o Cliente pede campanhas novas e acompanha as suas, e o Administrador decide os pedidos, define o budget e escolhe o marketeer responsável.

São doze user stories (M02 a M05, C05 a C09 e A11 a A13), em cinco unidades de trabalho, mais a release `v0.3.0`.

```
============================================================
Todas as campanhas
============================================================
N.º  Nome                     Cliente        Marketeer         Início      Fim         Budget       Estado
---  -----------------------  -------------  ----------------  ----------  ----------  -----------  -----------
1    Natal 2026               Carla Cliente  Miguel Marketeer  2026-12-01  2026-12-24  1 500,00 €   Por começar
2    Regresso às aulas        José Padeiro   Miguel Marketeer  2026-09-01  2026-09-30  800,00 €     Terminada
3    Bicicletas de primavera  Beatriz Lopes  Marta Marques     -           -           Por definir  Em curso

3 campanhas.

============================================================
Campanhas
============================================================
  1. Definir budget
  2. Atribuir marketeer
  0. Voltar
Opção:
```

Uma campanha nasce de duas maneiras: o Marketeer cria-a diretamente, ou o Cliente pede-a e o Administrador aprova o pedido.

| Unidade | O que traz | Quem usa |
|---|---|---|
| 3.1 | Criar e editar campanhas | Marketeer |
| 3.2 | Lista completa, ver detalhes e eliminar | Marketeer |
| 3.3 | Pedir uma campanha, acompanhar e cancelar o pedido | Cliente |
| 3.4 | Aprovar ou rejeitar pedidos, definir o budget, atribuir o marketeer | Administrador |
| 3.5 | Ver as campanhas, o budget e o marketeer responsável | Cliente |

O que muda em relação à Fase 2:

- **A forma de trabalhar é a mesma.** Issues das stories, ramo, commits copiados com o `copiar.py`, pull request, revisão e merge.
- **O link do pull request já traz o destino certo.** Em vez de abrirem a lista dos pull requests e escolherem os ramos à mão, o passo "Abre o pull request" tem um link que já abre com a base e o ramo escolhidos. Continua a ser preciso confirmar o que está escrito no topo.
- **Há um passo novo antes de publicar a release.** Nas Fases 1 e 2, o pull request da release foi junto ao `develop` em vez do `main`, e a tag ficou no sítio errado. Agora, quem publica a release confirma primeiro que o `main` já tem a versão 0.3.0. Se não tiver, o passo diz como corrigir antes de criar a tag.
- **Esta fase é maior.** São 42 commits (a Fase 2 tinha 30). A unidade 3.4 é a mais comprida.

As duas partes que tinham ficado da Fase 2 fecham-se nesta fase, na unidade 3.4: a lista de clientes ganha o número de campanhas ativas (A04), e um marketeer com campanhas por terminar deixa de poder ser desativado (A10).

Três partes ficam para as fases seguintes, porque dependem de coisas que ainda não existem. Ficam escritas nos critérios de aceitação das issues:

- **M04** pede o budget restante e o número de criativos por estado. Entram na Fase 4, com os criativos.
- **M05** só deixa eliminar campanhas sem criativos. A verificação entra na Fase 4.
- **C06** e **C08** falam dos pedidos de alteração de budget, que são da Fase 5.

Os dados de demonstração aumentam: passam a existir três campanhas (a partir da unidade 3.2) e dois pedidos de campanha (a partir da unidade 3.3). Para os criar, corre-se outra vez `python -m gestor_campanhas.dados_demo`, que só acrescenta o que faltar. Os passos de cada página dizem quando.

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
| 1 | Ricardo | Fazer a unidade 3.1 — Criar e editar campanhas | [ricardo.md](ricardo.md), passos 1 a 10 |
| 2 | Fabio | Rever e juntar a unidade 3.1 (de Ricardo) | [fabio.md](fabio.md), passos 1 a 7 |
| 3 | Fabio | Fazer a unidade 3.2 — Campanhas atribuídas e eliminar campanha | [fabio.md](fabio.md), passos 8 a 17 |
| 4 | Tomas | Rever e juntar a unidade 3.2 (de Fabio) | [tomas.md](tomas.md), passos 1 a 7 |
| 5 | Tomas | Fazer a unidade 3.3 — Pedidos de nova campanha | [tomas.md](tomas.md), passos 8 a 17 |
| 6 | Ricardo | Rever e juntar a unidade 3.3 (de Tomas) | [ricardo.md](ricardo.md), passos 11 a 17 |
| 7 | Ricardo | Fazer a unidade 3.4 — Decidir pedidos, budget e marketeer responsável | [ricardo.md](ricardo.md), passos 18 a 27 |
| 8 | Tomas | Rever e juntar a unidade 3.4 (de Ricardo) | [tomas.md](tomas.md), passos 18 a 24 |
| 9 | Fabio | Fazer a unidade 3.5 — Campanhas do cliente e marketeer responsável | [fabio.md](fabio.md), passos 18 a 27 |
| 10 | Ricardo | Rever e juntar a unidade 3.5 (de Fabio) | [ricardo.md](ricardo.md), passos 28 a 34 |
| 11 | Ricardo | Preparar a release v0.3.0 | [ricardo.md](ricardo.md), passos 35 a 43 |
| 12 | Fabio | Rever a release v0.3.0 e juntá-la ao main | [fabio.md](fabio.md), passos 28 a 35 |
| 13 | Ricardo | Publicar a release v0.3.0 e pedir o regresso ao develop | [ricardo.md](ricardo.md), passos 44 a 49 |
| 14 | Fabio | Juntar a release v0.3.0 ao develop | [fabio.md](fabio.md), passos 36 a 39 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Atualiza a página "Arquitetura" da wiki | [fabio.md](fabio.md), passo 40 |
| Tomas | Atualiza a página "Guia de utilização" da wiki | [tomas.md](tomas.md), passo 25 |
| Ricardo | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | [ricardo.md](ricardo.md), passos 50 a 51 |

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-3/ficheiros/
  3.1/    Criar e editar campanhas
    commit-1/    feat(bd): criar a tabela das campanhas
    commit-2/    feat(modelos): acrescentar a classe Campanha
    commit-3/    feat(repositorios): guardar e ler campanhas
    commit-4/    feat(validacao): validar datas e períodos
    commit-5/    feat(campanhas): criar campanhas para um cliente
    commit-6/    feat(campanhas): editar o nome, o objetivo e as datas
    commit-7/    feat(cli): menu de campanhas do marketeer
    commit-8/    docs: documentar a criação e a edição de campanhas
  3.2/    Campanhas atribuídas e eliminar campanha
    commit-1/    feat(dinheiro): converter e formatar valores em euros
    commit-2/    feat(campanhas): calcular o estado a partir das datas
    commit-3/    feat(cli): mostrar o budget, o estado e os detalhes das campanhas
    commit-4/    feat(campanhas): eliminar uma campanha
    commit-5/    feat(cli): opção para eliminar uma campanha, com confirmação
    commit-6/    feat(demo): acrescentar campanhas de demonstração
    commit-7/    docs: documentar a lista, os detalhes e a eliminação de campanhas
  3.3/    Pedidos de nova campanha
    commit-1/    feat(bd): criar a tabela dos pedidos de campanha
    commit-2/    feat(modelos): acrescentar a classe PedidoCampanha
    commit-3/    feat(repositorios): guardar e ler pedidos de campanha
    commit-4/    feat(pedidos): pedir uma campanha nova
    commit-5/    feat(pedidos): cancelar um pedido pendente
    commit-6/    feat(cli): menu de pedidos de campanha do cliente
    commit-7/    feat(cli): ver e cancelar um pedido de campanha
    commit-8/    feat(demo): acrescentar pedidos de campanha de demonstração
    commit-9/    docs: documentar os pedidos de campanha do cliente
  3.4/    Decidir pedidos, budget e marketeer responsável
    commit-1/    feat(repositorios): ler todos os pedidos e alterar o budget e o marketeer
    commit-2/    feat(campanhas): definir o budget de uma campanha
    commit-3/    feat(campanhas): atribuir um marketeer a uma campanha
    commit-4/    feat(pedidos): analisar, aprovar e rejeitar pedidos de campanha
    commit-5/    feat(cli): pedidos de campanha no menu do administrador
    commit-6/    feat(cli): campanhas no menu do administrador
    commit-7/    feat(gestao): mostrar as campanhas ativas de cada cliente e marketeer
    commit-8/    feat(gestao): impedir desativar um marketeer com campanhas por terminar
    commit-9/    docs: documentar as decisões do administrador sobre pedidos e campanhas
  3.5/    Campanhas do cliente e marketeer responsável
    commit-1/    feat(repositorios): listar as campanhas de um cliente
    commit-2/    feat(campanhas): campanhas do cliente e marketeer responsável
    commit-3/    feat(cli): lista das campanhas do cliente, com o budget
    commit-4/    feat(cli): mostrar ao cliente o marketeer responsável e os contactos
    commit-5/    docs: documentar as campanhas vistas pelo cliente
  3.6/    Release v0.3.0
    commit-1/    fix(cli): corrigir a mensagem de atribuição de marketeer
    commit-2/    chore(release): passar a versão para 0.3.0
    commit-3/    docs(release): registar as alterações da versão 0.3.0
    commit-4/    docs(release): atualizar o README para a versão 0.3.0
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 3.6
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 3.6.`

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `382 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] As 12 issues das user stories da fase estão fechadas (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- [ ] A release `v0.3.0` está publicada e a tag está num commit do `main` (ver https://github.com/Blive77/ADC-TrabGrupo/releases e https://github.com/Blive77/ADC-TrabGrupo/tags)
- [ ] O `main` tem a versão 0.3.0 (ver https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py)
- [ ] A milestone `Fase 3 — Campanhas e pedidos` está fechada
- [ ] A wiki diz `Versão atual: v0.3.0` na página inicial
- [ ] No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias
- [ ] Todos os pull requests da fase juntos, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] `verificar.py 3.6` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, Fabio diz ao Claude **"avança para a Fase 4"** e conta os problemas que o grupo teve.

## Trello

Antes de começarem, confirmem que os doze cards da Fase 3 estão em **Sprint Backlog**: M02, M03, M04, M05, C05, C06, C07, C08, C09, A11, A12 e A13.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com 27 cards: os 8 da Fase 1, os 7 da Fase 2 e os 12 desta fase.

Depois, movam para **Sprint Backlog** os quinze cards da Fase 4: M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, C10, C11, C12, C13 e C14.

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
