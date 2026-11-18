"""Regras dos pedidos de alteração de budget.

O cliente de uma campanha pode pedir que o budget dela seja alterado,
indicando o valor que pretende e o motivo. O pedido começa no estado
pendente; enquanto estiver pendente, o cliente pode cancelá-lo.

O marketeer responsável pela campanha dá o seu parecer: diz se o pedido é
viável e porquê. Com o parecer, o pedido passa a estar em análise e o cliente
deixa de o poder cancelar.

Depois do parecer, o Administrador decide. Se aprovar, o budget da campanha
passa a ser o valor pedido e a alteração fica no histórico do budget; se
rejeitar, indica o motivo.

Cada campanha só pode ter um pedido de cada vez à espera de decisão, para
não haver dois valores pedidos ao mesmo tempo para o mesmo budget.

O módulo calcula também o resumo global do budget, para o Administrador: o
budget atribuído, a despesa e o restante de cada cliente, e as campanhas que
já gastaram mais do que o budget.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from gestor_campanhas import dinheiro, modelos, relogio
from gestor_campanhas.erros import ErroValidacao
from gestor_campanhas.modelos import Campanha, PedidoBudget, Utilizador
from gestor_campanhas.repositorios import pedidos_budget
from gestor_campanhas.servicos import campanhas, criativos

#: Estados em que um pedido ainda espera pela decisão do Administrador.
POR_DECIDIR = (modelos.PENDENTE, modelos.EM_ANALISE)


def campanha_para_pedido(ligacao: sqlite3.Connection, cliente: Utilizador, campanha_id: int) -> Campanha:
    """Procura uma campanha do cliente e confirma que aceita um pedido de alteração de budget.

    O menu usa esta função logo depois de o cliente escolher a campanha, para
    o avisar antes de lhe pedir o valor e o motivo.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    :param campanha_id: Número da campanha.
    :return: A campanha.
    :raises ErroValidacao: Se a campanha não for do cliente, se já tiver
        terminado ou se já tiver um pedido por decidir.
    """
    campanha = campanhas.obter_do_cliente(ligacao, cliente, campanha_id)
    if campanha.terminada(relogio.hoje()):
        raise ErroValidacao(f"A campanha {campanha.nome} já terminou. O budget já não pode ser alterado.")
    anterior = pedidos_budget.obter_por_decidir(ligacao, campanha.id)
    if anterior is not None:
        raise ErroValidacao(
            f"A campanha {campanha.nome} já tem um pedido de alteração de budget por decidir (n.º {anterior.id})."
        )
    return campanha


def pedir(
    ligacao: sqlite3.Connection, cliente: Utilizador, campanha_id: int, budget: str, motivo: str
) -> PedidoBudget:
    """Regista um pedido de alteração do budget de uma campanha do cliente.

    O pedido guarda o budget que a campanha tem neste momento, para se poder
    comparar com o valor pedido mesmo depois de o budget mudar.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a fazer o pedido.
    :param campanha_id: Número da campanha. Tem de ser do cliente e não pode
        ter terminado.
    :param budget: Budget pretendido, em euros, tal como foi escrito (por
        exemplo ``"2000"`` ou ``"2000,50"``). Tem de ser maior do que zero e
        diferente do budget atual.
    :param motivo: Porque é que quer alterar o budget. Obrigatório.
    :return: O pedido criado, no estado pendente.
    :raises ErroValidacao: Se a campanha não for do cliente, se já tiver
        terminado, se já tiver um pedido por decidir, ou se algum dos valores
        não respeitar as regras.
    """
    campanha = campanha_para_pedido(ligacao, cliente, campanha_id)
    centimos = campanhas.budget_validado(budget)
    if centimos == campanha.budget_centimos:
        raise ErroValidacao("O valor pedido é igual ao budget atual da campanha.")
    motivo = motivo.strip()
    if not motivo:
        raise ErroValidacao("O motivo não pode ficar vazio.")
    return pedidos_budget.criar(ligacao, campanha.id, campanha.budget_centimos, centimos, motivo)


def listar_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador) -> list[PedidoBudget]:
    """Lista os pedidos de alteração de budget de um cliente, em qualquer estado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :return: Pedidos desse cliente, do mais recente para o mais antigo.
    """
    return pedidos_budget.listar_por_cliente(ligacao, cliente.id)


def obter_do_cliente(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoBudget:
    """Procura um pedido de alteração de budget pelo número, confirmando que é do cliente.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a consultar.
    :param identificador: Número do pedido, mostrado na primeira coluna da lista.
    :return: O pedido.
    :raises ErroValidacao: Se o cliente não tiver nenhum pedido de budget com esse número.
    """
    pedido = pedidos_budget.obter_por_id(ligacao, identificador)
    if pedido is None or pedido.cliente_id != cliente.id:
        raise ErroValidacao(f"Não tem nenhum pedido de budget com o número {identificador}.")
    return pedido


def cancelar(ligacao: sqlite3.Connection, cliente: Utilizador, identificador: int) -> PedidoBudget:
    """Cancela um pedido de alteração de budget do cliente que ainda esteja pendente.

    O pedido não é apagado: fica na lista, com o estado cancelado.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente: Cliente que está a cancelar.
    :param identificador: Número do pedido.
    :return: O pedido, já cancelado.
    :raises ErroValidacao: Se o pedido não for do cliente ou já não estiver pendente.
    """
    pedido = obter_do_cliente(ligacao, cliente, identificador)
    if pedido.estado != modelos.PENDENTE:
        raise ErroValidacao(
            f"Só é possível cancelar um pedido pendente. Este pedido está no estado {pedido.nome_estado}."
        )
    return pedidos_budget.definir_estado(ligacao, pedido.id, modelos.CANCELADO)


def listar_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador) -> list[PedidoBudget]:
    """Lista os pedidos de alteração de budget das campanhas de um marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :return: Primeiro os pedidos por decidir, depois os já decididos ou
        cancelados; dentro de cada grupo, do mais antigo para o mais recente.
    """
    todos = pedidos_budget.listar_por_marketeer(ligacao, marketeer.id)
    return sorted(todos, key=lambda pedido: (pedido.estado not in POR_DECIDIR, pedido.id))


def obter_do_marketeer(ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int) -> PedidoBudget:
    """Procura um pedido de alteração de budget, confirmando que é de uma campanha do marketeer.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer que está a consultar.
    :param identificador: Número do pedido.
    :return: O pedido.
    :raises ErroValidacao: Se não houver nenhum pedido com esse número nas
        campanhas do marketeer.
    """
    pedido = pedidos_budget.obter_por_id(ligacao, identificador)
    if pedido is None or pedido.marketeer_id != marketeer.id:
        raise ErroValidacao(f"Não há nenhum pedido de budget com o número {identificador} nas suas campanhas.")
    return pedido


def dar_parecer(
    ligacao: sqlite3.Connection, marketeer: Utilizador, identificador: int, viavel: bool, justificacao: str
) -> PedidoBudget:
    """Guarda o parecer do marketeer sobre um pedido de alteração de budget.

    O pedido passa a estar em análise. Enquanto o Administrador não o
    decidir, o marketeer pode mudar o parecer: o novo substitui o anterior.

    :param ligacao: Ligação aberta à base de dados.
    :param marketeer: Marketeer responsável pela campanha do pedido.
    :param identificador: Número do pedido.
    :param viavel: ``True`` se o pedido é viável, ``False`` se não é.
    :param justificacao: Porque é que é, ou não é, viável. Obrigatória.
    :return: O pedido, já com o parecer.
    :raises ErroValidacao: Se o pedido não for de uma campanha do marketeer,
        se já tiver sido decidido ou cancelado, ou se a justificação ficar vazia.
    """
    pedido = obter_do_marketeer(ligacao, marketeer, identificador)
    if pedido.estado not in POR_DECIDIR:
        raise ErroValidacao(f"Este pedido já não aceita parecer: está no estado {pedido.nome_estado}.")
    justificacao = justificacao.strip()
    if not justificacao:
        raise ErroValidacao("A justificação do parecer não pode ficar vazia.")
    return pedidos_budget.definir_parecer(ligacao, pedido.id, viavel, justificacao, modelos.EM_ANALISE)


def listar_todos(ligacao: sqlite3.Connection) -> list[PedidoBudget]:
    """Lista os pedidos de alteração de budget de todas as campanhas, para o Administrador.

    :param ligacao: Ligação aberta à base de dados.
    :return: Primeiro os pedidos por decidir, depois os já decididos ou
        cancelados; dentro de cada grupo, do mais antigo para o mais recente.
    """
    todos = pedidos_budget.listar_todos(ligacao)
    return sorted(todos, key=lambda pedido: (pedido.estado not in POR_DECIDIR, pedido.id))


def obter(ligacao: sqlite3.Connection, identificador: int) -> PedidoBudget:
    """Procura um pedido de alteração de budget pelo número, seja de que campanha for.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do pedido.
    :return: O pedido.
    :raises ErroValidacao: Se não existir nenhum pedido de budget com esse número.
    """
    pedido = pedidos_budget.obter_por_id(ligacao, identificador)
    if pedido is None:
        raise ErroValidacao(f"Não existe nenhum pedido de budget com o número {identificador}.")
    return pedido


def _para_decidir(ligacao: sqlite3.Connection, identificador: int) -> PedidoBudget:
    """Devolve um pedido, confirmando que está por decidir e já tem o parecer do marketeer."""
    pedido = obter(ligacao, identificador)
    if pedido.estado not in POR_DECIDIR:
        raise ErroValidacao(f"Este pedido já não pode ser decidido: está no estado {pedido.nome_estado}.")
    if pedido.parecer_viavel is None:
        raise ErroValidacao("Este pedido ainda não tem o parecer do marketeer. Só pode ser decidido depois do parecer.")
    return pedido


def aprovar(ligacao: sqlite3.Connection, identificador: int) -> PedidoBudget:
    """Aprova um pedido de alteração de budget e altera o budget da campanha.

    O budget da campanha passa a ser o valor pedido. A alteração fica no
    histórico do budget, com o número e o motivo do pedido.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do pedido.
    :return: O pedido, já aprovado.
    :raises ErroValidacao: Se o pedido não existir, se já tiver sido decidido
        ou cancelado, se ainda não tiver parecer, ou se a campanha já tiver o
        budget pedido. Nesse caso nada é alterado.
    """
    pedido = _para_decidir(ligacao, identificador)
    campanha = campanhas.obter(ligacao, pedido.campanha_id)
    if campanha.budget_centimos == pedido.budget_pedido_centimos:
        raise ErroValidacao(
            f"O budget da campanha já é {dinheiro.formatar(campanha.budget_centimos)}. "
            "Este pedido já não altera nada: rejeite-o, indicando o motivo."
        )
    motivo = f"Pedido de budget n.º {pedido.id}: {pedido.motivo}"
    campanhas.alterar_budget(ligacao, campanha, pedido.budget_pedido_centimos, motivo, pedido.id)
    return pedidos_budget.decidir(ligacao, pedido.id, modelos.APROVADO)


def rejeitar(ligacao: sqlite3.Connection, identificador: int, motivo: str) -> PedidoBudget:
    """Rejeita um pedido de alteração de budget, indicando o motivo. O budget não muda.

    :param ligacao: Ligação aberta à base de dados.
    :param identificador: Número do pedido.
    :param motivo: Porque é que o pedido não é aceite. Obrigatório.
    :return: O pedido, já rejeitado.
    :raises ErroValidacao: Se o pedido não existir, se já tiver sido decidido
        ou cancelado, se ainda não tiver parecer, ou se o motivo ficar vazio.
    """
    pedido = _para_decidir(ligacao, identificador)
    motivo = motivo.strip()
    if not motivo:
        raise ErroValidacao("O motivo da rejeição não pode ficar vazio.")
    return pedidos_budget.decidir(ligacao, pedido.id, modelos.REJEITADO, motivo)


@dataclass
class ResumoCliente:
    """Contas do budget das campanhas de um cliente, para o resumo global.

    :param cliente_id: Identificador do cliente.
    :param cliente_nome: Nome do cliente.
    :param campanhas: Número de campanhas do cliente.
    :param budget_centimos: Soma dos budgets das campanhas que já têm budget.
    :param despesa_centimos: Soma da despesa de todas as campanhas.
    :param sem_budget: Número de campanhas que ainda não têm budget.
    :param acima_do_budget: Número de campanhas cuja despesa passa o budget.
    """

    cliente_id: int
    cliente_nome: str
    campanhas: int = 0
    budget_centimos: int = 0
    despesa_centimos: int = 0
    sem_budget: int = 0
    acima_do_budget: int = 0

    @property
    def restante_centimos(self) -> int:
        """Budget menos despesa, em cêntimos. Fica negativo quando a despesa passa o budget."""
        return self.budget_centimos - self.despesa_centimos


def acima_do_budget(campanha: Campanha, gasto: int) -> bool:
    """Diz se uma campanha já gastou mais do que o budget.

    :param campanha: Campanha a avaliar.
    :param gasto: Despesa da campanha, em cêntimos.
    :return: ``True`` se a campanha tem budget e a despesa é maior do que ele.
        Uma campanha sem budget nunca está acima do budget.
    """
    return campanha.budget_centimos is not None and gasto > campanha.budget_centimos


def campanhas_com_despesa(ligacao: sqlite3.Connection) -> list[tuple[Campanha, int]]:
    """Lista todas as campanhas, cada uma com a sua despesa.

    :param ligacao: Ligação aberta à base de dados.
    :return: Pares ``(campanha, despesa em cêntimos)``, ordenados pelo nome do
        cliente e, dentro de cada cliente, pela ordem em que as campanhas
        foram criadas.
    """
    despesas = criativos.despesas(ligacao)
    todas = campanhas.listar_todas(ligacao)
    ordenadas = sorted(todas, key=lambda campanha: (campanha.cliente_nome.casefold(), campanha.id))
    return [(campanha, despesas.get(campanha.id, 0)) for campanha in ordenadas]


def resumo_por_cliente(ligacao: sqlite3.Connection) -> list[ResumoCliente]:
    """Calcula o budget atribuído, a despesa e o restante de cada cliente.

    Só aparecem os clientes que têm campanhas. O budget é a soma dos budgets
    das campanhas que já têm budget; a despesa é a soma da despesa de todas
    as campanhas, mesmo as que ainda não têm budget.

    :param ligacao: Ligação aberta à base de dados.
    :return: Um resumo por cliente, por ordem alfabética do nome.
    """
    resumos: dict[int, ResumoCliente] = {}
    for campanha, gasto in campanhas_com_despesa(ligacao):
        resumo = resumos.setdefault(campanha.cliente_id, ResumoCliente(campanha.cliente_id, campanha.cliente_nome))
        resumo.campanhas += 1
        resumo.despesa_centimos += gasto
        if campanha.budget_centimos is None:
            resumo.sem_budget += 1
        else:
            resumo.budget_centimos += campanha.budget_centimos
        if acima_do_budget(campanha, gasto):
            resumo.acima_do_budget += 1
    return list(resumos.values())


def somar(resumos: list[ResumoCliente]) -> ResumoCliente:
    """Soma os resumos de vários clientes, para a linha do total.

    :param resumos: Resumos a somar, como devolvidos por :func:`resumo_por_cliente`.
    :return: Um resumo com os totais. O número e o nome do cliente ficam
        ``0`` e ``"Total"``.
    """
    total = ResumoCliente(0, "Total")
    for resumo in resumos:
        total.campanhas += resumo.campanhas
        total.budget_centimos += resumo.budget_centimos
        total.despesa_centimos += resumo.despesa_centimos
        total.sem_budget += resumo.sem_budget
        total.acima_do_budget += resumo.acima_do_budget
    return total


def campanhas_acima_do_budget(ligacao: sqlite3.Connection) -> list[tuple[Campanha, int]]:
    """Lista as campanhas que já gastaram mais do que o budget.

    :param ligacao: Ligação aberta à base de dados.
    :return: Pares ``(campanha, despesa em cêntimos)``, pela mesma ordem de
        :func:`campanhas_com_despesa`.
    """
    return [(campanha, gasto) for campanha, gasto in campanhas_com_despesa(ligacao) if acima_do_budget(campanha, gasto)]


def campanhas_do_cliente(ligacao: sqlite3.Connection, cliente_id: int) -> list[tuple[Campanha, int]]:
    """Lista as campanhas de um cliente, cada uma com a sua despesa, para o resumo global.

    :param ligacao: Ligação aberta à base de dados.
    :param cliente_id: Número do cliente, como aparece no resumo.
    :return: Pares ``(campanha, despesa em cêntimos)``, pela ordem em que as
        campanhas foram criadas.
    :raises ErroValidacao: Se não houver nenhum cliente com campanhas com esse número.
    """
    lista = [(campanha, gasto) for campanha, gasto in campanhas_com_despesa(ligacao) if campanha.cliente_id == cliente_id]
    if not lista:
        raise ErroValidacao(f"Não há nenhum cliente com campanhas com o número {cliente_id}.")
    return lista
