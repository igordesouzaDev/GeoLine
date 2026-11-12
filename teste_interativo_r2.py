from backend.analisador import AnalisadorRetas

print("=== TESTE INTERATIVO DE RETAS NO R² ===")

x1 = float(input("Digite o x do ponto da reta 1: "))
y1 = float(input("Digite o y do ponto da reta 1: "))

dx1 = float(input("Digite o x do vetor diretor da reta 1: "))
dy1 = float(input("Digite o y do vetor diretor da reta 1: "))

x2 = float(input("Digite o x do ponto da reta 2: "))
y2 = float(input("Digite o y do ponto da reta 2: "))

dx2 = float(input("Digite o x do vetor diretor da reta 2: "))
dy2 = float(input("Digite o y do vetor diretor da reta 2: "))
resultado = AnalisadorRetas.analisar(
    (x1, y1),
    (dx1, dy1),
    (x2, y2),
    (dx2, dy2)
)

print("\n=== RESULTADO ===")
print(resultado)