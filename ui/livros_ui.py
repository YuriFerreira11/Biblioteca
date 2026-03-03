import customtkinter as ctk
from controllers.livros_controller import livros_funcoes
from PIL import Image
import io
import os


class LivrosUI:
    def __init__(self, master, nome, cpf):
        self.master = master
        self.nome = nome
        self.cpf = cpf  # guarda o CPF para usar no empréstimo
        master.geometry("700x600")
        master.configure(fg_color="#0f0f17")

        self.frame_outer = ctk.CTkFrame(master, fg_color="#0f0f17", corner_radius=0)
        self.frame_outer.pack(fill="both", expand=True)

        # Barra superior
        topbar = ctk.CTkFrame(self.frame_outer, fg_color="#13131f", height=64, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(
            topbar, text="📚  BIBLIOTECA",
            font=ctk.CTkFont(family="Georgia", size=18, weight="bold"),
            text_color="#e8d5b0"
        ).pack(side="left", padx=24)

        ctk.CTkLabel(
            topbar, text=f"Olá, {nome}",
            font=ctk.CTkFont(size=13),
            text_color="#9ca3af"
        ).pack(side="right", padx=24)

        ctk.CTkLabel(
            self.frame_outer,
            text="Acervo disponível",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280"
        ).pack(anchor="w", padx=28, pady=(18, 6))

        ctk.CTkFrame(self.frame_outer, height=1, fg_color="#1e1e30").pack(
            fill="x", padx=28, pady=(0, 12)
        )

        self.scroll = ctk.CTkScrollableFrame(
            self.frame_outer,
            fg_color="transparent",
            scrollbar_button_color="#2a2a4e",
            scrollbar_button_hover_color="#c9a84c"
        )
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        livros = livros_funcoes.listar_livros()

        if not livros:
            ctk.CTkLabel(
                self.scroll,
                text="Nenhum livro encontrado.",
                font=ctk.CTkFont(size=14),
                text_color="#4b5563"
            ).pack(pady=40)
        else:
            for livro in livros:
                self._criar_card(livro)

    def _criar_card(self, livro):
        card = ctk.CTkFrame(
            self.scroll,
            fg_color="#13131f",
            corner_radius=12,
            border_width=1,
            border_color="#1e1e30"
        )
        card.pack(pady=8, padx=4, fill="x")

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(pady=14, padx=14, fill="x")

        # Imagem
        img = None
        if livro.get("imagem"):
            try:
                img = Image.open(io.BytesIO(livro["imagem"]))
            except Exception:
                img = None

        if img is None:
            nome_arquivo = livro.get("titulo", "").lower().replace(" ", "") + ".png"
            caminho = os.path.join("assets", nome_arquivo)
            if os.path.exists(caminho):
                img = Image.open(caminho)

        if img is None:
            img = Image.new("RGB", (72, 108), color="#1e2a3a")

        capa = ctk.CTkImage(light_image=img, dark_image=img, size=(72, 108))
        img_label = ctk.CTkLabel(container, image=capa, text="", corner_radius=6)
        img_label.image = capa
        img_label.pack(side="left", padx=(4, 16))

        # Informações
        info = ctk.CTkFrame(container, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)

        disponivel = livro.get("quantidade", 0) > 0
        tem_emprestimo = livros_funcoes.verificar_emprestimo_ativo(self.cpf, livro["id"])

        ctk.CTkLabel(
            info,
            text=livro.get("titulo", ""),
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#e8d5b0", anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=livro.get("autor", "Autor desconhecido"),
            font=ctk.CTkFont(size=12),
            text_color="#9ca3af", anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            info,
            text=f"Ano: {livro.get('ano', '—')}",
            font=ctk.CTkFont(size=11),
            text_color="#6b7280", anchor="w"
        ).pack(anchor="w", pady=(2, 8))

        rodape = ctk.CTkFrame(info, fg_color="transparent")
        rodape.pack(anchor="w", fill="x")

        # Badge de disponibilidade
        badge_cor = "#14532d" if disponivel else "#450a0a"
        badge_texto = f"  {livro.get('quantidade', 0)} disponível(is)  " if disponivel else "  Indisponível  "
        badge_texto_cor = "#4ade80" if disponivel else "#f87171"

        ctk.CTkLabel(
            rodape,
            text=badge_texto,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=badge_texto_cor,
            fg_color=badge_cor,
            corner_radius=6
        ).pack(side="left", padx=(0, 10))

        label_status = ctk.CTkLabel(
            rodape, text="",
            font=ctk.CTkFont(size=11),
            text_color="#22c55e"
        )
        label_status.pack(side="right", padx=(0, 8))

        # Botão muda conforme estado do empréstimo
        if tem_emprestimo:
            atrasado = livros_funcoes.verificar_emprestimo_atrasado(self.cpf, livro["id"])
            ctk.CTkButton(
                rodape,
                text="Devolver ⚠" if atrasado else "Devolver",
                width=100, height=30,
                fg_color="#7f1d1d" if atrasado else "#1d4ed8",
                hover_color="#991b1b" if atrasado else "#1e40af",
                text_color="#fca5a5" if atrasado else "#ffffff",
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=6,
                command=lambda l=livro, lbl=label_status: self._devolver(l, lbl)
            ).pack(side="left")
        else:
            ctk.CTkButton(
                rodape,
                text="Emprestar",
                width=100, height=30,
                fg_color="#c9a84c" if disponivel else "#374151",
                hover_color="#a8893e" if disponivel else "#374151",
                text_color="#0f0f17" if disponivel else "#6b7280",
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=6,
                state="normal" if disponivel else "disabled",
                command=lambda l=livro, lbl=label_status: self._emprestar(l, lbl)
            ).pack(side="left")

    def _emprestar(self, livro, label_status):
        sucesso, mensagem = livros_funcoes.emprestar_livro(self.cpf, livro["id"])
        if sucesso:
            label_status.configure(text=mensagem, text_color="#22c55e")
            self.master.after(800, self._recarregar)
        else:
            label_status.configure(text=mensagem, text_color="#ef4444")

    def _devolver(self, livro, label_status):
        sucesso, mensagem = livros_funcoes.devolver_livro(self.cpf, livro["id"])
        if sucesso:
            label_status.configure(text=mensagem, text_color="#22c55e")
            self.master.after(800, self._recarregar)
        else:
            label_status.configure(text=mensagem, text_color="#ef4444")

    def _recarregar(self):
        self.frame_outer.destroy()
        LivrosUI(self.master, self.nome, self.cpf)