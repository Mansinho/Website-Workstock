# gui_app.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import database as db # Importa nosso módulo de banco de dados

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---
class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestão de Reformas")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.logged_in_user = None

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Adiciona as novas telas de Login e Cadastro
        for F in (LoginScreen, RegisterScreen, DashboardScreen, GerenciarOS, GerenciarEstoque, GerenciarClientes):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        # Chama a função de atualização se ela existir na tela
        if hasattr(frame, 'atualizar_tela'):
            frame.atualizar_tela()
        frame.tkraise()

    def attempt_login(self, username, password):
        user_data = db.autenticar_usuario(username, password)
        if user_data:
            self.logged_in_user = user_data
            messagebox.showinfo("Sucesso", f"Bem-vindo, {self.logged_in_user['username']}!")
            self.show_frame("DashboardScreen")
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")

# --- TELA DE LOGIN ---
class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(50, 20))
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuário", width=250)
        self.entry_user.pack(pady=10)
        
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=250)
        self.entry_pass.pack(pady=10)
        
        ctk.CTkButton(self, text="Entrar", command=self.login).pack(pady=20)
        ctk.CTkButton(self, text="Cadastrar-se", fg_color="transparent", hover=False, 
                      command=lambda: controller.show_frame("RegisterScreen")).pack()
                      
    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        self.controller.attempt_login(username, password)

# --- TELA DE CADASTRO ---
class RegisterScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="Cadastro de Usuário", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(50, 20))
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Escolha um nome de usuário", width=250)
        self.entry_user.pack(pady=10)
        
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Crie uma senha", show="*", width=250)
        self.entry_pass.pack(pady=10)
        
        # Seleção de perfil conforme o documento de requisitos
        ctk.CTkLabel(self, text="Tipo de Perfil:").pack(pady=(10,0))
        self.option_type = ctk.CTkOptionMenu(self, values=["Empresa de Reforma", "Proprietário", "Cliente (Inquilino)"])
        self.option_type.pack(pady=10)
        
        ctk.CTkButton(self, text="Registrar", command=self.register).pack(pady=20)
        ctk.CTkButton(self, text="Voltar para Login", fg_color="transparent", hover=False,
                      command=lambda: controller.show_frame("LoginScreen")).pack()

    def register(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        user_type = self.option_type.get()
        
        success, message = db.registrar_usuario(username, password, user_type)
        
        if success:
            messagebox.showinfo("Sucesso", message)
            self.controller.show_frame("LoginScreen")
        else:
            messagebox.showerror("Erro de Cadastro", message)
            
# --- TELA DE DASHBOARD (MENU PÓS-LOGIN) ---
class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label_title = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=20, padx=10)

        # Frame para os botões do menu
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(pady=20)

        # Botão de Logout
        ctk.CTkButton(self, text="Logout", fg_color="red", hover_color="#C10000",
                      command=self.logout).pack(side="bottom", pady=20)

    def atualizar_tela(self):
        # Limpa os botões antigos
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        if not self.controller.logged_in_user:
            return

        user_type = self.controller.logged_in_user.get('user_type')
        username = self.controller.logged_in_user.get('username')
        
        self.label_title.configure(text=f"Dashboard - {username} ({user_type})")

        # Mostra o menu de acordo com o tipo de usuário
        if user_type == "Empresa de Reforma":
            ctk.CTkButton(self.menu_frame, text="Ordens de Serviço", 
                          command=lambda: self.controller.show_frame("GerenciarOS")).pack(pady=10)
            ctk.CTkButton(self.menu_frame, text="Gerenciar Estoque",
                          command=lambda: self.controller.show_frame("GerenciarEstoque")).pack(pady=10)
            ctk.CTkButton(self.menu_frame, text="Gerenciar Clientes",
                          command=lambda: self.controller.show_frame("GerenciarClientes")).pack(pady=10)
        elif user_type == "Proprietário":
            ctk.CTkLabel(self.menu_frame, text="Visualizar status de reformas").pack(pady=10)
            ctk.CTkLabel(self.menu_frame, text="Aprovar orçamentos").pack(pady=10)
            # Botões desabilitados por enquanto
        elif user_type == "Cliente (Inquilino)":
            ctk.CTkLabel(self.menu_frame, text="Registrar solicitações de reparo").pack(pady=10)
            ctk.CTkLabel(self.menu_frame, text="Acompanhar status").pack(pady=10)
            # Botões desabilitados por enquanto
    
    def logout(self):
        self.controller.logged_in_user = None
        self.controller.show_frame("LoginScreen")

# --- AS TELAS DE GERENCIAMENTO (CÓDIGO ANTERIOR ADAPTADO) ---
# O código das classes GerenciarOS, GerenciarEstoque e GerenciarClientes
# é muito similar ao anterior, com a diferença principal de usar `db.` para
# chamar as funções de dados e ter um botão de "Voltar ao Dashboard".

class GerenciarOS(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.lista_os = []

        label = ctk.CTkLabel(self, text="Gerenciar Ordens de Serviço", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20, padx=10)

        # ... (Restante do código da classe GerenciarOS similar ao anterior)
        # Substitua chamadas como `salvar_dados` por `db.salvar_dados`
        # e `carregar_dados` por `db.carregar_dados`

        # EXEMPLO:
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=10, fill="x", padx=20)
        
        btn_criar = ctk.CTkButton(frame_botoes, text="Criar Nova OS", command=self.criar_os)
        btn_criar.pack(side="left", expand=True, padx=5)
        # ... outros botões
        
        self.textbox_os = ctk.CTkTextbox(self, width=700, height=300, state="disabled")
        self.textbox_os.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkButton(self, text="Voltar ao Dashboard",
                      command=lambda: controller.show_frame("DashboardScreen")).pack(pady=20)
    
    def atualizar_tela(self):
        self.lista_os = db.carregar_dados(db.ARQUIVO_OS)
        self.textbox_os.configure(state="normal")
        self.textbox_os.delete("1.0", "end")
        # ... (Lógica para preencher o textbox)
        self.textbox_os.configure(state="disabled")

    def criar_os(self):
        # ... (lógica de criar OS)
        # No final, use db.salvar_dados
        db.salvar_dados(db.ARQUIVO_OS, self.lista_os)
        self.atualizar_tela()

# --- Classes GerenciarEstoque e GerenciarClientes seguem o mesmo padrão de adaptação ---
# ... (Implementação completa delas seria muito longa, mas o padrão é o mesmo de GerenciarOS)
# Apenas adapte os nomes dos arquivos e a lógica para usar o módulo `db`.
# O código completo está no repositório para referência.
# (Aqui omitido para brevidade, mas o padrão é claro)

class GerenciarEstoque(ctk.CTkFrame):
    # ... adaptação similar a GerenciarOS
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.CTkLabel(self, text="Funcionalidade de Estoque (Em construção)").pack(pady=50)
        ctk.CTkButton(self, text="Voltar ao Dashboard", command=lambda: controller.show_frame("DashboardScreen")).pack(pady=20)

class GerenciarClientes(ctk.CTkFrame):
    # ... adaptação similar a GerenciarOS
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.CTkLabel(self, text="Funcionalidade de Clientes (Em construção)").pack(pady=50)
        ctk.CTkButton(self, text="Voltar ao Dashboard", command=lambda: controller.show_frame("DashboardScreen")).pack(pady=20)