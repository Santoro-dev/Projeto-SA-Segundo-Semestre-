from tkinter import Tk, Toplevel, Label, Button, Entry, messagebox, ttk, Scrollbar
from db.database import conectar

def buscar_produtos(filtro=""):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
            SELECT p.id_produto, p.nome, p.codigo_barras, p.categoria, p.quantidade, p.preco, f.nome AS fornecedor
            FROM produtos p
            LEFT JOIN fornecedores f ON p.fornecedor_id = f.id_fornecedor
        """
        if filtro:
            query += " WHERE p.id_produto LIKE %s OR p.nome LIKE %s OR f.nome LIKE %s"
            filtro = f"%{filtro}%"
            cursor.execute(query, (filtro, filtro, filtro))
        else:
            cursor.execute(query)

        resultados = cursor.fetchall()
        conn.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar produtos: {e}")
        return []


def exibir_produtos(tree, filtro=""):
    for item in tree.get_children():
        tree.delete(item)

    produtos = buscar_produtos(filtro)

    for produto in produtos:
        tree.insert("", "end", values=produto)


def abrir_janela_exibir_produtos():
    janela_exibir = Toplevel()
    janela_exibir.title("Produtos")
    janela_exibir.geometry("800x600")
    janela_exibir.resizable(width=False, height=False)



    Label(janela_exibir, text="Buscar Produto:").pack(pady=5)
    entry_busca = Entry(janela_exibir)
    entry_busca.pack(pady=5)

    def realizar_busca():
        filtro = entry_busca.get()
        exibir_produtos(tree, filtro)

    Button(janela_exibir, text="Buscar", command=realizar_busca).pack(pady=5)
    Button(janela_exibir, text="Adicionar Produto", command=adicionar_produto).pack(pady=5)
    Button(janela_exibir, text="Editar Produto", command=editar_produto).pack(pady=10)
    Button(janela_exibir, text="Excluir Produto", command=excluir_produto).pack(pady=15)

    frame_tabela = ttk.Frame(janela_exibir)
    frame_tabela.pack(expand=True, fill="both")

    colunas = ("ID", "Nome", "Código de Barras", "Categoria", "Quantidade", "Preço", "Fornecedor")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

    # Configurando cabeçalhos e largura das colunas
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Código de Barras", text="Código de Barras")
    tree.heading("Categoria", text="Categoria")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço", text="Preço")
    tree.heading("Fornecedor", text="Fornecedor")

    tree.column("ID", width=50, anchor="center")
    tree.column("Nome", width=150, anchor="w")
    tree.column("Código de Barras", width=120, anchor="center")
    tree.column("Categoria", width=100, anchor="w")
    tree.column("Quantidade", width=80, anchor="center")
    tree.column("Preço", width=100, anchor="center")
    tree.column("Fornecedor", width=150, anchor="w")

    tree.pack(side="left", expand=True, fill="both")

    # Adicionando barras de rolagem
    scroll_y = Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    scroll_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scroll_y.set)

    scroll_x = Scrollbar(janela_exibir, orient="horizontal", command=tree.xview)
    scroll_x.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scroll_x.set)

    exibir_produtos(tree)

# Função para adicionar produto
def adicionar_produto():
    def salvar_produto():
        nome = entry_nome.get()
        codigo_barras = entry_codigo_barras.get()
        categoria = entry_categoria.get()
        quantidade = entry_quantidade.get()
        preco = entry_preco.get()

        # Validando se todos os campos foram preenchidos
        if not nome or not codigo_barras or not quantidade or not preco:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        try:
            # Conectar ao banco de dados
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (nome, codigo_barras, categoria, quantidade, preco)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, codigo_barras, categoria, quantidade, preco))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            janela_adicionar_produto.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar produto: {e}")

    # Criando a janela de adicionar produto
    janela_adicionar_produto = Tk()
    janela_adicionar_produto.title("Adicionar Produto")
    janela_adicionar_produto.geometry("400x500")
    janela_adicionar_produto.resizable(width=False, height=False)



    Label(janela_adicionar_produto, text="Nome do Produto:").pack(pady=5)
    entry_nome = Entry(janela_adicionar_produto)
    entry_nome.pack(pady=5)

    Label(janela_adicionar_produto, text="Código de Barras:").pack(pady=5)
    entry_codigo_barras = Entry(janela_adicionar_produto)
    entry_codigo_barras.pack(pady=5)

    Label(janela_adicionar_produto, text="Categoria:").pack(pady=5)
    entry_categoria = Entry(janela_adicionar_produto)
    entry_categoria.pack(pady=5)

    Label(janela_adicionar_produto, text="Quantidade:").pack(pady=5)
    entry_quantidade = Entry(janela_adicionar_produto)
    entry_quantidade.pack(pady=5)

    Label(janela_adicionar_produto, text="Preço:").pack(pady=5)
    entry_preco = Entry(janela_adicionar_produto)
    entry_preco.pack(pady=5)

    Button(janela_adicionar_produto, text="Salvar Produto", command=salvar_produto).pack(pady=10)

# Função para editar produto
def editar_produto():
    def salvar_edicao():
        produto_id = entry_id.get()
        nome = entry_nome.get()
        codigo_barras = entry_codigo_barras.get()
        categoria = entry_categoria.get()
        quantidade = entry_quantidade.get()
        preco = entry_preco.get()

        # Validando se todos os campos foram preenchidos
        if not produto_id or not nome or not codigo_barras or not quantidade or not preco:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            # Conectar ao banco de dados
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produtos SET nome = %s, codigo_barras = %s, categoria = %s, quantidade = %s, preco = %s
                WHERE id_produto = %s
            """, (nome, codigo_barras, categoria, quantidade, preco, produto_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
            janela_editar_produto.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar produto: {e}")

    # Criando a janela de edição de produto
    janela_editar_produto = Tk()
    janela_editar_produto.title("Editar Produto")
    janela_editar_produto.geometry("400x500")
    janela_editar_produto.resizable(width=False, height=False)



    Label(janela_editar_produto, text="ID do Produto:").pack(pady=5)
    entry_id = Entry(janela_editar_produto)
    entry_id.pack(pady=5)

    Label(janela_editar_produto, text="Nome do Produto:").pack(pady=5)
    entry_nome = Entry(janela_editar_produto)
    entry_nome.pack(pady=5)

    Label(janela_editar_produto, text="Código de Barras:").pack(pady=5)
    entry_codigo_barras = Entry(janela_editar_produto)
    entry_codigo_barras.pack(pady=5)

    Label(janela_editar_produto, text="Categoria:").pack(pady=5)
    entry_categoria = Entry(janela_editar_produto)
    entry_categoria.pack(pady=5)

    Label(janela_editar_produto, text="Quantidade:").pack(pady=5)
    entry_quantidade = Entry(janela_editar_produto)
    entry_quantidade.pack(pady=5)

    Label(janela_editar_produto, text="Preço:").pack(pady=5)
    entry_preco = Entry(janela_editar_produto)
    entry_preco.pack(pady=5)

    Button(janela_editar_produto, text="Salvar Edição", command=salvar_edicao).pack(pady=10)

# Função para excluir produto
def excluir_produto():
    def confirmar_exclusao():
        produto_id = entry_id.get()

        # Validando se o campo ID foi preenchido
        if not produto_id:
            messagebox.showerror("Erro", "Por favor, insira o ID do produto.")
            return

        try:
            # Conectar ao banco de dados
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (produto_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            janela_excluir_produto.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")

    # Criando a janela de exclusão de produto
    janela_excluir_produto = Tk()
    janela_excluir_produto.title("Excluir Produto")
    janela_excluir_produto.geometry("400x200")
    janela_excluir_produto.resizable(width=False, height=False)


    Label(janela_excluir_produto, text="ID do Produto:").pack(pady=5)
    entry_id = Entry(janela_excluir_produto)
    entry_id.pack(pady=5)

    Button(janela_excluir_produto, text="Excluir Produto", command=confirmar_exclusao).pack(pady=10)

# Função para exibir o "Sobre Nós"
def exibir_sobre_nos():
    janela_sobre_nos = Toplevel()
    janela_sobre_nos.title("Sobre Nós - Drogaria Senai")
    janela_sobre_nos.geometry("600x400")
    janela_sobre_nos.resizable(width=False, height=False)


    texto_sobre_nos = """
    A Drogaria Senai é uma farmácia comprometida com a saúde e bem-estar de seus clientes.
    Com uma trajetória de excelência no atendimento, oferecemos uma ampla gama de medicamentos,
    produtos de cuidados pessoais e cosméticos, com a qualidade que você merece.

    Nossa missão é proporcionar um atendimento ágil, confiável e humanizado, com profissionais
    capacitados para orientações e aconselhamentos sobre os produtos que oferecemos. Trabalhamos
    com as melhores marcas do mercado, garantindo que você tenha acesso aos produtos mais eficazes
    para sua saúde e qualidade de vida.

    Na Drogaria Senai, nossa prioridade é o cuidado com você e sua família. Além de um ambiente
    seguro e confortável, buscamos sempre estar atualizados com as necessidades de nossos clientes,
    oferecendo soluções que atendam aos mais diversos requisitos.

    Acreditamos que o acesso à saúde de qualidade deve ser fácil e próximo, e é por isso que estamos
    sempre prontos para proporcionar uma experiência de compra eficiente e de confiança.

    Drogaria Senai - Cuidando de você com responsabilidade e carinho.
    """

    # Adicionando o texto na janela
    Label(janela_sobre_nos, text=texto_sobre_nos, justify="left", padx=10, pady=10).pack(expand=True, fill="both")
    Label(janela_sobre_nos, text="Desenvolvido por: João Santos, Lucas Bernardo e Ramon Benites.").pack(pady=15)

