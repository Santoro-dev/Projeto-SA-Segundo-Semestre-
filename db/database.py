import mysql.connector

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "projeto_sa"
}

def conectar():
    """Estabelece a conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar no banco de dados: {e}")
        return None
