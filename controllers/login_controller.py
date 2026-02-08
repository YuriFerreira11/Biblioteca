from dao.UsuarioDAO import UsuarioDAO

class login_funcoes():
    @staticmethod
    def validar_cpf(cpf: str) -> tuple[bool, str]:
        cpf = cpf.strip()
        if not cpf:
            return False, "Insira um CPF"
        if len(cpf) != 11:
            return False, "CPF deve ter 11 digitos"
        if not cpf.isdigit():
            return False, "CPF deve conter apenas números"
        return True, ""
    @staticmethod
    def realizar_login(cpf: str) -> tuple[bool, str, str]:
        '''
        Realizar login com CPF

        Args:
        cpf: CPF do usuario

        Returns:
            Tupla(sucesso, mensagem, nome)
        '''
        valido, mensagem_erro = login_funcoes.validar_cpf(cpf)
        if not valido:
            return False, mensagem_erro, ""
        resultado = UsuarioDAO.verificar_usuario(cpf)
        if resultado:
            nome = resultado[1]
            mensagem = f"Login realizado com sucesso! Bem vindo, {nome}"
            return True, mensagem, nome
        else:
            return False, "CPF não encontrado", ""
    @staticmethod
    def validar_tecla(texto_atual: str, tamanho_selecao: int, tecla: str, char: str) -> bool:
        '''
                Valida se a tecla pressionada deve ser aceita

                Args:
                Texto atual: Texto atual no campo
                Tecla: Tecla a ser pressionada
                char: Charactar da tecla

                Returns:
                    True se aceitar, false se não
                '''

        teclas_liberadas = (
            "BackSpace", "Delete", "Left", "Right", "Tab"
        )
        if tecla in teclas_liberadas:
            return True
        if not char.isdigit():
            return False
        tamanho_final = len(texto_atual) - tamanho_selecao
        if tamanho_final >= 11:
            return False
        return True