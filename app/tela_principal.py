from tkinter import Tk, Label, Button, Toplevel
from app.tela_crud import abrir_janela_crud

def abrir_janela_principal():
    janela_principal = Tk()  # Usando Toplevel ao invés de Tk()

    janela_principal.title("Tela Principal")
    janela_principal.geometry("600x400")

    # Exemplo de conteúdo na janela principal
    Label(janela_principal, text="Bem-vindo à tela principal!").pack(pady=20)
    Button(janela_principal, text="Produtos", command=abrir_janela_crud).pack(pady=10)
    Button(janela_principal, text="Sair", command=janela_principal.destroy).pack(pady=20)

    # Não é necessário chamar janela_principal.mainloop() porque a janela principal já foi criada na tela de login