from .reta import Reta
from .vetor import Vetor
from sympy import Eq, pretty, symbols

class RetaR2(Reta):

    __slots__ = ()

    
    def __init__(self, ponto_inicial, ponto_final):
        if not isinstance(ponto_inicial, Vetor):
            ponto_inicial = Vetor(ponto_inicial)

        if not isinstance(ponto_final, Vetor):
            ponto_final = Vetor(ponto_final)

        if ponto_inicial.dimensao != 2 or ponto_final.dimensao != 2:
            raise ValueError("A dimensão deve ser 2 para Reta em R².")

        vetor_diretor = ponto_final.subtrair(ponto_inicial)

        super().__init__(ponto_inicial, vetor_diretor)

    @property
    def ponto_final(self):
        return self.ponto_inicial.somar(self.vetor_diretor)
    
    @property
    def equacao_reduzida(self):
        x_inicial, y_inicial = self.ponto_inicial.coordenadas
        a, b = self.vetor_diretor.coordenadas

        if a == 0:
            return f"x = {x_inicial}"

        elif b == 0:
            return f"y = {y_inicial}"
        
        m = b / a

        coeficiente_linear = y_inicial - m * x_inicial

        return f"y = {m}x{coeficiente_linear:+}" # o modificador ":+" insere o sinal do número (+ ou -)

    def equacao_simetrica(self, form = 1):

        if form not in (0,1):
            raise ValueError("Form deve ser 0 ou 1.")
        
        x_inicial, y_inicial = self.ponto_inicial.coordenadas
        a, b = self.vetor_diretor.coordenadas

        if a == 0:
            return f"x = {x_inicial}"

        elif b == 0:
            return f"y = {y_inicial}"

        if form == 0:
            return (
                f"(x - ({x_inicial})) / ({a}) = "
                f"(y - ({y_inicial})) / ({b})"
            )
        
        else:
            x, y = symbols("x y")

            equacao = Eq(
                (x - x_inicial) / a,
                (y - y_inicial) / b
            )
            return(
                pretty(equacao)
            )