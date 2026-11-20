"""Exemplos de uso da API integrada do Analisador."""

from backend.analisador import Analisador
from backend.reta import Reta
from backend.vetor import Vetor


def main():
    reta1 = Reta(Vetor([0, 0]), Vetor([1, 1]))
    reta2 = Reta(Vetor([0, 2]), Vetor([1, -1]))
    print("R²:", Analisador.analisar(reta1, reta2))

    reta3 = Reta(Vetor([0, 0, 0]), Vetor([1, 0, 0]))
    reta4 = Reta(Vetor([0, 1, 1]), Vetor([0, 1, 0]))
    print("R³:", Analisador.analisar(reta3, reta4))


if __name__ == "__main__":
    main()
