from backend.reta_r2 import RetaR2
from backend.vetor import Vetor

#Criação de objetos
print("Criação das retas")

try:
    reta_inclinada = RetaR2((6,7), (4,2))
    reta_vertical = RetaR2((5,9), (5, 12))
    reta_horizontal = RetaR2((9,5), (12,5))
    print("\nCriação bem-sucedida!")

except (ValueError, TypeError):
    raise ValueError("\nCriação não realizada.")

#Obter ponto inicial
print("\nObter ponto inicial")
print(f"Ponto inicial reta inclinada: {reta_inclinada.ponto_inicial}")
print(f"Ponto inicial reta vertical: {reta_vertical.ponto_inicial}")
print(f"Ponto inicial reta horizontal: {reta_horizontal.ponto_inicial}")

#Obter ponto final
print("\nObter ponto final")
print(f"\nPonto final reta inclinada: {reta_inclinada.ponto_final}")
print(f"Ponto final reta vertical: {reta_vertical.ponto_final}")
print(f"Ponto final reta horizontal: {reta_horizontal.ponto_final}")

#Obter vetor diretor
print("\nObter vetor diretor")
print(f"\nVetor diretor reta inclinada: {reta_inclinada.vetor_diretor}")
print(f"Vetor diretor reta vertical: {reta_vertical.vetor_diretor}")
print(f"Vetor diretor reta horizontal: {reta_horizontal.vetor_diretor}")

#Equação reduzida
print("\nEquação reduzida")
print(f"\nReta inclinada: {reta_inclinada.equacao_reduzida}")
print(f"Reta vertical: {reta_vertical.equacao_reduzida}")
print(f"Reta horizontal: {reta_horizontal.equacao_reduzida}")

#Equação simétrica
#Sem formatação
print("\nEquação simétrica sem formatação")
print("\nReta inclinada:", reta_inclinada.equacao_simetrica(0))
print("Reta vertical:", reta_vertical.equacao_simetrica(0))
print("Reta horizontal:", reta_horizontal.equacao_simetrica(0))

#Com formatação
print("\nEquação simétrica com formatação")
print("\nReta inclinada:")
print(reta_inclinada.equacao_simetrica())
print("Reta vertical:", reta_vertical.equacao_simetrica()) #Tem que ser em linhas separadas
print("Reta horizontal:", reta_horizontal.equacao_simetrica())

#Equação vetorial
print("\nEquação vetorial")
print(f"\nReta inclinada: {reta_inclinada.equacao_vetorial()}")
print(f"Reta vertical: {reta_vertical.equacao_vetorial()}")
print(f"Reta horizontal: {reta_horizontal.equacao_vetorial()}")

#Equação paramétrica
print("\nEquação paramétrica")
print(f"\nReta inclinada:\n{reta_inclinada.equacao_parametrica()}\n")
print(f"Reta vertical:\n{reta_vertical.equacao_parametrica()}\n")
print(f"Reta horizontal:\n{reta_horizontal.equacao_parametrica()}")

#Pertencimento de ponto
p1 = Vetor((2,-3))
p2 = Vetor((-7,0))
p3 = Vetor((5,-2))
p4 = Vetor((-9,1))
p5 = Vetor((-6,5))
p6 = Vetor((-12,32))
print("\nPertencimento de ponto")
print(f"\nReta inclinada")
print("Verificar (2, -3): ", reta_inclinada.ponto_pertence(p1))
print("Verificar ponto (-7, 0): ", reta_inclinada.ponto_pertence(p2))
print(f"\nReta vertical")
print("Verificar (5, -2): ", reta_vertical.ponto_pertence(p3))
print("Verificar ponto (-9, 1): ", reta_vertical.ponto_pertence(p4))
print(f"\nReta horizontal")
print("Verificar (-6, 5): ", reta_horizontal.ponto_pertence(p5))
print("Verificar ponto (-12, 32): ", reta_horizontal.ponto_pertence(p6))




