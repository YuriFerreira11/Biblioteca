import customtkinter as ctk
from dao.AdminDAO import AdminDAO
from datetime import datetime
from dao.LivroDAO import LivroDAO

class AdminUI:
    def __init__(self, master, nome_admin):
        self.master = master
        self.nome_admin = nome_admin
        master.geometry("900x650")
        master.configure(fg_color="#0f0f17")

        self.frame = ctk.CTkFrame(master, fg_color="#0f0f17", corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        self._criar_topbar()
        self._criar_abas()

    def _criar_topbar(self):
        topbar = ctk.CTkFrame(self.frame, fg_color="#13131f", height=64, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(
            topbar, text="📚  BIBLIOTECA — PAINEL ADMIN",
            font=ctk.CTkFont(family="Georgia", size=17, weight="bold"),
            text_color="#e8d5b0"
        ).pack(side="left", padx=24)

        ctk.CTkLabel(
            topbar, text=f"Admin: {self.nome_admin}",
            font=ctk.CTkFont(size=12),
            text_color="#c9a84c"
        ).pack(side="right", padx=24)

    def _criar_abas(self):
        # Botões de aba
        nav = ctk.CTkFrame(self.frame, fg_color="#13131f", height=44, corner_radius=0)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        self.aba_atual = ctk.StringVar(value="atrasados")

        for texto, valor in [("Atrasados", "atrasados"),
                             ("Todos Empréstimos", "todos"),
                             ("Usuários", "usuarios"),
                             ("Adicionar livro", "adicionar"),
                             ("Editar livros", "editar"),
                             ]:
            ctk.CTkButton(
                nav, text=texto, width=160, height=32,
                fg_color="transparent", hover_color="#1e1e30",
                text_color="#9ca3af", font=ctk.CTkFont(size=12),
                corner_radius=0,
                command=lambda v=valor: self._trocar_aba(v)
            ).pack(side="left", padx=(8, 0))

        ctk.CTkFrame(self.frame, height=1, fg_color="#1e1e30").pack(fill="x")

        # Área de conteúdo
        self.conteudo = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.conteudo.pack(fill="both", expand=True, padx=20, pady=16)

        self._trocar_aba("atrasados")

    def _trocar_aba(self, aba):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        if aba == "atrasados":
            self._aba_atrasados()
        elif aba == "todos":
            self._aba_todos()
        elif aba == "usuarios":
            self._aba_usuarios()
        elif aba == "adicionar":
            self._aba_adicionar()
        elif aba == "editar":
            self._aba_editar()
    # ── ABA ATRASADOS ──────────────────────────────────────────────
    def _aba_atrasados(self):
        ctk.CTkLabel(
            self.conteudo,
            text="Empréstimos em atraso",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f87171"
        ).pack(anchor="w", pady=(0, 12))

        # Atualiza status atrasado no banco automaticamente
        AdminDAO.atualizar_atrasados()

        registros = AdminDAO.listar_atrasados()

        scroll = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        if not registros:
            ctk.CTkLabel(
                scroll,
                text="Nenhum empréstimo em atraso.",
                font=ctk.CTkFont(size=13),
                text_color="#4b5563"
            ).pack(pady=30)
            return

        self._cabecalho(scroll, ["Usuário", "CPF", "Livro", "Empréstimo", "Devol. Prevista", "Dias Atraso", "Ação"])

        for r in registros:
            self._linha_atrasado(scroll, r)

    def _linha_atrasado(self, parent, r):
        linha = ctk.CTkFrame(parent, fg_color="#1a0a0a", corner_radius=8, border_width=1, border_color="#450a0a")
        linha.pack(fill="x", pady=3)

        dias = (datetime.now() - r["data_devolucao"]).days

        dados = [
            r["nome"], r["cpf"], r["titulo"],
            r["data_emprestimo"].strftime("%d/%m/%Y"),
            r["data_devolucao"].strftime("%d/%m/%Y"),
            f"{dias} dias"
        ]
        for d in dados:
            ctk.CTkLabel(linha, text=str(d), font=ctk.CTkFont(size=12),
                         text_color="#fca5a5", width=120, anchor="w").pack(side="left", padx=8, pady=8)

        lbl = ctk.CTkLabel(linha, text="", font=ctk.CTkFont(size=11), text_color="#22c55e")
        lbl.pack(side="right", padx=8)

        ctk.CTkButton(
            linha, text="Forçar Devolução", width=130, height=28,
            fg_color="#7f1d1d", hover_color="#991b1b",
            text_color="#fca5a5", font=ctk.CTkFont(size=11),
            corner_radius=6,
            command=lambda emp_id=r["emprestimo_id"], livro_id=r["livro_id"], l=lbl: self._forcar_devolucao(emp_id, livro_id, l)
        ).pack(side="right", padx=8)

    # ── ABA TODOS ──────────────────────────────────────────────────
    def _aba_todos(self):
        ctk.CTkLabel(
            self.conteudo,
            text="Todos os empréstimos",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e8d5b0"
        ).pack(anchor="w", pady=(0, 12))

        registros = AdminDAO.listar_todos_emprestimos()

        scroll = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        self._cabecalho(scroll, ["Usuário", "Livro", "Empréstimo", "Devolução", "Status"])

        cores_status = {
            "ativo":      ("#1e3a5f", "#93c5fd"),
            "devolvido":  ("#14532d", "#4ade80"),
            "atrasado":   ("#450a0a", "#f87171"),
        }

        for r in registros:
            status = r["status"]
            bg, fg = cores_status.get(status, ("#1a1a2e", "#9ca3af"))

            linha = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=8)
            linha.pack(fill="x", pady=3)

            devolucao = r["data_devolucao"].strftime("%d/%m/%Y") if r["data_devolucao"] else "—"

            for texto in [r["nome"], r["titulo"],
                          r["data_emprestimo"].strftime("%d/%m/%Y"),
                          devolucao]:
                ctk.CTkLabel(linha, text=str(texto), font=ctk.CTkFont(size=12),
                             text_color=fg, width=160, anchor="w").pack(side="left", padx=10, pady=8)

            ctk.CTkLabel(
                linha, text=status.upper(),
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=fg, fg_color=bg, corner_radius=6
            ).pack(side="left", padx=10)

    # ── ABA USUÁRIOS ───────────────────────────────────────────────
    def _aba_usuarios(self):
        ctk.CTkLabel(
            self.conteudo,
            text="Usuários cadastrados",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e8d5b0"
        ).pack(anchor="w", pady=(0, 12))

        usuarios = AdminDAO.listar_usuarios()

        scroll = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        self._cabecalho(scroll, ["Nome", "CPF", "Idade", "Admin", "Ativos", "Atrasados"])

        for u in usuarios:
            linha = ctk.CTkFrame(scroll, fg_color="#13131f", corner_radius=8,
                                 border_width=1, border_color="#1e1e30")
            linha.pack(fill="x", pady=3)

            admin_txt = "SIM" if u["admin"] else "não"
            admin_cor = "#c9a84c" if u["admin"] else "#6b7280"

            for texto, cor in [
                (u["nome"], "#e8d5b0"), (u["cpf"], "#9ca3af"),
                (str(u["idade"]), "#9ca3af"), (admin_txt, admin_cor),
                (str(u["ativos"]), "#93c5fd"), (str(u["atrasados"]), "#f87171")
            ]:
                ctk.CTkLabel(linha, text=texto, font=ctk.CTkFont(size=12),
                             text_color=cor, width=120, anchor="w").pack(side="left", padx=10, pady=8)

    # ── HELPERS ────────────────────────────────────────────────────
    def _cabecalho(self, parent, colunas):
        cab = ctk.CTkFrame(parent, fg_color="#0f0f17", corner_radius=0)
        cab.pack(fill="x", pady=(0, 4))
        for col in colunas:
            ctk.CTkLabel(cab, text=col.upper(), font=ctk.CTkFont(size=10, weight="bold"),
                         text_color="#4b5563", width=120, anchor="w").pack(side="left", padx=10, pady=4)

    def _forcar_devolucao(self, emprestimo_id, livro_id, label):
        sucesso, msg = AdminDAO.forcar_devolucao(emprestimo_id, livro_id)
        if sucesso:
            label.configure(text="Devolvido!", text_color="#22c55e")
            self.master.after(800, lambda: self._trocar_aba("atrasados"))
        else:
            label.configure(text=msg, text_color="#ef4444")

    def _aba_adicionar(self):
        ctk.CTkLabel(
            self.conteudo,
            text="Adicionar novo livro",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e8d5b0"
        ).pack(anchor="w", pady=(0, 16))

        form = ctk.CTkFrame(self.conteudo, fg_color="#13131f", corner_radius=12)
        form.pack(fill="x", padx=4, pady=4, ipadx=16, ipady=16)

        self.campos_livro = {}
        self.imagem_bytes = None

        for label, key in [("Título", "titulo"), ("Autor", "autor"),
                           ("Ano", "ano"), ("Quantidade", "quantidade")]:
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="#9ca3af", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
            entry = ctk.CTkEntry(
                form, height=40,
                fg_color="#1a1a2e", border_color="#2a2a4e", border_width=1,
                text_color="#e8d5b0", font=ctk.CTkFont(size=13), corner_radius=8
            )
            entry.pack(fill="x", padx=20)
            self.campos_livro[key] = entry

        # Botão selecionar imagem
        self.label_imagem = ctk.CTkLabel(
            form, text="Nenhuma imagem selecionada",
            font=ctk.CTkFont(size=11), text_color="#6b7280"
        )
        self.label_imagem.pack(anchor="w", padx=20, pady=(14, 4))

        ctk.CTkButton(
            form, text="Selecionar Imagem (PNG/JPG)",
            height=38, width=240,
            fg_color="#1e1e30", hover_color="#2a2a4e",
            text_color="#9ca3af", font=ctk.CTkFont(size=12),
            corner_radius=8,
            command=self._selecionar_imagem
        ).pack(anchor="w", padx=20)

        # Feedback
        self.label_feedback_livro = ctk.CTkLabel(
            form, text="", font=ctk.CTkFont(size=12), text_color="#22c55e"
        )
        self.label_feedback_livro.pack(pady=(10, 0))

        # Botão salvar
        ctk.CTkButton(
            form, text="SALVAR LIVRO", height=44,
            fg_color="#c9a84c", hover_color="#a8893e",
            text_color="#0f0f17", font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8, command=self._salvar_livro
        ).pack(fill="x", padx=20, pady=(8, 16))

    def _selecionar_imagem(self):
        from tkinter import filedialog
        caminho = filedialog.askopenfilename(
            title="Selecionar imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if caminho:
            with open(caminho, "rb") as f:
                self.imagem_bytes = f.read()
            nome = caminho.split("/")[-1].split("\\")[-1]
            self.label_imagem.configure(
                text=f"✓ {nome}  ({len(self.imagem_bytes)} bytes)",
                text_color="#4ade80"
            )

    def _salvar_livro(self):
        from model.Livro import Livro

        titulo = self.campos_livro["titulo"].get().strip()
        autor = self.campos_livro["autor"].get().strip()
        ano_txt = self.campos_livro["ano"].get().strip()
        qtd_txt = self.campos_livro["quantidade"].get().strip()

        # Validações
        if not titulo or not autor or not ano_txt or not qtd_txt:
            self.label_feedback_livro.configure(
                text="Preencha todos os campos.", text_color="#ef4444"
            )
            return
        if not ano_txt.isdigit() or not qtd_txt.isdigit():
            self.label_feedback_livro.configure(
                text="Ano e Quantidade devem ser números.", text_color="#ef4444"
            )
            return

        livro = Livro(
            titulo=titulo,
            autor=autor,
            ano=int(ano_txt),
            quantidade=int(qtd_txt),
            imagem=self.imagem_bytes if self.imagem_bytes else None
        )

        sucesso, mensagem = AdminDAO.adicionar_livro(livro)

        if sucesso:
            self.label_feedback_livro.configure(text=mensagem, text_color="#22c55e")
            for entry in self.campos_livro.values():
                entry.delete(0, "end")
            self.imagem_bytes = None
            self.label_imagem.configure(
                text="Nenhuma imagem selecionada", text_color="#6b7280"
            )
        else:
            self.label_feedback_livro.configure(text=mensagem, text_color="#ef4444")

    def _aba_editar(self):
        ctk.CTkLabel(
            self.conteudo,
            text="Editar livro",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e8d5b0"
        ).pack(anchor="w", pady=(0, 12))

        livros = LivroDAO.listar_livros()

        scroll = ctk.CTkScrollableFrame(self.conteudo, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for livro in livros:
            linha = ctk.CTkFrame(
                scroll, fg_color="#13131f", corner_radius=10,
                border_width=1, border_color="#1e1e30"
            )
            linha.pack(fill="x", pady=5, padx=4)

            # Imagem
            import io
            from PIL import Image
            img = None
            if livro.get("imagem"):
                try:
                    img = Image.open(io.BytesIO(livro["imagem"]))
                except Exception:
                    img = None
            if img is None:
                img = Image.new("RGB", (48, 72), color="#1e2a3a")

            capa = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 72))
            img_label = ctk.CTkLabel(linha, image=capa, text="")
            img_label.image = capa
            img_label.pack(side="left", padx=12, pady=10)

            # Info
            info = ctk.CTkFrame(linha, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, pady=10)

            ctk.CTkLabel(
                info, text=livro["titulo"],
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#e8d5b0", anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                info, text=f"{livro['autor']}  •  {livro['ano']}  •  {livro['quantidade']} unid.",
                font=ctk.CTkFont(size=11),
                text_color="#6b7280", anchor="w"
            ).pack(anchor="w")

            ctk.CTkButton(
                linha, text="Editar", width=90, height=30,
                fg_color="#1e3a5f", hover_color="#1e40af",
                text_color="#93c5fd",
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=6,
                command=lambda l=livro: self._abrir_form_edicao(l)
            ).pack(side="right", padx=12)

    def _abrir_form_edicao(self, livro):
        # Limpa conteúdo e abre formulário de edição
        for widget in self.conteudo.winfo_children():
            widget.destroy()

        ctk.CTkButton(
            self.conteudo, text="← Voltar", width=80, height=28,
            fg_color="transparent", hover_color="#1e1e30",
            text_color="#9ca3af", font=ctk.CTkFont(size=12),
            corner_radius=6,
            command=lambda: self._trocar_aba("editar")
        ).pack(anchor="w", pady=(0, 12))

        ctk.CTkLabel(
            self.conteudo,
            text=f"Editando: {livro['titulo']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e8d5b0"
        ).pack(anchor="w", pady=(0, 12))

        form = ctk.CTkFrame(self.conteudo, fg_color="#13131f", corner_radius=12)
        form.pack(fill="x", padx=4, ipadx=16, ipady=8)

        self.campos_edicao = {}
        self.imagem_edicao = None  # None = não trocou

        valores_atuais = {
            "titulo": livro["titulo"],
            "autor": livro["autor"],
            "ano": str(livro["ano"]),
            "quantidade": str(livro["quantidade"])
        }

        for label, key in [("Título", "titulo"), ("Autor", "autor"),
                           ("Ano", "ano"), ("Quantidade", "quantidade")]:
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="#9ca3af", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
            entry = ctk.CTkEntry(
                form, height=40,
                fg_color="#1a1a2e", border_color="#2a2a4e", border_width=1,
                text_color="#e8d5b0", font=ctk.CTkFont(size=13), corner_radius=8
            )
            entry.insert(0, valores_atuais[key])
            entry.pack(fill="x", padx=20)
            self.campos_edicao[key] = entry

        # Imagem atual
        img_frame = ctk.CTkFrame(form, fg_color="transparent")
        img_frame.pack(fill="x", padx=20, pady=(14, 0))

        import io
        from PIL import Image
        img = None
        if livro.get("imagem"):
            try:
                img = Image.open(io.BytesIO(livro["imagem"]))
            except Exception:
                img = None
        if img is None:
            img = Image.new("RGB", (60, 90), color="#1e2a3a")

        preview = ctk.CTkImage(light_image=img, dark_image=img, size=(60, 90))
        self.preview_label = ctk.CTkLabel(img_frame, image=preview, text="")
        self.preview_label.image = preview
        self.preview_label.pack(side="left", padx=(0, 12))

        lado_img = ctk.CTkFrame(img_frame, fg_color="transparent")
        lado_img.pack(side="left")

        self.label_imagem_edicao = ctk.CTkLabel(
            lado_img,
            text="Imagem atual" if livro.get("imagem") else "Sem imagem",
            font=ctk.CTkFont(size=11),
            text_color="#6b7280"
        )
        self.label_imagem_edicao.pack(anchor="w", pady=(0, 6))

        ctk.CTkButton(
            lado_img, text="Trocar Imagem", width=140, height=32,
            fg_color="#1e1e30", hover_color="#2a2a4e",
            text_color="#9ca3af", font=ctk.CTkFont(size=12),
            corner_radius=8,
            command=self._trocar_imagem_edicao
        ).pack(anchor="w")

        # Feedback
        self.label_feedback_edicao = ctk.CTkLabel(
            form, text="", font=ctk.CTkFont(size=12), text_color="#22c55e"
        )
        self.label_feedback_edicao.pack(pady=(10, 0))

        ctk.CTkButton(
            form, text="SALVAR ALTERAÇÕES", height=44,
            fg_color="#c9a84c", hover_color="#a8893e",
            text_color="#0f0f17", font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            command=lambda: self._salvar_edicao(livro["id"])
        ).pack(fill="x", padx=20, pady=(8, 16))

    def _trocar_imagem_edicao(self):
        from tkinter import filedialog
        from PIL import Image
        import io
        caminho = filedialog.askopenfilename(
            title="Selecionar imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if caminho:
            with open(caminho, "rb") as f:
                self.imagem_edicao = f.read()
            # Atualiza preview
            img = Image.open(io.BytesIO(self.imagem_edicao))
            preview = ctk.CTkImage(light_image=img, dark_image=img, size=(60, 90))
            self.preview_label.configure(image=preview)
            self.preview_label.image = preview
            nome = caminho.split("/")[-1].split("\\")[-1]
            self.label_imagem_edicao.configure(
                text=f"✓ {nome}", text_color="#4ade80"
            )

    def _salvar_edicao(self, livro_id):
        titulo = self.campos_edicao["titulo"].get().strip()
        autor = self.campos_edicao["autor"].get().strip()
        ano_txt = self.campos_edicao["ano"].get().strip()
        qtd_txt = self.campos_edicao["quantidade"].get().strip()

        if not titulo or not autor or not ano_txt or not qtd_txt:
            self.label_feedback_edicao.configure(
                text="Preencha todos os campos.", text_color="#ef4444"
            )
            return
        if not ano_txt.isdigit() or not qtd_txt.isdigit():
            self.label_feedback_edicao.configure(
                text="Ano e Quantidade devem ser números.", text_color="#ef4444"
            )
            return

        sucesso, mensagem = AdminDAO.editar_livro(
            livro_id, titulo, autor, int(ano_txt), int(qtd_txt), self.imagem_edicao
        )

        if sucesso:
            self.label_feedback_edicao.configure(text=mensagem, text_color="#22c55e")
        else:
            self.label_feedback_edicao.configure(text=mensagem, text_color="#ef4444")