# Guia de utilização

Como usar a aplicação, na versão 0.2.0.

## Arrancar

```bash
python -m gestor_campanhas
```

```
============================================================
Gestor de Campanhas v0.2.0
============================================================
  1. Entrar
  2. Recuperar a password
  0. Sair
Opção:
```

Em todos os menus escreve-se o número da opção e prime-se Enter.

## Contas de demonstração

Uma instalação nova não tem contas. Para criar as contas de demonstração:

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

## Entrar e sair

A opção **Entrar** pede o email e a password. A password não aparece no ecrã enquanto é escrita (exceto no terminal Git Bash). Com as credenciais certas abre-se o menu do perfil; a opção **0. Terminar sessão** volta ao menu inicial.

Ao fim de 15 minutos sem atividade, a sessão termina sozinha e é preciso entrar de novo.

## O que cada perfil pode fazer

| Opção | Administrador | Marketeer | Cliente |
|---|---|---|---|
| Clientes | Sim | | |
| Marketeers | Sim | | |
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

Os emails são simulados: cada mensagem é um ficheiro de texto na pasta `dados/caixa_saida`. Para ver o código de recuperação ou as credenciais de uma conta nova, abre-se o ficheiro mais recente dessa pasta.
