# Testes

Como a aplicação é testada. Na versão 1.0.0 há 987 testes automáticos, todos a passar.

## Correr os testes

Com as ferramentas de desenvolvimento instaladas (ver [Instalação e configuração](Instalação-e-configuração)), dentro da pasta do projeto:

```bash
python -m pytest
```

Deve terminar com `987 passed`. Para ver o nome de cada teste, acrescenta-se `-v`; para correr só um ficheiro, indica-se o caminho:

```bash
python -m pytest -v tests/test_fluxos.py
```

## Três tipos de testes

| Tipo | Onde | O que confirma |
|---|---|---|
| Regras de cada parte | Um ficheiro por assunto, por exemplo `tests/test_criativos.py` | Cada regra sozinha: o que é permitido, o que é recusado e com que mensagem, e o que cada menu mostra |
| Fluxos completos | `tests/test_fluxos.py` | O caminho das pessoas na aplicação, com os três perfis, de uma ponta à outra |
| Documentação | `tests/test_documentacao.py` | Que todos os módulos, classes e funções têm docstring, e que a referência do Sphinx inclui todos os módulos |

Os dados de demonstração têm também os seus testes, em `tests/test_dados_demo.py`: confirmam o resultado final numa instalação nova (os estados dos criativos, o ficheiro anexado, as notificações e a atividade) e que o comando pode ser repetido sem criar nada em duplicado.

## Fluxos completos

| Fluxo | Perfis | O que se confirma no fim |
|---|---|---|
| Da conta nova à entrada | Administrador, Cliente | A password chega por email, a pessoa entra e troca-a; a password antiga deixa de servir |
| Conta desativada e reativada | Administrador, Marketeer | Desativada não entra; reativada volta a entrar |
| Do pedido de campanha ao criativo publicado | Os três | A campanha é criada com o budget e o marketeer; o cliente recebe uma notificação e um email por cada passo do marketeer; o painel mostra o criativo concluído; o relatório tem a linha certa |
| Criativo rejeitado e corrigido | Marketeer, Cliente | Rejeitado não pode ser aprovado; corrigido e reenviado, é aprovado |
| Pedido de campanha rejeitado | Cliente, Administrador | Não é criada campanha; o cliente recebe o motivo por email |
| Pedido de budget aprovado | Os três | O budget muda, o histórico tem as duas linhas, a campanha deixa de estar acima do budget e o resumo global bate certo |
| Pedido de budget rejeitado | Os três | Sem parecer não se pode decidir; rejeitado, o budget fica igual e o cliente pode pedir outra vez |

Os passos usam as funções das regras de negócio (pasta `servicos`), pela ordem em que os menus as chamam. O relógio avança um minuto entre passos, para as notificações e os emails ficarem pela ordem certa.

## Ficheiros de testes

| Ficheiro | O que testa |
|---|---|
| `conftest.py` | Não tem testes: define as peças partilhadas (*fixtures*) |
| `test_bd.py` | Base de dados, tabelas e caminhos de dados |
| `test_cli.py` | Funções comuns dos menus, menu inicial e ponto de entrada |
| `test_validacao.py` | Validação dos dados escritos pelo utilizador |
| `test_dinheiro.py` | Conversão de valores em euros |
| `test_autenticacao.py` | Passwords, entrada na aplicação e menus de cada perfil |
| `test_sessoes.py` | Entradas, saídas e fim da sessão por inatividade |
| `test_horarios.py` | Horários dos marketeers |
| `test_recuperacao.py` | Recuperação da password e emails simulados |
| `test_contas.py` | Alteração da própria password e dos próprios dados |
| `test_gestao.py` | Gestão de clientes e de marketeers |
| `test_campanhas.py` | Campanhas do Marketeer |
| `test_pedidos.py` | Pedidos de campanha do Cliente |
| `test_administracao.py` | Decisões do Administrador sobre pedidos e campanhas |
| `test_campanhas_cliente.py` | Campanhas vistas pelo Cliente |
| `test_criativos.py` | Criativos: dados, estados, aprovação, filtros e despesa |
| `test_ficheiros.py` | Ficheiros anexados aos criativos |
| `test_budget.py` | Pedidos de alteração de budget e parecer |
| `test_decisao_budget.py` | Decisão dos pedidos de budget e histórico |
| `test_resumo_budget.py` | Resumo global do budget |
| `test_comentarios.py` | Comentários e respostas |
| `test_notificacoes.py` | Notificações na aplicação e por email |
| `test_painel.py` | Painel de marketeers |
| `test_relatorios.py` | Relatório das campanhas em CSV |
| `test_fluxos.py` | Fluxos completos |
| `test_dados_demo.py` | Dados de demonstração |
| `test_documentacao.py` | Docstrings e referência da documentação |

## Como os testes ficam independentes

- **Base de dados nova em cada teste.** A *fixture* `ligacao` entrega uma base de dados em memória, já com as tabelas, que desaparece no fim do teste.
- **Pasta de dados temporária.** Todos os testes guardam os emails e os ficheiros numa pasta temporária, por isso nunca mexem na pasta `dados` do projeto.
- **Relógio substituível.** Toda a aplicação pergunta as horas ao módulo `relogio`. Os testes trocam-no por um relógio parado, para simular o dia de hoje, um prazo que passou ou uma sessão inativa sem esperar.
- **Teclado simulado.** A *fixture* `teclado` responde às perguntas dos menus, por ordem, para testar os ecrãs.

## Integração contínua

Em cada *push* e em cada *pull request* para `main` ou `develop`, o GitHub Actions corre os testes com duas versões do Python e gera a documentação com o Sphinx, que falha se houver algum aviso. O resultado aparece no próprio pull request, e um pull request só é junto com as verificações a verde.
