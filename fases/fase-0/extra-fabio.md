@@ passo: Cria as 19 issues do perfil Administrador
As 57 user stories do Trello passam a issues do repositório oficial, uma por story. Cada pessoa cria as de um perfil, com a sua conta. As tuas são as do **Administrador**, de A01 a A19.

Podes fazer este passo em qualquer altura depois da Preparação, por exemplo enquanto esperas pela tua vez.

Os textos estão em {{REPO_A}}/blob/guias/issues/issues.md, na secção **Administrador**. Abre essa página num separador do browser e deixa-a aberta.

Para cada issue, de A01 a A19:

**a)** Abre {{REPO_B}}/issues e clica em **New issue**. Se aparecer uma lista de modelos, escolhe **Blank issue**.

**b)** No título, cola o bloco **Título** dessa issue. Cada bloco tem um botão de copiar no canto superior direito.

**c)** Na caixa grande de texto, cola o bloco **Texto**.

**d)** Na coluna da direita, escolhe as duas **Labels** (`user story` e `Administrador`) e a **Milestone** indicada por baixo dos blocos. Deixa **Assignees** vazio: a issue é atribuída quando alguém pegar nela, na fase respetiva.

**e)** Clica em **Create**.

**Deves ver**, no fim, 19 issues em {{REPO_B}}/issues?q=is%3Aissue+label%3AAdministrador

**Atalho opcional.** Há um script que cria as 19 de uma vez. Precisa do GitHub CLI, um programa que deixa usar o GitHub pelo terminal. Só foi testado em modo de simulação, por isso corre primeiro com `--simular` e confirma a lista antes de o correr a sério. Numa pasta **fora** do repositório oficial:

```bash
winget install GitHub.cli
```

Fecha o terminal, abre outro, e inicia sessão (escolhe *GitHub.com*, *HTTPS* e *Login with a web browser*):

```bash
gh auth login
```

```bash
git clone -b guias {{REPO_A}} guias-adc
```

```bash
cd guias-adc/issues
```

```bash
python criar_issues.py --repo DONO/NOME --perfil Administrador --simular
```

```bash
python criar_issues.py --repo DONO/NOME --perfil Administrador
```

Troca `DONO/NOME` pela parte final do endereço do repositório oficial. Se o script parar com um erro, as issues anteriores já ficaram criadas: cria as restantes à mão.
