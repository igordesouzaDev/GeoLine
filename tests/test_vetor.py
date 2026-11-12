"""Menu interativo para experimentar manualmente a classe Vetor.

Execute a partir da pasta principal do projeto com:
    python -m tests.test_vetor
"""

import sys
from pathlib import Path

# Permite executar este arquivo diretamente de dentro da pasta tests.
PASTA_PROJETO = Path(__file__).resolve().parents[1]
if str(PASTA_PROJETO) not in sys.path:
    sys.path.insert(0, str(PASTA_PROJETO))

from backend.vetor import Vetor


def ler_vetor(mensagem):
    """Lê coordenadas separadas por vírgulas e cria um Vetor."""
    texto = input(mensagem)
    try:
        coordenadas = [float(valor.strip()) for valor in texto.split(",")]
    except ValueError as erro:
        raise ValueError("Digite somente números separados por vírgulas.") from erro
    return Vetor(coordenadas)


def mostrar_menu():
    print("\n=== Testador interativo da classe Vetor ===")
    print("1. Criar e mostrar vetor")
    print("2. Somar dois vetores")
    print("3. Subtrair dois vetores")
    print("4. Multiplicar vetor por escalar")
    print("5. Calcular módulo")
    print("6. Calcular produto escalar")
    print("7. Calcular produto vetorial (R³)")
    print("8. Verificar se dois vetores são proporcionais")
    print("0. Sair")


def executar_opcao(opcao):
    if opcao == "1":
        vetor = ler_vetor("Coordenadas (ex.: 2, 3 ou 1, 2, 3): ")
        print(f"Vetor: {vetor}")
        print(f"Dimensão: {vetor.dimensao}")

    elif opcao in {"2", "3", "6", "7", "8"}:
        primeiro = ler_vetor("Coordenadas do primeiro vetor: ")
        segundo = ler_vetor("Coordenadas do segundo vetor: ")

        if opcao == "2":
            print("Soma:", primeiro.somar(segundo))
        elif opcao == "3":
            print("Subtração:", primeiro.subtrair(segundo))
        elif opcao == "6":
            print("Produto escalar:", primeiro.produto_escalar(segundo))
        elif opcao == "7":
            print("Produto vetorial:", primeiro.produto_vetorial(segundo))
        else:
            print("São proporcionais?", primeiro.sao_proporcionais(segundo))

    elif opcao == "4":
        vetor = ler_vetor("Coordenadas do vetor: ")
        escalar = float(input("Valor do escalar: "))
        print("Resultado:", vetor.multiplicar_escalar(escalar))

    elif opcao == "5":
        vetor = ler_vetor("Coordenadas do vetor: ")
        print("Módulo:", vetor.modulo())

    else:
        print("Opção inválida. Escolha uma opção do menu.")


def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando o testador.")
            break

        try:
            executar_opcao(opcao)
        except (TypeError, ValueError) as erro:
            print(f"Não foi possível realizar a operação: {erro}")


if __name__ == "__main__":
    main()
