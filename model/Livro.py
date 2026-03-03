class Livro:
    def __init__(self, titulo, autor, ano, quantidade, imagem=None, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.quantidade = quantidade
        self.imagem = imagem