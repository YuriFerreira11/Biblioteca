from model.Usuario import Usuario
import bcrypt
import re
from database.ConnectionFactory import ConnectionFactory
class UsuarioDAO:
    @classmethod
    def salvar_usuarios(cls, user):
        conn = ConnectionFactory.get_connection()

        if not conn:
            return False
        try:
            senha_usuario = user.senha.encode("utf-8")
            if not cls.validar_senha(user.senha):
                print("Senha deve ter no mínimo 8 caracteres, uma maiúscula, uma minúscula e um número.")
                return False
            hash_senha = bcrypt.hashpw(senha_usuario, bcrypt.gensalt())
            hash_senha = hash_senha.decode("utf-8")
            cursor = conn.cursor()
            sql = """
            INSERT INTO usuarios(nome, idade, cpf, senha)
            VALUES (%s, %s, %s, %s)"""
            valores = (user.nome, user.idade, user.cpf, hash_senha)
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
    @staticmethod
    def validar_senha(senha):
        padrao = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        return re.match(padrao, senha) is not None

    @classmethod
    def verificar_usuario(cls, cpf, senha_digitada):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False, None, False

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf,))
            resultado = cursor.fetchone()

            if not resultado:
                return False, None, False

            senha_valida = bcrypt.checkpw(
                senha_digitada.encode("utf-8"),
                resultado["senha"].encode("utf-8")
            )

            if senha_valida:
                return True, resultado["nome"], resultado["admin"]
            else:
                return False, None, False

        finally:
            cursor.close()
            conn.close()

