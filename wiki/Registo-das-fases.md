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

## Fase 2 — Clientes e marketeers

Release: **v0.2.0**.

| Unidade | User stories | Quem fez | Quem reviu |
|---|---|---|---|
| 2.1 Lista de clientes com pesquisa | A04 | Fabio | Tomas |
| 2.2 Adicionar e editar clientes | A05, A06 | Tomas | Ricardo |
| 2.3 Desativar e reativar clientes | A07 | Ricardo | Fabio |
| 2.4 Adicionar e editar marketeers | A08, A09 | Fabio | Tomas |
| 2.5 Desativar e reativar marketeers | A10 | Tomas | Ricardo |
| 2.6 Release v0.2.0 | — | Tomas | Ricardo |

Resultado: 7 user stories concluídas (15 no total); 194 testes automáticos; segunda versão publicada.

Decisões tomadas nesta fase:

- **Remover é desativar.** As user stories falam em remover clientes e marketeers, mas pedem que o histórico se mantenha. A conta fica desativada, com os dados guardados, e pode ser reativada.
- **Password inicial aleatória.** Quem é adicionado recebe por email uma password gerada pela aplicação. O Administrador não a vê.
- **Os mesmos ecrãs para os dois perfis.** A gestão de marketeers reutiliza os ecrãs da gestão de clientes, que passaram a receber o perfil.
- **Pesquisa e ordenação sem acentos.** A pesquisa por nome e a ordem alfabética são feitas em Python, porque o SQLite põe as letras com acento depois do "z".
- **Duas partes adiadas para a Fase 3.** O número de campanhas ativas por cliente (A04) e a reatribuição das campanhas antes de desativar um marketeer (A10) dependem das campanhas, que ainda não existem.

O que correu mal e como se resolveu:

- **Release da Fase 1 junta ao ramo errado.** O pull request da release v0.1.0 foi junto ao `develop` em vez do `main`, e a tag ficou num commit sem código. Corrigiu-se com um pull request do `develop` para o `main` e refazendo a tag. O guia de trabalho passou a ter dois passos de confirmação do destino.

## Fases seguintes

| Fase | Tema | User stories | Release |
|---|---|---|---|
| 3 | Campanhas e pedidos de campanha | 12 | v0.3.0 |
| 4 | Criativos | 15 | v0.4.0 |
| 5 | Budget | 6 | v0.5.0 |
| 6 | Comentários, notificações, monitorização e relatórios | 9 | v0.6.0 |
| 7 | Fecho e entrega | — | v1.0.0 |
