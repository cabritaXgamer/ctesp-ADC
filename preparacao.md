# Preparação

Faz-se **uma só vez**, antes da Fase 0. No fim, cada pessoa fica com duas pastas no computador, uma para cada repositório, e o repositório oficial fica pronto para receber trabalho.

- **Parte A** — cada um dos três, no seu computador.
- **Parte B** — só Fabio, que criou o repositório oficial.

**Ordem:** Fabio faz a Parte A e a seguir a Parte B. Só depois é que as outras duas pessoas fazem a Parte A, porque precisam do convite que é enviado na Parte B.

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

Cada commit fica assinado com um nome e um email. Para o GitHub ligar os commits à tua conta, o email tem de ser um dos que tens registados nela (vê em GitHub → a tua foto no canto → **Settings → Emails**).

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

Fabio salta este passo.

Abre https://github.com/Blive77/ADC-TrabGrupo/invitations e clica em **Accept invitation**. Se a página disser que não há convite, pede a Fabio para te adicionar (passo B2).

### Passo A4 — Cria as duas pastas

Vais ter duas pastas lado a lado, uma para cada repositório, dentro de uma pasta chamada `ADC`:

```text
ADC/
  ADC-TrabGrupo/     o repositório oficial: é aqui que fazes commits
  ctesp-ADC/         o repositório de trabalho: só para ler e copiar
```

**a)** No Explorador de Ficheiros, cria uma pasta chamada `ADC` onde quiseres, por exemplo nos Documentos.

**b)** Abre um terminal dentro dela: clica com o botão direito num espaço vazio da pasta e escolhe **Abrir no Terminal** (ou **Git Bash Here**).

**c)** Copia os dois repositórios para o teu computador:

```bash
git clone https://github.com/Blive77/ADC-TrabGrupo
```

```bash
git clone -b guias https://github.com/cabritaXgamer/ctesp-ADC
```

| Comando | O que faz |
|---|---|
| `git clone https://github.com/Blive77/ADC-TrabGrupo` | Cria a pasta `ADC-TrabGrupo` com uma cópia do repositório oficial |
| `git clone -b guias https://github.com/cabritaXgamer/ctesp-ADC` | Cria a pasta `ctesp-ADC` com uma cópia do repositório de trabalho. O `-b guias` escolhe o ramo que tem as páginas e os ficheiros |

**d)** Entra na pasta do repositório oficial:

```bash
cd ADC-TrabGrupo
```

**e)** Confirma que as duas pastas estão no sítio certo:

```bash
python ../ctesp-ADC/copiar.py
```

**Deves ver** `Pastas no sítio certo.`, seguido do caminho das duas pastas.

Regras para o resto do trabalho:

- **Todos os comandos dos guias são corridos dentro da pasta `ADC-TrabGrupo`.** Se fechares o terminal, volta a abri-lo nessa pasta.
- **Na pasta `ctesp-ADC` nunca se altera nada nem se fazem commits.** Serve para ler estas páginas e para copiar os ficheiros de cada commit.

Fabio: no teu computador já existe a pasta `Documentos\ADC-TrabalhoGrupo`. É a pasta onde o Claude prepara o trabalho. Não a uses para estes passos e não lhe mexas. Cria a pasta `ADC` à parte, como os outros.

### Passo A5 — Instala as ferramentas de desenvolvimento

A aplicação não precisa de nada além do Python. Os testes e a documentação precisam de duas ferramentas:

```bash
python -m pip install pytest sphinx
```

**Deves ver**, no fim, uma linha a começar por `Successfully installed`, ou várias a dizer `Requirement already satisfied`.

A Parte A está feita.

---

## Parte B — Preparar o repositório oficial

Só para Fabio. Faz primeiro a Parte A.

O repositório oficial já existe e tem o ramo `main` com o `README.md` inicial. É esse o ponto de partida: não é preciso alterar nada no que lá está.

### Passo B1 — Cria o ramo develop

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git switch main
git pull
git switch -c develop
git push -u origin develop
```

| Comando | O que faz |
|---|---|
| `git switch main` | Muda para o ramo `main` |
| `git pull` | Garante que tens a versão mais recente |
| `git switch -c develop` | Cria o ramo `develop` a partir do `main` e muda para ele |
| `git push -u origin develop` | Envia o ramo novo para o GitHub |

O `develop` é o ramo onde o trabalho se vai juntando. O `main` fica reservado para as versões entregues.

**Deves ver**, perto do fim: `* [new branch]      develop -> develop`.

### Passo B2 — Adiciona as outras duas pessoas

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/settings/access

**b)** Clica em **Add people**, escreve `GLKIIRA` e confirma.

**c)** Repete para `CabritaXgamer`.

Cada pessoa aceita o convite no passo A3.

### Passo B3 — Definições do repositório

Abre https://github.com/Blive77/ADC-TrabGrupo/settings (página **General**).

**a)** **Default branch:** clica no ícone das duas setas, escolhe `develop`, clica em **Update** e confirma. Assim os pull requests ficam logo apontados ao `develop`.

**b)** **Features:** confirma que **Wikis** e **Issues** estão marcados.

**c)** **Pull Requests:** deixa marcado só **Allow merge commits**. Desmarca **Allow squash merging** e **Allow rebase merging**. Essas duas opções juntam ou reescrevem os commits, e o histórico deixaria de mostrar o trabalho de cada pessoa.

### Passo B4 — Protege os ramos principais

Impede que alguém altere o `main` ou o `develop` sem pull request e sem revisão.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/settings/branches

**b)** Clica em **Add classic branch protection rule** (pode aparecer só como **Add rule**).

**c)** Em **Branch name pattern**, escreve `main`.

**d)** Marca **Require a pull request before merging** e, por baixo, **Require approvals** com o valor 1.

**e)** Clica em **Create**.

**f)** Repete de b) a e) para `develop`.

### Passo B5 — Cria as labels

Abre https://github.com/Blive77/ADC-TrabGrupo/labels. Para cada linha da tabela: clica em **New label**, preenche o nome, a descrição e a cor, e clica em **Create label**. A label `bug` já existe.

| Name | Description | Color |
|---|---|---|
| `user story` | Funcionalidade descrita do ponto de vista de um utilizador | `#1D76DB` |
| `tarefa` | Trabalho técnico que não corresponde a uma user story | `#FBCA04` |
| `Administrador` | User story do perfil Administrador | `#8E44AD` |
| `Marketeer` | User story do perfil Marketeer | `#2ECC71` |
| `Cliente` | User story do perfil Cliente | `#3498DB` |

### Passo B6 — Cria as milestones

Abre https://github.com/Blive77/ADC-TrabGrupo/milestones. Para cada linha: clica em **New milestone**, preenche o título e a data, e clica em **Create milestone**.

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

### Passo B7 — Avisa o grupo

Diz às outras duas pessoas que já podem fazer a Parte A. Quando as três tiverem terminado, começa a [Fase 0](fase-0/README.md).
