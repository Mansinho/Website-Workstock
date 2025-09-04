# database.py
import json
import hashlib

# --- CONSTANTES DE ARQUIVOS ---
ARQUIVO_OS = 'ordens_de_servico.json'
ARQUIVO_ESTOQUE = 'estoque.json'
ARQUIVO_CLIENTES = 'clientes.json'
ARQUIVO_USUARIOS = 'usuarios.json'

# --- FUNÇÕES GENÉRICAS DE DADOS ---
def carregar_dados(nome_arquivo):
    """Carrega dados de um arquivo JSON."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arq:
            return json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(nome_arquivo, dados):
    """Salva dados em um arquivo JSON."""
    with open(nome_arquivo, 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, indent=4, ensure_ascii=False)

# --- FUNÇÕES DE GERENCIAMENTO DE USUÁRIOS ---

def hash_password(password):
    """Gera um hash SHA-256 para a senha."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password_hash, provided_password):
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return stored_password_hash == hash_password(provided_password)

def registrar_usuario(username, password, user_type):
    """Registra um novo usuário. Retorna True em caso de sucesso."""
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    
    # Verifica se o usuário já existe
    if any(u['username'].lower() == username.lower() for u in usuarios):
        return False, "Usuário já existe."

    novo_usuario = {
        "username": username,
        "password_hash": hash_password(password),
        "user_type": user_type
    }
    
    usuarios.append(novo_usuario)
    salvar_dados(ARQUIVO_USUARIOS, usuarios)
    return True, "Usuário registrado com sucesso!"

def autenticar_usuario(username, password):
    """Autentica um usuário. Retorna os dados do usuário em caso de sucesso, senão None."""
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    
    for usuario in usuarios:
        if usuario['username'].lower() == username.lower():
            if verify_password(usuario['password_hash'], password):
                return usuario # Retorna o dicionário do usuário (username, user_type)
    return None