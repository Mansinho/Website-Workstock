# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# --- CONSTANTES ---
ARQUIVO_OS = 'ordens_de_servico.json'
ARQUIVO_ESTOQUE = 'estoque.json'
ARQUIVO_CLIENTES = 'clientes.json'

# --- FUNÇÕES DE PERSISTÊNCIA DE DADOS (Inalteradas) ---

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

# --- CLASSES DE MODELO (Inalteradas) ---

class Cliente:
    """Representa um cliente no sistema."""
    def __init__(self, id, nome, telefone):
        self.id = id
        self.nome = nome
        self.telefone = telefone

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'telefone': self.telefone}

class ItemEstoque:
    """Representa um item no estoque."""
    def __init__(self, id, material, quantidade):
        self.id = id
        self.material = material
        self.quantidade = quantidade

    def to_dict(self):
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
        return {
            'numero_os': self.numero_os,
            'descricao': self.descricao,
            'cliente': self.cliente,
            'status': self.status,
            'data_criacao': self.data_criacao
        }

# --- CLASSES DA INTERFACE GRÁFICA (GUI com Tkinter) ---

class App(tk.Tk):
    """Classe principal da aplicação, que gerencia as janelas e frames."""
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento Integrado")
        self.geometry("800x600")

        # Container principal
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Adiciona as telas (frames) ao dicionário
        for F in (TelaInicial, TelaClientes, TelaEstoque, TelaOS):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("TelaInicial")

    def mostrar_frame(self, page_name):
        """Mostra um frame para a página solicitada."""
        frame = self.frames[page_name]
        frame.tkraise()
        # Chama o método 'atualizar' se ele existir no frame
        if hasattr(frame, 'atualizar'):
            frame.atualizar()

class TelaInicial(tk.Frame):
    """Tela de boas-vindas com os botões de navegação."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="MENU PRINCIPAL", font=("Helvetica", 16, "bold"))
        label.pack(pady=20)

        btn_os = ttk.Button(self, text="Ordens de Serviço", command=lambda: controller.mostrar_frame("TelaOS"))
        btn_os.pack(pady=10, ipadx=20, ipady=5)

        btn_estoque = ttk.Button(self, text="Gerenciar Estoque", command=lambda: controller.mostrar_frame("TelaEstoque"))
        btn_estoque.pack(pady=10, ipadx=20, ipady=5)

        btn_clientes = ttk.Button(self, text="Gerenciar Clientes", command=lambda: controller.mostrar_frame("TelaClientes"))
        btn_clientes.pack(pady=10, ipadx=20, ipady=5)

        btn_sair = ttk.Button(self, text="Sair do Programa", command=controller.destroy)
        btn_sair.pack(pady=10, ipadx=20, ipady=5)


class TelaClientes(tk.Frame):
    """Frame para gerenciar os clientes."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.arquivo = ARQUIVO_CLIENTES
        self._carregar()

        # --- Layout ---
        ttk.Label(self, text="Gerenciamento de Clientes", font=("Helvetica", 14, "bold")).pack(pady=10)

        # --- Formulário de Cadastro ---
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Telefone:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.telefone_entry = ttk.Entry(form_frame, width=40)
        self.telefone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        form_frame.grid_columnconfigure(1, weight=1)

        # --- Botões ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cadastrar Cliente", command=self.cadastrar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Remover Selecionado", command=self.remover).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Voltar ao Menu", command=lambda: controller.mostrar_frame("TelaInicial")).pack(side="left", padx=5)

        # --- Treeview para Listar ---
        cols = ('ID', 'Nome', 'Telefone')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.atualizar_lista()

    def _carregar(self):
        dados = carregar_dados(self.arquivo)
        self.clientes = [Cliente(**c) for c in dados]

    def _salvar(self):
        dados_para_salvar = [c.to_dict() for c in self.clientes]
        salvar_dados(self.arquivo, dados_para_salvar)

    def _proximo_id(self):
        return self.clientes[-1].id + 1 if self.clientes else 1

    def atualizar_lista(self):
        """Limpa e recarrega a lista de clientes na Treeview."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for cliente in self.clientes:
            self.tree.insert("", "end", values=(cliente.id, cliente.nome, cliente.telefone))

    def cadastrar(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        if not nome or not telefone:
            messagebox.showerror("Erro", "Nome e telefone são obrigatórios.")
            return
        
        novo_cliente = Cliente(id=self._proximo_id(), nome=nome, telefone=telefone)
        self.clientes.append(novo_cliente)
        self._salvar()
        messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!")
        self.nome_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.atualizar_lista()

    def remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um cliente para remover.")
            return

        item_id = self.tree.item(selecionado[0])['values'][0]
        cliente_a_remover = next((c for c in self.clientes if c.id == item_id), None)

        if cliente_a_remover:
            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o cliente '{cliente_a_remover.nome}'?"):
                self.clientes.remove(cliente_a_remover)
                self._salvar()
                messagebox.showinfo("Sucesso", "Cliente removido.")
                self.atualizar_lista()

    def atualizar(self):
        """Método chamado quando a tela se torna visível."""
        self._carregar()
        self.atualizar_lista()


class TelaEstoque(tk.Frame):
    """Frame para gerenciar o estoque."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.arquivo = ARQUIVO_ESTOQUE
        self._carregar()

        # --- Layout ---
        ttk.Label(self, text="Gerenciamento de Estoque", font=("Helvetica", 14, "bold")).pack(pady=10)

        # --- Formulário de Cadastro ---
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Material:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.material_entry = ttk.Entry(form_frame, width=40)
        self.material_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.quantidade_entry = ttk.Entry(form_frame, width=40)
        self.quantidade_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        form_frame.grid_columnconfigure(1, weight=1)

        # --- Botões ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cadastrar Material", command=self.cadastrar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar Quantidade", command=self.alterar_quantidade).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Voltar ao Menu", command=lambda: controller.mostrar_frame("TelaInicial")).pack(side="left", padx=5)

        # --- Treeview para Listar ---
        cols = ('ID', 'Material', 'Quantidade')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.atualizar_lista()

    def _carregar(self):
        dados = carregar_dados(self.arquivo)
        self.estoque = [ItemEstoque(**item) for item in dados]

    def _salvar(self):
        dados_para_salvar = [item.to_dict() for item in self.estoque]
        salvar_dados(self.arquivo, dados_para_salvar)

    def _proximo_id(self):
        return self.estoque[-1].id + 1 if self.estoque else 1

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.estoque:
            self.tree.insert("", "end", values=(item.id, item.material, item.quantidade))

    def cadastrar(self):
        material = self.material_entry.get()
        try:
            quantidade = int(self.quantidade_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
            return

        if not material:
            messagebox.showerror("Erro", "O nome do material é obrigatório.")
            return
        
        novo_item = ItemEstoque(id=self._proximo_id(), material=material, quantidade=quantidade)
        self.estoque.append(novo_item)
        self._salvar()
        messagebox.showinfo("Sucesso", f"Material '{material}' cadastrado!")
        self.material_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.atualizar_lista()

    def alterar_quantidade(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um item para alterar.")
            return

        item_id = self.tree.item(selecionado[0])['values'][0]
        item_a_alterar = next((item for item in self.estoque if item.id == item_id), None)

        if item_a_alterar:
            nova_quantidade = simpledialog.askinteger("Alterar Quantidade", 
                                                      f"Digite a nova quantidade para '{item_a_alterar.material}':",
                                                      parent=self,
                                                      minvalue=0)
            if nova_quantidade is not None:
                item_a_alterar.quantidade = nova_quantidade
                self._salvar()
                messagebox.showinfo("Sucesso", "Quantidade atualizada.")
                self.atualizar_lista()
    
    def atualizar(self):
        self._carregar()
        self.atualizar_lista()


class TelaOS(tk.Frame):
    """Frame para gerenciar as Ordens de Serviço."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.arquivo = ARQUIVO_OS
        self._carregar()

        # --- Layout ---
        ttk.Label(self, text="Gerenciamento de Ordens de Serviço", font=("Helvetica", 14, "bold")).pack(pady=10)

        # --- Formulário de Criação ---
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(form_frame, text="Descrição:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.descricao_entry = ttk.Entry(form_frame, width=40)
        self.descricao_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Cliente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cliente_combo = ttk.Combobox(form_frame, width=38)
        self.cliente_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        form_frame.grid_columnconfigure(1, weight=1)

        # --- Botões ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Criar OS", command=self.criar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar Status", command=self.alterar_status).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Gerar Relatório", command=self.gerar_relatorio).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Voltar ao Menu", command=lambda: controller.mostrar_frame("TelaInicial")).pack(side="left", padx=5)

        # --- Treeview para Listar ---
        cols = ('Nº OS', 'Descrição', 'Cliente', 'Status', 'Data de Criação')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.atualizar_lista()

    def _carregar(self):
        dados_os = carregar_dados(self.arquivo)
        self.ordens_servico = [OrdemServico(**os) for os in dados_os]
        
        dados_clientes = carregar_dados(ARQUIVO_CLIENTES)
        self.clientes = [Cliente(**c) for c in dados_clientes]

    def _salvar(self):
        dados_para_salvar = [os.to_dict() for os in self.ordens_servico]
        salvar_dados(self.arquivo, dados_para_salvar)

    def _proximo_numero_os(self):
        return self.ordens_servico[-1].numero_os + 1 if self.ordens_servico else 1
    
    def atualizar_combobox_clientes(self):
        """Atualiza a lista de clientes no combobox."""
        nomes_clientes = [c.nome for c in self.clientes]
        self.cliente_combo['values'] = nomes_clientes

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for os in self.ordens_servico:
            self.tree.insert("", "end", values=(os.numero_os, os.descricao, os.cliente, os.status, os.data_criacao))

    def criar(self):
        descricao = self.descricao_entry.get()
        cliente = self.cliente_combo.get()
        if not descricao or not cliente:
            messagebox.showerror("Erro", "Descrição e cliente são obrigatórios.")
            return
        
        nova_os = OrdemServico(numero_os=self._proximo_numero_os(), descricao=descricao, cliente=cliente)
        self.ordens_servico.append(nova_os)
        self._salvar()
        messagebox.showinfo("Sucesso", f"Ordem de serviço número {nova_os.numero_os} criada.")
        self.descricao_entry.delete(0, tk.END)
        self.cliente_combo.set('')
        self.atualizar_lista()

    def alterar_status(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma OS para alterar o status.")
            return

        os_id = self.tree.item(selecionado[0])['values'][0]
        os_a_alterar = next((os for os in self.ordens_servico if os.numero_os == os_id), None)

        if os_a_alterar:
            # Criar uma janela Toplevel para a escolha do status
            top = tk.Toplevel(self)
            top.title("Alterar Status")
            top.geometry("250x150")
            
            ttk.Label(top, text=f"Novo status para OS nº {os_id}:").pack(pady=10)
            
            novo_status_var = tk.StringVar()
            status_options = ["Aberta", "Concluída", "Cancelada"]
            combo = ttk.Combobox(top, textvariable=novo_status_var, values=status_options, state="readonly")
            combo.pack(pady=5)
            combo.set(os_a_alterar.status)

            def confirmar():
                novo_status = novo_status_var.get()
                if novo_status:
                    os_a_alterar.status = novo_status
                    self._salvar()
                    messagebox.showinfo("Sucesso", f"Status da OS {os_id} alterado para '{novo_status}'.")
                    self.atualizar_lista()
                    top.destroy()

            ttk.Button(top, text="Confirmar", command=confirmar).pack(pady=10)

    def gerar_relatorio(self):
        if not self.ordens_servico:
            messagebox.showinfo("Relatório", "Nenhuma ordem de serviço para gerar relatório.")
            return
        
        status_counts = {'Concluída': 0, 'Cancelada': 0, 'Aberta': 0}
        for os in self.ordens_servico:
            status = os.status
            if status in status_counts:
                status_counts[status] += 1
            else: # Trata status desconhecidos como 'Aberta'
                status_counts['Aberta'] += 1
        
        total = len(self.ordens_servico)
        relatorio_texto = (
            f"Total de Ordens de Serviço: {total}\n\n"
            f"Ordens Concluídas: {status_counts['Concluída']}\n"
            f"Ordens Canceladas: {status_counts['Cancelada']}\n"
            f"Ordens Abertas/Em Andamento: {status_counts['Aberta']}"
        )
        messagebox.showinfo("Relatório de Ordens de Serviço", relatorio_texto)

    def atualizar(self):
        """Método chamado quando a tela se torna visível para recarregar os dados."""
        self._carregar()
        self.atualizar_lista()
        self.atualizar_combobox_clientes()


# --- PONTO DE ENTRADA DO SCRIPT ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
