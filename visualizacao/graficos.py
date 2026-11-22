"""Geração de figuras 2D e 3D a partir dos objetos de reta do backend."""

from matplotlib.figure import Figure


class Graficos:
    """Cria figuras Matplotlib sem depender da interface Tkinter."""

    @staticmethod
    def _validar_retas(reta1, reta2=None, dimensao=2):
        from backend.reta import Reta

        if not isinstance(reta1, Reta):
            raise TypeError("A reta deve ser um objeto Reta.")
        if reta1.dimensao != dimensao:
            raise ValueError(f"A reta deve pertencer ao R{dimensao}.")
        if reta2 is not None:
            if not isinstance(reta2, Reta):
                raise TypeError("A segunda reta deve ser um objeto Reta.")
            if reta2.dimensao != dimensao:
                raise ValueError("As retas devem possuir a dimensão do gráfico.")

    @staticmethod
    def _intervalo(reta):
        ponto = reta.ponto_inicial.coordenadas
        direcao = reta.vetor_diretor.coordenadas
        escala = max(5.0, max((abs(valor) for valor in ponto), default=0.0) * 0.5)
        norma = reta.vetor_diretor.modulo()
        return escala / norma

    @classmethod
    def _desenhar_r2(cls, retas):
        fig = Figure(figsize=(7, 5), dpi=100, facecolor="white")
        ax = fig.add_subplot(111)
        cores = ("#2878D0", "#E67E22")
        for indice, reta in enumerate(retas):
            x0, y0 = reta.ponto_inicial.coordenadas
            dx, dy = reta.vetor_diretor.coordenadas
            escala = cls._intervalo(reta)
            xs = (x0 - escala * dx, x0 + escala * dx)
            ys = (y0 - escala * dy, y0 + escala * dy)
            nome = f"Reta {indice + 1}" if len(retas) == 2 else "Reta"
            cor = cores[indice]
            ax.plot(xs, ys, color=cor, linewidth=2, label=nome)
            ax.scatter([x0], [y0], color=cor, edgecolors="white", zorder=3,
                       label=f"Ponto inicial {indice + 1}" if len(retas) == 2 else "Ponto inicial")
            final = reta.obter_ponto(1).coordenadas
            ax.scatter([final[0]], [final[1]], color=cor, marker="D", edgecolors="white", zorder=3,
                       label=f"Ponto final {indice + 1}" if len(retas) == 2 else "Ponto final")
        ax.axhline(0, color="#687386", linewidth=0.8)
        ax.axvline(0, color="#687386", linewidth=0.8)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Retas no R²")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.set_aspect("equal", adjustable="datalim")
        ax.legend()
        fig.tight_layout()
        return fig, ax

    @classmethod
    def _desenhar_r3(cls, retas):
        fig = Figure(figsize=(7, 5), dpi=100, facecolor="white")
        ax = fig.add_subplot(111, projection="3d")
        cores = ("#2878D0", "#E67E22")
        for indice, reta in enumerate(retas):
            ponto = reta.ponto_inicial.coordenadas
            direcao = reta.vetor_diretor.coordenadas
            escala = cls._intervalo(reta)
            coordenadas = [
                (p - escala * d, p + escala * d)
                for p, d in zip(ponto, direcao)
            ]
            nome = f"Reta {indice + 1}" if len(retas) == 2 else "Reta"
            cor = cores[indice]
            ax.plot(*coordenadas, color=cor, linewidth=2, label=nome)
            ax.scatter(*ponto, color=cor, edgecolors="white", s=35,
                       label=f"Ponto inicial {indice + 1}" if len(retas) == 2 else "Ponto inicial")
            ponto_final = reta.obter_ponto(1).coordenadas
            ax.scatter(*ponto_final, color=cor, marker="D", edgecolors="white", s=35,
                       label=f"Ponto final {indice + 1}" if len(retas) == 2 else "Ponto final")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Retas no R³")
        ax.legend()
        fig.tight_layout()
        return fig, ax

    @classmethod
    def plotar_reta_r2(cls, reta):
        cls._validar_retas(reta, dimensao=2)
        return cls._desenhar_r2([reta])

    @classmethod
    def plotar_reta_r3(cls, reta):
        cls._validar_retas(reta, dimensao=3)
        return cls._desenhar_r3([reta])

    @classmethod
    def plotar_duas_retas_r2(cls, reta1, reta2):
        cls._validar_retas(reta1, reta2, dimensao=2)
        return cls._desenhar_r2([reta1, reta2])

    @classmethod
    def plotar_duas_retas_r3(cls, reta1, reta2):
        cls._validar_retas(reta1, reta2, dimensao=3)
        return cls._desenhar_r3([reta1, reta2])
