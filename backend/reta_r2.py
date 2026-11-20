from backend.reta import Reta
from backend.formatacao import formatar_numero, formatar_numerador
from backend.vetor import Vetor


class RetaR2(Reta):

    __slots__ = ()

    def __init__(self, ponto_inicial, ponto_final):
        if not isinstance(ponto_inicial, Vetor):
            raise TypeError("O ponto inicial deve ser um objeto Vetor.")
        if not isinstance(ponto_final, Vetor):
            raise TypeError("O ponto final deve ser um objeto Vetor.")
        if ponto_inicial.dimensao != ponto_final.dimensao:
            raise ValueError("Os pontos devem possuir a mesma dimensão.")
        if ponto_inicial.dimensao != 2:
            raise ValueError("Os pontos da RetaR2 devem possuir dimensão 2.")

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
            return f"x = {formatar_numero(x_inicial)}"

        elif b == 0:
            return f"y = {formatar_numero(y_inicial)}"
        
        m = b / a

        coeficiente_linear = y_inicial - m * x_inicial
        if coeficiente_linear == 0:
            return f"y = {formatar_numero(m)}x"
        sinal = "+" if coeficiente_linear > 0 else "-"
        return (
            f"y = {formatar_numero(m)}x {sinal} "
            f"{formatar_numero(abs(coeficiente_linear))}"
        )

    def equacao_simetrica(self, form=1):
        """Retorna a equação simétrica sem depender de bibliotecas externas.

        ``form`` é mantido por compatibilidade com os exemplos existentes:
        0 produz uma forma mais explícita e 1 uma forma compacta.
        """
        if form not in (0, 1):
            raise ValueError("O formato deve ser 0 ou 1.")

        x_inicial, y_inicial = self.ponto_inicial.coordenadas
        a, b = self.vetor_diretor.coordenadas

        if a == 0:
            return f"x = {formatar_numero(x_inicial)}"

        elif b == 0:
            return f"y = {formatar_numero(y_inicial)}"

        if form == 0:
            return (
                f"{formatar_numerador('x', x_inicial)} / ({formatar_numero(a)}) = "
                f"{formatar_numerador('y', y_inicial)} / ({formatar_numero(b)})"
            )

        return (
            f"{formatar_numerador('x', x_inicial)} / {formatar_numero(a)} = "
            f"{formatar_numerador('y', y_inicial)} / {formatar_numero(b)}"
        )
