import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

caminho_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(caminho_raiz))

from visualizacao import Grafico

class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screenWidth}x{self.screenHeight}")
        self.root.title("GeoLine")

        self.cor_principal = "RoyalBlue4"
        self.cor_secundaria = "DodgerBlue2"

    def menu_principal(self, frame_anterior=None):
        if frame_anterior:
            frame_anterior.pack_forget()

        self.menu_principal_frame = tk.Frame(self.root)
        self.menu_principal_frame.pack(fill="both", expand=True)

        self.topFrame = tk.Frame(self.menu_principal_frame, background=self.cor_principal, pady=30)
        self.topFrame.pack(fill="x")

        tk.Label(self.topFrame, text="GeoLine", font=("Arial", 35, "bold"), background=self.cor_principal, foreground="white").pack()
        tk.Label(self.topFrame, text="Sistema de construção e análise de retas", font=("Arial", 14), background=self.cor_principal, foreground="white").pack()

        self.bottomFrame = tk.Frame(self.menu_principal_frame)
        self.bottomFrame.pack(fill="both", expand=True)

        tk.Label(self.bottomFrame, text="Menu principal", font=("Arial", 18, "bold"), foreground=self.cor_principal).pack(pady=(30, 0))
        ttk.Button(self.bottomFrame, text="Construir reta no R²", command=lambda: self.menu_reta_r2(self.menu_principal_frame), cursor="hand2").pack(pady=(30, 0))
        ttk.Button(self.bottomFrame, text="Construir reta no R³", command=lambda: self.menu_reta_r3(self.menu_principal_frame), cursor="hand2").pack(pady=(30, 0))
        ttk.Button(self.bottomFrame, text="Analisar duas retas", cursor="hand2").pack(pady=(30, 0))
        ttk.Button(self.bottomFrame, text="Gráficos 2D / 3D", cursor="hand2", padding=(516, 18)).pack(pady=(30, 0))

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 14, "bold"), background=self.cor_secundaria, foreground="white", padding=(500, 18))

    def menu_reta_r2(self, frame_anterior):
        frame_anterior.pack_forget();

        self.menu_reta_r2_frame = tk.Frame(self.root)
        self.menu_reta_r2_frame.pack(fill="both", expand=True)

        self.topFrame = tk.Frame(self.menu_reta_r2_frame, background=self.cor_principal, pady=15)
        self.topFrame.pack(fill="x")

        tk.Button(self.topFrame, text="⬅", command=lambda: self.menu_principal(self.menu_reta_r2_frame), font=("Arial", 20, "bold"), relief="flat", background=self.cor_principal, foreground="white", cursor="hand2").pack(side="left", padx=(10, 0))
        tk.Label(self.topFrame, text="Construir reta no R²", font=("Arial", 16, "bold"), background=self.cor_principal, foreground="white").pack(side="left")

        self.bottomFrame = tk.Frame(self.menu_reta_r2_frame)
        self.bottomFrame.pack(fill="both", expand=True)

        tk.Label(self.bottomFrame, text="Ponto inicial (P1)", font=("Arial", 14, "bold")).pack(anchor="w", padx=(30, 0), pady=(30, 0))

        self.ponto_inicial_label_frame = tk.Frame(self.bottomFrame)
        self.ponto_inicial_label_frame.pack(fill="x", pady=(30, 0))
        
        tk.Label(self.ponto_inicial_label_frame, text="X", font=("Arial", 14, "bold")).pack(side="left", padx=(30, 0))
        tk.Label(self.ponto_inicial_label_frame, text="Y", font=("Arial", 14, "bold")).pack(side="left", padx=(650, 0))
        
        self.ponto_inicial_entry_frame = tk.Frame(self.bottomFrame)
        self.ponto_inicial_entry_frame.pack(fill="x", pady=(30, 0))
        self.ponto_inicial_x = tk.Entry(self.ponto_inicial_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_inicial_x.pack(side="left", ipady=15, ipadx=210, padx=(30, 0))
        self.ponto_inicial_y = tk.Entry(self.ponto_inicial_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_inicial_y.pack(side="left", ipady=15, ipadx=195, padx=(10, 0))
        self.ponto_inicial = (self.ponto_inicial_x, self.ponto_inicial_y)

        tk.Label(self.bottomFrame, text="Ponto final (P2)", font=("Arial", 14, "bold")).pack(anchor="w", padx=(30,0), pady=(30, 0))

        self.ponto_final_entry_frame = tk.Frame(self.bottomFrame)
        self.ponto_final_entry_frame.pack(fill="x", pady=(30, 0))
        self.ponto_final_x = tk.Entry(self.ponto_final_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_final_x.pack(side="left", ipady=15, ipadx=210, padx=(30, 0))
        self.ponto_final_y = tk.Entry(self.ponto_final_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_final_y.pack(side="left", ipady=15, ipadx=195, padx=(10, 0))
        self.ponto_final = (self.ponto_final_x, self.ponto_final_y)

        tk.Button(self.bottomFrame, text="Calcular", command=self.tela_reta_r2, font=("Arial", 18, "bold"), relief="flat", background=self.cor_secundaria, foreground="white", cursor="hand2", padx=600).pack(pady=(100, 0))

    def menu_reta_r3(self, frame_anterior):
        frame_anterior.pack_forget()

        self.menu_reta_r3_frame = tk.Frame(self.root)
        self.menu_reta_r3_frame.pack(fill="both", expand=True)
        
        self.topFrame = tk.Frame(self.menu_reta_r3_frame, background=self.cor_principal, pady=15)
        self.topFrame.pack(fill="x")
        
        tk.Button(self.topFrame, text="⬅", command=lambda: self.menu_principal(self.menu_reta_r3_frame), font=("Arial", 20, "bold"), relief="flat", background=self.cor_principal, foreground="white", cursor="hand2").pack(side="left", padx=(10, 0))
        tk.Label(self.topFrame, text="Construir reta no R³", font=("Arial", 16, "bold"), background=self.cor_principal, foreground="white").pack(side="left")

        self.bottomFrame = tk.Frame(self.menu_reta_r3_frame)
        self.bottomFrame.pack(fill="both", expand=True)

        tk.Label(self.bottomFrame, text="Ponto inicial (P1)", font=("Arial", 14, "bold")).pack(anchor="w", padx=(30, 0), pady=(30, 0))

        self.ponto_inicial_label_frame = tk.Frame(self.bottomFrame)
        self.ponto_inicial_label_frame.pack(fill="x", pady=(30, 0))
        
        tk.Label(self.ponto_inicial_label_frame, text="X", font=("Arial", 14, "bold")).pack(side="left", padx=(30, 0))
        tk.Label(self.ponto_inicial_label_frame, text="Y", font=("Arial", 14, "bold")).pack(side="left", padx=(420, 0))
        tk.Label(self.ponto_inicial_label_frame, text="Z", font=("Arial", 14, "bold")).pack(side="left", padx=(420, 0))
        
        self.ponto_inicial_entry_frame = tk.Frame(self.bottomFrame)
        self.ponto_inicial_entry_frame.pack(fill="x", pady=(30, 0))
        self.ponto_inicial_x = tk.Entry(self.ponto_inicial_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_inicial_x.pack(side="left", ipady=15, ipadx=95, padx=(30, 0))
        self.ponto_inicial_y = tk.Entry(self.ponto_inicial_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_inicial_y.pack(side="left", ipady=15, ipadx=90, padx=(10, 0))
        self.ponto_inicial_z = tk.Entry(self.ponto_inicial_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_inicial_z.pack(side="left", ipady=15, ipadx=85, padx=(10, 0))
        self.ponto_inicial = (self.ponto_inicial_x, self.ponto_inicial_y, self.ponto_inicial_z)

        self.ponto_final_entry_frame = tk.Frame(self.bottomFrame)
        self.ponto_final_entry_frame.pack(fill="x", pady=(30, 0))
        self.ponto_final_x = tk.Entry(self.ponto_final_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_final_x.pack(side="left", ipady=15, ipadx=95, padx=(30, 0))
        self.ponto_final_y = tk.Entry(self.ponto_final_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_final_y.pack(side="left", ipady=15, ipadx=90, padx=(10, 0))
        self.ponto_final_z = tk.Entry(self.ponto_final_entry_frame, relief="flat", font=("Aria", 16), border=0, highlightthickness=2, highlightbackground=self.cor_principal, highlightcolor=self.cor_secundaria)
        self.ponto_final_z.pack(side="left", ipady=15, ipadx=85, padx=(10, 0))
        self.ponto_final = (self.ponto_final_x, self.ponto_final_y, self.ponto_final_z)

        tk.Button(self.bottomFrame, text="Calcular", command=self.tela_reta_r3, font=("Arial", 18, "bold"), relief="flat", background=self.cor_secundaria, foreground="white", cursor="hand2", padx=600).pack(pady=(100, 0))

    def tela_reta_r2(self):
        self.menu_reta_r2_frame.pack_forget()

        self.tela_reta_r2_frame = tk.Frame(self.root)
        self.tela_reta_r2_frame.pack(fill="both", expand=True)

        self.topFrame = tk.Frame(self.tela_reta_r2_frame, background=self.cor_principal, pady=15)
        self.topFrame.pack(fill="x")

        tk.Button(self.topFrame, text="⬅", command=lambda: self.menu_reta_r2(self.tela_reta_r2_frame), font=("Arial", 20, "bold"), relief="flat", background=self.cor_principal, foreground="white", cursor="hand2").pack(side="left", padx=(10, 0))
        tk.Label(self.topFrame, text="Gráfico de reta no R²", font=("Arial", 16, "bold"), background=self.cor_principal, foreground="white").pack(side="left")

        self.bottomFrame = tk.Frame(self.tela_reta_r2_frame)
        self.bottomFrame.pack(fill="both", expand=True)

        self.grafico_frame = tk.Frame(self.bottomFrame)
        self.grafico = Grafico(tk, self.grafico_frame)
        self.grafico.grafico_r2(self.ponto_inicial, self.ponto_final)

    def tela_reta_r3(self):
        self.menu_reta_r3_frame.pack_forget()

        self.tela_reta_r3_frame = tk.Frame(self.root)
        self.tela_reta_r3_frame.pack(fill="both", expand=True)

        self.topFrame = tk.Frame(self.tela_reta_r3_frame, background=self.cor_principal, pady=15)
        self.topFrame.pack(fill="x")

        tk.Button(self.topFrame, text="⬅", command=lambda: self.menu_reta_r3(self.tela_reta_r3_frame), font=("Arial", 20, "bold"), relief="flat", background=self.cor_principal, foreground="white", cursor="hand2").pack(side="left", padx=(10, 0))
        tk.Label(self.topFrame, text="Gráfico de reta no R³", font=("Arial", 16, "bold"), background=self.cor_principal, foreground="white").pack(side="left")

        self.bottomFrame = tk.Frame(self.tela_reta_r3_frame)
        self.bottomFrame.pack(fill="both", expand=True)

        self.grafico_frame = tk.Frame(self.bottomFrame)
        self.grafico = Grafico(tk, self.grafico_frame)
        self.grafico.grafico_r3(self.ponto_inicial, self.ponto_final)

if __name__ == "__main__":
    interface = Interface();
    interface.menu_principal()
    interface.root.mainloop()