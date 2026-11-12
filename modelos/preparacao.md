# Preparação

Faz-se **uma só vez**, antes da Fase 0.

{{AVISO_REPO_B}}- **Parte A** — cada um dos três, no seu computador.
- **Parte B** — só uma pessoa: quem criou o repositório oficial.

Ordem: quem criou o repositório oficial faz a Parte A e a seguir a Parte B. Depois, as outras duas pessoas fazem a Parte A.

Se algum termo não for claro, vê [O que é o quê](conceitos.md).

---

## Parte A — No teu computador

### Passo A1 — Abre um terminal e confirma as ferramentas

O terminal é a janela onde se escrevem comandos. Serve qualquer um destes:

- no VS Code, menu **Terminal → New Terminal**;
- a aplicação **Git Bash** (vem com o Git);
- a aplicação **PowerShell** do Windows.

Para colar um comando: copia-o daqui (no GitHub, cada bloco tem um botão de copiar no canto), clica no terminal, cola com Ctrl+V (no Git Bash, Shift+Insert) e carrega em Enter.

Confirma que tens o Git e o Python:

```bash
git --version
```

```bash
python --version
```

**Deves ver** algo como `git version 2.50.0` e `Python 3.12.4`. O Python tem de ser 3.10 ou superior.

Se um deles não for reconhecido, instala-o (Git: https://git-scm.com/downloads, Python: https://www.python.org/downloads/ — na instalação do Python, marca a opção **Add python.exe to PATH**), fecha o terminal, abre outro e repete.

### Passo A2 — Diz ao Git quem és

Cada commit fica assinado com um nome e um email. Para o GitHub ligar os commits à tua conta, o email tem de ser um dos que tens registados nela (vê em GitHub → foto no canto → **Settings → Emails**).

```bash
git config --global user.name "O Teu Nome"
```

```bash
git config --global user.email "o-teu-email-do-github"
```

Troca o texto entre aspas pelos teus dados. Confirma:

```bash
git config --global user.name
```

```bash
git config --global user.email
```

**Deves ver** o nome e o email que escreveste.

### Passo A3 — Aceita o convite do repositório oficial

Só para quem **não** criou o repositório oficial. Quem o criou salta este passo.

Abre {{REPO_B}}/invitations e clica em **Accept invitation**. Se a página disser que não há convite, pede a quem criou o repositório para te adicionar (Parte B, passo B3).

### Passo A4 — Copia o repositório oficial para o teu computador

Escolhe a pasta onde queres guardar o projeto e entra nela. Por exemplo, para a pasta Documentos:

```bash
cd ~/Documents
```

Fabio: não uses a pasta `ADC-TrabalhoGrupo`. Essa é a cópia do repositório de trabalho.

Copia o repositório:

```bash
git clone {{REPO_B}}
```

Entra na pasta que foi criada. O nome é o do repositório (a última parte do endereço):

```bash
cd NOME-DO-REPOSITORIO
```

**Deves ver**, no `git clone`, uma linha `Cloning into '...'`. Se o repositório ainda estiver vazio, aparece também o aviso `You appear to have cloned an empty repository`, que é normal.

A partir de agora, **todos os comandos dos guias são corridos dentro desta pasta**.

### Passo A5 — Liga o repositório de trabalho

```bash
git remote add trabalho {{REPO_A}}
```

```bash
git fetch trabalho
```

```bash
git config checkout.defaultRemote origin
```

```bash
git remote -v
```

| Comando | O que faz |
|---|---|
| `git remote add trabalho ...` | Dá o nome `trabalho` ao endereço do repositório de trabalho. Fica guardado só no teu computador |
| `git fetch trabalho` | Vai buscar os commits que lá estão. Não altera os teus ficheiros |
| `git config checkout.defaultRemote origin` | Os dois repositórios têm ramos com o mesmo nome. Isto diz ao Git que, em caso de dúvida, o ramo a usar é o do repositório oficial |
| `git remote -v` | Mostra os endereços configurados |

**Deves ver**, no último comando, quatro linhas: duas com `origin` (o repositório oficial) e duas com `trabalho`.

### Passo A6 — Instala as ferramentas de desenvolvimento

A aplicação não precisa de nada além do Python. Os testes e a documentação precisam de duas ferramentas:

```bash
python -m pip install pytest sphinx
```

**Deves ver**, no fim, uma linha a começar por `Successfully installed`, ou várias a dizer `Requirement already satisfied`.

A Parte A está feita.

---

## Parte B — Preparar o repositório oficial

Só para quem criou o repositório oficial. Faz primeiro a Parte A.

### Passo B1 — Primeiro commit

O repositório oficial tem de começar igual ao de trabalho: com um único ficheiro, o `README.md` inicial.

Abre {{REPO_B}} no browser e vê em que caso estás.

**Caso 1 — a página mostra "Quick setup" e nenhum ficheiro** (repositório vazio):

```bash
git checkout {{INICIAL}} -- README.md
git commit -m "chore: commit inicial"
git branch -M main
git push -u origin main
```

**Caso 2 — a página já mostra um `README.md`** criado pelo GitHub:

```bash
git switch main
git pull
git checkout {{INICIAL}} -- README.md
git commit -m "docs: definir o README inicial"
git push
```

| Comando | O que faz |
|---|---|
| `git checkout {{INICIAL}} -- README.md` | Vai buscar ao repositório de trabalho o `README.md` inicial e põe-no na tua pasta |
| `git commit -m "..."` | Grava-o num commit teu |
| `git branch -M main` | Garante que o ramo se chama `main` |
| `git push -u origin main` | Envia o ramo `main` para o GitHub |

Se o repositório tiver **outros ficheiros** além do `README.md`, não continues: diz-me o que lá está.

**Deves ver**, ao recarregar a página do repositório, o `README.md` com o título "Gestor de Campanhas".

### Passo B2 — Cria o ramo develop

```bash
git switch -c develop
git push -u origin develop
```

O `develop` é o ramo onde o trabalho se vai juntando. O `main` fica reservado para as versões entregues.

### Passo B3 — Adiciona as outras duas pessoas

1. Abre {{REPO_B}}/settings/access
2. Clica em **Add people**, escreve o nome de utilizador e confirma. Repete para a segunda pessoa.

Os nomes de utilizador são `blive77`, `GLKIIRA` e `CabritaXgamer`. Cada pessoa aceita o convite no passo A3.

### Passo B4 — Definições do repositório

Abre {{REPO_B}}/settings (página **General**).

1. **Default branch:** clica no ícone das duas setas, escolhe `develop`, **Update** e confirma. Assim os pull requests ficam logo apontados ao `develop`.
2. **Features:** confirma que **Wikis** e **Issues** estão marcados.
3. **Pull Requests:** deixa marcado só **Allow merge commits**. Desmarca **Allow squash merging** e **Allow rebase merging**. Essas duas opções juntam ou reescrevem os commits, e o histórico deixaria de mostrar o trabalho de cada pessoa.

### Passo B5 — Protege os ramos principais

Impede que alguém altere o `main` ou o `develop` sem pull request e sem revisão.

1. Abre {{REPO_B}}/settings/branches
2. Clica em **Add classic branch protection rule** (pode aparecer só como **Add rule**).
3. Em **Branch name pattern**, escreve `main`.
4. Marca **Require a pull request before merging** e, por baixo, **Require approvals** com o valor 1.
5. Clica em **Create**.
6. Repete para `develop`.

Se o repositório for privado numa conta gratuita, o GitHub não deixa ativar estas regras. Nesse caso salta este passo e cumpram a regra por disciplina: nunca fazer commit direto em `main` nem em `develop`.

### Passo B6 — Cria as labels

Abre {{REPO_B}}/labels. Para cada linha da tabela: **New label**, preenche o nome, a descrição e a cor, e clica em **Create label**. A label `bug` já existe.

| Name | Description | Color |
|---|---|---|
| `user story` | Funcionalidade descrita do ponto de vista de um utilizador | `#1D76DB` |
| `tarefa` | Trabalho técnico que não corresponde a uma user story | `#FBCA04` |
| `Administrador` | User story do perfil Administrador | `#8E44AD` |
| `Marketeer` | User story do perfil Marketeer | `#2ECC71` |
| `Cliente` | User story do perfil Cliente | `#3498DB` |

### Passo B7 — Cria as milestones

Abre {{REPO_B}}/milestones. Para cada linha: **New milestone**, preenche o título e a data, e clica em **Create milestone**.

Copia os títulos tal como estão. As issues usam estes nomes.

| Title | Due date |
|---|---|
| `Fase 0 — Arranque` | 13/11/2026 |
| `Fase 1 — Autenticação e sessões` | 14/11/2026 |
| `Fase 2 — Clientes e marketeers` | 15/11/2026 |
| `Fase 3 — Campanhas e pedidos` | 16/11/2026 |
| `Fase 4 — Criativos` | 18/11/2026 |
| `Fase 5 — Budget` | 19/11/2026 |
| `Fase 6 — Comentários, notificações e relatórios` | 20/11/2026 |
| `Fase 7 — Fecho e entrega` | 21/11/2026 |

### Passo B8 — Avisa o grupo

Diz às outras duas pessoas que já podem fazer a Parte A. Quando as três tiverem terminado, começa a [Fase 0](fase-0/README.md).
