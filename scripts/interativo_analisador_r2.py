"""Entrada manual e análise de duas retas no R²."""

from backend.analisador import Analisador
from backend.reta import Reta
from backend.vetor import Vetor


def ler_vetor(rotulo):
    valores = input(f"{rotulo} (duas coordenadas separadas por vírgula): ")
    try:
        return Vetor(float(valor.strip()) for valor in valores.split(","))
    except ValueError as erro:
        raise ValueError("Informe coordenadas numéricas válidas.") from erro


def main():
    print("=== Analisador de retas no R² ===")
    reta1 = Reta(ler_vetor("Ponto inicial da reta 1"), ler_vetor("Direção da reta 1"))
    reta2 = Reta(ler_vetor("Ponto inicial da reta 2"), ler_vetor("Direção da reta 2"))
    print(Analisador.analisar(reta1, reta2)["mensagem"])


if __name__ == "__main__":
    main()
