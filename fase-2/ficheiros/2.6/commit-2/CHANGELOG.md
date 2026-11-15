# Registo de alterações

Todas as alterações relevantes da aplicação, por versão. Cada versão corresponde a uma fase do projeto.

## v0.2.0 — Clientes e marketeers (2026-11-16)

### Acrescentado

- Lista de clientes no menu do Administrador, por ordem alfabética, com pesquisa por nome que não distingue maiúsculas nem acentos.
- Adicionar clientes: a conta é criada com uma password aleatória e as credenciais são enviadas por email.
- Editar os dados de um cliente: nome, email, telefone, empresa e NIF.
- Desativar e reativar clientes, com pedido de confirmação. A conta desativada deixa de poder entrar, mas os dados mantêm-se.
- Lista de marketeers, com as mesmas opções: pesquisar, adicionar, editar, desativar e reativar.
- Aviso por email a quem tem a conta desativada ou reativada.
- Mais contas de demonstração: três clientes e dois marketeers.

### Alterado

- As regras de validação do nome, do email, do telefone e do NIF passaram para um módulo próprio, usado tanto pelo próprio utilizador como pelo Administrador.
- O menu do Administrador passa a começar pelas opções "Clientes" e "Marketeers".

### User stories concluídas

A04, A05, A06, A07, A08, A09 e A10.

O número de campanhas ativas na lista de clientes (A04) e a reatribuição das campanhas antes de desativar um marketeer (A10) entram na versão 0.3.0, com as campanhas.

## v0.1.0 — Autenticação e sessões (2026-11-14)

### Acrescentado

- Entrada na aplicação com email e password, para os três perfis: Administrador, Marketeer e Cliente.
- Menu próprio de cada perfil, com a opção de terminar a sessão.
- Passwords guardadas com hash e salt (PBKDF2), nunca em texto.
- Registo de todas as entradas e saídas, com data, hora e motivo da saída.
- Saída automática ao fim de 15 minutos sem atividade.
- Consulta, pelo Administrador, dos horários de entrada e saída dos marketeers, com filtro por datas.
- Edição dos próprios dados (nome, telefone e, nos clientes, empresa e NIF).
- Alteração da própria password.
- Recuperação da password com um código enviado por email, válido durante 15 minutos.
- Envio de emails simulado: cada mensagem é um ficheiro de texto na pasta `dados/caixa_saida`.
- Contas de demonstração, criadas com `python -m gestor_campanhas.dados_demo`.

### User stories concluídas

A01, A02, A03, M01, C01, C02, C03 e C04.

## v0.0.0 — Arranque

### Acrescentado

- Estrutura do projeto e ponto de entrada (`python -m gestor_campanhas`).
- Base de dados SQLite criada no arranque e menu inicial.
- Testes automáticos com o pytest e integração contínua no GitHub Actions.
- Documentação do código com o Sphinx, README e guia de contribuição.
