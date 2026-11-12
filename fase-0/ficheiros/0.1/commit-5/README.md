# ADC-TrabGrupo

## Introdução

Projeto desenvolvido em grupo na Universidade do Algarve (UAlg), no âmbito da unidade curricular **Ambiente de Desenvolvimento Corporativo** do CTESP - Sistemas e Técnologias de informação. O objetivo é criar uma aplicação de linha de comandos para gerir campanhas de marketing, usando Python e práticas de trabalho colaborativo.

### Como trabalhamos

- **Issues:** registam as tarefas e user stories, organizadas por etiquetas e fases.
- **Ramos:** cada tarefa é desenvolvida num ramo próprio, criado a partir de `develop`.
- **Pull requests:** permitem rever o código antes de o integrar.
- **GitHub Actions:** executa os testes e verifica a documentação.
- **Releases e tags:** assinalam as versões concluídas no fim de cada fase.
- **Trello:** acompanha o estado das tarefas.


### Mensagens dos commits

As mensagens dos commits começam com um tipo que resume a alteração, seguido de dois-pontos e uma descrição curta. Por exemplo:

- `feat`: acrescenta uma funcionalidade.
- `fix`: corrige um erro.
- `docs`: altera a documentação.
- `chore`: faz uma tarefa de manutenção ou configuração.

Usamos `chore` no commit dos ficheiros `.gitignore` e `.gitattributes` porque são configurações do Git e não alteram o comportamento da aplicação.

Exemplo: `chore: adicionar .gitignore e .gitattributes`



### Para que serve o `pyproject.toml`?

O ficheiro `pyproject.toml` não é necessário para executar a aplicação com `python -m gestor_campanhas` a partir da pasta do projeto. Decidimos incluí-lo para descrever o pacote Python e facilitar a sua instalação e configuração com ferramentas padrão.

Nele definimos, por exemplo, os metadados do projeto, a versão mínima do Python e como obter a versão da aplicação. Também configuramos o comando `gestor-campanhas`, que fica disponível depois de instalar o pacote.