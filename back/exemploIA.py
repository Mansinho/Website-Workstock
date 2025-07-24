from datetime import datetime

# --- Funções Auxiliares para Melhorar a Experiência do Usuário ---

def exibir_titulo(titulo):
    """Exibe um título formatado para menus."""
    print(f"\n========= {titulo.upper()} =========")

def exibir_subtitulo(subtitulo):
    """Exibe um subtítulo formatado para seções."""
    print(f"\n--- {subtitulo} ---")

def pedir_opcao(mensagem="Digite o número da sua escolha: "):
    """Pede uma opção ao usuário e retorna a entrada."""
    return input(mensagem)

def exibir_mensagem(mensagem):
    """Exibe uma mensagem para o usuário."""
    print(mensagem)

def obter_inteiro(mensagem, erro_mensagem="Erro: Por favor, digite um número inteiro válido."):
    """Pede um número inteiro ao usuário e trata erros de entrada."""
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            exibir_mensagem(erro_mensagem)

def encontrar_item_por_id(lista, id_procurado):
    """Procura um item em uma lista de dicionários pelo ID."""
    for item in lista:
        if item.get('id') == id_procurado or item.get('numero_os') == id_procurado:
            return item
    return None

# --- Funções do Menu Principal ---

def apresentar_menu_principal():
    """Mostra o menu principal do sistema."""
    exibir_titulo("MENU PRINCIPAL")
    exibir_mensagem("1. Ordens de Serviço")
    exibir_mensagem("2. Gerenciar Estoque")
    exibir_mensagem("3. Gerenciar Clientes")
    exibir_mensagem("4. Sair do Programa")
    exibir_mensagem("==================================")
    return pedir_opcao()

# --- Funções de Ordens de Serviço ---

def criar_nova_os(lista_de_os):
    """Cria uma nova Ordem de Serviço e adiciona à lista."""
    exibir_subtitulo("Criando Nova Ordem de Serviço")

    # Calcula o próximo número da OS.
    # Se a lista estiver vazia, o próximo número é 1.
    # Caso contrário, pega o número da última OS e adiciona 1.
    proximo_numero_os = lista_de_os[-1]['numero_os'] + 1 if lista_de_os else 1

    nova_os = {
        "numero_os": proximo_numero_os,
        "descricao": input("Descrição do serviço: "),
        "cliente": input("Nome do cliente: "),
        "status": "Aberta",  # Status padrão
        "data_criacao": datetime.now().strftime('%d/%m/%Y %H:%M')
    }

    lista_de_os.append(nova_os)
    exibir_mensagem(f"Sucesso! Ordem de Serviço número {nova_os['numero_os']} criada.")

def listar_todas_os(lista_de_os):
    """Lista todas as Ordens de Serviço cadastradas."""
    exibir_subtitulo("Listando Todas as Ordens de Serviço")

    if not lista_de_os:
        exibir_mensagem("Ainda não há Ordens de Serviço cadastradas.")
        return

    for os in lista_de_os:
        print("-" * 30)
        exibir_mensagem(f"Número: {os['numero_os']}")
        exibir_mensagem(f"Descrição: {os['descricao']}")
        exibir_mensagem(f"Cliente: {os['cliente']}")
        exibir_mensagem(f"Status: {os['status']}")
        exibir_mensagem(f"Data de Criação: {os['data_criacao']}")
    print("-" * 30)

def ver_relatorio_simples_os(lista_de_os):
    """Mostra um relatório simples de Ordens de Serviço."""
    exibir_subtitulo("Relatório de Ordens de Serviço")

    if not lista_de_os:
        exibir_mensagem("Nenhuma Ordem de Serviço para gerar relatório.")
        return

    concluidas = 0
    abertas_em_andamento = 0

    for os in lista_de_os:
        if os['status'].lower() == 'concluída':
            concluidas += 1
        else:
            abertas_em_andamento += 1

    exibir_mensagem(f"Total de Ordens de Serviço: {len(lista_de_os)}")
    exibir_mensagem(f"Ordens Concluídas: {concluidas}")
    exibir_mensagem(f"Ordens Abertas/Em Andamento: {abertas_em_andamento}")

def alterar_status_os(lista_de_os):
    """Permite alterar o status de uma Ordem de Serviço existente."""
    exibir_subtitulo("Gerenciar Status da Ordem de Serviço")

    if not lista_de_os:
        exibir_mensagem("Nenhuma Ordem de Serviço para alterar.")
        return

    numero_os = obter_inteiro("Digite o número da Ordem de Serviço para alterar o status: ")
    os_encontrada = encontrar_item_por_id(lista_de_os, numero_os)

    if os_encontrada:
        exibir_mensagem("\nEscolha o novo status:")
        exibir_mensagem("1 - Aberta")
        exibir_mensagem("2 - Concluída")
        exibir_mensagem("3 - Cancelada")
        opcao_status = pedir_opcao("Digite o número da opção: ")

        if opcao_status == '1':
            os_encontrada['status'] = 'Aberta'
            exibir_mensagem(f"Status da OS {numero_os} alterado para 'Aberta'.")
        elif opcao_status == '2':
            os_encontrada['status'] = 'Concluída'
            exibir_mensagem(f"Status da OS {numero_os} alterado para 'Concluída'.")
        elif opcao_status == '3':
            os_encontrada['status'] = 'Cancelada'
            exibir_mensagem(f"Status da OS {numero_os} alterado para 'Cancelada'.")
        else:
            exibir_mensagem("Opção de status inválida.")
    else:
        exibir_mensagem("Ordem de Serviço não encontrada.")

def gerenciar_ordens_de_servico(lista_de_os):
    """Função principal para o menu de Ordens de Serviço."""
    while True:
        exibir_subtitulo("Menu de Ordens de Serviço")
        exibir_mensagem("1. Criar Nova Ordem de Serviço")
        exibir_mensagem("2. Listar Todas as Ordens de Serviço")
        exibir_mensagem("3. Ver Relatório Simples")
        exibir_mensagem("4. Gerenciar Status da Ordem de Serviço")
        exibir_mensagem("5. Voltar ao Menu Principal")
        opcao = pedir_opcao("Sua escolha: ")

        if opcao == '1':
            criar_nova_os(lista_de_os)
        elif opcao == '2':
            listar_todas_os(lista_de_os)
        elif opcao == '3':
            ver_relatorio_simples_os(lista_de_os)
        elif opcao == '4':
            alterar_status_os(lista_de_os)
        elif opcao == '5':
            exibir_mensagem("Voltando ao menu principal...")
            break
        else:
            exibir_mensagem("Opção inválida! Por favor, escolha um número do menu.")

# --- Funções de Estoque ---

def cadastrar_novo_material(lista_de_estoque):
    """Cadastra um novo material no estoque."""
    exibir_subtitulo("Cadastrando Novo Material")

    novo_item = {
        "id": len(lista_de_estoque) + 1,
        "material": input("Nome do material: "),
        "quantidade": obter_inteiro("Quantidade inicial do material: ")
    }
    lista_de_estoque.append(novo_item)
    exibir_mensagem(f"Material '{novo_item['material']}' cadastrado!")

def ver_estoque(lista_de_estoque):
    """Exibe todos os materiais no estoque."""
    exibir_subtitulo("Estoque Atual")

    if not lista_de_estoque:
        exibir_mensagem("O estoque está vazio.")
        return

    print(f"{'ID':<5}{'Material':<20}{'Quantidade'}")
    print("-" * 35)
    for item in lista_de_estoque:
        print(f"{item['id']:<5}{item['material']:<20}{item['quantidade']}")
    print("-" * 35)

def alterar_material_estoque(lista_de_estoque):
    """Altera a quantidade de um material existente no estoque."""
    exibir_subtitulo("Alterar Estoque")

    if not lista_de_estoque:
        exibir_mensagem("O estoque está vazio. Não há materiais para alterar.")
        return

    id_material = obter_inteiro("Digite o ID do material que deseja alterar: ")
    material_encontrado = encontrar_item_por_id(lista_de_estoque, id_material)

    if material_encontrado:
        nova_quantidade = obter_inteiro(
            f"Quantidade atual de '{material_encontrado['material']}': {material_encontrado['quantidade']}. Digite a nova quantidade: "
        )
        material_encontrado['quantidade'] = nova_quantidade
        exibir_mensagem(f"Quantidade de '{material_encontrado['material']}' atualizada para {nova_quantidade}.")
    else:
        exibir_mensagem("Material não encontrado.")

def gerenciar_estoque(lista_de_estoque):
    """Função principal para o menu de Estoque."""
    while True:
        exibir_subtitulo("Menu de Estoque")
        exibir_mensagem("1. Cadastrar Novo Material")
        exibir_mensagem("2. Ver Estoque")
        exibir_mensagem("3. Alterar Estoque")
        exibir_mensagem("4. Voltar ao Menu Principal")
        opcao = pedir_opcao("Sua escolha: ")

        if opcao == '1':
            cadastrar_novo_material(lista_de_estoque)
        elif opcao == '2':
            ver_estoque(lista_de_estoque)
        elif opcao == '3':
            alterar_material_estoque(lista_de_estoque)
        elif opcao == '4':
            exibir_mensagem("Voltando ao menu principal...")
            break
        else:
            exibir_mensagem("Opção inválida!")

# --- Funções de Clientes ---

def cadastrar_novo_cliente(lista_de_clientes):
    """Cadastra um novo cliente."""
    exibir_subtitulo("Cadastrando Novo Cliente")
    novo_cliente = {
        "id": len(lista_de_clientes) + 1,
        "nome": input("Nome do cliente: "),
        "telefone": input("Telefone para contato: ")
    }
    lista_de_clientes.append(novo_cliente)
    exibir_mensagem(f"Cliente '{novo_cliente['nome']}' cadastrado com sucesso!")

def listar_clientes(lista_de_clientes):
    """Lista todos os clientes cadastrados."""
    exibir_subtitulo("Lista de Clientes")
    if not lista_de_clientes:
        exibir_mensagem("Nenhum cliente cadastrado.")
        return
    for cliente in lista_de_clientes:
        print("-" * 20)
        exibir_mensagem(f"ID: {cliente['id']}")
        exibir_mensagem(f"Nome: {cliente['nome']}")
        exibir_mensagem(f"Telefone: {cliente['telefone']}")
    print("-" * 20)

def remover_cliente(lista_de_clientes):
    """Remove um cliente da lista."""
    exibir_subtitulo("Remover Cliente")
    if not lista_de_clientes:
        exibir_mensagem("Nenhum cliente cadastrado para remover.")
        return

    id_cliente = obter_inteiro("Digite o ID do cliente que deseja remover: ")
    cliente_encontrado = encontrar_item_por_id(lista_de_clientes, id_cliente)

    if cliente_encontrado:
        lista_de_clientes.remove(cliente_encontrado)
        exibir_mensagem(f"Cliente '{cliente_encontrado['nome']}' removido com sucesso!")
    else:
        exibir_mensagem("Cliente não encontrado.")

def gerenciar_clientes(lista_de_clientes):
    """Função principal para o menu de Clientes."""
    while True:
        exibir_subtitulo("Menu de Clientes")
        exibir_mensagem("1. Cadastrar Novo Cliente")
        exibir_mensagem("2. Listar Clientes")
        exibir_mensagem("3. Remover Cliente")
        exibir_mensagem("4. Voltar ao Menu Principal")
        opcao = pedir_opcao("Sua escolha: ")

        if opcao == '1':
            cadastrar_novo_cliente(lista_de_clientes)
        elif opcao == '2':
            listar_clientes(lista_de_clientes)
        elif opcao == '3':
            remover_cliente(lista_de_clientes)
        elif opcao == '4':
            exibir_mensagem("Voltando ao menu principal...")
            break
        else:
            exibir_mensagem("Opção inválida!")

# --- Função Principal do Programa ---

def main():
    """
    Função principal que inicia e gerencia o fluxo do programa.
    Aqui as listas que armazenam os dados são inicializadas.
    """
    lista_os_principal = []
    lista_estoque_principal = []
    lista_clientes_principal = []

    while True:
        opcao_menu = apresentar_menu_principal()

        if opcao_menu == '1':
            gerenciar_ordens_de_servico(lista_os_principal)
        elif opcao_menu == '2':
            gerenciar_estoque(lista_estoque_principal)
        elif opcao_menu == '3':
            gerenciar_clientes(lista_clientes_principal)
        elif opcao_menu == '4':
            exibir_mensagem("\nObrigado por usar o sistema. Até logo!")
            break
        else:
            exibir_mensagem("\nErro: Opção não encontrada. Por favor, tente novamente.")

# Garante que a função main() seja executada apenas quando o script for rodado diretamente.
if __name__ == "__main__":
    main()