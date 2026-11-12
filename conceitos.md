# O que é o quê

Leitura de cinco minutos. Explica as palavras que aparecem nos guias, pela ordem em que vão ser precisas.

## Os dois repositórios

Um **repositório** é uma pasta de projeto que guarda, além dos ficheiros, o histórico de todas as alterações. O GitHub guarda uma cópia na internet; cada pessoa tem outra cópia no seu computador.

Neste trabalho há dois:

| | Repositório de trabalho | Repositório oficial |
|---|---|---|
| Para que serve | É onde o código de cada fase é preparado | É o que é entregue e avaliado |
| Quem escreve lá | Claude | Vocês os três |
| Nome nos comandos | `trabalho` | `origin` |

Nos comandos, `origin` e `trabalho` são os nomes dados a esses dois endereços. Chama-se a cada um **remote**.

## Palavras do Git

| Palavra | O que é |
|---|---|
| **Clone** | A cópia de um repositório no teu computador. Faz-se uma vez, com `git clone` |
| **Commit** | Uma fotografia das alterações, gravada no histórico com o teu nome, a data e uma mensagem. É a unidade de trabalho no Git |
| **Ramo** (*branch*) | Uma linha de trabalho separada. Num ramo podes fazer commits sem mexer no trabalho dos outros. Quando está pronto, junta-se ao ramo principal |
| **`main`** | O ramo das versões entregues |
| **`develop`** | O ramo onde se vai juntando o trabalho em curso |
| **Ramo `feature/...`** | Um ramo para um bocado de trabalho. Dura pouco: cria-se, recebe os commits, junta-se ao `develop` e apaga-se |
| **Push** | Enviar os teus commits do computador para o GitHub |
| **Pull** | Trazer para o teu computador os commits novos que estão no GitHub |
| **Fetch** | Ir ver o que há de novo num repositório, sem alterar os teus ficheiros |
| **Cherry-pick** | Copiar um commit de outro sítio para o ramo onde estás. É assim que o trabalho passa do repositório de trabalho para o oficial |
| **Merge** | Juntar um ramo a outro. Fica registado no histórico como um commit de merge |
| **Tag** | Uma etiqueta num commit, usada para marcar versões (`v0.1.0`) |

## Palavras do GitHub

| Palavra | O que é |
|---|---|
| **Issue** | Um registo de algo a fazer: uma funcionalidade, uma tarefa, um erro. Tem número (`#12`), responsável, etiquetas e estado (aberta ou fechada) |
| **Label** | Etiqueta de uma issue: `user story`, `tarefa`, `bug`, e o perfil (`Administrador`, `Marketeer`, `Cliente`) |
| **Milestone** | Um grupo de issues com data limite. Aqui, cada fase é uma milestone |
| **Pull request** (PR) | O pedido para juntar um ramo a outro. Mostra as alterações, permite comentar e fica à espera de aprovação |
| **Review** | A revisão de um pull request por outra pessoa, que no fim aprova ou pede correções |
| **Verificações** (*checks*) | Testes que o GitHub corre sozinho em cada pull request. Visto verde: passou. Cruz vermelha: falhou |
| **Wiki** | Páginas de documentação do repositório, editadas no próprio GitHub |
| **Release** | Uma versão publicada, associada a uma tag |

## O ciclo de um bocado de trabalho

Cada fase está dividida em **unidades**. Uma unidade é um bocado de trabalho com princípio e fim, feito por uma pessoa e revisto por outra.

```
quem faz                                       quem revê
────────                                       ─────────
1. cria a issue
2. cria um ramo a partir do develop
3. copia os commits para esse ramo
4. experimenta
5. envia o ramo para o GitHub (push)
6. abre o pull request
7. avisa  ─────────────────────────────────►   8. lê as alterações
                                               9. experimenta no seu computador
                                               10. aprova
                                               11. junta ao develop (merge)
12. atualiza o seu computador  ◄────────────   avisa
```

Só depois de uma unidade estar junta ao `develop` é que a seguinte começa, porque cada uma assenta na anterior.

## O que o professor vê

No repositório oficial fica registado, com nome e data:

- quem fez cada **commit**;
- quem abriu cada **issue** e cada **pull request**;
- quem **reviu** e quem **juntou** cada pull request;
- os **ramos** e os **merges**, no gráfico do histórico;
- quem editou cada página da **wiki**.

É por isso que cada pessoa faz os seus próprios passos, com a sua conta.
