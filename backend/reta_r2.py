from backend.reta import Reta
from backend.vetor import Vetor


def _formatar_numero(valor):
    return f"{valor:g}"


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
    
    def equacao_reduzida(self):
        """Retorna a forma reduzida; para retas verticais, retorna x = constante."""
        x_inicial, y_inicial = self.ponto_inicial.coordenadas
        a, b = self.vetor_diretor.coordenadas

        if a == 0:
            return f"x = {_formatar_numero(x_inicial)}"

        elif b == 0:
            return f"y = {_formatar_numero(y_inicial)}"
        
        m = b / a

        coeficiente_linear = y_inicial - m * x_inicial
        if coeficiente_linear == 0:
            return f"y = {_formatar_numero(m)}x"
        sinal = "+" if coeficiente_linear > 0 else "-"
        return (
            f"y = {_formatar_numero(m)}x {sinal} "
            f"{_formatar_numero(abs(coeficiente_linear))}"
        )

    def equacao_simetrica(self, form=1):
        """Retorna a equação simétrica sem depender de bibliotecas externas.

        ``form`` é mantido por compatibilidade com os exemplos existentes:
        0 produz uma forma mais explícita e 1 uma forma compacta.
        """
        if form not in (0, 1):
            raise ValueError("form deve ser 0 ou 1.")
        
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

        return f"(x - {x_inicial}) / {a} = (y - {y_inicial}) / {b}"
