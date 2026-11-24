import tkinter as tk
from tkinter import messagebox, ttk

from filas import ErroFila, GerenciadorFilas


TEMAS = {
    "escuro": {
        "bg": "#0f172a",
        "surface": "#1e293b",
        "surface_alt": "#162032",
        "border": "#334155",
        "text": "#f1f5f9",
        "text_muted": "#94a3b8",
        "accent": "#38bdf8",
        "accent_fg": "#082f49",
        "accent_hover": "#0284c7",
        "btn_bg": "#29384f",
        "btn_hover": "#374b69",
        "btn_fg": "#f8fafc",
        "pref_fg": "#fbbf24",
        "norm_fg": "#cbd5e1",
        "select_bg": "#0369a1",
        "select_fg": "#ffffff",
    },
    "claro": {
        "bg": "#f1f5f9",
        "surface": "#ffffff",
        "surface_alt": "#f8fafc",
        "border": "#cbd5e1",
        "text": "#0f172a",
        "text_muted": "#475569",
        "accent": "#0284c7",
        "accent_fg": "#ffffff",
        "accent_hover": "#0369a1",
        "btn_bg": "#e2e8f0",
        "btn_hover": "#cbd5e1",
        "btn_fg": "#0f172a",
        "pref_fg": "#b45309",
        "norm_fg": "#334155",
        "select_bg": "#0284c7",
        "select_fg": "#ffffff",
    },
}


class TelaClinica:
    def __init__(self, root, gerenciador=None):
        self.root = root
        self.root.title("Sistema de Filas — Clínica")
        self.root.geometry("820x520")
        self.root.minsize(720, 460)

        self.gerenciador = gerenciador if gerenciador is not None else GerenciadorFilas()
        self.tema_atual = "escuro"

        especialidades = list(self.gerenciador.ESPECIALIDADES.keys())
        self.var_especialidade = tk.StringVar(value=especialidades[0])
        self.var_categoria = tk.StringVar(value="Normal")
        self.var_tema = tk.StringVar(value="Modo Escuro")

        self._configurar_estilos()
        self._montar_interface(especialidades)
        self._aplicar_tema("escuro")
        self._atualizar_tudo()

    def _configurar_estilos(self):
        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

    def _montar_interface(self, especialidades):
        self.root_bg = tk.Frame(self.root)
        self.root_bg.pack(fill=tk.BOTH, expand=True)

        container = tk.Frame(self.root_bg)
        container.pack(fill=tk.BOTH, expand=True, padx=18, pady=16)

        # Topo simples: título à esquerda, seletor de tema à direita
        topo = tk.Frame(container)
        topo.pack(fill=tk.X, pady=(0, 14))

        self.lbl_titulo = tk.Label(
            topo,
            text="Filas da Clínica",
            font=("TkDefaultFont", 16, "bold"),
        )
        self.lbl_titulo.pack(side=tk.LEFT)

        tema_box = tk.Frame(topo)
        tema_box.pack(side=tk.RIGHT)

        self.lbl_tema = tk.Label(tema_box, text="Tema:", font=("TkDefaultFont", 9, "bold"))
        self.lbl_tema.pack(side=tk.LEFT, padx=(0, 6))

        self.combo_tema = ttk.Combobox(
            tema_box,
            textvariable=self.var_tema,
            values=["Modo Escuro", "Modo Claro"],
            state="readonly",
            width=12,
        )
        self.combo_tema.pack(side=tk.LEFT)
        self.combo_tema.bind("<<ComboboxSelected>>", self._ao_trocar_tema)

        # Corpo em 2 colunas: Esquerda = ações | Direita = chamada + fila
        corpo = tk.Frame(container)
        corpo.pack(fill=tk.BOTH, expand=True)

        coluna_esq = tk.Frame(corpo, width=265)
        coluna_esq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))
        coluna_esq.pack_propagate(False)

        coluna_dir = tk.Frame(corpo)
        coluna_dir.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Coluna esquerda: seleção e ações principais
        self.card_acoes = tk.Frame(coluna_esq, highlightthickness=1, padx=14, pady=14)
        self.card_acoes.pack(fill=tk.BOTH, expand=True)

        self.lbl_esp = tk.Label(
            self.card_acoes, text="Especialidade", font=("TkDefaultFont", 9, "bold")
        )
        self.lbl_esp.pack(anchor=tk.W, pady=(0, 4))

        self.combo_esp = ttk.Combobox(
            self.card_acoes,
            textvariable=self.var_especialidade,
            values=especialidades,
            state="readonly",
        )
        self.combo_esp.pack(fill=tk.X, pady=(0, 14))
        self.combo_esp.bind("<<ComboboxSelected>>", lambda _e: self._atualizar_tudo())

        self.lbl_cat = tk.Label(
            self.card_acoes, text="Categoria", font=("TkDefaultFont", 9, "bold")
        )
        self.lbl_cat.pack(anchor=tk.W, pady=(0, 4))

        self.rb_normal = tk.Radiobutton(
            self.card_acoes,
            text="Normal",
            variable=self.var_categoria,
            value="Normal",
            takefocus=False,
        )
        self.rb_normal.pack(anchor=tk.W)

        self.rb_pref = tk.Radiobutton(
            self.card_acoes,
            text="Preferencial",
            variable=self.var_categoria,
            value="Preferencial",
            takefocus=False,
        )
        self.rb_pref.pack(anchor=tk.W, pady=(0, 16))

        self.btn_emitir = tk.Button(
            self.card_acoes,
            text="Emitir Senha",
            font=("TkDefaultFont", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            pady=8,
            command=self._ao_emitir_senha,
        )
        self.btn_emitir.pack(fill=tk.X, pady=(0, 8))

        self.btn_chamar = tk.Button(
            self.card_acoes,
            text="Chamar Próxima",
            font=("TkDefaultFont", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            pady=8,
            command=self._ao_chamar_proxima,
        )
        self.btn_chamar.pack(fill=tk.X, pady=(0, 8))

        self.btn_historico = tk.Button(
            self.card_acoes,
            text="Ver Histórico",
            font=("TkDefaultFont", 9),
            relief=tk.FLAT,
            cursor="hand2",
            pady=7,
            command=self._abrir_historico,
        )
        self.btn_historico.pack(fill=tk.X)

        # Coluna direita superior: última chamada
        self.card_chamada = tk.Frame(coluna_dir, highlightthickness=1, padx=14, pady=12)
        self.card_chamada.pack(fill=tk.X, pady=(0, 12))

        self.lbl_tag_chamada = tk.Label(
            self.card_chamada, text="ÚLTIMA CHAMADA", font=("TkDefaultFont", 8, "bold")
        )
        self.lbl_tag_chamada.pack(anchor=tk.W)

        self.lbl_ultima_senha = tk.Label(
            self.card_chamada,
            text="Nenhuma senha chamada",
            font=("TkDefaultFont", 18, "bold"),
        )
        self.lbl_ultima_senha.pack(anchor=tk.W, pady=(2, 0))

        self.lbl_ultima_info = tk.Label(
            self.card_chamada,
            text="Aguardando chamada.",
            font=("TkDefaultFont", 9),
        )
        self.lbl_ultima_info.pack(anchor=tk.W)

        # Coluna direita inferior: fila de espera
        self.card_fila = tk.Frame(coluna_dir, highlightthickness=1, padx=14, pady=12)
        self.card_fila.pack(fill=tk.BOTH, expand=True)

        self.lbl_resumo_fila = tk.Label(
            self.card_fila, text="", font=("TkDefaultFont", 10, "bold")
        )
        self.lbl_resumo_fila.pack(anchor=tk.W, pady=(0, 8))

        lista_box = tk.Frame(self.card_fila, highlightthickness=1)
        lista_box.pack(fill=tk.BOTH, expand=True)

        self.scrollbar_fila = ttk.Scrollbar(lista_box, orient=tk.VERTICAL)
        self.listbox_fila = tk.Listbox(
            lista_box,
            yscrollcommand=self.scrollbar_fila.set,
            font=("TkFixedFont", 10),
            relief=tk.FLAT,
            highlightthickness=0,
            activestyle="none",
        )
        self.scrollbar_fila.config(command=self.listbox_fila.yview)

        self.listbox_fila.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.scrollbar_fila.pack(side=tk.RIGHT, fill=tk.Y)

    def _ao_trocar_tema(self, _evento=None):
        modo = "claro" if self.var_tema.get() == "Modo Claro" else "escuro"
        self._aplicar_tema(modo)
        self._atualizar_lista_fila()

    def _aplicar_tema(self, modo):
        self.tema_atual = modo
        t = TEMAS[modo]

        self.root.configure(bg=t["bg"])
        self._pintar_fundo(self.root_bg, t["bg"])

        self.style.configure(
            "TCombobox",
            fieldbackground=t["surface_alt"],
            background=t["btn_bg"],
            foreground=t["text"],
            arrowcolor=t["text"],
            bordercolor=t["border"],
            lightcolor=t["border"],
            darkcolor=t["border"],
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", t["surface_alt"])],
            foreground=[("readonly", t["text"])],
            selectbackground=[("readonly", t["select_bg"])],
            selectforeground=[("readonly", t["select_fg"])],
        )

        for card in (self.card_acoes, self.card_chamada, self.card_fila):
            card.configure(
                bg=t["surface"],
                highlightbackground=t["border"],
                highlightcolor=t["border"],
            )

        self.lbl_titulo.configure(bg=t["bg"], fg=t["text"])
        self.lbl_tema.configure(bg=t["bg"], fg=t["text_muted"])

        self.lbl_esp.configure(bg=t["surface"], fg=t["text"])
        self.lbl_cat.configure(bg=t["surface"], fg=t["text"])
        self.lbl_tag_chamada.configure(bg=t["surface"], fg=t["accent"])
        self.lbl_ultima_senha.configure(bg=t["surface"], fg=t["text"])
        self.lbl_ultima_info.configure(bg=t["surface"], fg=t["text_muted"])
        self.lbl_resumo_fila.configure(bg=t["surface"], fg=t["text"])

        for rb in (self.rb_normal, self.rb_pref):
            rb.configure(
                bg=t["surface"],
                fg=t["text"],
                activebackground=t["surface"],
                activeforeground=t["accent"],
                selectcolor=t["surface_alt"],
            )

        self.btn_emitir.configure(
            bg=t["accent"],
            fg=t["accent_fg"],
            activebackground=t["accent_hover"],
            activeforeground=t["accent_fg"],
        )
        for btn in (self.btn_chamar, self.btn_historico):
            btn.configure(
                bg=t["btn_bg"],
                fg=t["btn_fg"],
                activebackground=t["btn_hover"],
                activeforeground=t["btn_fg"],
            )

        lista_pai = self.listbox_fila.master
        lista_pai.configure(
            bg=t["surface_alt"],
            highlightbackground=t["border"],
            highlightcolor=t["border"],
        )
        self.listbox_fila.configure(
            bg=t["surface_alt"],
            fg=t["text"],
            selectbackground=t["select_bg"],
            selectforeground=t["select_fg"],
        )

    def _pintar_fundo(self, widget, cor):
        cards = {self.card_acoes, self.card_chamada, self.card_fila, self.listbox_fila.master}
        if isinstance(widget, tk.Frame) and widget not in cards:
            widget.configure(bg=cor)
            for filho in widget.winfo_children():
                self._pintar_fundo(filho, cor)

    def _ao_emitir_senha(self):
        esp = self.var_especialidade.get()
        cat = self.var_categoria.get()

        try:
            senha, espera_min = self.gerenciador.emitir_senha(esp, cat)
        except ErroFila as erro:
            messagebox.showerror("Erro ao emitir senha", str(erro))
            return

        self._atualizar_tudo()
        messagebox.showinfo(
            "Senha Emitida",
            f"Senha: {senha.codigo}\n"
            f"Especialidade: {senha.especialidade}\n"
            f"Categoria: {senha.categoria}\n"
            f"Horário: {senha.hora}\n"
            f"Tempo estimado de espera: {espera_min} min",
        )

    def _ao_chamar_proxima(self):
        esp = self.var_especialidade.get()

        try:
            self.gerenciador.chamar_proxima(esp)
        except ErroFila as erro:
            messagebox.showwarning("Aviso", str(erro))
            self._atualizar_tudo()
            return

        self._atualizar_tudo()

    def _atualizar_painel_chamada(self):
        ultima = self.gerenciador.ultima_chamada
        if ultima is None:
            self.lbl_ultima_senha.config(text="Nenhuma senha chamada")
            self.lbl_ultima_info.config(text="Aguardando chamada.")
        else:
            self.lbl_ultima_senha.config(text=f"{ultima.codigo}  ·  {ultima.especialidade}")
            self.lbl_ultima_info.config(
                text=f"{ultima.categoria}  ·  Emitida às {ultima.hora}"
            )

    def _atualizar_lista_fila(self):
        t = TEMAS[self.tema_atual]
        esp = self.var_especialidade.get()
        self.listbox_fila.delete(0, tk.END)

        try:
            dados = self.gerenciador.ver_fila(esp)
        except ErroFila as erro:
            messagebox.showerror("Erro", str(erro))
            return

        self.lbl_resumo_fila.config(
            text=(
                f"{esp} — {dados['total']} na fila "
                f"(Pref: {dados['preferenciais']} | Normal: {dados['normais']})"
            )
        )

        senhas = dados["senhas"]
        if not senhas:
            self.listbox_fila.insert(tk.END, "  Nenhum paciente aguardando.")
            self.listbox_fila.itemconfig(0, fg=t["text_muted"])
            return

        minutos = self.gerenciador.MINUTOS_POR_PACIENTE
        for idx, item in enumerate(senhas):
            espera = idx * minutos
            linha = (
                f"  {idx + 1:>2}º  {item.codigo:<8}  {item.categoria:<12}  "
                f"~{espera} min"
            )
            self.listbox_fila.insert(tk.END, linha)
            cor = t["pref_fg"] if item.categoria == "Preferencial" else t["norm_fg"]
            self.listbox_fila.itemconfig(idx, fg=cor)

    def _atualizar_tudo(self):
        self._atualizar_painel_chamada()
        self._atualizar_lista_fila()

    def _abrir_historico(self):
        t = TEMAS[self.tema_atual]

        janela = tk.Toplevel(self.root)
        janela.title("Histórico de Chamadas")
        janela.geometry("500x320")
        janela.configure(bg=t["bg"])
        janela.transient(self.root)

        frame = tk.Frame(janela, bg=t["bg"], padx=14, pady=14)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            frame,
            text="Histórico de Chamadas",
            bg=t["bg"],
            fg=t["text"],
            font=("TkDefaultFont", 12, "bold"),
        ).pack(anchor=tk.W, pady=(0, 8))

        lista_box = tk.Frame(
            frame,
            bg=t["surface_alt"],
            highlightbackground=t["border"],
            highlightcolor=t["border"],
            highlightthickness=1,
        )
        lista_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        lista = tk.Listbox(
            lista_box,
            bg=t["surface_alt"],
            fg=t["text"],
            selectbackground=t["select_bg"],
            selectforeground=t["select_fg"],
            font=("TkFixedFont", 10),
            relief=tk.FLAT,
            highlightthickness=0,
            activestyle="none",
        )
        lista.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        historico = self.gerenciador.ver_historico()
        if not historico:
            lista.insert(tk.END, "  Nenhuma senha chamada ainda.")
            lista.itemconfig(0, fg=t["text_muted"])
        else:
            for pos, senha in enumerate(historico, start=1):
                linha = (
                    f"  {pos:>2}. {senha.codigo:<8}  {senha.especialidade:<14}  "
                    f"{senha.categoria:<12}  {senha.hora}"
                )
                lista.insert(tk.END, linha)
                cor = t["pref_fg"] if senha.categoria == "Preferencial" else t["norm_fg"]
                lista.itemconfig(pos - 1, fg=cor)

        tk.Button(
            frame,
            text="Fechar",
            bg=t["btn_bg"],
            fg=t["btn_fg"],
            activebackground=t["btn_hover"],
            activeforeground=t["btn_fg"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=6,
            command=janela.destroy,
        ).pack(anchor=tk.E)


if __name__ == "__main__":
    root = tk.Tk()
    app = TelaClinica(root)
    root.mainloop()
