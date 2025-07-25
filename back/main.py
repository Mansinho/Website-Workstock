import json
from datetime import datetime
def carregar_dados():
    try:
        with open('bancoDeDados.json', 'r', encoding='utf-8') as arq:
            return json.load(arq)
    except FileNotFoundError:
        return []

def salvar_dados(lista_de_os):
    with open('bancoDeDados.json', 'w', encoding='utf-8') as arq:
        json.dump(lista_de_os, arq, indent=4)
        
def apresentar_menu_principal():
    print("\n========= MENU PRINCIPAL =========")
    print("1. Ordens de Serviço")
    print("2. Gerenciar Estoque")
    print("3. Gerenciar Clientes")
    print("4. Sair do Programa")
    print("==================================")
    opcao = input("Digite o número da sua escolha: ")
    return opcao

def gerenciar_ordens_de_servico(lista_de_os):
    # Para saber o número da próxima ordem de serviço, olhamos o número da última ordem de serviço na lista.
    # Se a lista estiver vazia, começamos com 0.
    if lista_de_os:
        ultimo_numero = lista_de_os[-1]['numero_os']
    else:
        ultimo_numero = 0

    # Laço de Repetição (while): mantém o usuário no menu de ordemDeServico até ele decidir sair.
    while True:
        print("\n--- Menu de Ordens de Serviço ---")
        print("1. Criar Nova Ordem de Serviço")
        print("2. Listar Todas as Ordens de Serviço")
        print("3. Ver Relatório Simples")
        print("4. Gerenciar Status da Ordem de Serviço")
        print("5. Voltar ao Menu Principal")
        opcao = input("Sua escolha: ")

        # Condicional (if/elif/else): decide o que fazer com base na escolha do usuário.
        if opcao == '1':
            print("\n-> Criando nova ordemDeServico...")
            
            nova_os = {
                "numero_os": ultimo_numero + 1,
                "descricao": input("Descrição do serviço: "),
                "cliente": input("Nome do cliente: "),
                "status": "Aberta", # Status padrão ao criar
                # Usamos o módulo datetime para pegar a data e hora atuais.
                "data_criacao": datetime.now().strftime('%d/%m/%Y %H:%M') 
            }
            
            # Adicionamos o novo dicionário (a nova ordemDeServico) na nossa lista principal de ordemDeServico.
            lista_de_os.append(nova_os)
            ultimo_numero += 1 # Atualizamos o contador do último número.
            salvar_dados(lista_de_os)
            print(f"Sucesso! ordem de serviço número {nova_os['numero_os']} criada.")

        elif opcao == '2':
            print("\n-> Listando todas as ordem de derviço...")
            # Verifica se a lista está vazia antes de tentar percorrê-la.
            lista_de_os = carregar_dados()
            if not lista_de_os:
                print("Ainda não há ordens de serviço cadastradas.")
            else:
                # Laço de Repetição (for): passa por cada item (cada ordemDeServico) na lista.
                for ordemDeServico in lista_de_os:
                    if ordemDeServico == lista_de_os[0]:
                        print(f"{'ID':<5}{'descrição':<20}{'cliente':<15}{'status':<12}{'data de criação':<20}")
                        print("-" * 70)
                    print(f"{ordemDeServico['numero_os']:<5}{ordemDeServico['descricao']:<20}{ordemDeServico['cliente']:<15}{ordemDeServico['status']:<12}{ordemDeServico['data_criacao']:<20}")
                    print("-" * 70)

        elif opcao == '3':
            print("\n-> Relatório de ordem de serviço...")
            lista_de_os = carregar_dados()
            if not lista_de_os:
                print("Nenhuma ordem de serviço para gerar relatório.")
            else:
                # 1. Criamos contadores zerados.
                concluidas = 0
                abertas = 0
                
                for ordemDeServico in lista_de_os:
                    if ordemDeServico['status'].lower() == 'concluída':
                        concluidas += 1
                    else:
                        abertas += 1
                        
                print(f"Total de Ordens de Serviço: {len(lista_de_os)}")
                print(f"Ordens Concluídas: {concluidas}")
                print(f"Ordens Abertas/Em Andamento: {abertas}")
        elif opcao == '4':
            numero_ordem = int(input("Digite o número da ordem de serviço para alterar o status: "))
            encontrou = False
            for ordemDeServico in lista_de_os:
                if ordemDeServico['numero_os'] == numero_ordem:
                    encontrou = True
                    print("\n-> Alterando status da ordem de serviço...")
                    print("1 - Aberta")
                    print("2 - Concluída")
                    print("3 - Cancelada")
                    # print("4 - Voltar")
                    opcao_status = input("Digite o número da opção para alterar o status: ")
                    if opcao_status == '1':
                        ordemDeServico['status'] = 'Aberta'
                    elif opcao_status == '2':
                        ordemDeServico['status'] = 'Concluída'
                    elif opcao_status == '3':
                        ordemDeServico['status'] = 'Cancelada'
                    else:
                        print("Opcao invalida")
            if encontrou == False:
                    print("Ordem de serviço não encontrada.")

            
        elif opcao == '5':
            print("Voltando ao menu principal...")
            break
        
        else:
            print("Opção inválida! Por favor, escolha um número do menu.")

def gerenciar_estoque(lista_de_estoque):

    # Responsável pelo controle de materiais no estoque.
    # Recebe a lista de estoque para poder alterá-la.

    while True:
        print("\n--- Menu de Estoque ---")
        print("1. Cadastrar Novo Material")
        print("2. Ver Estoque")
        print("3. Alterar estoque")
        print("4. Voltar ao Menu Principal")
        opcao = input("Sua escolha: ")

        if opcao == '1':
            print("\n-> Cadastrando novo material...")
            
            # Tratamento de erro: E se o usuário digitar "dez" em vez de "10"?
            # O 'try/except' tenta executar o código. Se der um erro (ValueError),
            # ele executa o bloco 'except' em vez de quebrar o programa.
            try:
                novo_item = {
                    "id": len(lista_de_estoque) + 1,
                    "material": input("Nome do material: "),
                    "quantidade": 0  # Inicialmente, a quantidade é zero.  
                }
                quantidade = int(input("Quantidade inicial do material: "))
                novo_item['quantidade'] = quantidade
                lista_de_estoque.append(novo_item)
                print(f"Material '{novo_item['material']}' cadastrado!")

            except ValueError:
                print("Erro: A quantidade deve ser um número inteiro. Tente novamente.")

        elif opcao == '2':
            print("\n-> Estoque Atual")
            if not lista_de_estoque:
                print("O estoque está vazio.")
            else:
                # Imprime um cabeçalho para a tabela ficar bonita
                print(f"{'ID':<5}{'Material':<20}{'Quantidade'}")
                print("-" * 35)
                for item in lista_de_estoque:
                    # A formatação (<5, <20) alinha o texto, deixando a lista organizada.
                    print(f"{item['id']:<5}{item['material']:<20}{item['quantidade']}")
        
        elif opcao == '3':
            # Alterar Estoque
            # Verifica se a lista de estoque está vazia antes de tentar alterar.
            print("\n-> Alterar Estoque")
            if not lista_de_estoque:
                print("O estoque está vazio. Não há materiais para alterar.")
            # Se a lista não estiver vazia, pedimos o ID do material a ser alterado.
            else:
                # Pedimos o ID do material que o usuário deseja alterar.
                # Usamos 'int' para garantir que o usuário digite um número.
                id_material = int(input("Digite o ID do material que deseja alterar: "))
                material_encontrado = None
                # Percorremos a lista de estoque para encontrar o material com o ID fornecido.
                # Se encontrarmos, guardamos o material em 'material_encontrado'.
                for item in lista_de_estoque:
                    if item['id'] == id_material:
                        material_encontrado = item
                        break
                # Se encontramos o material, pedimos a nova quantidade.
                # Se não encontramos, informamos que o material não foi encontrado.
                if material_encontrado:
                    # Pedimos a nova quantidade.
                    # Usamos 'try/except' para garantir que o usuário digite um número inteiro.
                    # Se o usuário digitar algo que não seja um número, mostramos uma mensagem de erro
                    try:
                        nova_quantidade = int(input(f"Quantidade atual de '{material_encontrado['material']}': {material_encontrado['quantidade']}. Digite a nova quantidade: "))
                        # Atualizamos a quantidade do material encontrado.
                        # Isso altera o dicionário dentro da lista, então a mudança é permanente.
                        material_encontrado['quantidade'] = nova_quantidade + material_encontrado['quantidade']
                        print(f"Quantidade de '{material_encontrado['material']}' atualizada para {material_encontrado['quantidade']}.")
                    except ValueError:
                        print("Erro: A quantidade deve ser um número inteiro. Tente novamente.")
                else:
                    print("Material não encontrado.")
        
        elif opcao == '4':
            print("Voltando ao menu principal...")
            break
        else:
            print("Opção inválida!")

def gerenciar_clientes(lista_de_clientes):
    # Responsável pelo cadastro dos clientes.
    while True:
        print("\n--- Menu de Clientes ---")
        print("1. Cadastrar Novo Cliente")
        print("2. Listar Clientes")
        print("3. Remover Cliente")
        print("4. Voltar ao Menu Principal")
        opcao = input("Sua escolha: ")

        if opcao == '1':
            print("\n-> Cadastrando novo cliente...")
            novo_cliente = {
                "id": len(lista_de_clientes) + 1,
                "nome": input("Nome do cliente: "),
                "telefone": input("Telefone para contato: ")
            }
            lista_de_clientes.append(novo_cliente)
            print(f"Cliente '{novo_cliente['nome']}' cadastrado com sucesso!")
        
        elif opcao == '2':
            print("\n-> Lista de Clientes")
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado.")
            else:
                for cliente in lista_de_clientes:
                    print("-" * 20)
                    print(f"ID: {cliente['id']}")
                    print(f"Nome: {cliente['nome']}")
                    print(f"Telefone: {cliente['telefone']}")

        elif opcao == '3':
            # Remover Cliente
            print("\n-> Remover Cliente")
            # Verifica se a lista de clientes está vazia antes de tentar remover.
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado.")
            # Se a lista não estiver vazia, pedimos o ID do cliente a ser removido.
            else:
                id_cliente = int(input("Digite o ID do cliente que deseja remover: "))
                cliente_removido = None
                # Percorremos a lista de clientes para encontrar o cliente com o ID fornecido.
                # Se encontrarmos, removemos da lista.
                for cliente in lista_de_clientes:
                    if cliente['id'] == id_cliente:
                        cliente_removido = cliente
                        break
                # Se encontramos o cliente, removemos e informamos ao usuário.
                # Se não encontramos, informamos que o cliente não foi encontrado.
                if cliente_removido:
                    lista_de_clientes.remove(cliente_removido)
                    print(f"Cliente '{cliente_removido['nome']}' removido com sucesso!")
                # Se não encontramos o cliente, informamos ao usuário.
                else:
                    print("Cliente não encontrado.")

        elif opcao == '4':
            print("Voltando ao menu principal...")
            break
        else:
            print("Opção inválida!")


# --- FUNÇÃO PRINCIPAL ---
# O "Cérebro" do nosso programa.

def main():
     
    # Listas: Estas são as nossas "bases de dados". Elas vão guardar tudo.
    lista_os_principal = []
    lista_estoque_principal = []
    lista_clientes_principal = []
    
    # Loop principal do programa
    while True:
        opcao_menu = apresentar_menu_principal()
        
        if opcao_menu == '1':
            # Chamamos a função e passamos a lista principal para ela.
            # Qualquer alteração que a função fizer na lista, valerá aqui também.
            gerenciar_ordens_de_servico(lista_os_principal)
            
        elif opcao_menu == '2':
            gerenciar_estoque(lista_estoque_principal)
            
        elif opcao_menu == '3':
            gerenciar_clientes(lista_clientes_principal)
            
        elif opcao_menu == '4':
            print("\nObrigado por usar o sistema. Até logo!")
            break # Encerra o programa
            
        else:
            print("\nErro: Opção não encontrada. Por favor, tente novamente.")

# Esta linha é uma convenção em Python.
# Ela garante que a função main() só será executada quando você rodar este arquivo diretamente.
if __name__ == "__main__":
    main()