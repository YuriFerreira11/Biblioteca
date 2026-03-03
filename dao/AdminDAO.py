from database.ConnectionFactory import ConnectionFactory
from dao.LivroDAO import LivroDAO

class AdminDAO:

    @classmethod
    def atualizar_atrasados(cls):
        """Marca como 'atrasado' empréstimos ativos cuja data_devolucao já passou."""
        conn = ConnectionFactory.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE emprestimos
                SET status = 'atrasado'
                WHERE status = 'ativo' AND data_devolucao < NOW()
            """)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def listar_atrasados(cls):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    e.id        AS emprestimo_id,
                    e.livro_id,
                    e.data_emprestimo,
                    e.data_devolucao,
                    u.nome,
                    u.cpf,
                    l.titulo
                FROM emprestimos e
                JOIN usuarios u ON e.usuario_id = u.id
                JOIN livros   l ON e.livro_id   = l.id
                WHERE e.status = 'atrasado'
                ORDER BY e.data_devolucao ASC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def listar_todos_emprestimos(cls):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    e.data_emprestimo,
                    e.data_devolucao,
                    e.status,
                    u.nome,
                    l.titulo
                FROM emprestimos e
                JOIN usuarios u ON e.usuario_id = u.id
                JOIN livros   l ON e.livro_id   = l.id
                ORDER BY e.data_emprestimo DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def listar_usuarios(cls):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    u.nome, u.cpf, u.idade, u.admin,
                    SUM(e.status = 'ativo')    AS ativos,
                    SUM(e.status = 'atrasado') AS atrasados
                FROM usuarios u
                LEFT JOIN emprestimos e ON e.usuario_id = u.id
                GROUP BY u.id
                ORDER BY u.nome
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def forcar_devolucao(cls, emprestimo_id, livro_id):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False, "Erro de conexão"
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE emprestimos
                SET status = 'devolvido', data_devolucao = NOW()
                WHERE id = %s
            """, (emprestimo_id,))
            cursor.execute("""
                UPDATE livros
                SET quantidade = quantidade + 1
                WHERE id = %s
            """, (livro_id,))
            conn.commit()
            return True, "Devolvido!"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
    @classmethod
    def adicionar_livro(cls, livro):
        return LivroDAO.salvar_livro(livro)

    @classmethod
    def editar_livro(cls, livro_id, titulo, autor, ano, quantidade, imagem=None):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False, "Erro de conexão"
        try:
            cursor = conn.cursor()

            if imagem is not None:
                cursor.execute("""
                               UPDATE livros
                               SET titulo     = %s,
                                   autor      = %s,
                                   ano        = %s,
                                   quantidade = %s,
                                   imagem     = %s
                               WHERE id = %s
                               """, (titulo, autor, ano, quantidade, imagem, livro_id))
            else:
                cursor.execute("""
                               UPDATE livros
                               SET titulo     = %s,
                                   autor      = %s,
                                   ano        = %s,
                                   quantidade = %s
                               WHERE id = %s
                               """, (titulo, autor, ano, quantidade, livro_id))

            conn.commit()
            return True, "Livro atualizado com sucesso!"
        except Exception as e:
            conn.rollback()
            return False, f"Erro: {e}"
        finally:
            cursor.close()
            conn.close()
