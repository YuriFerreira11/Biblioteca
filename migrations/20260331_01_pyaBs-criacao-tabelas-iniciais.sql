-- criacao_tabelas_iniciais
-- depends: 

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    idade INTEGER NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE livros (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    ano INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    imagem VARCHAR(255)
);

CREATE TABLE emprestimos (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    livro_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    data_emprestimo DATE DEFAULT (CURRENT_DATE),
    data_devolucao DATE DEFAULT (CURRENT_DATE + INTERVAL 14 DAY),
    status VARCHAR(30) DEFAULT 'ativo',
    FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);