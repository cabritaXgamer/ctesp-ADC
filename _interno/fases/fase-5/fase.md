---
numero: 5
titulo: Budget
testes: 707
---

@@ entrega
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

@@ verificacao
- As 6 issues das user stories da fase estão fechadas (ver {{REPO_B}}/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- A release `v0.5.0` está publicada e a tag está num commit do `main` (ver {{REPO_B}}/releases e {{REPO_B}}/tags)
- O `main` tem a versão 0.5.0 (ver {{REPO_B}}/blob/main/gestor_campanhas/__init__.py)
- A milestone `Fase 5 — Budget` está fechada
- A wiki diz `Versão atual: v0.5.0` na página inicial
- No Trello, as listas **Work In Progress** e **Ready to Verify** estão vazias

@@ trello
Antes de começarem, confirmem que os seis cards da Fase 5 estão em **Sprint Backlog**: C15, M16, A14, A15, C16 e A16.

Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, a lista **Ready** fica com 48 cards: os 8 da Fase 1, os 7 da Fase 2, os 12 da Fase 3, os 15 da Fase 4 e os 6 desta fase.

Depois, movam para **Sprint Backlog** os nove cards da Fase 6: C17, C18, C19, C20, M17, M18, A17, A18 e A19.
