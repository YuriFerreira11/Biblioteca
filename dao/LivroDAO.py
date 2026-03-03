from database.ConnectionFactory import ConnectionFactory
from dao.UsuarioDAO import UsuarioDAO

class LivroDAO:
    @classmethod
    def salvar_livro(cls, livro):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False, "Erro de conexão"
        try:
            cursor = conn.cursor()
            sql = """
                  INSERT INTO livros (titulo, autor, ano, quantidade, imagem)
                  VALUES (%s, %s, %s, %s, %s) \
                  """
            valores = (livro.titulo, livro.autor, livro.ano, livro.quantidade, livro.imagem)
            cursor.execute(sql, valores)
            conn.commit()
            return True, "Livro salvo com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar livro: {e}"
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
                  FROM livros
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
                     FROM livros \
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
    def emprestar_livro_por_cpf(cls, cpf, livro_id):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False, "Erro de conexão"

        try:
            cursor = conn.cursor(dictionary=True)

            # 1. Busca o ID do usuário pelo CPF
            cursor.execute("SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
            usuario = cursor.fetchone()
            if not usuario:
                return False, "Usuário não encontrado"

            # 2. Verifica se livro existe e está disponível
            cursor.execute("SELECT quantidade FROM livros WHERE id = %s", (livro_id,))
            livro = cursor.fetchone()
            if not livro:
                return False, "Livro não registrado"
            if livro["quantidade"] <= 0:
                return False, "Livro indisponível"

            # 3. Diminui quantidade
            cursor.execute(
                "UPDATE livros SET quantidade = quantidade - 1 WHERE id = %s",
                (livro_id,)
            )

            # 4. Registra empréstimo (status e data_devolucao já têm DEFAULT no banco)
            cursor.execute(
                "INSERT INTO emprestimos (usuario_id, livro_id) VALUES (%s, %s)",
                (usuario["id"], livro_id)
            )

            conn.commit()
            return True, "Emprestado com sucesso!"

        except Exception as e:
            conn.rollback()
            return False, f"Erro: {e}"

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def listar_livros(cls):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT id, titulo, autor, ano, quantidade, imagem FROM livros"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def devolver_livro(cls, cpf, livro_id):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False, "Erro de conexão"

        try:
            cursor = conn.cursor(dictionary=True)

            # 1. Busca o usuário pelo CPF
            cursor.execute("SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
            usuario = cursor.fetchone()
            if not usuario:
                return False, "Usuário não encontrado"

            # 2. Verifica se existe empréstimo ativo desse livro por esse usuário
            cursor.execute("""
                           SELECT id
                           FROM emprestimos
                           WHERE usuario_id = %s
                             AND livro_id = %s
                             AND status IN ('ativo', 'atrasado')
                           ORDER BY data_emprestimo DESC LIMIT 1
                           """, (usuario["id"], livro_id))
            emprestimo = cursor.fetchone()
            if not emprestimo:
                return False, "Nenhum empréstimo ativo encontrado"

            # 3. Atualiza o empréstimo para devolvido
            cursor.execute("""
                           UPDATE emprestimos
                           SET status         = 'devolvido',
                               data_devolucao = NOW()
                           WHERE id = %s
                           """, (emprestimo["id"],))

            # 4. Devolve o livro ao estoque
            cursor.execute("""
                           UPDATE livros
                           SET quantidade = quantidade + 1
                           WHERE id = %s
                           """, (livro_id,))

            conn.commit()
            return True, "Devolvido com sucesso!"

        except Exception as e:
            conn.rollback()
            return False, f"Erro: {e}"

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def verificar_emprestimo_ativo(cls, cpf, livro_id):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
            usuario = cursor.fetchone()
            if not usuario:
                return False
            cursor.execute("""
                           SELECT id
                           FROM emprestimos
                           WHERE usuario_id = %s
                             AND livro_id = %s
                             AND status IN ('ativo', 'atrasado') LIMIT 1
                           """, (usuario["id"], livro_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def verificar_emprestimo_atrasado(cls, cpf, livro_id):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
            usuario = cursor.fetchone()
            if not usuario:
                return False
            cursor.execute("""
                           SELECT id
                           FROM emprestimos
                           WHERE usuario_id = %s
                             AND livro_id = %s
                             AND status = 'atrasado' LIMIT 1
                           """, (usuario["id"], livro_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

