import customtkinter as ctk
from controllers.login_controller import login_funcoes
class LoginUI:
    def __init__(self):
        #Configurações iniciais
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        #Janela principal
        self.app = ctk.CTk()
        self.app.title("Login")
        self.app.geometry("500x500")

        # Frames
        self.frame_login = ctk.CTkFrame(self.app)
        self.frame_login.pack(fill="both", expand=True)

        self.criar_componentes()

    def criar_componentes(self):
        ctk.CTkLabel(
            self.frame_login,
            text="CPF (somente números)",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(40, 10))

        self.entry_usuario = ctk.CTkEntry(
            self.frame_login,
            width=320,
            height=38,
            show="*"
        )
        self.entry_usuario.pack(pady=(0, 10))
        self.entry_usuario.bind("<KeyPress>", self.validar_tecla)

        self.label_feedback = ctk.CTkLabel(
            self.frame_login,
            text="",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_feedback.pack(pady=(10, 0))

        self.botao = ctk.CTkButton(
            self.frame_login,
            text="Entrar",
            width=180,
            height=36,
            command=self.realizar_login
        )
        self.botao.pack(pady=20)

    def realizar_login(self):
        cpf = self.entry_usuario.get()
        sucesso, mensagem, nome = login_funcoes.realizar_login(cpf)
        cor = "green" if sucesso else "red"
        self.label_feedback.configure(
            text = mensagem,
            text_color = cor
        )
        if sucesso:
            pass

    def validar_tecla(self, event):
        texto_atual = self.entry_usuario.get()
        try:
            inicio = self.entry_usuario.index("sel.first")
            fim = self.entry_usuario.index("sel.last")
            tamanho_selecao = fim - inicio
        except:
            tamanho_selecao = 0
        aceitar = login_funcoes.validar_tecla(
            texto_atual,
            tamanho_selecao,
            event.keysym,
            event.char
        )

        if not aceitar:
            return "break"
    def executar(self):
        self.app.mainloop()

if __name__ == "__main__":
    tela = LoginUI()
    tela.executar()