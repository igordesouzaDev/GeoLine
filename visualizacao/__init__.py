
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Grafico:
    def __init__(self, tk, tk_frame):
        self.tk = tk
        self.tk_frame = tk_frame
        self.x = []
        self.y = []
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

    def grafico_r2(self, p1, p2, frame_anterior):
        frame_anterior.pack_forget()

        self.x.clear()
        self.y.clear()

        for a, b in zip(p1, p2):
            self.x.append(a)
            self.y.append(b)

        self.limite_x = self.x[1]*1.2
        self.limite_y = self.y[1]*1.2

        self.ax.spines["left"].set_position("zero")
        self.ax.spines["bottom"].set_position("zero")
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        
        self.ax.grid(True, linestyle="--")
        self.ax.set_axisbelow(True)
        self.ax.set_xlim((-self.limite_x, self.limite_x))
        self.ax.set_ylim((-self.limite_y, self.limite_y))

        self.ax.plot(self.x, self.y, marker="o", label=f"Reta R2: ({self.x[0]}, {self.y[0]}) - ({self.x[1]}, {self.y[1]})")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tk_frame)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tk_frame, pack_toolbar=False)
        self.toolbar.update()

        self.ax.legend()
        self.toolbar.pack(side=self.tk.BOTTOM, fill=self.tk.X)
        self.canvas.get_tk_widget().pack(side=self.tk.TOP, fill=self.tk.BOTH, expand=True)
        self.tk_frame.pack(fill="both", expand=True)