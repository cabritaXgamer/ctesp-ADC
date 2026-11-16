---
numero: 3
titulo: Campanhas e pedidos
testes: 382
---

@@ entrega
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

@@ verificacao
- As 12 issues das user stories da fase estão fechadas (ver {{REPO_B}}/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- A release `v0.3.0` está publicada e a tag está num commit do `main` (ver {{REPO_B}}/releases e {{REPO_B}}/tags)
- O `main` tem a versão 0.3.0 (ver {{REPO_B}}/blob/main/gestor_campanhas/__init__.py)
- A milestone `Fase 3 — Campanhas e pedidos` está fechada
- A wiki diz `Versão atual: v0.3.0` na página inicial
- No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias

@@ trello
Antes de começarem, confirmem que os doze cards da Fase 3 estão em **Sprint Backlog**: M02, M03, M04, M05, C05, C06, C07, C08, C09, A11, A12 e A13.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com 27 cards: os 8 da Fase 1, os 7 da Fase 2 e os 12 desta fase.

Depois, movam para **Sprint Backlog** os quinze cards da Fase 4: M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, C10, C11, C12, C13 e C14.
