---
numero: 4
titulo: Criativos
testes: 566
---

@@ entrega
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

@@ verificacao
- As 15 issues das user stories da fase estão fechadas (ver {{REPO_B}}/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- A release `v0.4.0` está publicada e a tag está num commit do `main` (ver {{REPO_B}}/releases e {{REPO_B}}/tags)
- O `main` tem a versão 0.4.0 (ver {{REPO_B}}/blob/main/gestor_campanhas/__init__.py)
- A milestone `Fase 4 — Criativos` está fechada
- A wiki diz `Versão atual: v0.4.0` na página inicial
- No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias

@@ trello
Antes de começarem, confirmem que os quinze cards da Fase 4 estão em **Sprint Backlog**: M06, M07, M08, M09, M10, M11, M12, M13, M14, M15, C10, C11, C12, C13 e C14.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com 42 cards: os 8 da Fase 1, os 7 da Fase 2, os 12 da Fase 3 e os 15 desta fase.

Depois, movam para **Sprint Backlog** os seis cards da Fase 5: C15, M16, A14, A15, C16 e A16.
