# Modelo de dados

Como os dados estão guardados. A base de dados é SQLite, num único ficheiro (`dados/app.db`), e as tabelas são criadas no primeiro arranque a partir da constante `ESQUEMA` de `gestor_campanhas/bd.py`.

## Relações

O centro do modelo é a campanha: pertence a um cliente, tem um marketeer responsável e reúne os criativos, os pedidos de budget e o histórico do budget. `1 ---< N` lê-se "um para muitos".

```
cliente    1 ---< N  pedidos_campanha  1 ---  0..1  campanhas
cliente    1 ---< N  campanhas
marketeer  1 ---< N  campanhas

campanhas  1 ---< N  criativos          1 ---< N  comentarios
campanhas  1 ---< N  pedidos_budget     1 ---  0..1  alteracoes_budget
campanhas  1 ---< N  alteracoes_budget
```

O cliente, o marketeer e o Administrador são linhas da mesma tabela, `utilizadores`, distinguidas pela coluna `perfil`.

## Tabelas

| Tabela | Uma linha por | Colunas principais |
|---|---|---|
| `utilizadores` | Conta | `nome`, `email` (único), `password_hash`, `perfil`, `ativo`, `telefone`, `empresa`, `nif` |
| `sessoes` | Entrada na aplicação | `utilizador_id`, `entrada`, `saida`, `motivo_saida` (`logout` ou `inatividade`) |
| `recuperacoes` | Pedido de recuperação da password | `utilizador_id`, `codigo_hash`, `expira_em`, `usado` |
| `campanhas` | Campanha | `nome`, `objetivo`, `cliente_id`, `marketeer_id`, `budget_centimos`, `data_inicio`, `data_fim` |
| `pedidos_campanha` | Pedido de nova campanha | `cliente_id`, `objetivo`, `orcamento_centimos`, `prazo`, `plataformas`, `estado`, `motivo_rejeicao`, `campanha_id` |
| `criativos` | Criativo | `campanha_id`, `nome`, `descricao`, `custo_centimos`, `prazo`, `publico_alvo`, `plataforma`, `estado`, `motivo_rejeicao`, `ficheiro` |
| `pedidos_budget` | Pedido de alteração de budget | `campanha_id`, `budget_atual_centimos`, `budget_pedido_centimos`, `motivo`, `estado`, `parecer_viavel`, `parecer_justificacao`, `motivo_rejeicao`, `decidido_em` |
| `alteracoes_budget` | Alteração do budget (o histórico) | `campanha_id`, `budget_anterior_centimos`, `budget_novo_centimos`, `motivo`, `pedido_budget_id`, `alterado_em` |
| `comentarios` | Comentário ou resposta | `criativo_id`, `autor_id`, `texto`, `resposta_a` |
| `notificacoes` | Notificação | `utilizador_id`, `texto`, `sobre` (`campanha`, `pedido_budget` ou `criativo`), `item_id`, `lida` |
| `atividades` | Alteração feita por um marketeer | `utilizador_id`, `descricao`, `registada_em` |
| `configuracoes` | Definição | `chave`, `valor` |

Todas as tabelas, exceto `configuracoes`, têm a coluna `id`, o número que aparece nos menus ("Criativo n.º 3"), e quase todas guardam a data em que a linha foi criada.

## Estados

| Tabela | Estados |
|---|---|
| `pedidos_campanha` e `pedidos_budget` | `pendente`, `em_analise`, `aprovado`, `rejeitado`, `cancelado` |
| `criativos` | `em_preparacao`, `em_revisao`, `aprovado`, `rejeitado`, `publicado` |

O próprio SQLite recusa um estado fora da lista (`CHECK`). Os nomes com acentos que aparecem nos menus ("Em análise") estão em `gestor_campanhas/modelos.py`.

## Como os valores são guardados

| Valor | Como fica |
|---|---|
| Dinheiro | Em cêntimos, num número inteiro: `150050` são 1500,50 €. As colunas acabam em `_centimos` |
| Datas | Texto `AAAA-MM-DD` |
| Datas e horas | Texto `AAAA-MM-DD HH:MM:SS` |
| Sim ou não | `1` ou `0` |
| Plataformas de um pedido | Um só texto, separadas por vírgula |
| Passwords e códigos de recuperação | Só o hash, nunca o valor |
| Ficheiros dos criativos | Só o nome; o ficheiro fica em `dados/ficheiros/<n.º do criativo>/` |

## O que acontece quando se apaga

| Quando se apaga | Acontece |
|---|---|
| Uma campanha com criativos | Não se pode: o SQLite recusa, e a aplicação explica que é preciso eliminar os criativos primeiro |
| Uma campanha sem criativos | Os pedidos de budget e o histórico do budget dela são apagados com ela (`ON DELETE CASCADE`); o pedido de campanha que lhe deu origem fica, sem a ligação (`ON DELETE SET NULL`) |
| Um criativo | Os comentários dele são apagados com ele (`ON DELETE CASCADE`), e a pasta do ficheiro também |
| Uma conta | Não acontece: as contas são desativadas, nunca apagadas |

## Tabelas novas numa base de dados antiga

O `CREATE TABLE IF NOT EXISTS` cria as tabelas que faltam, mas não acrescenta colunas a uma tabela que já existe. Por isso cada tabela foi criada logo com todas as colunas, mesmo as que só passaram a ser usadas numa fase seguinte. Quem atualizou a aplicação de uma versão para a outra continuou com a mesma base de dados, sem perder nada.
