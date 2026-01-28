from database.ConnectionFactory import ConnectionFactory

def testar():
    conn = ConnectionFactory.get_connection()
    if conn:
        print("Conexão estabelecida com sucesso!")
        conn.close()
    else:
        print("Falha na conexão. Verifique se o nome do banco 'biblioteca_db' existe no Workbench.")

if __name__ == "__main__":
    testar()