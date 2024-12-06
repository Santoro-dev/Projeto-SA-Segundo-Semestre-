from tkinter import Tk, Label, Button, Toplevel
from app.tela_crud import abrir_janela_exibir_produtos, exibir_sobre_nos


def abrir_janela_principal():
    janela_principal = Tk()  # Usando Toplevel ao invés de Tk()

    janela_principal.title("Tela Principal")
    janela_principal.geometry("600x400")
    janela_principal.resizable(width=False, height=False)


    # Exemplo de conteúdo na janela principal
    Label(janela_principal, text="Drogaria Senai").pack(pady=20)
    Button(janela_principal, text="Produtos", command=abrir_janela_exibir_produtos).pack(pady=10)
    Button(janela_principal, text="Sobre nós", command=exibir_sobre_nos).pack(pady=15)
    Button(janela_principal, text="Sair", command=janela_principal.destroy).pack(pady=20)

    # Não é necessário chamar janela_principal.mainloop() porque a janela principal já foi criada na tela de login