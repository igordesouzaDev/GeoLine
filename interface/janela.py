"""Janela principal e telas do GeoLine."""

import tkinter as tk
from tkinter import messagebox, ttk

from backend.analisador import Analisador
from backend.reta_r2 import RetaR2
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor


class JanelaPrincipal:
    """Gerencia a navegação e conecta as telas às classes do backend."""

    AZUL_ESCURO = "#172B4D"
    AZUL = "#2878D0"
    FUNDO = "#F3F5F8"
    TEXTO = "#243247"

    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("GeoLine")
        self.root.geometry("900x760")
        self.root.minsize(720, 600)
        self.root.configure(bg=self.FUNDO)
        self.estilo = ttk.Style(self.root)
        self.estilo.theme_use("clam")
        self.estilo.configure("TButton", font=("Segoe UI", 11, "bold"), padding=(12, 10))
        self.estilo.configure("Principal.TButton", background=self.AZUL, foreground="white")
        self.estilo.map("Principal.TButton", background=[("active", "#1D5FA8")])
        self.estilo.configure("TLabel", background=self.FUNDO, foreground=self.TEXTO,
                              font=("Segoe UI", 10))
        self.estilo.configure("Titulo.TLabel", background=self.AZUL_ESCURO,
                              foreground="white", font=("Segoe UI", 17, "bold"))
        self.estilo.configure("Subtitulo.TLabel", background=self.AZUL_ESCURO,
                              foreground="white", font=("Segoe UI", 10))
        self.estilo.configure("TLabelframe", background=self.FUNDO, foreground=self.AZUL_ESCURO)
        self.estilo.configure("TLabelframe.Label", background=self.FUNDO,
                              foreground=self.AZUL_ESCURO, font=("Segoe UI", 10, "bold"))
        self.tela_atual = None
        self.campos = {}
        self.resultado = None
        self.grafico_container = None
        self.grafico_figura = None
        self.grafico_canvas = None
        self.grafico_toolbar = None
        self._grafico_pagina = False
        self.criar_menu()

    def _nova_tela(self, titulo, subtitulo=None, voltar=True):
        if self.tela_atual is not None:
            if self._grafico_pagina:
                self._limpar_grafico(mensagem=None)
                self.root.unbind_all("<MouseWheel>")
                self.root.unbind_all("<Button-4>")
                self.root.unbind_all("<Button-5>")
                self._grafico_pagina = False
                self.grafico_container = None
            self.tela_atual.destroy()
            self.resultado = None
        self.tela_atual = tk.Frame(self.root, bg=self.FUNDO)
        self.tela_atual.pack(fill="both", expand=True)
        cabecalho = tk.Frame(self.tela_atual, bg=self.AZUL_ESCURO, padx=24, pady=18)
        cabecalho.pack(fill="x")
        if voltar:
            tk.Button(cabecalho, text="← Menu", command=self.criar_menu,
                      bg=self.AZUL_ESCURO, fg="white", activebackground=self.AZUL,
                      activeforeground="white", relief="flat", font=("Segoe UI", 10, "bold"),
                      cursor="hand2").pack(side="left", padx=(0, 20))
        self.titulo_label = tk.Label(cabecalho, text=titulo, bg=self.AZUL_ESCURO, fg="white",
                                     font=("Segoe UI", 17, "bold"))
        if voltar:
            self.titulo_label.pack(side="left")
        else:
            self.titulo_label.configure(font=("Segoe UI", 35, "bold"))
            self.titulo_label.pack(fill="x")
        if subtitulo:
            tk.Label(self.tela_atual, text=subtitulo, bg=self.FUNDO, fg=self.TEXTO,
                     font=("Segoe UI", 10)).pack(anchor="w", padx=28, pady=(16, 4))
        self.conteudo = tk.Frame(self.tela_atual, bg=self.FUNDO, padx=28, pady=12)
        self.conteudo.pack(fill="both", expand=True)
        self.campos = {}
        return self.conteudo

    def criar_menu(self):
        conteudo = self._nova_tela("GeoLine", "Sistema de construção e análise de retas.", voltar=False)
        caixa = tk.Frame(conteudo, bg=self.FUNDO)
        caixa.place(relx=0.5, rely=0.48, anchor="center", relwidth=0.72)
        tk.Label(caixa, text="Menu principal", bg=self.FUNDO, fg=self.AZUL_ESCURO,
                 font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        botoes = (
            ("Construir reta no R²", self.tela_reta_r2),
            ("Construir reta no R³", self.tela_reta_r3),
            ("Analisar duas retas", self.tela_analisador),
            ("Gráficos 2D / 3D", self.tela_graficos),
        )
        for texto, comando in botoes:
            ttk.Button(caixa, text=texto, command=comando,
                       style="Principal.TButton").pack(fill="x", pady=7)

    def criar_campos_entrada(self, pai, prefixo, dimensao, linha=0):
        """Adiciona um grupo de coordenadas e guarda os Entry pelo nome."""
        grupo = ttk.LabelFrame(pai, text=prefixo, padding=10)
        grupo.grid(row=linha, column=0, sticky="ew", pady=5)
        pai.columnconfigure(0, weight=1)
        simbolos = ("X", "Y", "Z")[:dimensao]
        campos = []
        for coluna, simbolo in enumerate(simbolos):
            ttk.Label(grupo, text=simbolo).grid(row=0, column=coluna, sticky="w", padx=5)
            entrada = ttk.Entry(grupo, width=18, font=("Segoe UI", 10))
            entrada.grid(row=1, column=coluna, sticky="ew", padx=5, pady=(3, 0))
            grupo.columnconfigure(coluna, weight=1)
            campos.append(entrada)
        self.campos[prefixo] = campos
        return campos

    @staticmethod
    def _coordenadas(campos, descricao):
        valores = []
        for indice, campo in enumerate(campos, start=1):
            texto = campo.get().strip().replace(",", ".")
            if not texto:
                raise ValueError(f"Preencha todas as coordenadas de {descricao}.")
            try:
                valores.append(float(texto))
            except ValueError as exc:
                raise ValueError(f"A coordenada {indice} de {descricao} deve ser numérica.") from exc
        return Vetor(valores)

    def obter_dados(self, prefixo):
        """Lê os campos nomeados e retorna um Vetor validado pelo backend."""
        if prefixo not in self.campos:
            raise ValueError(f"Campos não encontrados: {prefixo}.")
        return self._coordenadas(self.campos[prefixo], prefixo)

    def _construir_reta(self, dimensao, prefixo):
        ponto_inicial = self.obter_dados(f"{prefixo} — ponto inicial")
        ponto_final = self.obter_dados(f"{prefixo} — ponto final")
        classe = RetaR2 if dimensao == 2 else RetaR3
        return classe(ponto_inicial, ponto_final)

    def _formulario_reta(self, dimensao, titulo):
        conteudo = self._nova_tela(titulo, "Informe dois pontos distintos para definir a reta.")
        self.criar_campos_entrada(conteudo, "Reta — ponto inicial", dimensao)
        self.criar_campos_entrada(conteudo, "Reta — ponto final", dimensao, linha=1)
        ttk.Button(conteudo, text="CALCULAR", style="Principal.TButton",
                   command=lambda: self.calcular_reta(dimensao)).grid(row=2, column=0, sticky="ew", pady=12)
        self.resultado = tk.Text(conteudo, height=8, wrap="word", font=("Consolas", 10),
                                 relief="solid", bd=1, state="disabled")
        self.resultado.grid(row=3, column=0, sticky="ew", pady=5)
        self.criar_campos_entrada(conteudo, "Ponto para verificar", dimensao, linha=4)
        ttk.Button(conteudo, text="VERIFICAR PERTENCIMENTO",
                   command=lambda: self.verificar_pertencimento(dimensao)).grid(
                       row=5, column=0, sticky="ew", pady=(4, 8))
        conteudo.rowconfigure(3, weight=1)

    def tela_reta_r2(self):
        self._formulario_reta(2, "Construir reta no R²")

    def tela_reta_r3(self):
        self._formulario_reta(3, "Construir reta no R³")

    def exibir_resultados(self, texto):
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("end", texto)
        self.resultado.configure(state="disabled")

    def calcular_reta(self, dimensao=None):
        self._limpar_resultados()
        try:
            if dimensao is None:
                dimensao = 2 if len(self.campos.get("Reta — ponto inicial", [])) == 2 else 3
            reta = self._construir_reta(dimensao, "Reta")
            linhas = [
                f"Ponto inicial: {reta.ponto_inicial}",
                f"Ponto final: {reta.obter_ponto(1)}",
                f"Vetor diretor: {reta.vetor_diretor}",
                f"Equação vetorial: {reta.equacao_vetorial()}",
                "Equações paramétricas:", reta.equacao_parametrica(),
                f"Equação simétrica: {reta.equacao_simetrica()}",
            ]
            if dimensao == 2:
                linhas.append(f"Equação reduzida: {reta.equacao_reduzida()}")
            self.exibir_resultados("\n".join(linhas))
        except (TypeError, ValueError, OverflowError) as erro:
            messagebox.showerror("Não foi possível calcular a reta", str(erro), parent=self.root)

    def verificar_pertencimento(self, dimensao):
        try:
            reta = self._construir_reta(dimensao, "Reta")
            ponto = self.obter_dados("Ponto para verificar")
            pertence = reta.ponto_pertence(ponto)
            mensagem = "O ponto pertence à reta." if pertence else "O ponto não pertence à reta."
            messagebox.showinfo("Verificação de pertencimento", mensagem, parent=self.root)
        except (TypeError, ValueError, OverflowError) as erro:
            messagebox.showerror("Não foi possível verificar o ponto", str(erro), parent=self.root)

    def tela_analisador(self):
        conteudo = self._nova_tela("Analisar duas retas", "Escolha o espaço e informe dois pontos para cada reta.")
        seletor = ttk.Frame(conteudo)
        seletor.grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Label(seletor, text="Dimensão:").pack(side="left", padx=(0, 10))
        self.dimensao_analise = tk.IntVar(value=2)
        ttk.Radiobutton(seletor, text="R²", variable=self.dimensao_analise, value=2,
                        command=self._atualizar_form_analisador).pack(side="left", padx=5)
        ttk.Radiobutton(seletor, text="R³", variable=self.dimensao_analise, value=3,
                        command=self._atualizar_form_analisador).pack(side="left", padx=5)
        self.form_analisador = ttk.Frame(conteudo)
        self.form_analisador.grid(row=1, column=0, sticky="ew")
        self._atualizar_form_analisador()
        ttk.Button(conteudo, text="ANALISAR RETAS", style="Principal.TButton",
                   command=self.analisar_retas).grid(row=2, column=0, sticky="ew", pady=10)
        self.resultado = tk.Text(conteudo, height=8, wrap="word", font=("Segoe UI", 10),
                                 relief="solid", bd=1, state="disabled")
        self.resultado.grid(row=3, column=0, sticky="nsew")
        conteudo.rowconfigure(3, weight=1)

    def _atualizar_form_analisador(self):
        for filho in self.form_analisador.winfo_children():
            filho.destroy()
        self.campos = {}
        dimensao = self.dimensao_analise.get()
        for indice, nome in enumerate(("Reta 1", "Reta 2")):
            bloco = ttk.LabelFrame(self.form_analisador, text=nome, padding=7)
            bloco.grid(row=indice, column=0, sticky="ew", pady=4)
            bloco.columnconfigure(0, weight=1)
            self.criar_campos_entrada(bloco, f"{nome} — ponto inicial", dimensao, 0)
            self.criar_campos_entrada(bloco, f"{nome} — ponto final", dimensao, 1)
        self.form_analisador.columnconfigure(0, weight=1)

    def analisar_retas(self):
        self._limpar_resultados()
        try:
            dimensao = self.dimensao_analise.get()
            reta1 = self._construir_reta(dimensao, "Reta 1")
            reta2 = self._construir_reta(dimensao, "Reta 2")
            resultado = Analisador.analisar(reta1, reta2)
            relacao = resultado["relacao"].capitalize()
            linhas = [f"Relação: {relacao}", resultado["mensagem"],
                      f"Paralelas: {'Sim' if resultado['sao_paralelas'] else 'Não'}",
                      f"Coincidentes: {'Sim' if resultado['sao_coincidentes'] else 'Não'}",
                      f"Reversas: {'Sim' if resultado['sao_reversas'] else 'Não'}"]
            ponto = resultado["ponto_intersecao"]
            linhas.append(f"Ponto de interseção: {ponto}" if ponto is not None
                          else "Ponto de interseção: não há ponto único.")
            if dimensao == 3:
                produto_escalar = reta1.vetor_diretor.produto_escalar(reta2.vetor_diretor)
                ortogonais = reta1.eh_ortogonal(reta2)
                angulo = reta1.angulo_com(reta2)
                distancia = reta1.distancia_reta(reta2)
                linhas.extend((
                    f"Produto escalar dos vetores diretores: {self._formatar_numero_exibicao(produto_escalar)}",
                    f"Ortogonalidade: {'Sim' if ortogonais else 'Não'}",
                    f"Ângulo entre as retas: {self._formatar_numero_exibicao(angulo)}°",
                    f"Distância entre as retas: {self._formatar_numero_exibicao(distancia)}",
                ))
            self.exibir_resultados("\n".join(linhas))
        except (TypeError, ValueError, OverflowError) as erro:
            messagebox.showerror("Não foi possível analisar as retas", str(erro), parent=self.root)

    def tela_graficos(self):
        conteudo = self._nova_tela(
            "Gráficos 2D / 3D",
            "Escolha a dimensão, a quantidade de retas e informe os pontos.",
        )
        conteudo.destroy()
        self._criar_area_rolavel()
        conteudo = self.conteudo
        opcoes = ttk.Frame(conteudo)
        opcoes.grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.dimensao_grafico = tk.IntVar(value=2)
        ttk.Label(opcoes, text="Dimensão:").pack(side="left")
        for texto, valor in (("2D (R²)", 2), ("3D (R³)", 3)):
            ttk.Radiobutton(opcoes, text=texto, variable=self.dimensao_grafico, value=valor,
                            command=self._atualizar_form_graficos).pack(side="left", padx=8)
        ttk.Label(opcoes, text="Quantidade:").pack(side="left", padx=(20, 5))
        self.quantidade_graficos = tk.IntVar(value=1)
        for texto, valor in (("Uma reta", 1), ("Duas retas", 2)):
            ttk.Radiobutton(opcoes, text=texto, variable=self.quantidade_graficos, value=valor,
                            command=self._atualizar_form_graficos).pack(side="left", padx=5)
        self.form_graficos = ttk.Frame(conteudo)
        self.form_graficos.grid(row=1, column=0, sticky="ew")
        self.grafico_container = tk.Frame(conteudo, bg="white")
        self.grafico_container.grid(row=3, column=0, sticky="nsew", pady=(12, 0))
        conteudo.rowconfigure(3, weight=1)
        self._grafico_pagina = True
        self._atualizar_form_graficos()

    def _criar_area_rolavel(self):
        """Substitui a área do conteúdo por um painel vertical rolável."""
        area = tk.Frame(self.tela_atual, bg=self.FUNDO)
        area.pack(fill="both", expand=True)
        self.canvas_rolagem = tk.Canvas(
            area, bg=self.FUNDO, highlightthickness=0, yscrollincrement=24
        )
        barra = ttk.Scrollbar(area, orient="vertical", command=self.canvas_rolagem.yview)
        self.canvas_rolagem.configure(yscrollcommand=barra.set)
        self.canvas_rolagem.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.conteudo = tk.Frame(self.canvas_rolagem, bg=self.FUNDO, padx=28, pady=12)
        self._janela_conteudo = self.canvas_rolagem.create_window(
            (0, 0), window=self.conteudo, anchor="nw"
        )
        self.conteudo.bind(
            "<Configure>",
            lambda _evento: self.canvas_rolagem.configure(
                scrollregion=self.canvas_rolagem.bbox("all")
            ),
        )
        self.canvas_rolagem.bind(
            "<Configure>",
            lambda evento: self.canvas_rolagem.itemconfigure(
                self._janela_conteudo, width=evento.width
            ),
        )
        self.root.bind_all("<MouseWheel>", self._rolar_com_mouse)
        self.root.bind_all("<Button-4>", self._rolar_com_mouse)
        self.root.bind_all("<Button-5>", self._rolar_com_mouse)
        self._rolagem_ativa = True

    def _rolar_com_mouse(self, evento):
        if getattr(evento, "num", None) == 4:
            unidades = -1
        elif getattr(evento, "num", None) == 5:
            unidades = 1
        else:
            unidades = -int(evento.delta / 120)
            if evento.delta and unidades == 0:
                unidades = -1 if evento.delta > 0 else 1
        if unidades:
            self.canvas_rolagem.yview_scroll(unidades, "units")
        return "break"

    def _rolar_para_grafico(self):
        if not self._grafico_pagina or self.grafico_container is None:
            return
        self.canvas_rolagem.update_idletasks()
        limites = self.canvas_rolagem.bbox("all")
        if limites and limites[3] > 0:
            topo = self.grafico_container.winfo_y()
            self.canvas_rolagem.yview_moveto(min(topo / limites[3], 1.0))

    def _atualizar_form_graficos(self):
        self._limpar_grafico()
        for filho in self.form_graficos.winfo_children():
            filho.destroy()
        self.campos = {}
        dimensao = self.dimensao_grafico.get()
        for indice in range(self.quantidade_graficos.get()):
            nome = f"Reta {indice + 1}"
            bloco = ttk.LabelFrame(self.form_graficos, text=nome, padding=7)
            bloco.grid(row=indice, column=0, sticky="ew", pady=4)
            bloco.columnconfigure(0, weight=1)
            self.criar_campos_entrada(bloco, f"{nome} — ponto inicial", dimensao, 0)
            self.criar_campos_entrada(bloco, f"{nome} — ponto final", dimensao, 1)
        self.form_graficos.columnconfigure(0, weight=1)
        ttk.Button(self.form_graficos, text="GERAR GRÁFICO", style="Principal.TButton",
                   command=self.exibir_grafico).grid(row=self.quantidade_graficos.get(), column=0,
                                                     sticky="ew", pady=8)

    def _limpar_grafico(self, mensagem="A figura será exibida aqui após gerar o gráfico."):
        """Destrói canvas e barra existentes e libera os dados da figura anterior."""
        if self.grafico_container is None:
            return
        if self.grafico_figura is not None:
            try:
                self.grafico_figura.clear()
            except tk.TclError:
                # A barra pode já ter perdido a janela Tcl durante uma falha de renderização.
                pass
        for filho in self.grafico_container.winfo_children():
            try:
                filho.destroy()
            except tk.TclError:
                pass
        self.grafico_figura = None
        self.grafico_canvas = None
        self.grafico_toolbar = None
        if mensagem:
            tk.Label(self.grafico_container, text=mensagem, bg="white",
                     fg=self.TEXTO, font=("Segoe UI", 10)).pack(
                         fill="both", expand=True, padx=10, pady=24
                     )

    @staticmethod
    def _formatar_numero_exibicao(valor):
        return f"{valor:.6g}"

    def _limpar_resultados(self):
        if self.resultado is not None and self.resultado.winfo_exists():
            self.exibir_resultados("")

    def exibir_grafico(self):
        self._limpar_grafico("Preparando o gráfico...")
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            from visualizacao.graficos import Graficos

            dimensao = self.dimensao_grafico.get()
            quantidade = self.quantidade_graficos.get()
            retas = [self._construir_reta(dimensao, f"Reta {indice + 1}")
                     for indice in range(quantidade)]
            if dimensao == 2:
                figura, _ = (Graficos.plotar_reta_r2(retas[0]) if quantidade == 1
                             else Graficos.plotar_duas_retas_r2(*retas))
            else:
                figura, _ = (Graficos.plotar_reta_r3(retas[0]) if quantidade == 1
                             else Graficos.plotar_duas_retas_r3(*retas))
            self._limpar_grafico(mensagem=None)
            self.grafico_figura = figura
            self.grafico_canvas = FigureCanvasTkAgg(figura, master=self.grafico_container)
            self.grafico_canvas.draw()
            self.grafico_toolbar = NavigationToolbar2Tk(
                self.grafico_canvas, self.grafico_container, pack_toolbar=False
            )
            self.grafico_toolbar.update()
            self.grafico_toolbar.pack(side="bottom", fill="x")
            self.grafico_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
            self.root.after_idle(self._rolar_para_grafico)
        except (ImportError, TypeError, ValueError, OverflowError, RuntimeError, tk.TclError) as erro:
            self._limpar_grafico("Não foi possível gerar. Corrija os dados e tente novamente.")
            messagebox.showerror("Não foi possível gerar o gráfico", str(erro), parent=self.root)

    def iniciar(self):
        self.root.mainloop()


Interface = JanelaPrincipal
