---
numero: 2
titulo: Clientes e marketeers
testes: 194
fechada: sim
---

@@ entrega
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

@@ verificacao
- As 7 issues das user stories da fase estão fechadas (ver {{REPO_B}}/issues?q=is%3Aissue+is%3Aclosed+label%3A%22user+story%22)
- A release `v0.2.0` está publicada e a tag está num commit do `main` (ver {{REPO_B}}/releases e {{REPO_B}}/tags)
- O `main` tem a versão 0.2.0 (ver {{REPO_B}}/blob/main/gestor_campanhas/__init__.py)
- A milestone `Fase 2 — Clientes e marketeers` está fechada
- A wiki diz `Versão atual: v0.2.0` na página inicial

@@ trello
Durante a fase, cada pessoa move os cards das suas stories: para **Work In Progress** quando começa a unidade, para **Ready to Verify** quando abre o pull request, e quem revê move-os para **Ready** depois do merge. Estes passos estão nas páginas de cada um, com os cards indicados pelo nome.

No fim da fase, movam para **Sprint Backlog** os doze cards da Fase 3: M02, M03, M04, M05, C05, C06, C07, C08, C09, A11, A12 e A13.
