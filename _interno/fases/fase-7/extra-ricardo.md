---
quando: No fim da fase, depois de publicares a release
---
@@ passo: Cria a página "Backlog e user stories" da wiki
Uma página nova, com as 57 user stories do projeto, por fase e por perfil, e para cada uma a unidade em que foi feita e quem a fez.

Faz os teus passos da wiki no fim da fase, depois de publicares a release `v1.0.0`.

**a)** Abre {{REPO_A}}/blob/guias/wiki/Backlog-e-user-stories.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre {{REPO_B}}/wiki e clica em **New Page**, no canto superior direito.

**c)** Em **Title**, escreve exatamente:

```text
Backlog e user stories
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Backlog e user stories` e clica em **Save page**.

**Deves ver** a página com a tabela `Por fase` e uma tabela por perfil: `Administrador` (19 linhas), `Marketeer` (18) e `Cliente` (20).

@@ passo: Cria a página "Changelog" da wiki
Uma página nova, com as alterações de cada versão, da v0.1.0 à v1.0.0. É uma cópia do ficheiro `CHANGELOG.md` do repositório.

**a)** Abre {{REPO_A}}/blob/guias/wiki/Changelog.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre {{REPO_B}}/wiki e clica em **New Page**, no canto superior direito.

**c)** Em **Title**, escreve exatamente:

```text
Changelog
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Changelog` e clica em **Save page**.

**Deves ver** a página a começar pela secção `v1.0.0 — Fecho e entrega (2026-11-21)` e a acabar na `v0.1.0`.

@@ passo: Atualiza a página "Registo das fases" da wiki
A página ganha o que correu mal na Fase 6, a secção da Fase 7 e, no fim, o resumo do projeto.

Na Fase 6, o texto desta página foi colado na página inicial, e esta página ficou com uma versão antiga, só com as Fases 0 e 1. Este passo e o da página inicial substituem as duas por inteiro, por isso ficam corrigidas. Antes de colar, confirma no topo que a página aberta é a certa: o título tem de ser **Registo das fases**.

**a)** Abre {{REPO_A}}/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre {{REPO_B}}/wiki, clica em **Registo das fases** na lista de páginas, à direita, e depois em **Edit**.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Registar a Fase 7` e clica em **Save page**.

**Deves ver** a secção `Fase 7 — Fecho e entrega`, com a tabela das três unidades, e no fim a secção `Resumo do projeto`.

@@ passo: Atualiza a página inicial da wiki
A página inicial passa a indicar a versão 1.0.0 e a ligar para as dez páginas da wiki. É o último passo da wiki: faz este passo depois de Fabio e Tomas criarem as páginas deles ("Testes", "Instalação e configuração" e "Modelo de dados"), para todas as ligações abrirem.

**a)** Abre {{REPO_A}}/blob/guias/wiki/Home.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre {{REPO_B}}/wiki e clica em **Edit**, no canto superior direito. Confirma que estás a editar a página **Home**: é o título que aparece no topo.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar a página inicial para a versão 1.0.0` e clica em **Save page**.

**Deves ver** a linha `Versão atual: v1.0.0 (Fase 7 — Fecho e entrega). As 57 user stories estão implementadas.`

**e)** Na tabela `Páginas desta wiki`, clica em cada uma das nove ligações e confirma que abre a página certa. Se uma abrir uma página vazia a pedir para a criar, não a cries: o título da página verdadeira ficou diferente. Avisa quem a criou, que corrige o título no **Edit** dessa página.
