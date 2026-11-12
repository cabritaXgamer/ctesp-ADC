@@ passo: Cria as 18 issues do perfil Marketeer
As 57 user stories do Trello passam a issues do repositório oficial, uma por story. Cada pessoa cria as de um perfil, com a sua conta. As tuas são as do **Marketeer**, de M01 a M18.

Podes fazer este passo em qualquer altura depois da Preparação, por exemplo enquanto esperas pela tua vez.

Os textos estão em {{REPO_A}}/blob/guias/issues/issues.md, na secção **Marketeer**. Abre essa página num separador do browser e deixa-a aberta.

Para cada issue, de M01 a M18:

**a)** Abre {{REPO_B}}/issues e clica em **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No título, cola o bloco **Título** dessa issue. Cada bloco tem um botão de copiar no canto superior direito.

**c)** Na caixa grande de texto, cola o bloco **Texto**.

**d)** Na coluna da direita, escolhe as duas **Labels** (`user story` e `Marketeer`) e a **Milestone** indicada por baixo dos blocos. Deixa **Assignees** vazio: a issue é atribuída quando alguém pegar nela, na fase respetiva.

**e)** Clica em **Create**.

**Deves ver**, no fim, 18 issues em {{REPO_B}}/issues?q=is%3Aissue+label%3AMarketeer

**Atalho opcional.** Há um script que cria as 18 de uma vez. Está explicado no passo equivalente da [página de Fabio](fabio.md); usa `--perfil Marketeer`.

@@ passo: Cria a página "Fluxo Git" da wiki
A wiki é a documentação do repositório, editada no próprio GitHub. Esta página explica como o grupo usa os ramos, os commits e os pull requests.

Faz este passo depois de Ricardo ter criado a página inicial da wiki. O GitHub só deixa criar outras páginas depois de a primeira existir.

**a)** Abre {{REPO_A}}/blob/guias/wiki/Fluxo-Git.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre {{REPO_B}}/wiki e clica em **New page**.

**c)** Em **Title**, escreve:

```text
Fluxo Git
```

**d)** Na caixa de texto, apaga o que lá estiver e cola o que copiaste.

**e)** Em **Edit message**, escreve `Criar a página Fluxo Git` e clica em **Save page**.

**Deves ver** a página com as tabelas dos ramos e dos tipos de commit. Na página inicial da wiki, a ligação "Fluxo Git" passa a funcionar.
