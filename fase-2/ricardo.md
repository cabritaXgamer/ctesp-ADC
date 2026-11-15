# Fase 2 — Passo a passo de Ricardo

Esta página tem tudo o que **Ricardo** faz na Fase 2 (Clientes e marketeers), por ordem. Cada passo diz o que fazer, onde, e o que deves ver no fim. Não saltes passos e não avances se o resultado não for o esperado.

## Antes de começares

Tens duas pastas lado a lado no teu computador, criadas na [Preparação](../preparacao.md):

| Pasta | O que é | O que fazes lá |
|---|---|---|
| `ADC-TrabGrupo` | O repositório oficial, o que é avaliado | **Tudo.** Todos os comandos desta página são corridos dentro desta pasta |
| `ctesp-ADC` | O repositório de trabalho, com os ficheiros preparados e estas páginas | Nada. Só se lê e se copia de lá |

Abre o terminal dentro da pasta `ADC-TrabGrupo` e deixa-o lá até ao fim. Os comandos funcionam no terminal do VS Code, no PowerShell e no Git Bash.

Se algum termo não for claro, vê [O que é o quê](../conceitos.md). A ordem geral da fase está na [página da fase](README.md).

## Os teus passos

| Passos | O que fazes | Quando |
|---|---|---|
| 1 a 7 | Rever e juntar a unidade 2.2 (de Tomas) | Quando Tomas avisar |
| 8 a 17 | Fazer a unidade 2.3 — Desativar e reativar clientes | A seguir ao teu passo anterior |
| 18 a 24 | Rever e juntar a unidade 2.5 (de Tomas) | Quando Tomas avisar |
| 25 a 32 | Rever a release v0.2.0 e juntá-la ao main | Quando Tomas avisar |
| 33 a 36 | Juntar a release v0.2.0 ao develop | Quando Tomas avisar |
| 37 a 38 | Atualiza a página "Guia de utilização" da wiki; Atualiza a página "Registo das fases" da wiki | Em qualquer altura durante a fase |

---

## Rever e juntar a unidade 2.2 — Adicionar e editar clientes

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 1 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 2.2 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Adicionar e editar clientes**.

### Passo 2 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 3 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/2.2-adicionar-editar-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/2.2-adicionar-editar-cliente` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/2.2-adicionar-editar-cliente'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `166 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`) e escolhe `1` (Clientes). **Deves ver** a tabela dos clientes e, por baixo, o menu `Gestão de clientes`.

Adiciona um cliente:

| Escreves | Deves ver |
|---|---|
| `2` e Enter | O título `Adicionar cliente` e a pergunta `Nome` |
| `Rita Reis` | A pergunta `Email` |
| `rita@loja.pt` | A pergunta `Telefone (opcional)` |
| Enter | A pergunta `Empresa (opcional)` |
| `Loja da Rita` | A pergunta `NIF (opcional)` |
| Enter | `Cliente criado com o número ...` e `As credenciais de acesso foram enviadas para rita@loja.pt.` |
| Enter | A tabela outra vez, agora com a linha de `Rita Reis` |

Aponta o número que aparece na primeira coluna da linha de `Rita Reis`. Agora edita esse cliente:

| Escreves | Deves ver |
|---|---|
| `3` e Enter | O título `Editar cliente` e a pergunta `Número do cliente (Enter para cancelar)` |
| O número de Rita Reis | `A editar Rita Reis.` e a pergunta `Nome [Rita Reis]` |
| Enter | A pergunta `Email [rita@loja.pt]` |
| Enter | A pergunta `Telefone []` |
| `912345678` | A pergunta `Empresa [Loja da Rita]` |
| Enter | A pergunta `NIF []` |
| Enter | `Dados guardados.` |
| Enter | A tabela, com o telefone `912345678` na linha de Rita Reis |

Sai com `0`, `0` e `0`.

Por fim, vê o email com as credenciais:

```bash
ls dados/caixa_saida
```

**Deves ver** um ficheiro cujo nome acaba em `rita_loja.pt.txt`. Abre-o no VS Code ou no Bloco de Notas: tem o email e a password da conta nova.

Confirma também:

- Tenta adicionar um cliente com o email `cliente@empresa.pt`: aparece `Já existe uma conta com este email. O cliente não foi criado.`
- Tenta adicionar um cliente com o email `rita`: aparece `O email não é válido.`
- Na opção "Editar cliente", escreve `999`: aparece `Não existe nenhum cliente com o número 999.`
- Entra com o email e a password que estão no ficheiro da pasta `dados/caixa_saida`: abre o menu "Cliente".

### Passo 4 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 5 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move os cards das stories A05 e A06 para **Ready**.

### Passo 6 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/2.2-adicionar-editar-cliente
python ../ctesp-ADC/verificar.py 2.2
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/2.2-adicionar-editar-cliente` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 2.2` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 2.2 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 2.2.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 7 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 17 da [página de Tomas](tomas.md)).

A vez seguinte é tua: continua no passo 8.

---

## Fazer a unidade 2.3 — Desativar e reativar clientes

O Administrador passa a poder remover o acesso de um cliente. A conta não é apagada: fica desativada, com os dados e o histórico guardados, e pode ser reativada.

### Passo 8 — Confirma que podes começar

Esta unidade assenta na anterior. O pull request **Adicionar e editar clientes** (unidade 2.2) tem de estar junto ao `develop`.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls?q=is%3Apr+is%3Amerged e confirma que ele está na lista, com o símbolo roxo **Merged**. Se não estiver, espera: ainda não podes começar.

### Passo 9 — Fica com as issues da unidade 2.3

As issues desta unidade já existem: foram criadas na Fase 0, uma por user story. Esta unidade tem 1 issue: A07. Vais ficar responsável por elas e escrever os critérios de aceitação, que dizem o que tem de funcionar para a story estar feita.

Para cada uma:

**a)** Abre a ligação indicada e clica na issue.

**b)** Na coluna da direita, em **Assignees**, clica em *assign yourself*.

**c)** No canto superior direito da descrição da issue, clica nos três pontos **…** e em **Edit**.

**d)** Apaga a linha `A detalhar quando a story entrar no Sprint Backlog.` e cola no lugar dela os critérios indicados aqui.

**e)** Clica em **Save** (em alguns ecrãs chama-se *Update comment*).

**f)** Aponta o número da issue, que aparece a seguir ao título, por exemplo `#12`.

**Issue A07** — https://github.com/Blive77/ADC-TrabGrupo/issues?q=is%3Aissue+in%3Atitle+%22%5BA07%5D%22

```markdown
- [ ] Por baixo da lista de clientes há a opção "Desativar ou reativar cliente", que pede o número do cliente
- [ ] São mostrados o nome, o email e o estado atual da conta, e é pedida uma confirmação (s/n)
- [ ] Sem confirmação, nada é alterado
- [ ] Um cliente com a conta desativada não consegue entrar e vê o aviso de conta desativada
- [ ] A conta desativada continua na lista, com o estado "Desativada", e mantém todos os dados
- [ ] A mesma opção reativa a conta, e o cliente volta a entrar com a password que tinha
- [ ] Não é possível alterar por aqui o estado de uma conta que não seja de um cliente
```

Por fim, no quadro Trello, move o card da story A07 de **Sprint Backlog** para **Work In Progress**.

### Passo 10 — Atualiza as duas pastas e cria o ramo

No terminal, dentro da pasta `ADC-TrabGrupo`:

```bash
git -C ../ctesp-ADC pull
git switch develop
git pull
git switch -c feature/2.3-desativar-cliente
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho, sem saíres da pasta onde estás. É de lá que vais copiar os ficheiros |
| `git switch develop` | Muda para o ramo `develop` do repositório oficial |
| `git pull` | Atualiza o teu `develop` com o que o grupo já juntou no GitHub |
| `git switch -c feature/2.3-desativar-cliente` | Cria um ramo novo a partir do `develop` e muda para ele. É neste ramo que vais trabalhar |

**Deves ver**, na última linha: `Switched to a new branch 'feature/2.3-desativar-cliente'`.

### Passo 11 — Copia e grava os 5 commits

São 5 commits. Cada um faz-se em dois tempos: primeiro copias os ficheiros, depois gravas.

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 2.3 1` | Copia para esta pasta os ficheiros do commit 1 da unidade 2.3. Eles estão na pasta `ctesp-ADC/fase-2/ficheiros/2.3/commit-1`. Antes de copiar, confirma que estás no ramo certo e que não saltaste nenhum commit |
| `git add -A` | Diz ao Git que as alterações que estão na pasta são para entrar no próximo commit |
| `git commit -m "mensagem"` | Grava essas alterações num commit **teu**, com o teu nome e a mensagem entre aspas |

Faz um commit de cada vez, pela ordem em que estão aqui. Se o primeiro comando responder com `ERRO`, para e lê a mensagem: ela diz o que está mal e o que fazer. Não corras os comandos seguintes.

Se aparecerem linhas começadas por `warning:` a falar de `LF` e `CRLF`, podes ignorá-las. São avisos sobre o tipo de fim de linha dos ficheiros e não afetam nada.

**Commit 1 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.3 1
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/repositorios/utilizadores.py`.

```bash
git add -A
git commit -m "feat(utilizadores): ativar e desativar a conta de um utilizador"
```

**Deves ver** uma linha a terminar em `1 file changed, 15 insertions(+)`.

**Commit 2 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.3 2
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/servicos/gestao.py`.

```bash
git add -A
git commit -m "feat(gestao): desativar e reativar contas"
```

**Deves ver** uma linha a terminar em `1 file changed, 22 insertions(+)`.

**Commit 3 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.3 3
```

**Deves ver** `Copiados 1 ficheiro`: `gestor_campanhas/cli/gestao.py`.

```bash
git add -A
git commit -m "feat(admin): desativar e reativar clientes, com confirmação"
```

**Deves ver** uma linha a terminar em `1 file changed, 31 insertions(+)`.

**Commit 4 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.3 4
```

**Deves ver** `Copiados 1 ficheiro`: `tests/test_gestao.py`.

```bash
git add -A
git commit -m "test(gestao): testar a desativação e a reativação de clientes"
```

**Deves ver** uma linha a terminar em `1 file changed, 95 insertions(+)`.

**Commit 5 de 5**

```bash
python ../ctesp-ADC/copiar.py 2.3 5
```

**Deves ver** `Copiados 1 ficheiro`: `docs/utilizacao.rst`.

```bash
git add -A
git commit -m "docs(gestao): documentar como desativar e reativar clientes"
```

**Deves ver** uma linha a terminar em `1 file changed, 11 insertions(+)`.


### Passo 12 — Confirma que ficou igual ao original

```bash
python ../ctesp-ADC/verificar.py 2.3
git log --oneline -5
```

| Comando | O que deves ver |
|---|---|
| `python ../ctesp-ADC/verificar.py 2.3` | `Tudo certo: o ramo 'feature/2.3-desativar-cliente' está igual ao original no fim da unidade 2.3.` Este comando compara o que gravaste com o que está no repositório de trabalho. Não altera nada |
| `git log --oneline -5` | Os teus 5 commits, do mais recente para o mais antigo |

A lista do `git log` deve ser esta. No lugar de `xxxxxxx` aparece um código diferente em cada commit, que é a identificação que o Git lhe deu:

```text
xxxxxxx docs(gestao): documentar como desativar e reativar clientes
xxxxxxx test(gestao): testar a desativação e a reativação de clientes
xxxxxxx feat(admin): desativar e reativar clientes, com confirmação
xxxxxxx feat(gestao): desativar e reativar contas
xxxxxxx feat(utilizadores): ativar e desativar a conta de um utilizador
```

### Passo 13 — Experimenta o que gravaste

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `175 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`) e escolhe `1` (Clientes). Aponta o número que está na primeira coluna da linha de `Beatriz Lopes`.

| Escreves | Deves ver |
|---|---|
| `4` e Enter | O título `Desativar ou reativar cliente` e a pergunta `Número do cliente (Enter para cancelar)` |
| O número de Beatriz Lopes | `Beatriz Lopes (beatriz@bicicletas.pt) tem a conta ativa.` e a pergunta `Desativar a conta? (s/n)` |
| `n` | `Nada foi alterado.` |
| Enter, `4`, o mesmo número, `s` | `Conta desativada.` |
| Enter | A tabela, com `Desativada` na linha de Beatriz Lopes |

Sai da gestão e termina a sessão com `0` e `0`. Agora tenta entrar com a conta desativada:

| Escreves | Deves ver |
|---|---|
| `1`, `beatriz@bicicletas.pt`, `beatriz12345` | `Esta conta está desativada. Fale com o administrador.` |

Carrega em Enter, entra outra vez como administrador e reativa a conta: `1`, `4`, o número de Beatriz Lopes, `s`. **Deves ver** `Conta reativada.` e, na tabela, `Ativa`.

Sai com Enter, `0`, `0` e `0`.

### Passo 14 — Envia o ramo para o GitHub

```bash
git push -u origin feature/2.3-desativar-cliente
```

O `push` envia o teu ramo e os teus commits para o repositório oficial no GitHub. O `-u` liga o ramo do teu computador ao do GitHub.

**Deves ver**, perto do fim: `* [new branch]      feature/2.3-desativar-cliente -> feature/2.3-desativar-cliente`.

### Passo 15 — Abre o pull request

O pull request é o pedido para juntar o teu ramo ao `develop`. É nele que Fabio vai rever o teu trabalho.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls. Normalmente aparece uma faixa amarela com o nome do teu ramo e o botão **Compare & pull request**: clica nele. Se a faixa não aparecer, clica em **New pull request** e, em *compare*, escolhe `feature/2.3-desativar-cliente`.

**b)** Confirma, no topo, que está **base: develop** e **compare: feature/2.3-desativar-cliente**. Se a base for `main`, muda para `develop`.

**c)** No título, cola:

```text
Desativar e reativar clientes
```

**d)** Na descrição, apaga o que lá estiver e cola o texto seguinte. Troca cada `#(número da issue ...)` pelo número que apontaste, por exemplo `#12`. A palavra `Closes` tem de ficar antes de cada número:

```markdown
## O que muda

O Administrador passa a poder desativar e reativar a conta de um cliente, com pedido de confirmação.

- Função do repositório que ativa ou desativa uma conta
- Regra no serviço: só contas de clientes e de marketeers, e só se o estado mudar
- Opção "Desativar ou reativar cliente" no menu de gestão de clientes

A conta nunca é apagada, para o histórico do cliente se manter.

Closes #(número da issue A07)

## Como testar

1. `python -m pytest` (175 testes)
2. `python -m gestor_campanhas`, entrar como administrador e escolher "Clientes"
3. Desativar um cliente, tentar entrar com a conta dele e reativá-lo
```

**e)** Na coluna da direita, escolhe:

- **Reviewers:** Fabio (no GitHub, `blive77`)
- **Assignees:** tu
- **Labels:** `user story`
- **Milestone:** `Fase 2 — Clientes e marketeers`

**f)** Clica no botão verde **Create pull request**.

**g)** No fundo da página aparecem as verificações automáticas (*Testes*, *Documentação*). Espera um ou dois minutos até ficarem com um visto verde.

**h)** No Trello, move o card da story A07 para **Ready to Verify**.

### Passo 16 — Avisa Fabio

Diz a Fabio que o pull request da unidade 2.3 está pronto para rever. A partir daqui é a vez de Fabio: [página de Fabio](fabio.md), passos 11 a 17.

### Passo 17 — Quando Fabio disser que juntou, arruma o teu computador

```bash
git switch develop
git pull
git branch -d feature/2.3-desativar-cliente
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` já com o teu trabalho junto |
| `git branch -d feature/2.3-desativar-cliente` | Apaga o ramo do teu computador. Já não é preciso: os commits estão no `develop` |

---

## Rever e juntar a unidade 2.5 — Desativar e reativar marketeers

Quem fez: Tomas. Tu confirmas que funciona e juntas o trabalho ao `develop`.

### Passo 18 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 2.5 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Desativar e reativar marketeers**.

### Passo 19 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 20 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch feature/2.5-desativar-marketeer
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch feature/2.5-desativar-marketeer` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'feature/2.5-desativar-marketeer'`.

Agora experimenta:

Corre os testes:

```bash
python -m pytest
```

**Deves ver** `194 passed`.

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

Entra como administrador (`1`, depois `admin@agencia.pt` e `admin12345`) e escolhe `2` (Marketeers). **Deves ver**, no menu de gestão, `4. Desativar ou reativar marketeer`. Aponta o número de `Marta Marques`.

| Escreves | Deves ver |
|---|---|
| `4` e Enter | O título `Desativar ou reativar marketeer` e a pergunta do número |
| O número de Marta Marques | `Marta Marques (marta@agencia.pt) tem a conta ativa.` e a pergunta `Desativar a conta? (s/n)` |
| `s` | `Conta desativada.` e `Foi enviado um aviso para marta@agencia.pt.` |
| Enter | A tabela, com `Desativada` na linha de Marta Marques |

Sai da gestão e termina a sessão com `0` e `0`. Tenta entrar com a conta desativada:

| Escreves | Deves ver |
|---|---|
| `1`, `marta@agencia.pt`, `marta12345` | `Esta conta está desativada. Fale com o administrador.` |

Carrega em Enter, entra outra vez como administrador e reativa a conta: `2`, `4`, o número de Marta Marques, `s`. **Deves ver** `Conta reativada.`

Sai com Enter, `0`, `0` e `0`. Por fim, vê os emails:

```bash
ls dados/caixa_saida
```

**Deves ver** dois ficheiros com `marta_agencia.pt` no nome. Um tem o assunto `A sua conta foi desativada` e o outro `A sua conta foi reativada`.

Confirma também:

- Na gestão de clientes, desativa e reativa um cliente: também aparece `Foi enviado um aviso para ...`.
- Entra e sai como `marketeer@agencia.pt` / `marketeer12345`, desativa essa conta como administrador e abre "Horários de entrada e saída dos marketeers": as sessões de `Miguel Marketeer` continuam lá. No fim, reativa a conta.
- Responde `n` à confirmação: aparece `Nada foi alterado.` e não é criado nenhum ficheiro novo em `dados/caixa_saida`.

### Passo 21 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 22 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `develop`.

**Deves ver** o símbolo roxo **Merged** no topo da página. As issues da unidade ficam fechadas sozinhas.

**f)** No Trello, move o card da story A10 para **Ready**.

### Passo 23 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
git branch -d feature/2.5-desativar-marketeer
python ../ctesp-ADC/verificar.py 2.5
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `git branch -d feature/2.5-desativar-marketeer` | Apaga a cópia do ramo que criaste para experimentar |
| `python ../ctesp-ADC/verificar.py 2.5` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 2.5 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 2.5.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 24 — Avisa o grupo

Diz a Tomas que o pull request está junto e que já pode arrumar o computador (passo 34 da [página de Tomas](tomas.md)).

Diz também a Tomas que já pode avançar ([página de Tomas](tomas.md), passos 35 a 43).

---

## Rever a release v0.2.0 e juntá-la ao main

Quem fez: Tomas. Tu confirmas que a versão está pronta e juntas o ramo da release ao `main`.

### Passo 25 — Abre o pull request de Tomas

Faz este passo quando Tomas te avisar que o pull request da unidade 2.6 está pronto.

Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Release v0.2.0**.

### Passo 26 — Lê as alterações

Clica no separador **Files changed**. A verde estão as linhas acrescentadas e a vermelho as retiradas.

Não precisas de perceber todas as linhas. Percorre os ficheiros e confirma que correspondem ao que a descrição do pull request diz. Se tiveres uma dúvida sobre uma linha, passa o rato por cima do número da linha, clica no `+` azul e escreve a pergunta.

### Passo 27 — Experimenta no teu computador

No terminal, dentro da pasta `ADC-TrabGrupo`, atualiza a pasta de trabalho e traz o ramo de Tomas:

```bash
git -C ../ctesp-ADC pull
git fetch origin
git switch release/v0.2.0
```

| Comando | O que faz |
|---|---|
| `git -C ../ctesp-ADC pull` | Atualiza a pasta do repositório de trabalho. Sem isto, o `verificar.py` não conhece as unidades desta fase |
| `git fetch origin` | Vai ver o que há de novo no GitHub, incluindo o ramo de Tomas. Não mexe nos teus ficheiros |
| `git switch release/v0.2.0` | Cria no teu computador uma cópia desse ramo e muda para ela |

**Deves ver** `Switched to a new branch 'release/v0.2.0'`.

Agora experimenta:

Corre os testes e gera a documentação:

```bash
python -m pytest
```

**Deves ver** `194 passed`.

```bash
python -m sphinx -W -b html docs docs/_build/html
```

**Deves ver**, no fim, `build succeeded.`

Arranca a aplicação:

```bash
python -m gestor_campanhas
```

**Deves ver** o título `Gestor de Campanhas v0.2.0`. Sai com `0`.

Confirma também:

- No separador **Files changed** do pull request aparecem só três ficheiros: `gestor_campanhas/__init__.py`, `CHANGELOG.md` e `README.md`.
- O `CHANGELOG.md` tem a secção `v0.2.0` por cima da `v0.1.0`.

### Passo 28 — Aprova

**a)** Na página do pull request, separador **Files changed**, clica no botão verde **Review changes** (em alguns ecrãs chama-se *Submit review*).

**b)** Escreve o que verificaste, pelas tuas palavras. Por exemplo: que correste a aplicação, o que experimentaste e o que viste.

**c)** Escolhe **Approve** e clica em **Submit review**.

Se encontraste um problema, escolhe **Request changes** em vez de **Approve**, descreve o problema e avisa Tomas. Não avances para o passo seguinte.

### Passo 29 — Confirma que o pull request vai para o main

Este é o único pull request da fase que não vai para o `develop`. Se for junto ao ramo errado, o `main` fica sem a versão e a tag fica no sítio errado.

Por baixo do título do pull request tem de estar escrito `... wants to merge 3 commits into main from release/v0.2.0`.

Se disser `into develop`, **não juntes**. Avisa Tomas, que corrige o destino no botão **Edit**, à direita do título. Depois de corrigido, atualiza a página e confirma outra vez.

### Passo 30 — Junta o pull request ao main (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** Clica em **Delete branch**. O ramo já não é preciso: os commits ficaram no `main`.

**Deves ver** o símbolo roxo **Merged** no topo da página.

### Passo 31 — Arruma o teu computador

```bash
git switch develop
git branch -D release/v0.2.0
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git branch -D release/v0.2.0` | Apaga a cópia do ramo que criaste para experimentar. O `-D` maiúsculo é preciso porque o `develop` ainda não tem estes commits: chegam lá no pull request seguinte |

### Passo 32 — Avisa Tomas

Diz a Tomas que a release v0.2.0 já está no `main`. A partir daqui é a vez de Tomas: [página de Tomas](tomas.md), passos 44 a 48.

---

## Juntar a release v0.2.0 ao develop

É o último pull request da fase.

### Passo 33 — Aprova o pull request que leva a release para o develop

Faz este passo quando Tomas te avisar.

**a)** Abre https://github.com/Blive77/ADC-TrabGrupo/pulls e clica em **Juntar a release v0.2.0 ao develop**.

**b)** No separador **Files changed**, confirma que as alterações são as da release: o número da versão, o `CHANGELOG.md` e o `README.md`.

**c)** Clica em **Review changes**, escolhe **Approve** e clica em **Submit review**.

### Passo 34 — Junta o pull request ao develop (merge)

**a)** Volta ao separador **Conversation** e desce até ao fundo da página.

**b)** Confirma que as verificações automáticas têm um visto verde.

**c)** O botão verde tem de dizer **Merge pull request**. Se disser *Squash and merge* ou *Rebase and merge*, clica na seta ao lado e escolhe **Create a merge commit**.

**d)** Clica em **Merge pull request** e depois em **Confirm merge**.

**e)** **Não cliques em Delete branch.** O ramo deste pull request é o `main`, que tem de continuar a existir.

**Deves ver** o símbolo roxo **Merged** no topo da página. A issue da release fica fechada sozinha.

### Passo 35 — Atualiza o teu computador e confirma o resultado

```bash
git switch develop
git pull
python ../ctesp-ADC/verificar.py 2.6
```

| Comando | O que faz |
|---|---|
| `git switch develop` | Volta ao ramo `develop` |
| `git pull` | Traz do GitHub o `develop` com o pull request já junto |
| `python ../ctesp-ADC/verificar.py 2.6` | Confirma que o `develop` do repositório oficial ficou igual ao original no fim da unidade 2.6 |

**Deves ver** `Tudo certo: o ramo 'develop' está igual ao original no fim da unidade 2.6.`

Se aparecer `ERRO`, não avancem. Copia a mensagem e passa-a a Fabio, para a enviar ao Claude.

### Passo 36 — Avisa o grupo

Diz a Tomas que a release está no `develop` e que já pode arrumar o computador (passo 48 da [página de Tomas](tomas.md)).

Esta era a última vez da fase. Falta o fecho, descrito na [página da fase](README.md).

---

## Outras tarefas desta fase

### Passo 37 — Atualiza a página "Guia de utilização" da wiki

A página passa a explicar as opções "Clientes" e "Marketeers" do Administrador e a ter as seis contas de demonstração.

Faz este passo depois de a unidade 2.5 estar junta ao `develop`, para a wiki não falar de coisas que ainda não existem.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Guia-de-utilizacao.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki/Guia-de-utilização e clica em **Edit**, no canto superior direito. Se o endereço não abrir a página, abre https://github.com/Blive77/ADC-TrabGrupo/wiki e clica em **Guia de utilização** na lista de páginas, à direita.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Atualizar o Guia de utilização para a versão 0.2.0` e clica em **Save page**.

**Deves ver** a página com as secções novas `Clientes` e `Marketeers`, e a tabela das contas de demonstração com seis linhas.

### Passo 38 — Atualiza a página "Registo das fases" da wiki

A página ganha a secção da Fase 2: quem fez e quem reviu cada unidade, as decisões tomadas e o que correu mal na release da Fase 1.

Faz este passo no fim da fase, depois de a release v0.2.0 estar publicada.

**a)** Abre https://github.com/cabritaXgamer/ctesp-ADC/blob/guias/wiki/Registo-das-fases.md e clica no botão de copiar no canto superior direito do ficheiro (*Copy raw file*).

**b)** Abre https://github.com/Blive77/ADC-TrabGrupo/wiki, clica em **Registo das fases** na lista de páginas, à direita, e depois em **Edit**.

**c)** Na caixa de texto, apaga tudo (Ctrl+A e Delete) e cola o que copiaste.

**d)** Em **Edit message**, escreve `Registar a Fase 2` e clica em **Save page**.

**Deves ver** a secção `Fase 2 — Clientes e marketeers`, com a tabela das seis unidades.

---

## O código que gravaste, explicado

Os commits ficam em teu nome, por isso convém saberes explicar o que está neles. Lê com os ficheiros abertos ao lado.

### Unidade 2.3 — Desativar e reativar clientes

- **Porque é que a conta não é apagada.** A user story diz "remover", mas a descrição dela pede que o histórico se mantenha. Se a linha fosse apagada da tabela `utilizadores`, as sessões desse cliente (e, mais tarde, as campanhas) ficavam a apontar para uma conta que já não existe. Por isso "remover" significa desativar: a coluna `ativo` passa a `0`.
- **`gestor_campanhas/repositorios/utilizadores.py`** ganha `definir_ativo`, um `UPDATE` da coluna `ativo`. O SQLite não tem verdadeiro e falso, por isso guarda-se `1` ou `0`.
- **`gestor_campanhas/servicos/gestao.py`** ganha `definir_estado`. Tem duas regras: o perfil tem de ser um dos geridos, e o estado tem de mudar (desativar uma conta já desativada dá erro). Usa a função `obter`, da unidade anterior, para confirmar que o número é de um cliente.
- **O bloqueio da entrada já existia.** Desde a unidade 1.1 que `autenticar` recusa contas com `ativo` a falso, e a recuperação da password ignora-as. Esta unidade só acrescentou a forma de mudar o estado. O teste `test_cliente_desativado_deixa_de_poder_entrar` confirma que as duas peças funcionam juntas.
- **`gestor_campanhas/cli/gestao.py`** ganha `alterar_estado_cliente` e a opção 4 do menu. A pergunta de confirmação usa `comum.confirmar`, feita na Fase 0, que só aceita `s` ou `n`. A mesma função serve para desativar e para reativar: decide pelo estado atual da conta.
- **`tests/test_gestao.py`**: os testes do ecrã passam as respostas pela fixture `teclado`. Em `teclado("4", str(cliente.id), "s", "", "0")`, as respostas são: a opção 4, o número do cliente, a confirmação, o Enter da pausa e o `0` para voltar.
