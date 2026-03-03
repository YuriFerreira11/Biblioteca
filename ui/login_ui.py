import customtkinter as ctk
from controllers.login_controller import login_funcoes
from ui.livros_ui import LivrosUI


class LoginUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Biblioteca")
        self.app.geometry("460x560")

        self.app.configure(fg_color="#0f0f17")

        self.frame_login = ctk.CTkFrame(self.app, fg_color="#0f0f17", corner_radius=0)
        self.frame_login.pack(fill="both", expand=True)

        self.criar_componentes()

    def criar_componentes(self):
        header = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        header.pack(pady=(45, 0))


        ctk.CTkLabel(
            header,
            text="BIBLIOTECA",
            font=ctk.CTkFont(family="Georgia", size=26, weight="bold"),
            text_color="#e8d5b0"
        ).pack(pady=(6, 2))

        ctk.CTkLabel(
            header,
            text="Sistema de Gestão de Livros",
            font=ctk.CTkFont(size=11),
            text_color="#6b7280"
        ).pack()

        ctk.CTkFrame(self.frame_login, height=1, fg_color="#2a2a3e").pack(
            fill="x", padx=55, pady=(28, 32)
        )

        form = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        form.pack(padx=55, fill="x")

        ctk.CTkLabel(form, text="CPF", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#9ca3af", anchor="w").pack(fill="x", pady=(0, 5))

        self.entry_usuario = ctk.CTkEntry(
            form, height=44,
            placeholder_text="Somente números (11 dígitos)",
            placeholder_text_color="#4b5563",
            fg_color="#1a1a2e", border_color="#2a2a4e", border_width=1,
            text_color="#e8d5b0", font=ctk.CTkFont(size=14), corner_radius=8
        )
        self.entry_usuario.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(form, text="SENHA", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#9ca3af", anchor="w").pack(fill="x", pady=(0, 5))

        self.entry_senha = ctk.CTkEntry(
            form, height=44, show="*",
            placeholder_text="Digite sua senha",
            placeholder_text_color="#4b5563",
            fg_color="#1a1a2e", border_color="#2a2a4e", border_width=1,
            text_color="#e8d5b0", font=ctk.CTkFont(size=14), corner_radius=8
        )
        self.entry_senha.pack(fill="x", pady=(0, 6))
        self.entry_senha.bind("<Return>", lambda e: self.realizar_login())

        self.label_feedback = ctk.CTkLabel(
            form, text="", font=ctk.CTkFont(size=12),
            text_color="#ef4444", height=22
        )
        self.label_feedback.pack(pady=(4, 0))

        self.botao = ctk.CTkButton(
            form, text="ENTRAR", height=46,
            fg_color="#c9a84c", hover_color="#a8893e",
            text_color="#0f0f17", font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8, command=self.realizar_login
        )
        self.botao.pack(fill="x", pady=(18, 0))

        ctk.CTkLabel(
            self.frame_login, text="Sistema de Biblioteca 2026",
            font=ctk.CTkFont(size=10), text_color="#2d3748"
        ).pack(side="bottom", pady=16)

    def realizar_login(self):
        cpf = self.entry_usuario.get()
        senha = self.entry_senha.get()
        self.botao.configure(text="Verificando...", state="disabled")
        self.app.update()
        sucesso, mensagem, nome, admin = login_funcoes.realizar_login(cpf, senha)
        self.botao.configure(text="ENTRAR", state="normal")
        if sucesso:
            self.label_feedback.configure(text="Login realizado com sucesso!", text_color="#22c55e")
            self.app.after(500, lambda: self._abrir_tela(nome, cpf, admin))
        else:
            self.label_feedback.configure(text=mensagem, text_color="#ef4444")
            self.entry_senha.delete(0, "end")

    def _abrir_tela(self, nome, cpf, admin):
        self.frame_login.pack_forget()
        if admin:
            from ui.admin_ui import AdminUI
            self.tela = AdminUI(self.app, nome)
        else:
            self.tela = LivrosUI(self.app, nome, cpf)

    def _abrir_livros(self, nome, cpf):
        self.frame_login.pack_forget()
        self.tela_livros = LivrosUI(self.app, nome, cpf)

    def validar_tecla(self, event):
        texto_atual = self.entry_usuario.get()
        try:
            inicio = self.entry_usuario.index("sel.first")
            fim = self.entry_usuario.index("sel.last")
            tamanho_selecao = fim - inicio
        except Exception:
            tamanho_selecao = 0
        aceitar = login_funcoes.validar_tecla(
            texto_atual, tamanho_selecao, event.keysym, event.char
        )
        if not aceitar:
            return "break"

    def executar(self):
        self.app.mainloop()


if __name__ == "__main__":
    tela = LoginUI()
    tela.executar()