# Importa a biblioteca de data e hora para registrar a data de criação automaticamente.
from datetime import datetime

def menu_empresaDeReforma():
    """Exibe o menu principal e retorna a opção escolhida pelo usuário."""
    print("\nMenu - Empresa de Reforma")
    print("===========================")
    print("1. Dashboard")
    print("2. Ordens de Serviço")
    print("3. Estoque")
    print("4. Clientes")
    print("5. Sair") # Adicionada uma opção para sair do programa
    opcao = input("Escolha uma opção: ")
    return opcao

def ordemServico(lista_os):
    """
    Gerencia as Ordens de Serviço (OS).
    Recebe a lista de OS como parâmetro para manter os dados.
    """
    # Usa o número da última OS da lista para continuar a sequência, ou começa em 0 se a lista estiver vazia.
    ultimo_num = lista_os[-1]['ordem_serv'] if lista_os else 0
    
    while True:
        print("\nMenu - Ordens de Serviço")
        print("===========================")
        print("1. Criar Nova OS")
        print("2. Listar Todas as OS")
        print("3. Relatórios de OS")
        print("4. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            ultimo_num += 1
            # Cada OS é um dicionário para organizar as informações.
            nova_os = {
                "ordem_serv": ultimo_num,
                "descricao": input("Digite a descrição da OS: "),
                "status": "Abertta", # Status inicial padrão
                # Pega a data e hora atuais automaticamente.
                "data_criacao": datetime.now().strftime('%d/%m/%Y %H:%M'),
                "data_conclusao": None, # Data de conclusão fica vazia até ser finalizada.
                "cliente": input("Nome do cliente: ")
            }
            # Adiciona a nova OS (dicionário) na lista de OS.
            lista_os.append(nova_os)
            print(f"\nOrdem de Serviço {nova_os['ordem_serv']} criada com sucesso!")

        elif opcao == '2':
            print("\nListando Todas as Ordens de Serviço...")
            if not lista_os:
                print("Nenhuma ordem de serviço cadastrada.")
            else:
                # Itera sobre a lista e imprime os dados de cada OS.
                for os in lista_os:
                    print("-" * 20)
                    print(f"Número da OS: {os['ordem_serv']}")
                    print(f"Descrição: {os['descricao']}")
                    print(f"Status: {os['status']}")
                    print(f"Cliente: {os['cliente']}")
                    print(f"Data de Criação: {os['data_criacao']}")
                    print(f"Data de Conclusão: {os.get('data_conclusao', 'Pendente')}")

        elif opcao == '3':
            print("\nGerando Relatórios de Ordens de Serviço...")
            # Usa list comprehension para filtrar OS com status 'Concluída'.
            concluidas = [os for os in lista_os if os['status'].lower() == 'concluída']
            abertas = [os for os in lista_os if os['status'].lower() == 'aberta']
            print(f"Total de OS: {len(lista_os)}")
            print(f"OS Concluídas: {len(concluidas)}")
            print(f"OS Abertas: {len(abertas)}")

        elif opcao == '4':
            # Interrompe o loop do menu de OS para voltar ao menu principal.
            break
        else:
            print("Opção inválida. Tente novamente.")

def gerenciar_estoque(lista_estoque):
    """
    Gerencia o estoque de materiais.
    Recebe a lista de estoque como parâmetro para manter os dados.
    """
    while True:
        print("\nMenu - Estoque")
        print("===========================")
        print("1. Cadastrar Novo Material")
        print("2. Registrar Entrada/Saída")
        print("3. Ver Estoque Completo")
        print("4. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\nCadastrando Material...")
            # Cria um dicionário para o novo material.
            novo_material = {
                "id": len(lista_estoque) + 1,
                "material": input("Nome do material: "),
                # Converte a quantidade para inteiro.
                "quantidade": int(input("Quantidade inicial: "))
            }
            # Adiciona o novo material à lista de estoque.
            lista_estoque.append(novo_material)
            print(f"Material '{novo_material['material']}' cadastrado com sucesso!")

        elif opcao == '2':
            print("\nRegistrar Entrada/Saída...")
            if not lista_estoque:
                print("Nenhum material cadastrado. Cadastre um material primeiro.")
                continue

            id_material = int(input("Digite o ID do material para atualizar: "))
            # Procura o material na lista pelo ID.
            material_encontrado = None
            for item in lista_estoque:
                if item["id"] == id_material:
                    material_encontrado = item
                    break
            
            if material_encontrado:
                tipo = input("Registrar 'entrada' ou 'saida'? ").lower()
                qtd = int(input("Qual a quantidade? "))
                if tipo == 'entrada':
                    material_encontrado['quantidade'] += qtd
                    print(f"Entrada registrada. Novo estoque de '{material_encontrado['material']}': {material_encontrado['quantidade']}")
                elif tipo == 'saida':
                    if qtd > material_encontrado['quantidade']:
                        print("Erro: Quantidade de saída maior que o estoque atual.")
                    else:
                        material_encontrado['quantidade'] -= qtd
                        print(f"Saída registrada. Novo estoque de '{material_encontrado['material']}': {material_encontrado['quantidade']}")
                else:
                    print("Operação inválida.")
            else:
                print("Material não encontrado.")

        elif opcao == '3':
            print("\nVerificando Estoque...")
            if not lista_estoque:
                print("Estoque vazio.")
            else:
                print(f"{'ID':<5}{'Material':<20}{'Quantidade'}")
                print("-" * 35)
                # Itera e exibe cada item do estoque formatado.
                for item in lista_estoque:
                    print(f"{item['id']:<5}{item['material']:<20}{item['quantidade']}")

        elif opcao == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

def gerenciar_clientes(lista_clientes):
    """
    Gerencia o cadastro de clientes.
    Recebe a lista de clientes como parâmetro para manter os dados.
    """
    while True:
        print("\nMenu - Clientes")
        print("===========================")
        print("1. Cadastrar Novo Cliente")
        print("2. Listar Todos os Clientes")
        print("3. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\nCadastrando Cliente...")
            novo_cliente = {
                "id": len(lista_clientes) + 1,
                "nome": input("Nome do cliente: "),
                "telefone": input("Telefone: "),
                "email": input("Email: ")
            }
            lista_clientes.append(novo_cliente)
            print(f"Cliente '{novo_cliente['nome']}' cadastrado com sucesso!")

        elif opcao == '2':
            print("\nListando Clientes...")
            if not lista_clientes:
                print("Nenhum cliente cadastrado.")
            else:
                for cliente in lista_clientes:
                    print("-" * 20)
                    print(f"ID: {cliente['id']}")
                    print(f"Nome: {cliente['nome']}")
                    print(f"Telefone: {cliente['telefone']}")
                    print(f"Email: {cliente['email']}")
        
        elif opcao == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")


def main():
    """
    Função principal que controla o fluxo do programa.
    Inicializa as listas de dados para que sejam persistentes durante a execução.
    """
    # As listas são criadas aqui para que seus dados não sejam perdidos
    # ao navegar entre os diferentes menus do sistema.
    lista_de_os = []
    lista_de_estoque = []
    lista_de_clientes = []

    # Loop principal do programa. Continua executando até o usuário escolher sair.
    while True:
        opcao = menu_empresaDeReforma()
        if opcao == '1':
            print("\nAcessando Dashboard...")
            # Lógica do Dashboard (pode mostrar resumos das outras áreas)
            print(f"Resumo: {len(lista_de_os)} Ordens de Serviço, {len(lista_de_clientes)} Clientes, {len(lista_de_estoque)} Itens no Estoque.")

        elif opcao == '2':
            # Passa a lista de OS para a função, permitindo que ela seja modificada.
            ordemServico(lista_de_os)

        elif opcao == '3':
            # Passa a lista de estoque para a função.
            gerenciar_estoque(lista_de_estoque)

        elif opcao == '4':
            # Passa a lista de clientes para a função.
            gerenciar_clientes(lista_de_clientes)

        elif opcao == '5':
            print("Saindo do sistema. Até logo!")
            break # Encerra o loop e o programa.
            
        else:
            print("Opção inválida. Tente novamente.")

# Este bloco garante que a função main() seja chamada apenas quando
# o script é executado diretamente. É uma boa prática em Python.
if __name__ == "__main__":
    main()