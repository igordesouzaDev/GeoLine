
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import MultipleLocator, ScalarFormatter
import numpy as np

class Grafico:
    def __init__(self, tk, tk_frame):
        self.tk = tk
        self.tk_frame = tk_frame
        self.coordenadas = []
        self.x = []
        self.y = []
        self.z = []
        self.fig = Figure()

    def grafico_r2(self, ponto_inicial, ponto_final):
        self.ax = self.fig.add_subplot(111)

        self.coordenadas.clear()
        self.x.clear()
        self.y.clear()

        self.ponto_inicial_coordenadas = (float(ponto_inicial[0].get()), float(ponto_inicial[1].get()))
        self.ponto_final_coordenadas = (float(ponto_final[0].get()), float(ponto_final[1].get()))

        for a, b in zip(self.ponto_inicial_coordenadas, self.ponto_final_coordenadas):
            self.coordenadas.append([a, b])

        self.x = self.coordenadas[0]
        self.y = self.coordenadas[1]

        self.limite_x = max(self.x)*1.2
        self.limite_y = max(self.y)*1.2

        self.ax.spines["left"].set_position("zero")
        self.ax.spines["bottom"].set_position("zero")
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)

        self.ax.set_xlabel("X", loc="right", labelpad=5)
        self.ax.set_ylabel("Y", loc="top", rotation=0, labelpad=5)
        self.ax.grid(which="major", linestyle="-", linewidth=0.8, alpha=0.8)
        self.ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.7)
        self.ax.set_axisbelow(True)
        self.ax.set_xlim((-self.limite_x, self.limite_x))
        self.ax.set_ylim((-self.limite_y, self.limite_y))

        self.ax.xaxis.set_major_locator(MultipleLocator(5))
        self.ax.yaxis.set_major_locator(MultipleLocator(5))
        self.ax.xaxis.set_minor_locator(MultipleLocator(1))
        self.ax.yaxis.set_minor_locator(MultipleLocator(1))
        self.ax.minorticks_on()
        self.ax.tick_params(axis="x", which="minor", labelsize=8, labelcolor="gray")
        self.ax.tick_params(axis="y", which="minor", labelsize=8, labelcolor="gray")

        self.ax.plot(self.ponto_inicial_coordenadas[0], self.ponto_inicial_coordenadas[1], marker="o", color="green", markersize=5, label=f"Ponto inicial: ({self.ponto_inicial_coordenadas[0]}, {self.ponto_inicial_coordenadas[1]})")
        self.ax.plot(self.ponto_final_coordenadas[0], self.ponto_final_coordenadas[1], marker="o", color="red", markersize=5, label=f"Ponto final: ({self.ponto_final_coordenadas[0]}, {self.ponto_final_coordenadas[1]})")
        self.ax.plot(self.x, self.y, label=f"Reta R2: (Ponto inicial ➔ Ponto final)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tk_frame)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tk_frame, pack_toolbar=False)
        self.toolbar.update()

        self.ax.legend()
        self.toolbar.pack(side=self.tk.BOTTOM, fill=self.tk.X)
        self.canvas.get_tk_widget().pack(side=self.tk.TOP, fill=self.tk.BOTH, expand=True)
        self.tk_frame.pack(fill="both", expand=True)

    def grafico_r3(self, ponto_inicial, ponto_final):
        self.ax = self.fig.add_subplot(111, projection="3d")

        self.coordenadas.clear()
        self.x.clear()
        self.y.clear()
        self.z.clear()

        self.ponto_inicial_coordenadas = (float(ponto_inicial[0].get()), float(ponto_inicial[1].get()), float(ponto_inicial[2].get()))
        self.ponto_final_coordenadas = (float(ponto_final[0].get()), float(ponto_final[1].get()), float(ponto_final[2].get()))

        for a, b in zip(self.ponto_inicial_coordenadas, self.ponto_final_coordenadas):
            self.coordenadas.append([a, b])

        self.x = self.coordenadas[0]
        self.y = self.coordenadas[1]
        self.z = self.coordenadas[2]

        self.x, self.y = np.meshgrid(self.x, self.y)
        self.z = np.array([
            [self.z[0], self.z[1]],
            [self.z[0], self.z[1]],
        ])

        self.ax.set_xlabel("X", loc="right", labelpad=5)
        self.ax.set_ylabel("Y", loc="top", rotation=0, labelpad=5)

        self.ax.plot_surface(self.x, self.y, self.z, cmap="viridis", edgecolor="none")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tk_frame)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tk_frame, pack_toolbar=False)
        self.toolbar.update()

        self.toolbar.pack(side=self.tk.BOTTOM, fill=self.tk.X)
        self.canvas.get_tk_widget().pack(side=self.tk.TOP, fill=self.tk.BOTH, expand=True)
        self.tk_frame.pack(fill="both", expand=True)