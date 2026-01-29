from model.Usuario import Usuario
from model.Livro import Livro
from dao.LivroDAO import LivroDAO
from dao.UsuarioDAO import UsuarioDAO
from database.ConnectionFactory import ConnectionFactory

def main():
    # ConnectionFactory.testar() # APENAS PARA TESTES
    UsuarioDAO.carregar_usuarios()
    while True:
        print("1 - Adicionar usuario")
        print("2 - Procurar usuario")
        print("3 - Listar usuarios")
        print("4 - Adicionar livro")
        print("0 - Sair")

        try:
            op = int(input("Digite a operação: "))

            match op:
                case 1:
                    nome = input("Digite o nome: ")
                    idade_str = input("Digite a idade: ").strip()

                    if not idade_str.isdigit():
                        print("Idade inválida!")
                        continue

                    idade = int(idade_str)

                    usuario = Usuario(nome, idade)
                    usuario.registrar_usuario()

                    print(f"{usuario.nome} registrado com sucesso!")
                case 2:
                    chave = input("Digite o usuario que quer encontrar: ")
                    resultado = Usuario.procurar_usuario(chave)
                    if resultado:
                        print("Usuário encontrado:", resultado)
                    else:
                        print("Usuário não encontrado")
                case 3:
                    usuarios = Usuario.listar_usuarios()
                    if usuarios:
                        print("\n=== USUÁRIOS CADASTRADOS ===")
                        for idx, user in enumerate(usuarios, 1):
                            print(f"{idx}. {user}")
                    else:
                        print("Nenhum usuário cadastrado")
                case 4:
                    titulo = input("Digite o título do livro: ")
                    ano = input("Digite o ano: ")
                    quantidade = input("Digite a quantidade: ")

                    if not ano.isdigit() or not quantidade.isdigit():
                        print("Ano e quantidade devem ser números.")
                        break

                    livro = Livro(None, titulo, int(ano), int(quantidade))
                    LivroDAO.salvar_livro(livro)

                case 0:
                    break

                case _:
                    print("Opção inválida")

        except ValueError:
            print("Erro: digite apenas números!")


if __name__ == "__main__":
    main()
