# Fase 7 — Fecho e entrega

A Fase 7 é a última. Não traz user stories novas: as 57 ficaram feitas na Fase 6. Esta fase confirma que as peças funcionam juntas, completa os dados de demonstração e a documentação, completa a wiki e publica a versão `v1.0.0`, que é a que se entrega a 22 de novembro.

São três unidades de trabalho, uma por pessoa, e as páginas da wiki que faltam, repartidas pelos três:

| Unidade | O que traz | Quem faz | Quem revê |
|---|---|---|---|
| 7.1 | Testes dos fluxos completos, com os três perfis, e dados de demonstração finais | Fabio | Tomas |
| 7.2 | Revisão dos docstrings, página do modelo de dados no Sphinx, README final | Tomas | Ricardo |
| 7.3 | Release `v1.0.0` | Ricardo | Fabio |

| Páginas da wiki | Quem |
|---|---|
| Testes (nova), Guia de utilização | Fabio |
| Instalação e configuração (nova), Modelo de dados (nova), Arquitetura | Tomas |
| Backlog e user stories (nova), Changelog (nova), Registo das fases, página inicial | Ricardo |

No fim, a wiki fica com as dez páginas do plano, e os dados de demonstração deixam cada perfil pronto a experimentar logo à primeira:

```
============================================================
As minhas notificações
============================================================
N.º  Data              Estado   Sobre           Mensagem
---  ----------------  -------  --------------  ------------------------------------------------------------
8    2026-11-21 10:00  Por ler  Criativo n.º 1  Miguel Marketeer respondeu ao seu comentário sobre o cria...
2    2026-11-21 10:00  Por ler  Criativo n.º 1  O criativo Banner de Natal, da campanha Natal 2026, passo...
1    2026-11-21 10:00  Por ler  Criativo n.º 1  Foi anexado o ficheiro banner-natal.svg ao criativo Banne...

3 notificações, 3 por ler.
```

O que muda em relação à Fase 6:

- **Não há user stories, por isso cada pessoa cria a issue da sua unidade**, com o modelo **Tarefa**, a label `tarefa` e a milestone `Fase 7 — Fecho e entrega`. O passo diz o texto a colar. Foi assim na Fase 0.
- **Cada commit faz-se em três passos, sempre por esta ordem:** `copiar.py`, `git add -A`, `git commit`. Na Fase 6, o `copiar.py` foi corrido outra vez antes de gravar o commit anterior e respondeu `ERRO: Tens alterações por gravar nesta pasta`. Os ficheiros estavam certos: faltava só gravar. Se isso acontecer, corre o `git add -A` e o `git commit` do commit que copiaste, e depois o `copiar.py` do seguinte.
- **O `verificar.py` leva o número da unidade do passo.** Na Fase 6, correr `verificar.py 5.5` comparou o `develop` com o fim da Fase 5 e mostrou como diferentes todos os ficheiros da Fase 6. Usa sempre o número que o passo indica.
- **Os dados de demonstração novos experimentam-se numa pasta à parte.** O `python -m gestor_campanhas.dados_demo` só acrescenta o que falta e não mexe no que já existe, por isso nos teus dados os criativos ficam como estavam. Para ver o resultado de uma instalação nova sem perderes nada, os passos "Testa" mandam usar uma pasta de dados ao lado das outras duas (`../dados-demo`), com a variável `GESTOR_CAMPANHAS_DADOS`, e voltar à pasta de sempre no fim. Os comandos são diferentes no PowerShell e no Git Bash: o passo tem os dois.
- **A wiki ganha cinco páginas novas.** Criar uma página nova é diferente de atualizar: em vez de **Edit**, clica-se em **New Page** e escreve-se o título exatamente como o passo diz, porque as ligações entre páginas usam esse título.

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
| 1 | Fabio | Fazer a unidade 7.1 — Testes dos fluxos completos e dados de demonstração finais | [fabio.md](fabio.md), passos 1 a 10 |
| 2 | Tomas | Rever e juntar a unidade 7.1 (de Fabio) | [tomas.md](tomas.md), passos 1 a 7 |
| 3 | Tomas | Fazer a unidade 7.2 — Revisão dos docstrings, Sphinx e README final | [tomas.md](tomas.md), passos 8 a 17 |
| 4 | Ricardo | Rever e juntar a unidade 7.2 (de Tomas) | [ricardo.md](ricardo.md), passos 1 a 7 |
| 5 | Ricardo | Preparar a release v1.0.0 | [ricardo.md](ricardo.md), passos 8 a 16 |
| 6 | Fabio | Rever a release v1.0.0 e juntá-la ao main | [fabio.md](fabio.md), passos 11 a 18 |
| 7 | Ricardo | Publicar a release v1.0.0 e pedir o regresso ao develop | [ricardo.md](ricardo.md), passos 17 a 22 |
| 8 | Fabio | Juntar a release v1.0.0 ao develop | [fabio.md](fabio.md), passos 19 a 22 |

Tarefas que não dependem da ordem. Podem ser feitas enquanto se espera pela vez:

| Quem | O que faz | Onde está explicado |
|---|---|---|
| Fabio | Cria a página "Testes" da wiki; Atualiza a página "Guia de utilização" da wiki | [fabio.md](fabio.md), passos 23 a 24 |
| Tomas | Cria a página "Instalação e configuração" da wiki; Cria a página "Modelo de dados" da wiki; Atualiza a página "Arquitetura" da wiki | [tomas.md](tomas.md), passos 18 a 20 |
| Ricardo | Cria a página "Backlog e user stories" da wiki; Cria a página "Changelog" da wiki; Atualiza a página "Registo das fases" da wiki; Atualiza a página inicial da wiki | [ricardo.md](ricardo.md), passos 23 a 26 |

## Onde estão os ficheiros

Os ficheiros de cada commit estão na pasta [`ficheiros`](ficheiros/), uma subpasta por unidade e, dentro dela, uma por commit:

```text
ctesp-ADC/fase-7/ficheiros/
  7.1/    Testes dos fluxos completos e dados de demonstração finais
    commit-1/    test(fluxos): da conta nova ao criativo publicado
    commit-2/    test(fluxos): do pedido de budget à decisão do Administrador
    commit-3/    feat(demo): dados de demonstração finais, com criativos em vários estados e notificações
    commit-4/    test(demo): testar os dados de demonstração no seu conjunto
    commit-5/    docs: documentar os testes dos fluxos e os dados de demonstração finais
  7.2/    Revisão dos docstrings, Sphinx e README final
    commit-1/    docs(código): completar os docstrings que faltavam
    commit-2/    test(docs): confirmar que o código e a referência ficam documentados
    commit-3/    docs(sphinx): página do modelo de dados
    commit-4/    docs(sphinx): atualizar a arquitetura e a configuração
    commit-5/    docs(readme): README final
  7.3/    Release v1.0.0
    commit-1/    chore(release): passar a versão para 1.0.0
    commit-2/    docs(release): registar as alterações da versão 1.0.0
    commit-3/    docs(release): atualizar o README para a versão 1.0.0
```

O comando `python ../ctesp-ADC/copiar.py` copia uma dessas pastas para dentro do repositório oficial. Copiar a pasta à mão, com o Explorador de Ficheiros, dá o mesmo resultado.

## Fecho da fase

Quando todas as vezes estiverem feitas, uma pessoa qualquer confirma que o repositório oficial ficou igual ao original. No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 7.3
```

Deve aparecer `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 7.3.`

Depois, confirma que tudo funciona:

```bash
python -m pytest
```

Deve terminar com `987 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

Deve terminar com `build succeeded.`

```bash
python -m gestor_campanhas
```

Deve aparecer o menu inicial.

### Lista de verificação

- [ ] Já não há nenhuma issue aberta (ver https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+is%3Aopen)
- [ ] As oito milestones, da Fase 0 à Fase 7, estão fechadas (ver https://github.com/Blive77/ADC-TrabGrupo/milestones?state=closed)
- [ ] Há sete releases publicadas, de `v0.1.0` a `v0.6.0` e `v1.0.0`, e a tag `v1.0.0` está num commit do `main` (ver https://github.com/Blive77/ADC-TrabGrupo/releases e https://github.com/Blive77/ADC-TrabGrupo/tags)
- [ ] O `main` tem a versão 1.0.0 (ver https://github.com/Blive77/ADC-TrabGrupo/blob/main/gestor_campanhas/__init__.py)
- [ ] A wiki tem as dez páginas: Home, Instalação e configuração, Guia de utilização, Arquitetura, Modelo de dados, Testes, Backlog e user stories, Fluxo Git, Registo das fases e Changelog (ver https://github.com/Blive77/ADC-TrabGrupo/wiki/_pages)
- [ ] A wiki diz `Versão atual: v1.0.0` na página inicial, e as ligações da tabela "Páginas desta wiki" abrem todas a página certa
- [ ] No Trello, a lista **Ready** tem os 57 cards e as listas **Work In Progress** e **Ready to Verify** estão vazias
- [ ] Todos os pull requests da fase juntos, cada um aprovado por outra pessoa do grupo (ver https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged)
- [ ] `verificar.py 7.3` responde `Tudo certo`
- [ ] Testes a passar e documentação gerada sem avisos

Quando estiver tudo, o trabalho está pronto para entregar. Fabio avisa o Claude, que confirma pela última vez que o repositório oficial ficou igual ao original, e conta os problemas que o grupo teve, para ficarem no registo das fases.

## Trello

A Fase 7 não tem user stories, por isso não há cards para mover. Antes de começarem, confirmem que os 57 cards estão em **Ready** e que as listas **Sprint Backlog**, **Work In Progress** e **Ready to Verify** estão vazias. Se algum card ainda estiver noutra lista, é de uma story já feita numa fase anterior: movam-no para **Ready**.

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
