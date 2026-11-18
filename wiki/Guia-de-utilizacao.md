# Guia de utilização

Como usar a aplicação, na versão 0.5.0.

## Arrancar

```bash
python -m gestor_campanhas
```

```
============================================================
Gestor de Campanhas v0.4.0
============================================================
  1. Entrar
  2. Recuperar a password
  0. Sair
Opção:
```

Em todos os menus escreve-se o número da opção e prime-se Enter.

## Contas de demonstração

Uma instalação nova não tem contas. Para criar as contas, as campanhas, os pedidos, os criativos e o pedido de budget de demonstração:

```bash
python -m gestor_campanhas.dados_demo
```

| Perfil | Email | Password |
|---|---|---|
| Administrador | `admin@agencia.pt` | `admin12345` |
| Marketeer | `marketeer@agencia.pt` | `marketeer12345` |
| Marketeer | `marta@agencia.pt` | `marta12345` |
| Cliente | `cliente@empresa.pt` | `cliente12345` |
| Cliente | `jose@padaria.pt` | `jose12345` |
| Cliente | `beatriz@bicicletas.pt` | `beatriz12345` |

Estas passwords são públicas e servem só para demonstração.

O mesmo comando cria três campanhas (`Natal 2026`, `Regresso às aulas` e `Bicicletas de primavera`), dois pedidos de campanha pendentes, quatro criativos (três nas campanhas do Miguel e um na da Marta) e um pedido de alteração de budget pendente, da Carla, para a campanha `Natal 2026` passar de 1500 € para 2000 €. Pode ser repetido: só acrescenta o que faltar.

## Entrar e sair

A opção **Entrar** pede o email e a password. A password não aparece no ecrã enquanto é escrita (exceto no terminal Git Bash). Com as credenciais certas abre-se o menu do perfil; a opção **0. Terminar sessão** volta ao menu inicial.

Ao fim de 15 minutos sem atividade, a sessão termina sozinha e é preciso entrar de novo.

## O que cada perfil pode fazer

| Opção | Administrador | Marketeer | Cliente |
|---|---|---|---|
| Clientes | Sim | | |
| Marketeers | Sim | | |
| Pedidos de campanha | Decide os pedidos de todos os clientes | | Faz pedidos de campanha e de alteração de budget, acompanha-os e cancela os pendentes |
| Pedidos de budget | Aprova ou rejeita os pedidos de alteração de budget que já têm parecer | Dá parecer sobre os pedidos das suas campanhas | |
| Campanhas | Vê todas, define o budget, atribui o marketeer e vê o histórico do budget | Cria, edita, consulta e elimina as suas | Vê as suas, o budget, a despesa, o marketeer responsável e o histórico do budget |
| Resumo do budget | Budget atribuído face à despesa, por cliente e por campanha | | |
| Criativos | | Cria, edita, consulta e elimina os das suas campanhas, muda o estado e anexa o ficheiro | Vê os das suas campanhas, procura-os, aprova-os ou rejeita-os e descarrega os ficheiros |
| Horários de entrada e saída dos marketeers | Sim | | |
| Editar os meus dados | Sim | Sim | Sim |
| Alterar a password | Sim | Sim | Sim |

### Clientes

Mostra a lista de todos os clientes, por ordem alfabética do nome, e por baixo as opções de gestão. Depois de cada opção, a lista volta a aparecer, já atualizada.

```
N.º  Nome           Empresa                  Email                  Telefone   Estado
---  -------------  -----------------------  ---------------------  ---------  ------
5    Beatriz Lopes  Bicicletas do Sul, Lda.  beatriz@bicicletas.pt  910000005  Ativa
3    Carla Cliente  Empresa Exemplo, Lda.    cliente@empresa.pt     910000003  Ativa
4    José Padeiro   Padaria Central, Lda.    jose@padaria.pt        910000004  Ativa

3 clientes.
```

| Opção | O que faz |
|---|---|
| Pesquisar por nome | Mostra só os clientes cujo nome contém o texto escrito. Não distingue maiúsculas nem acentos: `jose` encontra `José Padeiro`. Com Enter, voltam a aparecer todos |
| Adicionar cliente | Pede o nome e o email (obrigatórios) e o telefone, a empresa e o NIF (opcionais). A conta começa com uma password aleatória, enviada por email ao cliente |
| Editar cliente | Pede o número do cliente (primeira coluna da lista) e mostra cada dado com o valor atual. Com Enter, o valor mantém-se |
| Desativar ou reativar cliente | Pede o número do cliente e uma confirmação. Uma conta desativada deixa de poder entrar, mas não é apagada e pode ser reativada. O cliente é avisado por email |

Regras dos dados: o email tem a forma `nome@empresa.pt` e não pode repetir o de outra conta; o telefone tem 9 a 15 algarismos; o NIF tem 9 algarismos.

### Marketeers

Funciona como a opção Clientes, com as mesmas quatro opções de gestão. Um marketeer não tem empresa nem NIF, por isso esses dados não são pedidos nem aparecem na lista.

As duas listas têm a coluna **Campanhas ativas**: o número de campanhas de cada conta que ainda não terminaram. Um marketeer com campanhas ativas não pode ser desativado: primeiro o Administrador atribui cada uma a outro marketeer, na opção Campanhas.

### Como nasce uma campanha

Uma campanha pertence a um cliente e tem um marketeer responsável. Nasce de duas maneiras:

1. O **Marketeer** cria-a na sua opção Campanhas. Fica responsável por ela, e a campanha começa sem budget.
2. O **Cliente** faz um pedido de campanha. O **Administrador** analisa-o e, se o aprovar, a campanha é criada com o budget inicial e o marketeer que escolher.

O budget é sempre definido pelo Administrador. Para o mudar, o cliente faz um pedido de alteração de budget (ver [Pedidos de alteração de budget](#pedidos-de-alteração-de-budget)).

### Campanhas (Marketeer)

Mostra as campanhas de que o marketeer é responsável, com o cliente, as datas, o budget, o estado, a despesa e o que resta do budget.

```
N.º  Nome               Cliente        Início      Fim         Budget      Estado       Despesa     Restante
---  -----------------  -------------  ----------  ----------  ----------  -----------  ----------  --------
1    Natal 2026         Carla Cliente  2026-12-01  2026-12-24  1 500,00 €  Por começar  1 300,00 €  200,00 €
2    Regresso às aulas  José Padeiro   2026-09-01  2026-09-30  800,00 €    Terminada    300,00 €    500,00 €
```

| Opção | O que faz |
|---|---|
| Criar campanha | Mostra os clientes ativos e pede o cliente, o nome, o objetivo e as datas de início e de fim. Só o cliente e o nome são obrigatórios |
| Editar campanha | Altera o nome, o objetivo e as datas. Com Enter, o valor mantém-se; com `-`, a data é apagada |
| Ver campanha | Mostra todos os dados da campanha, incluindo o objetivo, a despesa, o restante e quantos criativos há em cada estado |
| Eliminar campanha | Pede confirmação. Uma campanha eliminada não pode ser recuperada. Só se elimina uma campanha sem criativos |

O estado é calculado a partir das datas: `Por começar` antes da data de início, `Terminada` depois da data de fim e `Em curso` nos outros casos. O budget aparece como `Por definir` enquanto o Administrador não o atribuir.

A **despesa** é a soma do custo estimado dos criativos da campanha, seja qual for o estado deles. O **restante** é o budget menos a despesa: fica negativo (por exemplo `-200,00 €`) quando a despesa passa o budget.

### Pedidos de campanha (Cliente)

Mostra os pedidos do cliente em duas listas, cada uma do mais recente para o mais antigo: primeiro os pedidos de nova campanha, depois os pedidos de alteração de budget. Os dois tipos têm numerações próprias, por isso cada um tem as suas opções.

| Opção | O que faz |
|---|---|
| Novo pedido de campanha | Pede o objetivo, o orçamento em euros, o prazo pretendido (`AAAA-MM-DD`) e as plataformas, escolhidas por número numa lista |
| Ver pedido de campanha | Mostra todos os dados do pedido. Num pedido rejeitado mostra o motivo; num aprovado, o número da campanha criada |
| Cancelar pedido de campanha | Só para pedidos pendentes, com confirmação. O pedido fica na lista, com o estado `Cancelado` |
| Pedir alteração de budget | Mostra as campanhas que ainda não terminaram e pede a campanha, o budget pretendido e o motivo |
| Ver pedido de budget | Mostra todos os dados do pedido de budget. Num pedido rejeitado mostra o motivo da rejeição |
| Cancelar pedido de budget | Só para pedidos pendentes, com confirmação |

| Estado | Significado |
|---|---|
| Pendente | Ainda ninguém analisou o pedido |
| Em análise | O Administrador já abriu o pedido, mas ainda não decidiu |
| Aprovado | O pedido foi aceite e deu origem a uma campanha |
| Rejeitado | O pedido foi recusado, com um motivo |
| Cancelado | O cliente desistiu do pedido |

### Pedidos de campanha (Administrador)

Mostra os pedidos de todos os clientes, com os que estão por decidir em primeiro lugar. A opção **Analisar pedido** mostra o pedido, passa-o a `Em análise` e pergunta a decisão:

| Decisão | O que acontece |
|---|---|
| Aprovar e criar a campanha | Pede o nome da campanha, o budget inicial (o valor proposto é o orçamento do pedido) e o marketeer responsável. A campanha fica com o objetivo do pedido e com o prazo como data de fim. O cliente e o marketeer são avisados por email |
| Rejeitar | Pede o motivo, que é obrigatório, e uma confirmação. O cliente é avisado por email |
| Decidir mais tarde | O pedido fica `Em análise` |

### Pedidos de alteração de budget

Um pedido de alteração de budget passa por três pessoas:

```
Cliente pede --> Marketeer dá parecer --> Administrador aprova ou rejeita
   Pendente         Em análise               Aprovado / Rejeitado
```

**Cliente**, na opção Pedidos de campanha: escolhe uma campanha que ainda não terminou, escreve o budget que pretende (maior do que zero e diferente do atual) e o motivo. Cada campanha só pode ter um pedido por decidir de cada vez. Enquanto o pedido está `Pendente`, o cliente pode cancelá-lo.

**Marketeer**, na opção **Pedidos de budget**: vê os pedidos das campanhas de que é responsável, com o cliente, o budget de partida (`De`), o budget pedido (`Para`), o estado e o parecer.

```
N.º  Feito em    Campanha    Cliente        De          Para        Estado    Parecer
---  ----------  ----------  -------------  ----------  ----------  --------  -------
1    2026-11-18  Natal 2026  Carla Cliente  1 500,00 €  2 000,00 €  Pendente  Por dar

1 pedido, 1 por decidir.
```

A opção **Dar parecer** mostra o pedido, com a despesa atual da campanha, e pergunta se o pedido é viável (`s`/`n`) e porquê. A justificação é obrigatória. Com o parecer, o pedido passa a `Em análise` e o cliente já não o pode cancelar. Até o Administrador decidir, o marketeer pode dar outro parecer, que substitui o anterior.

**Administrador**, na opção **Pedidos de budget**: vê os pedidos de todas as campanhas, com o parecer. A opção **Analisar pedido** mostra o pedido, o parecer e a justificação, e o budget e a despesa atuais da campanha. Só se decide um pedido que já tenha parecer:

| Decisão | O que acontece |
|---|---|
| Aprovar e passar o budget para ... | O budget da campanha passa logo a ser o valor pedido, e a alteração fica no histórico do budget. Um parecer `Não viável` não impede aprovar |
| Rejeitar | Pede o motivo, que é obrigatório, e uma confirmação. O budget fica como estava |
| Decidir mais tarde | O pedido fica `Em análise` |

### Campanhas (Administrador)

Mostra as campanhas de todos os marketeers.

| Opção | O que faz |
|---|---|
| Definir budget | Atribui ou corrige o budget de uma campanha. Tem de ser maior do que zero e diferente do atual. Quando a campanha já tem budget, pede também o motivo da alteração |
| Atribuir marketeer | Muda o marketeer responsável, escolhido entre os que têm a conta ativa. O novo responsável é avisado por email |
| Histórico do budget | Mostra todas as alterações do budget de uma campanha |

O **histórico do budget** tem uma linha por alteração, com a data, o valor anterior, o valor novo e o motivo. Fica lá tudo: o budget inicial, as alterações feitas em Definir budget e as que vêm de pedidos aprovados.

```
Data              De           Para        Motivo
----------------  -----------  ----------  -------------------------------------------------------------------------------------
2026-11-18 10:00  Por definir  1 500,00 €  Budget inicial
2026-11-18 11:30  1 500,00 €   2 000,00 €  Pedido de budget n.º 1: Reforçar os anúncios em vídeo na última semana antes do Natal
```

### Resumo do budget (Administrador)

Mostra, para cada cliente com campanhas, o budget atribuído, a despesa e o restante, com os totais por baixo:

```
N.º  Cliente        Campanhas  Budget      Despesa     Restante  Sem budget  Acima do budget
---  -------------  ---------  ----------  ----------  --------  ----------  ---------------
6    Beatriz Lopes  1          0,00 €      0,00 €      0,00 €    1           0
4    Carla Cliente  1          1 500,00 €  1 300,00 €  200,00 €  0           0
5    José Padeiro   1          800,00 €    300,00 €    500,00 €  0           0

Total: 3 campanhas, budget atribuído 2 300,00 €, despesa 1 600,00 €, restante 700,00 €.
```

O budget é a soma das campanhas que já têm budget; a despesa conta todas as campanhas. Por baixo aparecem, em destaque, as campanhas que gastaram mais do que o budget. A opção **Ver as campanhas de um cliente** mostra as campanhas de um cliente, uma por linha, com a situação de cada uma: `Dentro do budget`, `Acima do budget` ou `Sem budget`.

### Campanhas (Cliente)

Mostra as campanhas do cliente, com as datas, o budget, o estado, o marketeer responsável, a despesa e o restante. A opção **Ver campanha e marketeer responsável** mostra todos os dados de uma campanha, a parte do budget já gasta (por exemplo `Gasto:     86% do budget`) e o nome, o email e o telefone do marketeer. A opção **Histórico do budget** mostra as alterações do budget de uma campanha, como no menu do Administrador.

### Criativos (Marketeer)

Um criativo é uma peça de uma campanha: uma imagem, um vídeo ou um texto a publicar. A opção **Criativos** mostra as campanhas do marketeer e pede o número de uma. Depois, mostra os criativos dessa campanha:

```
N.º  Nome             Custo     Prazo       Público-alvo               Plataforma  Estado
---  ---------------  --------  ----------  -------------------------  ----------  -------------
1    Banner de Natal  400,00 €  2026-11-25  Famílias da região de...   Facebook    Em preparação
2    Vídeo da montra  900,00 €  2026-11-28  Jovens adultos, 18 a 3...  Instagram   Em preparação

2 criativos.
Custo dos criativos: 1 300,00 €. Budget da campanha: 1 500,00 €.
```

| Opção | O que faz |
|---|---|
| Criar criativo | Pede o nome (obrigatório), a descrição, o custo estimado em euros, o prazo (`AAAA-MM-DD`), o público-alvo e a plataforma, escolhida numa lista. O criativo fica `Em preparação` |
| Editar criativo | Altera os mesmos dados. Com Enter, o valor mantém-se; com `-`, é apagado. Só para criativos em preparação ou rejeitados |
| Ver criativo | Mostra todos os dados, incluindo o público-alvo completo, o motivo da rejeição e o nome do ficheiro |
| Eliminar criativo | Pede confirmação. Um criativo publicado não pode ser eliminado |
| Atualizar estado | Mostra só os estados para onde o criativo pode passar (ver a secção seguinte) |
| Anexar ficheiro | Pede o caminho de um ficheiro do computador e copia-o para a aplicação. Substitui o ficheiro anterior, se houver |
| Pré-visualizar ficheiro | Mostra o nome, o tipo e o tamanho do ficheiro e pergunta se o deve abrir no programa predefinido |

O prazo não pode ser depois do fim da campanha. Quando o custo dos criativos passa o budget, aparece um aviso por baixo da lista, depois de criar ou editar um criativo, e em "Ver campanha":

```
Atenção: o custo dos criativos (1 700,00 €) ultrapassa o budget da campanha (1 500,00 €) em 200,00 €.
```

O criativo é guardado na mesma: o aviso serve para ajustar os custos ou pedir mais budget ao Administrador.

### Estados de um criativo

```
Em preparação --> Em revisão --> Aprovado --> Publicado
                       |
                       +-------> Rejeitado --> Em preparação ou Em revisão
```

| Estado | Significado | Quem o muda |
|---|---|---|
| Em preparação | O marketeer está a fazer o criativo | O marketeer envia-o para revisão |
| Em revisão | Está à espera da decisão do cliente | O cliente aprova ou rejeita; o marketeer pode retirá-lo para preparação |
| Aprovado | O cliente aceitou-o | O marketeer marca-o como publicado |
| Rejeitado | O cliente recusou-o, com um motivo | O marketeer põe-no em preparação ou envia-o outra vez para revisão |
| Publicado | Já saiu na plataforma | Ninguém: é o fim do caminho |

### Criativos (Cliente)

A opção **Criativos** mostra os criativos de todas as campanhas do cliente, com a campanha de cada um, e diz quantos estão à espera de aprovação.

| Opção | O que faz |
|---|---|
| Filtrar e pesquisar | Pede um texto (procurado no nome, na descrição e no público-alvo, sem distinguir acentos), uma campanha, uma plataforma e um estado. Com Enter, a pergunta não é usada |
| Ver criativo | Mostra todos os dados de um criativo |
| Aprovar ou rejeitar criativo | Só para criativos em revisão. Para rejeitar, o motivo é obrigatório |
| Pré-visualizar ficheiro | Como no menu do marketeer |
| Descarregar ficheiro | Copia o ficheiro para uma pasta à escolha (com Enter, a pasta Transferências). Nunca escreve por cima de um ficheiro que já lá esteja: a cópia fica, por exemplo, `banner-natal (1).svg` |

### Ficheiros dos criativos

Os ficheiros anexados são copiados para a pasta `dados/ficheiros`, com uma pasta por criativo. O original pode ser apagado ou mudado de sítio sem afetar a aplicação. No Windows, para escrever o caminho de um ficheiro, pode clicar nele com o botão direito, escolher "Copiar como caminho" e colar: as aspas são tiradas sozinhas.

Para experimentar, o projeto tem o ficheiro `exemplos/banner-natal.svg`.

### Horários de entrada e saída dos marketeers

Mostra as sessões dos marketeers, da mais recente para a mais antiga. Antes de mostrar a tabela, a aplicação pergunta o período: duas datas no formato `AAAA-MM-DD`, ambas opcionais.

```
Marketeer         Entrada           Saída             Duração  Motivo
----------------  ----------------  ----------------  -------  -----------------
Miguel Marketeer  2026-11-11 14:00  2026-11-11 14:15  0h15     Inatividade
Miguel Marketeer  2026-11-10 09:00  2026-11-10 12:30  3h30     Terminou a sessão
```

### Editar os meus dados

Mostra cada dado com o valor atual entre parênteses retos. Com Enter, o valor mantém-se. O email não pode ser alterado. A empresa e o NIF só são pedidos aos clientes.

### Alterar a password

Pede a password atual e a nova, duas vezes. A password nova tem de ter pelo menos 8 caracteres.

## Recuperar a password

No menu inicial, a opção **Recuperar a password** envia um código de 6 algarismos para o email da conta. Com esse código define-se uma password nova. O código vale durante 15 minutos e só pode ser usado uma vez.

## Emails

Os emails são simulados: cada mensagem é um ficheiro de texto na pasta `dados/caixa_saida`. Para ver o código de recuperação, as credenciais de uma conta nova ou o aviso de que um pedido foi decidido, abre-se o ficheiro mais recente dessa pasta.
