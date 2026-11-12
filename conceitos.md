# O que é o quê

Leitura de cinco minutos. Explica as palavras que aparecem nos guias, pela ordem em que vão ser precisas.

## Os dois repositórios e as duas pastas

Um **repositório** é uma pasta de projeto que guarda, além dos ficheiros, o histórico de todas as alterações. O GitHub guarda uma cópia na internet; cada pessoa tem outra cópia no seu computador.

Neste trabalho há dois repositórios, e cada pessoa tem uma pasta para cada um:

| | Repositório oficial | Repositório de trabalho |
|---|---|---|
| Pasta no teu computador | `ADC-TrabGrupo` | `ctesp-ADC` |
| Endereço | https://github.com/Blive77/ADC-TrabGrupo | https://github.com/cabritaXgamer/ctesp-ADC |
| Para que serve | É o que é entregue e avaliado | Tem os ficheiros de cada fase já preparados e estas páginas |
| Quem escreve lá | Vocês os três | Claude |
| O que fazes lá | Tudo: ramos, commits, envio para o GitHub | Nada: só lês e copias |

O trabalho passa de um para o outro por **cópia de ficheiros**: os ficheiros de cada commit são copiados da pasta `ctesp-ADC` para a pasta `ADC-TrabGrupo`, e é lá que cada pessoa os grava com o seu nome.

## Palavras do Git

| Palavra | O que é |
|---|---|
| **Clone** | A cópia de um repositório no teu computador. Faz-se uma vez, com `git clone` |
| **Commit** | Uma fotografia das alterações, gravada no histórico com o teu nome, a data e uma mensagem. É a unidade de trabalho no Git |
| **`git add`** | Escolhe as alterações que vão entrar no próximo commit. `git add -A` escolhe todas |
| **`git commit`** | Grava o commit com as alterações escolhidas |
| **Ramo** (*branch*) | Uma linha de trabalho separada. Num ramo podes fazer commits sem mexer no trabalho dos outros. Quando está pronto, junta-se ao ramo principal |
| **`main`** | O ramo das versões entregues |
| **`develop`** | O ramo onde se vai juntando o trabalho em curso |
| **Ramo `feature/...`** | Um ramo para um bocado de trabalho. Dura pouco: cria-se, recebe os commits, junta-se ao `develop` e apaga-se |
| **Push** | Enviar os teus commits do computador para o GitHub |
| **Pull** | Trazer para o teu computador os commits novos que estão no GitHub |
| **Fetch** | Ir ver o que há de novo no GitHub, sem alterar os teus ficheiros |
| **`origin`** | O nome que o Git dá ao endereço do repositório no GitHub |
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

## Os dois comandos de ajuda

Na pasta `ctesp-ADC` há dois pequenos programas. Correm-se de dentro da pasta `ADC-TrabGrupo`:

| Comando | O que faz |
|---|---|
| `python ../ctesp-ADC/copiar.py 0.1 1` | Copia para a pasta onde estás os ficheiros do commit 1 da unidade 0.1. Antes de copiar, confirma que estás na pasta certa, no ramo certo e que não saltaste nenhum commit. Não grava nada: o commit és tu que fazes |
| `python ../ctesp-ADC/verificar.py 0.1` | Confirma que o que gravaste está igual ao original no fim da unidade 0.1. Não altera nada |

O `../` quer dizer "a pasta acima". Como as duas pastas estão lado a lado, `../ctesp-ADC` é a pasta do repositório de trabalho vista de dentro da pasta do repositório oficial.

## O ciclo de um bocado de trabalho

Cada fase está dividida em **unidades**. Uma unidade é um bocado de trabalho com princípio e fim, feito por uma pessoa e revisto por outra.

```
quem faz                                       quem revê
────────                                       ─────────
1. cria a issue
2. cria um ramo a partir do develop
3. copia os ficheiros e grava os commits
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
