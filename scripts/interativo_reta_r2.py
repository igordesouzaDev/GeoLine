"""Menu para analisar duas retas do R² manualmente."""

from backend.analisador import Analisador
from backend.reta_r2 import RetaR2
from backend.vetor import Vetor


def ler_ponto(numero):
    x = float(input(f"Ponto {numero} — x: "))
    y = float(input(f"Ponto {numero} — y: "))
    return Vetor([x, y])


def main():
    print("=== Análise interativa de retas no R² ===")
    ponto_a1 = ler_ponto("inicial da reta 1")
    ponto_b1 = ler_ponto("final da reta 1")
    ponto_a2 = ler_ponto("inicial da reta 2")
    ponto_b2 = ler_ponto("final da reta 2")

    reta1 = RetaR2(ponto_a1, ponto_b1)
    reta2 = RetaR2(ponto_a2, ponto_b2)
    print(Analisador.analisar(reta1, reta2)["mensagem"])


if __name__ == "__main__":
    main()
