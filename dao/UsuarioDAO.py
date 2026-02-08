from model.Usuario import Usuario
from database.ConnectionFactory import ConnectionFactory
class UsuarioDAO:
    @classmethod
    def salvar_usuarios(cls, user):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """
            INSERT INTO usuarios(nome, idade, cpf)
            VALUES (%s, %s, %s)"""
            valores = (user.nome, user.idade, user.cpf)
            cursor.execute(sql, valores)
            conn.commit()
            print("Usuario salvo com sucesso")
            return True

        except Exception as e:
            print(f"Erro ao salvar o usuario: {e}")
            return False

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    @classmethod
    def verificar_usuario(cls, cpf):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """
            SELECT *
            FROM usuarios
            WHERE cpf = %s"""
            cursor.execute(sql, (cpf,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            return resultado  # Retorna os dados do usuário ou None se não encontrado

        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            print(f"Erro ao verificar usuário: {e}")
            return None
