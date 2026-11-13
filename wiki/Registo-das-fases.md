# Registo das fases

O que foi feito em cada fase do projeto, e por quem. Cada fase corresponde a uma milestone do repositório.

## Fase 0 — Arranque

Base do projeto, ainda sem user stories.

| Unidade | Quem fez | Quem reviu |
|---|---|---|
| 0.1 Estrutura do pacote Python | Fabio | Tomas |
| 0.2 Base de dados e menu inicial | Tomas | Ricardo |
| 0.3 Testes automáticos e integração contínua | Ricardo | Fabio |
| 0.4 Documentação base | Fabio | Tomas |

Resultado: a aplicação arranca, cria a base de dados e mostra o menu inicial; 20 testes automáticos; documentação Sphinx; 57 issues criadas a partir das user stories.

## Fase 1 — Autenticação e sessões

Release: **v0.1.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 1.1 Login e logout dos três perfis | A01, M01, C01 | Tomas | Ricardo |
| 1.2 Registo de sessões e saída por inatividade | A02 | Ricardo | Fabio |
| 1.3 Horários de entrada e saída dos marketeers | A03 | Fabio | Tomas |
| 1.4 Alterar a password e editar os meus dados | C03, C04 | Tomas | Ricardo |
| 1.5 Recuperar a password | C02 | Ricardo | Fabio |
| 1.6 Release v0.1.0 | — | Fabio | Tomas |

Resultado: 8 user stories concluídas; 104 testes automáticos; primeira versão publicada.

Decisões tomadas nesta fase:

- **Código em vez de link na recuperação da password.** A user story fala num link enviado por email. Na linha de comandos não há onde clicar, por isso é enviado um código de 6 algarismos, com validade de 15 minutos.
- **Emails simulados.** A aplicação escreve cada email num ficheiro de texto, em vez de o enviar.
- **Inatividade verificada ao responder.** A aplicação fica parada à espera do teclado, por isso a inatividade é detetada quando o utilizador responde a um menu.
- **Opções da conta em todos os perfis.** As user stories de alterar a password e editar os dados são do Cliente, mas as opções ficaram disponíveis para os três perfis.

## Fases seguintes

| Fase | Tema | User stories | Release |
|---|---|---|---|
| 2 | Gestão de clientes e marketeers | 7 | v0.2.0 |
| 3 | Campanhas e pedidos de campanha | 12 | v0.3.0 |
| 4 | Criativos | 15 | v0.4.0 |
| 5 | Budget | 6 | v0.5.0 |
| 6 | Comentários, notificações, monitorização e relatórios | 9 | v0.6.0 |
| 7 | Fecho e entrega | — | v1.0.0 |
