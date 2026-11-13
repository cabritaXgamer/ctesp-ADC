# Registo de alterações

Todas as alterações relevantes da aplicação, por versão. Cada versão corresponde a uma fase do projeto.

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
