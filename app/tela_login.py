from tkinter import Tk, Label, Entry, Button, messagebox
from db.database import conectar
from app.tela_principal import abrir_janela_principal  # Importa a função da janela principal

# Função para realizar o login
def realizar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        janela_login.destroy()
        abrir_janela_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")


# Função para voltar para a tela de login
def voltar_tela_login():
    janela_registro.withdraw()  # Esconde a janela de registro
    janela_login.deiconify()  # Exibe a janela de login

# Função para realizar o registro (apenas exemplo simples)
def realizar_registro():
    usuario = entry_usuario_registro.get()
    senha = entry_senha_registro.get()
    if usuario and senha:
        messagebox.showinfo("Sucesso", f"Usuário {usuario} registrado com sucesso!")
        voltar_tela_login()
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

# Função para criar a tela de login
def criar_tela_login():
    global entry_usuario, entry_senha

    janela_login = Tk()
    janela_login.title("Login")
    janela_login.geometry("400x200")

    Label(janela_login, text="Usuário:").pack()
    entry_usuario = Entry(janela_login)
    entry_usuario.pack()

    Label(janela_login, text="Senha:").pack()
    entry_senha = Entry(janela_login, show="*")
    entry_senha.pack()

    Button(janela_login, text="Login", command=realizar_login).pack(pady=10)
    
    # Botão para abrir a tela de registro
    Button(janela_login, text="Criar Conta", command=abrir_janela_registro).pack(pady=5)

    return janela_login

# Função para criar a tela de registro
def criar_tela_registro():
    global entry_usuario_registro, entry_senha_registro

    janela_registro = Tk()
    janela_registro.title("Criar Conta")
    janela_registro.geometry("400x250")

    Label(janela_registro, text="Escolha um Usuário:").pack(pady=10)
    entry_usuario_registro = Entry(janela_registro)
    entry_usuario_registro.pack(pady=5)

    Label(janela_registro, text="Escolha uma Senha:").pack(pady=10)
    entry_senha_registro = Entry(janela_registro, show="*")
    entry_senha_registro.pack(pady=5)

    Button(janela_registro, text="Registrar", command=realizar_registro).pack(pady=10)
    
    # Botão para voltar para a tela de login
    Button(janela_registro, text="Já tenho uma conta", command=voltar_tela_login).pack(pady=5)

    janela_registro.withdraw()  # A tela de registro começa oculta
    return janela_registro

# Função para alternar entre as telas
def abrir_janela_registro():
    janela_login.withdraw()
    janela_registro.deiconify()

# Criando as janelas
janela_login = criar_tela_login()
janela_registro = criar_tela_registro()

# Iniciar a tela de login
janela_login.mainloop()