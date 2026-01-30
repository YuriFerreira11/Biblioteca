from database.ConnectionFactory import ConnectionFactory
from dao.UsuarioDAO import UsuarioDAO

class LivroDAO:
    @classmethod # ÚNICO METODO CORRETO COM SQL
    def salvar_livro(cls, livro):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO teste (titulo, ano, quantidade)
                VALUES (%s, %s, %s)
            """
            valores = (livro.titulo, livro.ano, livro.quantidade)
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

    def mostrar_livro(self):
        print(f"Titulo: {self.titulo}, id: {self.livro_id}, ano: {self.ano}")
    @classmethod
    def disponibilidade(cls, livro_id):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            sql = """
                  SELECT quantidade
                  FROM teste
                  WHERE id = %s"""  # Mudado de 'livro_id' para 'id'
            cursor.execute(sql, (livro_id,))
            resultado = cursor.fetchone()

            if resultado is None:
                return False
            return resultado[0] > 0

        except Exception as e:
            print(f"Erro ao verificar disponibilidade: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def verificar_livro(cls, livro_id):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            sql = """SELECT * \
                     FROM teste \
                     WHERE id = %s"""  # Mudado de 'livro_id' para 'id'
            cursor.execute(sql, (livro_id,))
            resultado = cursor.fetchone()

            return resultado

        except Exception as e:
            print(f"Erro ao verificar livro: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @classmethod
    def emprestar_livro(cls, cpf, livro_id):
        # 1. Verificar se usuário existe
        usuario = UsuarioDAO.verificar_usuario(cpf)
        if not usuario:
            print("Usuário não cadastrado. Registre-se primeiro.")
            return False

        # 2. Verificar se livro existe
        livro = cls.verificar_livro(livro_id)
        if not livro:
            print("Livro não registrado")
            return False

        # 3. Verificar disponibilidade
        if not cls.disponibilidade(livro_id):
            print("Livro não disponível")
            return False

        # 4. Atualizar quantidade no banco de dados
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # Diminuir quantidade
            sql_update = """
                         UPDATE teste
                         SET quantidade = quantidade - 1
                         WHERE id = %s"""  # Mudado de 'livro_id' para 'id'
            cursor.execute(sql_update, (livro_id,))

            # Registrar empréstimo (se tiver tabela de empréstimos)
            sql_emprestimo = """
                             INSERT INTO emprestimos (usuario_id, livro_id, data_emprestimo)
                             VALUES (%s, %s, NOW())"""
            cursor.execute(sql_emprestimo, (usuario[0], livro_id))

            conn.commit()
            print(f"Livro emprestado com sucesso!")
            return True

        except Exception as e:
            conn.rollback()
            print(f"Erro ao emprestar livro: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()