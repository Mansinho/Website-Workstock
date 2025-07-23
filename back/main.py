from datetime import datetime

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
    """
    Responsável por tudo relacionado às Ordens de Serviço (OS).
    Recebe a 'lista_de_os' como um "parâmetro" para que possa adicionar ou ler os dados dela.
    """
    # Para saber o número da próxima OS, olhamos o número da última OS na lista.
    # Se a lista estiver vazia, começamos com 0.
    if lista_de_os:
        ultimo_numero = lista_de_os[-1]['numero_os']
    else:
        ultimo_numero = 0

    # Laço de Repetição (while): mantém o usuário no menu de OS até ele decidir sair.
    while True:
        print("\n--- Menu de Ordens de Serviço ---")
        print("1. Criar Nova OS")
        print("2. Listar Todas as OS")
        print("3. Ver Relatório Simples")
        print("4. Voltar ao Menu Principal")
        opcao = input("Sua escolha: ")

        # Condicional (if/elif/else): decide o que fazer com base na escolha do usuário.
        if opcao == '1':
            print("\n-> Criando nova OS...")
            
            # Cada OS será um Dicionário. Dicionários são ótimos para organizar
            # informações com "chave" e "valor" (ex: "nome": "João").
            nova_os = {
                "numero_os": ultimo_numero + 1,
                "descricao": input("Descrição do serviço: "),
                "cliente": input("Nome do cliente: "),
                "status": "Abertta", # Status padrão ao criar
                # Usamos o módulo datetime para pegar a data e hora atuais.
                "data_criacao": datetime.now().strftime('%d/%m/%Y %H:%M') 
            }
            
            # Adicionamos o novo dicionário (a nova OS) na nossa lista principal de OS.
            lista_de_os.append(nova_os)
            ultimo_numero += 1 # Atualizamos o contador do último número.
            
            print(f"Sucesso! OS número {nova_os['numero_os']} criada.")

        elif opcao == '2':
            print("\n-> Listando todas as OS...")
            # Verifica se a lista está vazia antes de tentar percorrê-la.
            if not lista_de_os:
                print("Ainda não há Ordens de Serviço cadastradas.")
            else:
                # Laço de Repetição (for): passa por cada item (cada OS) na lista.
                for os in lista_de_os:
                    print("-" * 20) # Uma linha para separar visualmente
                    print(f"Número: {os['numero_os']}")
                    print(f"Descrição: {os['descricao']}")
                    print(f"Cliente: {os['cliente']}")
                    print(f"Status: {os['status']}")
                    print(f"Data de Criação: {os['data_criacao']}")

        elif opcao == '3':
            print("\n-> Relatório de OS...")
            if not lista_de_os:
                print("Nenhuma OS para gerar relatório.")
            else:
                # Lógica simplificada para contar, ideal para iniciantes:
                # 1. Criamos contadores zerados.
                concluidas = 0
                abertas = 0
                
                # 2. Usamos um laço 'for' para checar cada OS uma por uma.
                for os in lista_de_os:
                    # 3. Usamos um 'if' para ver o status e incrementar o contador certo.
                    if os['status'].lower() == 'concluída':
                        concluidas += 1
                    else:
                        abertas += 1
                        
                print(f"Total de Ordens de Serviço: {len(lista_de_os)}")
                print(f"Ordens Concluídas: {concluidas}")
                print(f"Ordens Abertas/Em Andamento: {abertas}")
        
        elif opcao == '4':
            print("Voltando ao menu principal...")
            break # 'break' é o comando que quebra o laço 'while' e encerra o menu de OS.
        
        else:
            print("Opção inválida! Por favor, escolha um número do menu.")

def gerenciar_estoque(lista_de_estoque):

    # Responsável pelo controle de materiais no estoque.
    # Recebe a lista de estoque para poder alterá-la.

    while True:
        print("\n--- Menu de Estoque ---")
        print("1. Cadastrar Novo Material")
        print("2. Ver Estoque")
        print("3. Voltar ao Menu Principal")
        opcao = input("Sua escolha: ")

        if opcao == '1':
            print("\n-> Cadastrando novo material...")
            
            # Tratamento de erro: E se o usuário digitar "dez" em vez de "10"?
            # O 'try/except' tenta executar o código. Se der um erro (ValueError),
            # ele executa o bloco 'except' em vez de quebrar o programa.
            try:
                quantidade = int(input("Quantidade inicial do material: "))
                
                novo_item = {
                    "id": len(lista_de_estoque) + 1,
                    "material": input("Nome do material: "),
                    "quantidade": quantidade
                }
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
        print("3. Voltar ao Menu Principal")
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