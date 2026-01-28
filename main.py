from models.Usuario import Usuario
def main():
    Usuario.carregar_usuarios()
    while True:
        print("1 - Adicionar usuario")
        print("2 - Procurar usuario")
        print("3 - Listar usuarios")
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
                case 0:
                    break

                case _:
                    print("Opção inválida")

        except ValueError:
            print("Erro: digite apenas números!")


if __name__ == "__main__":
    main()
