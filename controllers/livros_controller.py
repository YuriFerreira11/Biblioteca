from dao.LivroDAO import LivroDAO


class livros_funcoes:

    @classmethod
    def listar_livros(cls):
        return LivroDAO.listar_livros()

    @classmethod
    def emprestar_livro(cls, cpf, livro_id):
        return LivroDAO.emprestar_livro_por_cpf(cpf, livro_id)

    @classmethod
    def devolver_livro(cls, cpf, livro_id):
        return LivroDAO.devolver_livro(cpf, livro_id)

    @classmethod
    def verificar_emprestimo_ativo(cls, cpf, livro_id):
        return LivroDAO.verificar_emprestimo_ativo(cpf, livro_id)
    @classmethod
    def verificar_emprestimo_atrasado(cls, cpf, livro_id):
        return LivroDAO.verificar_emprestimo_atrasado(cpf, livro_id)