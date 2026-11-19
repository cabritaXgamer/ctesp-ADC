---
numero: 6
titulo: Comentários, notificações, painel e relatório
testes: 863
fechada: sim
---

@@ entrega
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

@@ verificacao
- As 9 issues das user stories da fase estão fechadas, e já não há nenhuma issue de user story aberta (ver {{REPO_B}}/issues?q=is%3Aissue+is%3Aopen+label%3A%22user+story%22)
- A release `v0.6.0` está publicada e a tag está num commit do `main` (ver {{REPO_B}}/releases e {{REPO_B}}/tags)
- O `main` tem a versão 0.6.0 (ver {{REPO_B}}/blob/main/gestor_campanhas/__init__.py)
- A milestone `Fase 6 — Comentários, notificações e relatórios` está fechada
- A wiki diz `Versão atual: v0.6.0` na página inicial
- No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias

@@ trello
Antes de começarem, confirmem que os nove cards da Fase 6 estão em **Sprint Backlog**: C17, C18, C19, C20, M17, M18, A17, A18 e A19.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com os 57 cards do projeto: os 8 da Fase 1, os 7 da Fase 2, os 12 da Fase 3, os 15 da Fase 4, os 6 da Fase 5 e os 9 desta fase. A Fase 7 não tem user stories.
