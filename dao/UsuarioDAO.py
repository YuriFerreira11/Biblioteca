import os
import json
from model.Usuario import Usuario
from database.ConnectionFactory import ConnectionFactory
class UsuarioDAO:

    lista = []
    arquivo = "Nomes.json"

    @classmethod
    def carregar_usuarios(cls):
        if os.path.exists(cls.arquivo):
            try:
                with open(cls.arquivo, "r", encoding="utf-8") as f:
                    cls.lista = json.load(f)
            except json.JSONDecodeError:
                cls.lista = []

    @classmethod
    def gerar_id(cls):
        if not cls.lista:
            return "0001"
        ultimo_id = cls.lista[-1]["ID"]
        novo_id = int(ultimo_id) + 1
        return f"{novo_id:04d}"

    def registrar_usuario(self):
        if Usuario.procurar_usuario(self.nome):
            print("Usuário ja cadastrado")
            return
        usuario = {
            "Nome": self.nome,
            "Idade": self.idade,
            "ID": Usuario.gerar_id()
        }
        Usuario.lista.append(usuario)
        Usuario.salvar_usuarios()

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
            print("Livro salvo com sucesso")
            return True

        except Exception as e:
            print(f"Erro ao salvar livro: {e}")
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
    @classmethod
    def procurar_usuario(cls, chave):
        chave_lower = chave.lower()
        for usuario in cls.lista:
            if usuario["Nome"].lower() == chave_lower:
                return usuario
        return None

    @classmethod
    def listar_usuarios(cls):
        return cls.lista
