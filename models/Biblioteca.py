from Usuario import Usuario
from database import ConnectionFactory

class Biblioteca:
    arquivo = "Livros.csv"
    lista_livro = []
    def __init__(self, livro_id, titulo, ano, quantidade):
        self.quantidade = quantidade
        self.livro_id = livro_id
        self.titulo = titulo
        self.ano = ano
    def registrar_livro(self):
        lista_livro = {"id": self.livro_id,
                       "titulo": self.titulo,
                       "ano": self.ano,
                       "quantidade": self.quantidade
        }
        return lista_livro
    @classmethod
    def salvar_livro(cls, livro):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """
            INSERT INTO livros (id, titulo, ano, quantidade)
            VALUES (%s, %s, %s, %s)
            """
            valores = (livro["ID"], livro["titulo"], livro["ano"], livro["quantidade"])
            cursor.execute(sql, valores)
            conn.commit()
            print("Livro salvo com sucesso")
            return True
        except Exception as e:
            print(f"Erro na salvar livro: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    def mostrar_livro(self):
        print(f"Titulo: {self.titulo}, id: {self.livro_id}, ano: {self.ano}")
    def disponibilidade(self):
        return self.quantidade > 0
    def modificar_disponibilidade(self, quantidade):
        self.quantidade += quantidade
    @classmethod
    def verificar_livro(cls, livro_id):
        for livro in cls.lista_livro:
            if livro["ID"] == livro_id:
                return livro
            else:
                return False
    def emprestar_livro(self, user_id, livro_id):
        usuario = Usuario.verificar_usuario(user_id)
        if not usuario:
            print("Registe primeiro")
            return False
        if not self.disponibilidade():
            print("Livro não está disponivel")
        if not self.verificar_livro(livro_id):
            print("Livro não existe")

        self.quantidade -= 1
        print(f"Livro emprestado para {usuario["Nome"]}")
        return True



