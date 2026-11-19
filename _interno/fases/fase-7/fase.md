---
numero: 7
titulo: Fecho e entrega
testes: 987
ultima: sim
---

@@ entrega
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

@@ verificacao
- Já não há nenhuma issue aberta (ver {{REPO_B}}/issues?q=is%3Aissue+is%3Aopen)
- As oito milestones, da Fase 0 à Fase 7, estão fechadas (ver {{REPO_B}}/milestones?state=closed)
- Há sete releases publicadas, de `v0.1.0` a `v0.6.0` e `v1.0.0`, e a tag `v1.0.0` está num commit do `main` (ver {{REPO_B}}/releases e {{REPO_B}}/tags)
- O `main` tem a versão 1.0.0 (ver {{REPO_B}}/blob/main/gestor_campanhas/__init__.py)
- A wiki tem as dez páginas: Home, Instalação e configuração, Guia de utilização, Arquitetura, Modelo de dados, Testes, Backlog e user stories, Fluxo Git, Registo das fases e Changelog (ver {{REPO_B}}/wiki/_pages)
- A wiki diz `Versão atual: v1.0.0` na página inicial, e as ligações da tabela "Páginas desta wiki" abrem todas a página certa
- No Trello, a lista **Ready** tem os 57 cards e as listas **Work In Progress** e **Ready to Verify** estão vazias

@@ trello
A Fase 7 não tem user stories, por isso não há cards para mover. Antes de começarem, confirmem que os 57 cards estão em **Ready** e que as listas **Sprint Backlog**, **Work In Progress** e **Ready to Verify** estão vazias. Se algum card ainda estiver noutra lista, é de uma story já feita numa fase anterior: movam-no para **Ready**.
