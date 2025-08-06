# -*- coding: utf-8 -*-
import json
from datetime import datetime

# --- CONSTANTES ---
ARQUIVO_OS = 'ordens_de_servico.json'
ARQUIVO_ESTOQUE = 'estoque.json'
ARQUIVO_CLIENTES = 'clientes.json'

# --- FUNÇÕES DE PERSISTÊNCIA DE DADOS ---

def carregar_dados(nome_arquivo):
    """Carrega dados de um arquivo JSON. Retorna uma lista vazia se o arquivo não existir ou estiver corrompido."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(nome_arquivo, dados):
    """Salva uma lista de dicionários em um arquivo JSON com formatação legível."""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# --- CLASSES DE MODELO ---

class Cliente:
    """Representa um cliente no sistema."""
    def __init__(self, id, nome, telefone):
        self.id = id
        self.nome = nome
        self.telefone = telefone

    def to_dict(self):
        """Converte o objeto Cliente para um dicionário para serialização JSON."""
        return {'id': self.id, 'nome': self.nome, 'telefone': self.telefone}

class ItemEstoque:
    """Representa um item no estoque."""
    def __init__(self, id, material, quantidade):
        self.id = id
        self.material = material
        self.quantidade = quantidade

    def to_dict(self):
        """Converte o objeto ItemEstoque para um dicionário."""
        return {'id': self.id, 'material': self.material, 'quantidade': self.quantidade}

class OrdemServico:
    """Representa uma Ordem de Serviço."""
    def __init__(self, numero_os, descricao, cliente, status="Aberta", data_criacao=None):
        self.numero_os = numero_os
        self.descricao = descricao
        self.cliente = cliente
        self.status = status
        self.data_criacao = data_criacao or datetime.now().strftime('%d/%m/%Y %H:%M')

    def to_dict(self):
        """Converte o objeto OrdemServico para um dicionário."""
        return {
            'numero_os': self.numero_os,
            'descricao': self.descricao,
            'cliente': self.cliente,
            'status': self.status,
            'data_criacao': self.data_criacao
        }

# --- CLASSES GERENCIADORAS ---

class GerenciadorClientes:
    """Gerencia o cadastro, listagem e remoção de clientes."""
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self._carregar()

    def _carregar(self):
        """Carrega os clientes do arquivo JSON, convertendo dicionários em objetos Cliente."""
        dados = carregar_dados(self.arquivo)
        self.clientes = [Cliente(**c) for c in dados]

    def _salvar(self):
        """Salva a lista de clientes no arquivo JSON."""
        dados_para_salvar = [c.to_dict() for c in self.clientes]
        salvar_dados(self.arquivo, dados_para_salvar)

    def _proximo_id(self):
        """Calcula o próximo ID disponível para um novo cliente."""
        return self.clientes[-1].id + 1 if self.clientes else 1
    
    def buscar_por_id(self, id_cliente):
        """Busca um cliente pelo seu ID."""
        for cliente in self.clientes:
            if cliente.id == id_cliente:
                return cliente
        return None

    def cadastrar(self):
        """Solicita os dados e cadastra um novo cliente."""
        print("\n-> Cadastrando novo cliente...")
        nome = input("Nome do cliente: ")
        telefone = input("Telefone para contato: ")
        
        novo_cliente = Cliente(id=self._proximo_id(), nome=nome, telefone=telefone)
        self.clientes.append(novo_cliente)
        self._salvar()
        print(f"Cliente '{novo_cliente.nome}' cadastrado com sucesso!")

    def listar(self):
        """Exibe uma lista formatada de todos os clientes."""
        print("\n-> Lista de Clientes")
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return
            
        print("-" * 50)
        print(f"{'ID':<5}{'Nome':<25}{'Telefone'}")
        print("-" * 50)
        for cliente in self.clientes:
            print(f"{cliente.id:<5}{cliente.nome:<25}{cliente.telefone}")
        print("-" * 50)

    def remover(self):
        """Solicita um ID e remove o cliente correspondente."""
        print("\n-> Remover Cliente")
        if not self.clientes:
            print("Nenhum cliente para remover.")
            return

        try:
            id_cliente = int(input("Digite o ID do cliente que deseja remover: "))
            cliente = self.buscar_por_id(id_cliente)

            if cliente:
                self.clientes.remove(cliente)
                self._salvar()
                print(f"Cliente '{cliente.nome}' removido com sucesso!")
            else:
                print("Cliente não encontrado com o ID fornecido.")
        except ValueError:
            print("Erro: O ID deve ser um número.")

    def menu(self):
        """Exibe o menu de gerenciamento de clientes e processa a escolha do usuário."""
        while True:
            print("\n--- Menu de Clientes ---")
            print("1. Cadastrar Novo Cliente")
            print("2. Listar Clientes")
            print("3. Remover Cliente")
            print("4. Voltar ao Menu Principal")
            opcao = input("Sua escolha: ")

            if opcao == '1': self.cadastrar()
            elif opcao == '2': self.listar()
            elif opcao == '3': self.remover()
            elif opcao == '4':
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida!")


class GerenciadorEstoque:
    """Gerencia o cadastro e a atualização de itens de estoque."""
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self._carregar()

    def _carregar(self):
        """Carrega os itens do arquivo JSON, convertendo-os em objetos ItemEstoque."""
        dados = carregar_dados(self.arquivo)
        self.estoque = [ItemEstoque(**item) for item in dados]
        
    def _salvar(self):
        """Salva a lista de itens de estoque no arquivo JSON."""
        dados_para_salvar = [item.to_dict() for item in self.estoque]
        salvar_dados(self.arquivo, dados_para_salvar)
        
    def _proximo_id(self):
        return self.estoque[-1].id + 1 if self.estoque else 1

    def buscar_por_id(self, id_material):
        for item in self.estoque:
            if item.id == id_material:
                return item
        return None

    def cadastrar(self):
        print("\n-> Cadastrando novo material...")
        try:
            material = input("Nome do material: ")
            quantidade = int(input("Quantidade inicial do material: "))
            novo_item = ItemEstoque(id=self._proximo_id(), material=material, quantidade=quantidade)
            self.estoque.append(novo_item)
            self._salvar()
            print(f"Material '{novo_item.material}' cadastrado!")
        except ValueError:
            print("Erro: A quantidade deve ser um número inteiro.")

    def listar(self):
        print("\n-> Estoque Atual")
        if not self.estoque:
            print("O estoque está vazio.")
            return
            
        print("-" * 40)
        print(f"{'ID':<5}{'Material':<25}{'Quantidade'}")
        print("-" * 40)
        for item in self.estoque:
            print(f"{item.id:<5}{item.material:<25}{item.quantidade}")
        print("-" * 40)
        
    def alterar_quantidade(self):
        print("\n-> Alterar Estoque")
        if not self.estoque:
            print("O estoque está vazio. Não há materiais para alterar.")
            return

        try:
            id_material = int(input("Digite o ID do material que deseja alterar: "))
            item = self.buscar_por_id(id_material)
            
            if item:
                print(f"Material selecionado: '{item.material}' (Quantidade atual: {item.quantidade})")
                nova_quantidade = int(input("Digite a nova quantidade total: "))
                item.quantidade = nova_quantidade
                self._salvar()
                print(f"Quantidade de '{item.material}' atualizada.")
            else:
                print("Material não encontrado com o ID fornecido.")
        except ValueError:
            print("Erro: O ID e a quantidade devem ser números inteiros.")

    def menu(self):
        while True:
            print("\n--- Menu de Estoque ---")
            print("1. Cadastrar Novo Material")
            print("2. Ver Estoque")
            print("3. Alterar quantidade de um material")
            print("4. Voltar ao Menu Principal")
            opcao = input("Sua escolha: ")

            if opcao == '1': self.cadastrar()
            elif opcao == '2': self.listar()
            elif opcao == '3': self.alterar_quantidade()
            elif opcao == '4':
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida!")


class GerenciadorOS:
    """Gerencia a criação, listagem e atualização de Ordens de Serviço."""
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self._carregar()

    def _carregar(self):
        dados = carregar_dados(self.arquivo)
        self.ordens_servico = [OrdemServico(**os) for os in dados]

    def _salvar(self):
        dados_para_salvar = [os.to_dict() for os in self.ordens_servico]
        salvar_dados(self.arquivo, dados_para_salvar)

    def _proximo_numero_os(self):
        return self.ordens_servico[-1].numero_os + 1 if self.ordens_servico else 1

    def buscar_por_numero(self, numero_os):
        for os in self.ordens_servico:
            if os.numero_os == numero_os:
                return os
        return None

    def criar(self):
        print("\n-> Criando nova Ordem de Serviço...")
        descricao = input("Descrição do serviço: ")
        cliente = input("Nome do cliente: ")
        
        nova_os = OrdemServico(
            numero_os=self._proximo_numero_os(),
            descricao=descricao,
            cliente=cliente
        )
        self.ordens_servico.append(nova_os)
        self._salvar()
        print(f"Sucesso! Ordem de serviço número {nova_os.numero_os} criada.")

    def listar(self):
        print("\n-> Listando todas as Ordens de Serviço...")
        if not self.ordens_servico:
            print("Ainda não há ordens de serviço cadastradas.")
            return

        print("-" * 85)
        print(f"{'ID':<5}{'Descrição':<25}{'Cliente':<20}{'Status':<15}{'Data de Criação'}")
        print("-" * 85)
        for os in self.ordens_servico:
            print(f"{os.numero_os:<5}{os.descricao:<25}{os.cliente:<20}{os.status:<15}{os.data_criacao}")
        print("-" * 85)

    def gerar_relatorio(self):
        print("\n-> Relatório de Ordens de Serviço...")
        if not self.ordens_servico:
            print("Nenhuma ordem de serviço para gerar relatório.")
            return
            
        # Contadores para cada status
        status_counts = {'concluída': 0, 'cancelada': 0, 'aberta': 0}
        for os in self.ordens_servico:
            status = os.status.lower()
            if status in status_counts:
                status_counts[status] += 1
            else:
                # Trata outros status como 'abertos' ou 'em andamento'
                status_counts['aberta'] += 1
                
        print(f"Total de Ordens de Serviço: {len(self.ordens_servico)}")
        print(f"Ordens Concluídas: {status_counts['concluída']}")
        print(f"Ordens Canceladas: {status_counts['cancelada']}")
        print(f"Ordens Abertas/Em Andamento: {status_counts['aberta']}")

    def alterar_status(self):
        try:
            numero_ordem = int(input("Digite o número da OS para alterar o status: "))
            os_encontrada = self.buscar_por_numero(numero_ordem)

            if not os_encontrada:
                print("Ordem de serviço não encontrada.")
                return

            print(f"\n-> Alterando status da OS {numero_ordem} (Status atual: {os_encontrada.status})")
            print("1 - Aberta\n2 - Concluída\n3 - Cancelada")
            opcao_status = input("Digite o número da nova opção de status: ")

            novos_status = {'1': 'Aberta', '2': 'Concluída', '3': 'Cancelada'}
            
            if opcao_status in novos_status:
                os_encontrada.status = novos_status[opcao_status]
                self._salvar()
                print(f"Status da OS {numero_ordem} alterado para '{os_encontrada.status}' com sucesso.")
            else:
                print("Opção de status inválida.")

        except ValueError:
            print("Erro: O número da OS deve ser um valor numérico.")

    def menu(self):
        while True:
            print("\n--- Menu de Ordens de Serviço ---")
            print("1. Criar Nova Ordem de Serviço")
            print("2. Listar Todas as Ordens de Serviço")
            print("3. Ver Relatório Simples")
            print("4. Gerenciar Status da Ordem de Serviço")
            print("5. Voltar ao Menu Principal")
            opcao = input("Sua escolha: ")

            if opcao == '1': self.criar()
            elif opcao == '2': self.listar()
            elif opcao == '3': self.gerar_relatorio()
            elif opcao == '4': self.alterar_status()
            elif opcao == '5':
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida! Por favor, escolha um número do menu.")


# --- CLASSE PRINCIPAL DO SISTEMA ---

class Sistema:
    """Classe principal que orquestra o sistema de gerenciamento."""
    def __init__(self):
        """Inicializa os gerenciadores de cada módulo do sistema."""
        self.gerenciador_os = GerenciadorOS(ARQUIVO_OS)
        self.gerenciador_estoque = GerenciadorEstoque(ARQUIVO_ESTOQUE)
        self.gerenciador_clientes = GerenciadorClientes(ARQUIVO_CLIENTES)

    def apresentar_menu_principal(self):
        """Exibe o menu principal e retorna a opção escolhida pelo usuário."""
        print("\n========= MENU PRINCIPAL =========")
        print("1. Ordens de Serviço")
        print("2. Gerenciar Estoque")
        print("3. Gerenciar Clientes")
        print("4. Sair do Programa")
        print("==================================")
        return input("Digite o número da sua escolha: ")

    def executar(self):
        """Inicia o loop principal do programa."""
        print("Bem-vindo ao Sistema de Gerenciamento!")
        while True:
            opcao = self.apresentar_menu_principal()
            
            if opcao == '1': self.gerenciador_os.menu()
            elif opcao == '2': self.gerenciador_estoque.menu()
            elif opcao == '3': self.gerenciador_clientes.menu()
            elif opcao == '4':
                print("\nObrigado por usar o sistema. Até logo!")
                break
            else:
                print("\nErro: Opção não encontrada. Por favor, tente novamente.")

# --- PONTO DE ENTRADA DO SCRIPT ---
if __name__ == "__main__":
    app = Sistema()
    app.executar()