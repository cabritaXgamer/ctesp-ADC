# Fase 5 — Budget

A Fase 5 trata do budget das campanhas. No fim, o Cliente pede a alteração do budget de uma campanha, o Marketeer responsável diz se o pedido é viável e o Administrador decide. Cada campanha passa a ter um histórico do budget, e o Administrador ganha um resumo global: o budget atribuído face à despesa, por cliente, com as campanhas acima do budget em destaque.

São seis user stories (C15, M16, A14, A15, C16 e A16), em quatro unidades de trabalho, mais a release `v0.5.0`.

Um pedido de alteração de budget passa por três pessoas:

```
Cliente pede --> Marketeer dá parecer --> Administrador aprova ou rejeita
   Pendente         Em análise               Aprovado / Rejeitado
```

```
============================================================
Pedidos de alteração de budget de todos os clientes
============================================================
N.º  Feito em    Campanha    Cliente        De          Para        Estado      Parecer
---  ----------  ----------  -------------  ----------  ----------  ----------  -------
1    2026-11-18  Natal 2026  Carla Cliente  1 500,00 €  2 000,00 €  Em análise  Viável

1 pedido, 1 por decidir.
```

| Unidade | O que traz | Quem usa |
|---|---|---|
| 5.1 | Pedir a alteração do budget; ver e cancelar os pedidos | Cliente |
| 5.2 | Dar parecer sobre os pedidos | Marketeer |
| 5.3 | Decidir os pedidos; histórico do budget | Administrador e Cliente |
| 5.4 | Resumo global do budget | Administrador |

O que muda em relação à Fase 4:

- **A forma de trabalhar é a mesma.** Issues das stories, ramo, commits copiados com o `copiar.py`, pull request, revisão e merge.
- **Os menus mudam de número.** O Marketeer ganha a opção `3. Pedidos de budget` (unidade 5.2). O Administrador ganha `4. Pedidos de budget` (5.3) e `6. Resumo do budget` (5.4), e as opções que vinham a seguir descem. Os passos "Experimenta" dizem sempre o número certo para a unidade em causa.
- **Testar volta a mexer nos teus dados.** Os passos criam pedidos de budget, dão pareceres e alteram o budget da campanha `Natal 2026`. No fim, o passo da unidade 5.3 põe o budget outra vez em 1500 €, para os valores do resumo (5.4) baterem certo. Os pedidos de budget não se apagam: um pedido cancelado ou decidido fica na lista, e isso é normal.
- **Duas tabelas novas.** `pedidos_budget` (5.1) e `alteracoes_budget` (5.3). São criadas sozinhas no primeiro arranque depois do merge, sem apagar nada.

Decisões do grupo, que estão escritas nos critérios de aceitação:

- **Os pedidos de budget ficam na opção "Pedidos de campanha" do Cliente**, numa segunda lista, por baixo dos pedidos de nova campanha. Assim fica concluída a parte de C06 que tinha ficado da Fase 3.
- **O Administrador só decide depois do parecer** (A15). O parecer não obriga: um pedido "Não viável" pode ser aprovado.
- **Aprovar é alterar.** Aprovar muda logo o budget para o valor pedido. Para outro valor, o Administrador usa "Definir budget", que passa a pedir o motivo.
- **Um pedido por decidir de cada vez, por campanha.** Uma campanha que já terminou não aceita pedidos.
- **O histórico regista todas as alterações** (C16): o budget inicial, as alterações diretas do Administrador e os pedidos aprovados.
- **Os avisos ficam para a Fase 6.** O aviso ao cliente sobre a decisão (C17) e ao marketeer sobre um pedido novo (M18) entram com as notificações.

Os dados de demonstração ganham um pedido de alteração de budget, a partir da unidade 5.1, e o budget inicial das campanhas no histórico, a partir da 5.3. Para os criar, corre-se outra vez `python -m gestor_campanhas.dados_demo`, que só acrescenta o que faltar. Os passos de cada página dizem quando.

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
| 1 | Tomas | Fazer a unidade 5.1 — Pedido de alteração de budget | [tomas.md](tomas.md), passos 1 a 10 |
| 2 | Ricardo | Rever e juntar a unidade 5.1 (de Tomas) | [ricardo.md](ricardo.md), passos 1 a 7 |
| 3 | Ricardo | Fazer a unidade 5.2 — Parecer do marketeer sobre os pedidos de budget | [ricardo.md](ricardo.md), passos 8 a 17 |
| 4 | Fabio | Rever e juntar a unidade 5.2 (de Ricardo) | [fabio.md](fabio.md), passos 1 a 7 |
| 5 | Fabio | Fazer a unidade 5.3 — Decisão dos pedidos de budget e histórico do budget | [fabio.md](fabio.md), passos 8 a 17 |
| 6 | Tomas | Rever e juntar a unidade 5.3 (de Fabio) | [tomas.md](tomas.md), passos 11 a 17 |
| 7 | Tomas | Fazer a unidade 5.4 — Resumo global do budget | [tomas.md](tomas.md), passos 18 a 27 |
| 8 | Ricardo | Rever e juntar a unidade 5.4 (de Tomas) | [ricardo.md](ricardo.md), passos 18 a 24 |
| 9 | Tomas | Preparar a release v0.5.0 | [tomas.md](tomas.md), passos 28 a 36 |
| 10 | Fabio | Rever a release v0.5.0 e juntá-la ao main | [fabio.md](fabio.md), passos 18 a 25 |
| 11 | Tomas | Publicar a release v0.5.0 e pedir o regresso ao develop | [tomas.md](tomas.md), passos 37 a 42 |
| 12 | Fabio | Juntar a release v0.5.0 ao develop | [fabio.md](fabio.md), passos 26 a 29 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Atualiza a página "Guia de utilização" da wiki | [fabio.md](fabio.md), passo 30 |
| Tomas | Atualiza a página inicial da wiki; Atualiza a página "Registo das fases" da wiki | [tomas.md](tomas.md), passos 43 a 44 |
| Ricardo | Atualiza a página "Arquitetura" da wiki | [ricardo.md](ricardo.md), passo 25 |

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-5/ficheiros/
  5.1/    Pedido de alteração de budget
    commit-1/    feat(bd): criar a tabela dos pedidos de alteração de budget
    commit-2/    feat(repositorios): guardar e ler pedidos de alteração de budget
    commit-3/    feat(budget): pedir e cancelar uma alteração de budget
    commit-4/    feat(cli): pedidos de alteração de budget no menu do cliente
    commit-5/    feat(demo): acrescentar um pedido de alteração de budget de demonstração
    commit-6/    docs: documentar os pedidos de alteração de budget
  5.2/    Parecer do marketeer sobre os pedidos de budget
    commit-1/    feat(repositorios): guardar o parecer do marketeer
    commit-2/    feat(budget): dar parecer sobre um pedido de alteração de budget
    commit-3/    feat(cli): pedidos de budget e parecer no menu do marketeer
    commit-4/    docs: documentar o parecer do marketeer sobre os pedidos de budget
  5.3/    Decisão dos pedidos de budget e histórico do budget
    commit-1/    feat(bd): criar a tabela do histórico do budget
    commit-2/    feat(repositorios): registar o histórico do budget e as decisões dos pedidos
    commit-3/    feat(campanhas): registar no histórico cada alteração do budget
    commit-4/    feat(budget): decidir os pedidos de alteração de budget
    commit-5/    feat(cli): decidir os pedidos de budget no menu do administrador
    commit-6/    feat(cli): histórico do budget de cada campanha
    commit-7/    feat(demo): registar o budget inicial das campanhas de demonstração
    commit-8/    docs: documentar a decisão dos pedidos de budget e o histórico do budget
  5.4/    Resumo global do budget
    commit-1/    feat(budget): calcular o resumo global do budget por cliente
    commit-2/    feat(cli): resumo global do budget no menu do administrador
    commit-3/    docs: documentar o resumo global do budget
  5.5/    Release v0.5.0
    commit-1/    chore(release): passar a versão para 0.5.0
    commit-2/    docs(release): registar as alterações da versão 0.5.0
    commit-3/    docs(release): atualizar o README para a versão 0.5.0
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 5.5
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 5.5.`

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `707 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] As 6 issues das user stories da fase estão fechadas (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- [ ] A release `v0.5.0` está publicada e a tag está num commit do `main` (ver https://github.com/Blive77/ADC-TrabGrupo/releases e https://github.com/Blive77/ADC-TrabGrupo/tags)
- [ ] O `main` tem a versão 0.5.0 (ver https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py)
- [ ] A milestone `Fase 5 — Budget` está fechada
- [ ] A wiki diz `Versão atual: v0.5.0` na página inicial
- [ ] No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias
- [ ] Todos os pull requests da fase juntos, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] `verificar.py 5.5` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, Fabio diz ao Claude **"avança para a Fase 6"** e conta os problemas que o grupo teve.

## Trello

Antes de começarem, confirmem que os seis cards da Fase 5 estão em **Sprint Backlog**: C15, M16, A14, A15, C16 e A16.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com 48 cards: os 8 da Fase 1, os 7 da Fase 2, os 12 da Fase 3, os 15 da Fase 4 e os 6 desta fase.

Depois, movam para **Sprint Backlog** os nove cards da Fase 6: C17, C18, C19, C20, M17, M18, A17, A18 e A19.

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
