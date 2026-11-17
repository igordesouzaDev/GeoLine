"""Exemplos não interativos de classificação pelo Analisador atual."""

from backend.analisador import Analisador
from backend.reta_r2 import RetaR2
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor


def main():
    reta_base = RetaR2(Vetor([0, 0]), Vetor([1, 1]))
    reta_secante = RetaR2(Vetor([0, 2]), Vetor([1, 1]))
    reta_paralela = RetaR2(Vetor([0, 2]), Vetor([1, 2]))

    print("R² - concorrentes:", Analisador.analisar(reta_base, reta_secante))
    print("R² - paralelas:", Analisador.analisar(reta_base, reta_paralela))

    eixo_x = RetaR3(Vetor([0, 0, 0]), Vetor([1, 0, 0]))
    reta_reversa = RetaR3(Vetor([0, 1, 1]), Vetor([0, 2, 1]))
    print("R³ - reversas:", Analisador.analisar(eixo_x, reta_reversa))


if __name__ == "__main__":
    main()
