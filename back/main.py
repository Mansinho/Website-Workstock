def menu_empresaDeReforma():
    print("Menu - Empresa de Reforma")
    print("===========================")
    print("1. Dashboard")
    print("2. Ordens de Serviço")
    print("3. Estoque")
    print("4. Clientes e Proprietários")
    opcao = input("Escolha uma opção: ")
    return opcao


def main():
    while True:
        opcao = menu_empresaDeReforma()
        if opcao == '1':
            print("Acessando Dashboard...")
        elif opcao == '2':
            print("Gerenciando Ordens de Serviço...")
            ordemServico()
        elif opcao == '3':
            print("Gerenciando Estoque...")
            gerenciar_estoque()
        elif opcao == '4':
            print("Gerenciando Clientes e Proprietários...")
            clientesEProprietarios()
        else:
            print("Opção inválida. Tente novamente.")
        continuar = input("Deseja continuar? (s/n): ")
        if continuar.lower() != 's':
            break

def ordemServico():
    lista_os = []
    ultimo_num = 0
    while True:    
        print("Menu - Ordens de Serviço")
        print("===========================")
        print("1. Criar Nova OS")
        print("2. Listar Todas as OS")
        print("3. Relatórios de OS")
        print("4. Voltar ao menu")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            ultimo_num += 1   
            nova_os = {}
            nova_os["ordem_serv"] = ultimo_num              
            nova_os["descricao"] = input("Digite a descrição da OS: ")
            nova_os["status"] = input("Digite o status da OS: ")
            nova_os["data_criacao"] = input("Digite a data de criação (DD/MM/AAAA): ")
            nova_os["data_conclusao"] = input("Digite a data de conclusão (DD/MM/AAAA): ")
            print("Criando Nova Ordem de Serviço...")
            print(f"Ordem de Serviço {nova_os['ordem_serv']} criada com sucesso!")
            lista_os.append(nova_os)
            # Implementar lógica para criar nova OS
        elif opcao == '2':
            print("Listando Todas as Ordens de Serviço...")
            if not lista_os:
                print("Nenhuma ordem de serviço cadastrada..")
            else:
                for os in lista_os:
                    print(f"Numero da ordem de serviço:{os['ordem_serv']}")
                    print(f"Descrição:{os['descricao']}")
                    print(f"Status:{os['status']}")
                    print(f"Data de começo:{os['data_criacao']}")
                    print(f"Data de término:{os['data_conclusao']}")
            # Implementar lógica para listar todas as OS
        elif opcao == '3':
            print("Gerando Relatórios de Ordens de Serviço...")
            concluidas = [os for os in lista_os if os['status'].lower() == 'concluída']
            print(f"Total de OS: {len(lista_os)}")
            print(f"OS Concluídas: {len(concluidas)}")
            # Implementar lógica para gerar relatórios
        elif opcao == '4':
            main()
        else:
            print("Opção inválida. Tente novamente.")

def gerenciar_estoque():
    lista_material = []
    ultimo_material = 0
    while True:
        print("Menu - Estoque")
        print("===========================")
        print("1. Cadastrar Material")
        print("2. Controlar Entradas/Saídas")
        print("3. Ver Estoque")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            ultimo_material += 1
            print("Cadastrando Material...")
            lista_material["numero_material"] = ultimo_material              
            lista_material["material"] = input("Material:")
            lista_material["quantidade"] = input("Quantidade:")         
            # Implementar lógica para cadastrar material
        elif opcao == '2':
            print("Controlando Entradas/Saídas...")
            # Implementar lógica para controlar entradas/saídas
        elif opcao == '3':
            print("Verificando Estoque...")
            # Implementar lógica para ver estoque
        else:
            print("Opção inválida. Tente novamente.")

def clientesEProprietarios():
    print("Menu - Clientes e Proprietários")
    print("===========================")
    print("1. Cadastrar Cliente")
    print("2. Listar Clientes")
    print("3. Gerenciar Proprietários")
    opcao = input("Escolha uma opção: ")
    
    if opcao == '1':
        print("Cadastrando Cliente...")
        # Implementar lógica para cadastrar cliente
    elif opcao == '2':
        print("Listando Clientes...")
        # Implementar lógica para listar clientes
    elif opcao == '3':
        print("Gerenciando Proprietários...")
        # Implementar lógica para gerenciar proprietários
    else:
        print("Opção inválida. Tente novamente.")

main()