# Fase 2 — Clientes e marketeers

A Fase 2 dá ao Administrador a gestão das contas. No fim, o Administrador vê a lista dos clientes e a dos marketeers, pesquisa por nome, adiciona contas novas, edita os dados e desativa ou reativa contas.

São sete user stories (A04 a A10), em cinco unidades de trabalho, mais a release `v0.2.0`.

```
============================================================
Clientes
============================================================
N.º  Nome           Empresa                  Email                  Telefone   Estado
---  -------------  -----------------------  ---------------------  ---------  ------
5    Beatriz Lopes  Bicicletas do Sul, Lda.  beatriz@bicicletas.pt  910000005  Ativa
3    Carla Cliente  Empresa Exemplo, Lda.    cliente@empresa.pt     910000003  Ativa
4    José Padeiro   Padaria Central, Lda.    jose@padaria.pt        910000004  Ativa

3 clientes.

============================================================
Gestão de clientes
============================================================
  1. Pesquisar por nome
  2. Adicionar cliente
  3. Editar cliente
  4. Desativar ou reativar cliente
  0. Voltar
Opção:
```

O que muda em relação à Fase 1:

- **A forma de trabalhar é a mesma.** Issues das stories, ramo, commits copiados com o `copiar.py`, pull request, revisão e merge.
- **A release tem mais verificações.** Na Fase 1, o pull request da release foi junto ao `develop` em vez do `main`, e a tag ficou no commit errado. As páginas têm agora um passo para confirmar o destino antes de avisar quem revê e outro antes de juntar.
- **A milestone fecha-se no fim.** O fecho da milestone passou para o último passo da fase, quando todas as issues já estão fechadas.
- **Os passos do Trello dizem os cards pelo nome.**

Duas stories ficam com uma parte para a Fase 3, porque dependem das campanhas, que ainda não existem:

- **A04** pede o número de campanhas ativas de cada cliente. A coluna entra na lista quando houver campanhas.
- **A10** pede que as campanhas de um marketeer sejam reatribuídas antes de a conta ser desativada. A verificação entra com as campanhas.

Isto fica escrito nos critérios de aceitação das duas issues.

As contas de demonstração aumentam nesta fase: passam a ser três clientes e dois marketeers. Para as criar, corre-se outra vez `python -m gestor_campanhas.dados_demo`, que só acrescenta as que faltam.

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
| 1 | Fabio | Fazer a unidade 2.1 — Lista de clientes com pesquisa | [fabio.md](fabio.md), passos 1 a 10 |
| 2 | Tomas | Rever e juntar a unidade 2.1 (de Fabio) | [tomas.md](tomas.md), passos 1 a 7 |
| 3 | Tomas | Fazer a unidade 2.2 — Adicionar e editar clientes | [tomas.md](tomas.md), passos 8 a 17 |
| 4 | Ricardo | Rever e juntar a unidade 2.2 (de Tomas) | [ricardo.md](ricardo.md), passos 1 a 7 |
| 5 | Ricardo | Fazer a unidade 2.3 — Desativar e reativar clientes | [ricardo.md](ricardo.md), passos 8 a 17 |
| 6 | Fabio | Rever e juntar a unidade 2.3 (de Ricardo) | [fabio.md](fabio.md), passos 11 a 17 |
| 7 | Fabio | Fazer a unidade 2.4 — Adicionar e editar marketeers | [fabio.md](fabio.md), passos 18 a 27 |
| 8 | Tomas | Rever e juntar a unidade 2.4 (de Fabio) | [tomas.md](tomas.md), passos 18 a 24 |
| 9 | Tomas | Fazer a unidade 2.5 — Desativar e reativar marketeers | [tomas.md](tomas.md), passos 25 a 34 |
| 10 | Ricardo | Rever e juntar a unidade 2.5 (de Tomas) | [ricardo.md](ricardo.md), passos 18 a 24 |
| 11 | Tomas | Preparar a release v0.2.0 | [tomas.md](tomas.md), passos 35 a 43 |
| 12 | Ricardo | Rever a release v0.2.0 e juntá-la ao main | [ricardo.md](ricardo.md), passos 25 a 32 |
| 13 | Tomas | Publicar a release v0.2.0 e pedir o regresso ao develop | [tomas.md](tomas.md), passos 44 a 48 |
| 14 | Ricardo | Juntar a release v0.2.0 ao develop | [ricardo.md](ricardo.md), passos 33 a 36 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Atualiza a página "Arquitetura" da wiki | [fabio.md](fabio.md), passo 28 |
| Tomas | Atualiza a página inicial da wiki | [tomas.md](tomas.md), passo 49 |
| Ricardo | Atualiza a página "Guia de utilização" da wiki; Atualiza a página "Registo das fases" da wiki | [ricardo.md](ricardo.md), passos 37 a 38 |

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-2/ficheiros/
  2.1/    Lista de clientes com pesquisa
    commit-1/    feat(utilizadores): listar os utilizadores de um perfil
    commit-2/    feat(gestao): listar as contas de um perfil com pesquisa por nome
    commit-3/    feat(admin): mostrar a lista de clientes no menu do Administrador
    commit-4/    feat(demo): acrescentar dois clientes às contas de demonstração
    commit-5/    test(gestao): testar a lista de clientes e a pesquisa por nome
    commit-6/    docs(gestao): documentar a lista de clientes
  2.2/    Adicionar e editar clientes
    commit-1/    refactor(validacao): juntar num módulo as validações dos dados de uma conta
    commit-2/    feat(utilizadores): atualizar o email de um utilizador
    commit-3/    feat(gestao): criar contas e enviar as credenciais por email
    commit-4/    feat(gestao): editar os dados de uma conta
    commit-5/    feat(admin): adicionar e editar clientes a partir da lista
    commit-6/    test(gestao): testar a criação e a edição de clientes e as validações
    commit-7/    docs(gestao): documentar como adicionar e editar clientes
  2.3/    Desativar e reativar clientes
    commit-1/    feat(utilizadores): ativar e desativar a conta de um utilizador
    commit-2/    feat(gestao): desativar e reativar contas
    commit-3/    feat(admin): desativar e reativar clientes, com confirmação
    commit-4/    test(gestao): testar a desativação e a reativação de clientes
    commit-5/    docs(gestao): documentar como desativar e reativar clientes
  2.4/    Adicionar e editar marketeers
    commit-1/    refactor(cli): preparar os ecrãs de gestão para mais do que um perfil
    commit-2/    feat(admin): listar, pesquisar, adicionar e editar marketeers
    commit-3/    feat(demo): acrescentar um segundo marketeer às contas de demonstração
    commit-4/    test(gestao): testar a gestão de marketeers
    commit-5/    docs(gestao): documentar a gestão de marketeers
  2.5/    Desativar e reativar marketeers
    commit-1/    feat(admin): desativar e reativar marketeers, com confirmação
    commit-2/    feat(gestao): avisar por email quem tem a conta desativada ou reativada
    commit-3/    test(gestao): testar a desativação de marketeers e os avisos por email
    commit-4/    docs(gestao): documentar a desativação de marketeers e as contas desativadas
  2.6/    Release v0.2.0
    commit-1/    chore(release): passar a versão para 0.2.0
    commit-2/    docs(release): registar as alterações da versão 0.2.0
    commit-3/    docs(release): atualizar o README para a versão 0.2.0
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 2.6
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 2.6.`

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `194 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] As 7 issues das user stories da fase estão fechadas (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- [ ] A release `v0.2.0` está publicada e a tag está num commit do `main` (ver https://github.com/Blive77/ADC-TrabGrupo/releases e https://github.com/Blive77/ADC-TrabGrupo/tags)
- [ ] O `main` tem a versão 0.2.0 (ver https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py)
- [ ] A milestone `Fase 2 — Clientes e marketeers` está fechada
- [ ] A wiki diz `Versão atual: v0.2.0` na página inicial
- [ ] Todos os pull requests da fase juntos, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] `verificar.py 2.6` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, Fabio diz ao Claude **"avança para a Fase 3"** e conta os problemas que o grupo teve.

## Trello

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, movam para **Sprint Backlog** os doze cards da Fase 3: M02, M03, M04, M05, C05, C06, C07, C08, C09, A11, A12 e A13.

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
