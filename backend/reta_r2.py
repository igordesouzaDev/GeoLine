"""Especialização de Reta para retas no plano."""

from backend.reta import Reta
from backend.vetor import Vetor


def _formatar_numero(valor):
    return f"{valor:g}"


class RetaR2(Reta):
    """Reta do R² definida por dois pontos distintos."""

    __slots__ = ()

    def __init__(self, ponto_inicial, ponto_final):
        if not isinstance(ponto_inicial, Vetor) or not isinstance(ponto_final, Vetor):
            raise TypeError("Os pontos devem ser objetos Vetor.")
        if ponto_inicial.dimensao != 2 or ponto_final.dimensao != 2:
            raise ValueError("RetaR2 exige dois pontos do R².")

        vetor_diretor = ponto_final.subtrair(ponto_inicial)
        super().__init__(ponto_inicial, vetor_diretor)

    def equacao_simetrica(self):
        """Retorna a forma simétrica, incluindo casos horizontais e verticais."""
        x0, y0 = self.ponto_inicial.coordenadas
        dx, dy = self.vetor_diretor.coordenadas

        if dx == 0:
            return f"x = {_formatar_numero(x0)}"
        if dy == 0:
            return f"y = {_formatar_numero(y0)}"
        return (
            f"(x - {_formatar_numero(x0)}) / {_formatar_numero(dx)} = "
            f"(y - {_formatar_numero(y0)}) / {_formatar_numero(dy)}"
        )

    def equacao_reduzida(self):
        """Retorna y = mx + b; uma reta vertical não possui essa forma."""
        x0, y0 = self.ponto_inicial.coordenadas
        dx, dy = self.vetor_diretor.coordenadas
        if dx == 0:
            raise ValueError("Uma reta vertical não possui equação reduzida y = mx + b.")

        inclinacao = dy / dx
        intercepto = y0 - inclinacao * x0
        if inclinacao == 0:
            return f"y = {_formatar_numero(intercepto)}"

        sinal = "+" if intercepto >= 0 else "-"
        return (
            f"y = {_formatar_numero(inclinacao)}x {sinal} "
            f"{_formatar_numero(abs(intercepto))}"
        )

    def __repr__(self):
        return f"RetaR2({self.ponto_inicial!r}, {self.obter_ponto(1)!r})"
