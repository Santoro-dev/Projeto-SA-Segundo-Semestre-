from app.tela_login import criar_tela_login

# Inicia a aplicação
if __name__ == "__main__":
    janela_login = criar_tela_login()
    janela_login.mainloop()
    janela_login.resizable(width=False, height=False)

    
