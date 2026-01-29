import mysql.connector
import os  # Biblioteca para ler variáveis do sistema
from mysql.connector import Error

class ConnectionFactory:
    # As configurações agora buscam a senha do ambiente
    _config = {
        'host': 'localhost',
        'database': 'biblioteca', # a minha é assim
        'user': 'root',
        'password': os.getenv('DB_PASSWORD')  # Busca a senha configurada no PyCharm
    }

    @classmethod
    def get_connection(cls):
        try:
            if not cls._config['password']:
                raise ValueError("A senha do banco de dados não foi configurada no PyCharm!")

            return mysql.connector.connect(**cls._config)
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    @classmethod
    def testar(cls):
        conn = ConnectionFactory.get_connection()
        if conn:
            print("Conexão estabelecida com sucesso!")
            conn.close()
        else:
            print("Falha na conexão. Verifique se o nome do banco 'biblioteca_db' existe no Workbench.")