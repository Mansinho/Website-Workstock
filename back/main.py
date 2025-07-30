# -*- coding: utf-8 -*-
import json
from datetime import datetime

# --- CONSTANTES DE ARQUIVOS ---
# É uma boa prática definir nomes de arquivos como constantes.
# Facilita a manutenção se precisarmos mudar os nomes depois.
ARQUIVO_OS = 'ordens_de_servico.json'
ARQUIVO_ESTOQUE = 'estoque.json'
ARQUIVO_CLIENTES = 'clientes.json'


# --- FUNÇÕES DE PERSISTÊNCIA DE DADOS (AGORA GENERALIZADAS) ---

def carregar_dados(nome_arquivo):
    """
    Carrega dados de um arquivo JSON específico.
    Recebe o nome do arquivo como parâmetro para ser reutilizável.
    """
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arq:
            return json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio/corrompido, retorna uma lista vazia.
        return []

def salvar_dados(nome_arquivo, dados):
    """
    Salva uma lista de dados (dicionários) em um arquivo JSON.
    Recebe o nome do arquivo e os dados a serem salvos.
    """
    with open(nome_arquivo, 'w', encoding='utf-8') as arq:
        # 'indent=4' formata o arquivo JSON para que seja legível por humanos.
        json.dump(dados, arq, indent=4)

# --- FUNÇÕES DE MENU E GERENCIAMENTO ---

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
    # Para saber o número da próxima ordem de serviço, olhamos o número da última OS na lista.
    # Se a lista estiver vazia, começamos com 0.
    if lista_de_os:
        ultimo_numero = lista_de_os[-1]['numero_os']
    else:
        ultimo_numero = 0

    while True:
        print("\n--- Menu de Ordens de Serviço ---")
        print("1. Criar Nova Ordem de Serviço")
        print("2. Listar Todas as Ordens de Serviço")
        print("3. Ver Relatório Simples")
        print("4. Gerenciar Status da Ordem de Serviço")
        print("5. Voltar ao Menu Principal")
        opcao = input("Sua escolha: ")

        if opcao == '1':
            print("\n-> Criando nova Ordem de Serviço...")
            
            nova_os = {
                "numero_os": ultimo_numero + 1,
                "descricao": input("Descrição do serviço: "),
                "cliente": input("Nome do cliente: "),
                "status": "Aberta", # Status padrão ao criar
                # Usamos o módulo datetime para pegar a data e hora atuais e formatar.
                "data_criacao": datetime.now().strftime('%d/%m/%Y %H:%M') 
            }
            
            lista_de_os.append(nova_os)
            ultimo_numero += 1 # Atualizamos o contador do último número.
            salvar_dados(ARQUIVO_OS, lista_de_os) # **IMPORTANTE: Salva os dados após a alteração**
            print(f"Sucesso! Ordem de serviço número {nova_os['numero_os']} criada.")

        elif opcao == '2':
            print("\n-> Listando todas as Ordens de Serviço...")
            # Não é mais necessário carregar os dados aqui, pois a lista já está em memória.
            if not lista_de_os:
                print("Ainda não há ordens de serviço cadastradas.")
            else:
                # Imprime um cabeçalho formatado para melhor visualização.
                print("-" * 85)
                print(f"{'ID':<5}{'Descrição':<25}{'Cliente':<20}{'Status':<15}{'Data de Criação'}")
                print("-" * 85)
                for os in lista_de_os:
                    print(f"{os['numero_os']:<5}{os['descricao']:<25}{os['cliente']:<20}{os['status']:<15}{os['data_criacao']}")
                print("-" * 85)


        elif opcao == '3':
            print("\n-> Relatório de Ordens de Serviço...")
            if not lista_de_os:
                print("Nenhuma ordem de serviço para gerar relatório.")
            else:
                concluidas = 0
                abertas = 0
                canceladas = 0
                
                # Conta as OS por status. Usar .lower() torna a comparação mais robusta.
                for os in lista_de_os:
                    if os['status'].lower() == 'concluída':
                        concluidas += 1
                    elif os['status'].lower() == 'cancelada':
                        canceladas += 1
                    else: # Considera 'Aberta' e outros possíveis status como não concluídos.
                        abertas += 1
                        
                print(f"Total de Ordens de Serviço: {len(lista_de_os)}")
                print(f"Ordens Concluídas: {concluidas}")
                print(f"Ordens Canceladas: {canceladas}")
                print(f"Ordens Abertas/Em Andamento: {abertas}")

        elif opcao == '4':
            try:
                numero_ordem = int(input("Digite o número da OS para alterar o status: "))
                encontrou = False
                for os in lista_de_os:
                    if os['numero_os'] == numero_ordem:
                        encontrou = True
                        print(f"\n-> Alterando status da OS {numero_ordem} (Status atual: {os['status']})")
                        print("1 - Aberta")
                        print("2 - Concluída")
                        print("3 - Cancelada")
                        
                        opcao_status = input("Digite o número da nova opção de status: ")
                        
                        if opcao_status == '1':
                            os['status'] = 'Aberta'
                        elif opcao_status == '2':
                            os['status'] = 'Concluída'
                        elif opcao_status == '3':
                            os['status'] = 'Cancelada'
                        else:
                            print("Opção de status inválida.")
                            break # Sai do loop 'for' para não salvar uma alteração inválida.
                        
                        salvar_dados(ARQUIVO_OS, lista_de_os) # **IMPORTANTE: Salva os dados após a alteração**
                        print(f"Status da OS {numero_ordem} alterado para '{os['status']}' com sucesso.")
                        break # Sai do loop 'for' pois já encontrou e alterou a OS.
                
                if not encontrou:
                    print("Ordem de serviço não encontrada.")
            except ValueError:
                print("Erro: O número da OS deve ser um valor numérico.")

        elif opcao == '5':
            print("Voltando ao menu principal...")
            break
        
        else:
            print("Opção inválida! Por favor, escolha um número do menu.")

def gerenciar_estoque(lista_de_estoque):
    while True:
        print("\n--- Menu de Estoque ---")
        print("1. Cadastrar Novo Material")
        print("2. Ver Estoque")
        print("3. Alterar quantidade de um material")
        print("4. Voltar ao Menu Principal")
        opcao = input("Sua escolha: ")

        if opcao == '1':
            print("\n-> Cadastrando novo material...")
            try:
                novo_item = {
                    # O ID agora é baseado no tamanho atual da lista, mais seguro que um contador separado.
                    "id": len(lista_de_estoque) + 1,
                    "material": input("Nome do material: "),
                    "quantidade": int(input("Quantidade inicial do material: "))
                }
                lista_de_estoque.append(novo_item)
                salvar_dados(ARQUIVO_ESTOQUE, lista_de_estoque) # **IMPORTANTE: Salva os dados**
                print(f"Material '{novo_item['material']}' cadastrado!")

            except ValueError:
                print("Erro: A quantidade deve ser um número inteiro. Tente novamente.")

        elif opcao == '2':
            print("\n-> Estoque Atual")
            if not lista_de_estoque:
                print("O estoque está vazio.")
            else:
                print("-" * 40)
                print(f"{'ID':<5}{'Material':<25}{'Quantidade'}")
                print("-" * 40)
                for item in lista_de_estoque:
                    print(f"{item['id']:<5}{item['material']:<25}{item['quantidade']}")
                print("-" * 40)
        
        elif opcao == '3':
            print("\n-> Alterar Estoque")
            if not lista_de_estoque:
                print("O estoque está vazio. Não há materiais para alterar.")
                continue

            try:
                id_material = int(input("Digite o ID do material que deseja alterar: "))
                material_encontrado = None
                for item in lista_de_estoque:
                    if item['id'] == id_material:
                        material_encontrado = item
                        break
                
                if material_encontrado:
                    print(f"Material selecionado: '{material_encontrado['material']}' (Quantidade atual: {material_encontrado['quantidade']})")
                    nova_quantidade = int(input(f"Digite a nova quantidade total: "))
                    material_encontrado['quantidade'] = nova_quantidade
                    salvar_dados(ARQUIVO_ESTOQUE, lista_de_estoque) # **IMPORTANTE: Salva os dados**
                    print(f"Quantidade de '{material_encontrado['material']}' atualizada para {material_encontrado['quantidade']}.")
                else:
                    print("Material não encontrado com o ID fornecido.")
            except ValueError:
                print("Erro: O ID e a quantidade devem ser números inteiros.")
        
        elif opcao == '4':
            print("Voltando ao menu principal...")
            break
        else:
            print("Opção inválida!")

def gerenciar_clientes(lista_de_clientes):
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
            salvar_dados(ARQUIVO_CLIENTES, lista_de_clientes) # **IMPORTANTE: Salva os dados**
            print(f"Cliente '{novo_cliente['nome']}' cadastrado com sucesso!")
        
        elif opcao == '2':
            print("\n-> Lista de Clientes")
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado.")
            else:
                print("-" * 50)
                print(f"{'ID':<5}{'Nome':<25}{'Telefone'}")
                print("-" * 50)
                for cliente in lista_de_clientes:
                    print(f"{cliente['id']:<5}{cliente['nome']:<25}{cliente['telefone']}")
                print("-" * 50)

        elif opcao == '3':
            print("\n-> Remover Cliente")
            if not lista_de_clientes:
                print("Nenhum cliente cadastrado para remover.")
                continue
            try:
                id_cliente = int(input("Digite o ID do cliente que deseja remover: "))
                cliente_removido = None
                for cliente in lista_de_clientes:
                    if cliente['id'] == id_cliente:
                        cliente_removido = cliente
                        break
                
                if cliente_removido:
                    lista_de_clientes.remove(cliente_removido)
                    salvar_dados(ARQUIVO_CLIENTES, lista_de_clientes) # **IMPORTANTE: Salva os dados**
                    print(f"Cliente '{cliente_removido['nome']}' removido com sucesso!")
                else:
                    print("Cliente não encontrado com o ID fornecido.")
            except ValueError:
                print("Erro: O ID deve ser um número.")

        elif opcao == '4':
            print("Voltando ao menu principal...")
            break
        else:
            print("Opção inválida!")

# --- FUNÇÃO PRINCIPAL ---
# O "Cérebro" do nosso programa.
def main():
    """
    Função principal que inicia o programa, carrega os dados
    e gerencia o loop do menu principal.
    """
    # **IMPORTANTE**: Carrega todos os dados dos arquivos ao iniciar o programa.
    # Se os arquivos não existirem, as funções de carregar retornarão listas vazias.
    lista_os_principal = carregar_dados(ARQUIVO_OS)
    lista_estoque_principal = carregar_dados(ARQUIVO_ESTOQUE)
    lista_clientes_principal = carregar_dados(ARQUIVO_CLIENTES)
    
    print("Bem-vindo ao Sistema de Gerenciamento!")

    while True:
        opcao_menu = apresentar_menu_principal()
        
        if opcao_menu == '1':
            # Passamos a lista principal para a função.
            # Qualquer alteração que a função fizer na lista (que é um objeto mutável),
            # será refletida aqui na função main.
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

# --- PONTO DE ENTRADA DO SCRIPT ---
# Esta linha é uma convenção em Python.
# Ela garante que a função main() só será executada quando você rodar este arquivo diretamente.
if __name__ == "__main__":
    main()