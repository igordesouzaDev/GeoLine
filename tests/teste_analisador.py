from backend.analisador import AnalisadorRetas


def main():
    print("================================")
    print("       TESTES DO GEOLINE")
    print("================================")

    # Teste 1: Retas intersectantes
    resultado1 = AnalisadorRetas.analisar(
        (0, 0), (1, 1),
        (0, 2), (1, -1)
    )

    print("\nTeste 1 - Retas intersectantes:")
    print(resultado1)

    # Teste 2: Retas paralelas
    resultado2 = AnalisadorRetas.analisar(
        (0, 0), (1, 1),
        (0, 2), (1, 1)
    )

    print("\nTeste 2 - Retas paralelas:")
    print(resultado2)

    # Teste 3: Retas coincidentes
    resultado3 = AnalisadorRetas.analisar(
        (0, 0), (1, 1),
        (2, 2), (2, 2)
    )

    print("\nTeste 3 - Retas coincidentes:")
    print(resultado3)

    # Teste 4: Pertencimento de ponto à reta
    pertence = AnalisadorRetas.ponto_pertence_reta(
        (2, 2),
        (0, 0),
        (1, 1)
    )

    print("\nTeste 4 - Pertencimento de ponto:")
    print(pertence)
    # Teste 5 - Vetores proporcionais no R²
    resultado = AnalisadorRetas.vetores_proporcionais(
        (2, 4),
        (1, 2)
    )

    print("\nTeste 5 - Vetores proporcionais no R²:")
    print(resultado)

    # Teste 6 - Vetores proporcionais no R³
    resultado = AnalisadorRetas.vetores_proporcionais(
        (2, 4, 6),
        (1, 2, 3)
    )

    print("\nTeste 6 - Vetores proporcionais no R³:")
    print(resultado)

    # Teste 7 - Vetores não proporcionais
    resultado = AnalisadorRetas.vetores_proporcionais(
        (1, 2, 3),
        (1, 2, 4)
    )

    print("\nTeste 7 - Vetores não proporcionais:")
    print(resultado)

    # Teste 8 - Retas coincidentes no R³
    resultado = AnalisadorRetas.analisar_paralelismo_r3(
        (0, 0, 0),
        (1, 2, 3),
        (2, 4, 6),
        (2, 4, 6)
    )

    print("\nTeste 8 - Retas coincidentes no R³:")
    print(resultado)

    # Teste 9 - Retas paralelas distintas no R³
    resultado = AnalisadorRetas.analisar_paralelismo_r3(
        (0, 0, 0),
        (1, 2, 3),
        (1, 0, 0),
        (2, 4, 6)
    )

    print("\nTeste 9 - Retas paralelas distintas no R³:")
    print(resultado)

    # Teste 10 - Retas não paralelas no R³
    resultado = AnalisadorRetas.analisar_paralelismo_r3(
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    )

    print("\nTeste 10 - Retas não paralelas no R³:")
    print(resultado)

    # Teste 11 - Retas intersectantes no R³
    resultado = AnalisadorRetas.calcular_intersecao_r3(
        (0, 0, 0),
        (1, 1, 0),
        (1, 0, 0),
        (0, 1, 0)
    )

    print("\nTeste 11 - Retas intersectantes no R³:")
    print(resultado)

    # Teste 12 - Retas reversas no R³
    resultado = AnalisadorRetas.calcular_intersecao_r3(
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 1),
        (0, 1, 0)
    )

    print("\nTeste 12 - Retas reversas no R³:")
    print(resultado)

    # Teste 13 - Retas paralelas no R³
    resultado = AnalisadorRetas.calcular_intersecao_r3(
        (0, 0, 0),
        (1, 2, 3),
        (1, 0, 0),
        (2, 4, 6)
    )

    print("\nTeste 13 - Retas paralelas no R³:")
    print(resultado)

    # Teste 14 - Vetores proporcionais com primeira coordenada zero
    resultado = AnalisadorRetas.vetores_proporcionais(
        (0, 2, 4),
        (0, 1, 2)
    )

    print("\nTeste 14 - Vetores proporcionais com zero:")
    print(resultado)

    # Teste 15 - Vetores não proporcionais com primeira coordenada zero
    resultado = AnalisadorRetas.vetores_proporcionais(
        (0, 2, 4),
        (0, 1, 3)
    )

    print("\nTeste 15 - Vetores não proporcionais com zero:")
    print(resultado)

        # Teste 16 - Retas coincidentes no R³
    resultado = AnalisadorRetas.calcular_intersecao_r3(
        (0, 0, 0),
        (1, 2, 3),
        (2, 4, 6),
        (2, 4, 6)
    )

    print("\nTeste 16 - Interseção de retas coincidentes no R³:")

     # Teste 17 - Ponto que não pertence à reta no R²
    resultado = AnalisadorRetas.ponto_pertence_reta(
        (3, 4),
        (1, 1),
        (1, 2)
    )

    print("\nTeste 17 - Ponto fora da reta:")
    print(resultado)
    print(resultado)

        # Teste 18 - Vetor diretor nulo no R³
    try:
        resultado = AnalisadorRetas.analisar_paralelismo_r3(
            (0, 0, 0),
            (0, 0, 0),
            (1, 1, 1),
            (1, 0, 0)
        )

        print("\nTeste 18 - Vetor diretor nulo:")
        print(resultado)

    except ValueError as erro:
        print("\nTeste 18 - Vetor diretor nulo:")
        print(f"Erro identificado corretamente: {erro}")

         # Teste 19 - Vetor diretor quase nulo no R²
    try:
        resultado = AnalisadorRetas.ponto_pertence_reta(
            (1, 1),
            (0, 0),
            (1e-10, 0)
        )

        print("\nTeste 19 - Vetor quase nulo:")
        print(resultado)

    except ValueError as erro:
        print("\nTeste 19 - Vetor quase nulo:")
        print(f"Erro identificado corretamente: {erro}")
        
if __name__ == "__main__":
    main()