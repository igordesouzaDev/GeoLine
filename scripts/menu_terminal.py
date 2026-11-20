"""Menu de demonstração das operações matemáticas do GeoLine."""

from math import isfinite

from backend.analisador import Analisador
from backend.reta_r2 import RetaR2
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor


def ler_numero(mensagem):
    """Lê um número real finito do terminal."""
    texto = input(mensagem).strip()
    try:
        numero = float(texto)
    except ValueError as erro:
        raise ValueError("Digite um número válido.") from erro
    if not isfinite(numero):
        raise ValueError("O número deve ser finito.")
    return numero


def ler_vetor(dimensao=None, rotulo="vetor"):
    """Lê coordenadas separadas por vírgula e cria um Vetor."""
    if dimensao is None:
        texto_dimensao = input("Dimensão do vetor (2 ou 3): ").strip()
        if texto_dimensao not in {"2", "3"}:
            raise ValueError("A dimensão deve ser 2 ou 3.")
        dimensao = int(texto_dimensao)

    texto = input(
        f"Coordenadas do {rotulo}, separadas por vírgula ({dimensao} valores): "
    ).strip()
    try:
        coordenadas = [float(valor.strip()) for valor in texto.split(",")]
    except ValueError as erro:
        raise ValueError("Digite somente números separados por vírgulas.") from erro
    if len(coordenadas) != dimensao:
        raise ValueError(f"Informe exatamente {dimensao} coordenadas.")
    return Vetor(coordenadas)


def mostrar_menu():
    print("\n========================================")
    print("                 GEOLINE")
    print("       MENU DE TESTES MATEMÁTICOS")
    print("========================================")
    print("1 - Testar operações com vetores")
    print("2 - Construir reta no R²")
    print("3 - Construir reta no R³")
    print("4 - Analisar duas retas no R²")
    print("5 - Analisar duas retas no R³")
    print("0 - Sair")


def testar_vetores():
    operacao = input(
        "Operação (soma, subtração, escalar, módulo, escalar-produto, "
        "vetorial, proporcionalidade): "
    ).strip().lower()
    operacoes = {
        "1": "soma",
        "2": "subtração",
        "3": "escalar",
        "4": "módulo",
        "5": "escalar-produto",
        "6": "vetorial",
        "7": "proporcionalidade",
        "soma": "soma",
        "somar": "soma",
        "subtração": "subtração",
        "subtracao": "subtração",
        "subtrair": "subtração",
        "escalar": "escalar",
        "módulo": "módulo",
        "modulo": "módulo",
        "escalar-produto": "escalar-produto",
        "produto escalar": "escalar-produto",
        "vetorial": "vetorial",
        "produto vetorial": "vetorial",
        "proporcionalidade": "proporcionalidade",
        "proporcionais": "proporcionalidade",
    }
    operacao = operacoes.get(operacao)
    if operacao is None:
        raise ValueError("Operação inválida.")

    primeiro = ler_vetor(rotulo="primeiro vetor")
    if operacao == "módulo":
        print(f"Módulo: {primeiro.modulo():g}")
    elif operacao == "escalar":
        escalar = ler_numero("Valor do escalar: ")
        print("Resultado:", primeiro.multiplicar_escalar(escalar))
    else:
        segundo = ler_vetor(primeiro.dimensao, "segundo vetor")
        if operacao == "soma":
            print("Soma:", primeiro.somar(segundo))
        elif operacao == "subtração":
            print("Subtração:", primeiro.subtrair(segundo))
        elif operacao == "escalar-produto":
            print(f"Produto escalar: {primeiro.produto_escalar(segundo):g}")
        elif operacao == "vetorial":
            print("Produto vetorial:", primeiro.produto_vetorial(segundo))
        else:
            print("São proporcionais?", primeiro.sao_proporcionais(segundo))


def _mostrar_reta(reta, ponto_final):
    print("Ponto inicial:", reta.ponto_inicial)
    print("Ponto final:", ponto_final)
    print("Vetor diretor:", reta.vetor_diretor)
    print("Equação vetorial:", reta.equacao_vetorial())
    print("Equações paramétricas:")
    print(reta.equacao_parametrica())
    print("Equação simétrica:", reta.equacao_simetrica())
    if reta.dimensao == 2:
        print("Equação reduzida:", reta.equacao_reduzida())


def construir_reta_r2():
    ponto_inicial = ler_vetor(2, "ponto inicial")
    ponto_final = ler_vetor(2, "ponto final")
    reta = RetaR2(ponto_inicial, ponto_final)
    _mostrar_reta(reta, reta.ponto_final)


def construir_reta_r3():
    ponto_inicial = ler_vetor(3, "ponto inicial")
    ponto_final = ler_vetor(3, "ponto final")
    reta = RetaR3(ponto_inicial, ponto_final)
    _mostrar_reta(reta, ponto_final)


def _mostrar_analise(resultado):
    relacao = resultado["relacao"]
    print("Relação:", relacao)
    print("Paralelas:", resultado["sao_paralelas"])
    print("Coincidentes:", resultado["sao_coincidentes"])
    print("Concorrentes:", relacao == "concorrentes")
    if "sao_reversas" in resultado:
        print("Reversas:", resultado["sao_reversas"])
    print("Ponto de interseção:", resultado["ponto_intersecao"])
    print("Mensagem:", resultado["mensagem"])


def analisar_retas_r2():
    retas = []
    for numero in (1, 2):
        print(f"\nReta {numero}")
        ponto_inicial = ler_vetor(2, f"ponto inicial da reta {numero}")
        ponto_final = ler_vetor(2, f"ponto final da reta {numero}")
        retas.append(RetaR2(ponto_inicial, ponto_final))
    _mostrar_analise(Analisador.analisar(*retas))


def analisar_retas_r3():
    retas = []
    for numero in (1, 2):
        print(f"\nReta {numero}")
        ponto_inicial = ler_vetor(3, f"ponto inicial da reta {numero}")
        ponto_final = ler_vetor(3, f"ponto final da reta {numero}")
        retas.append(RetaR3(ponto_inicial, ponto_final))
    _mostrar_analise(Analisador.analisar(*retas))


def main():
    """Executa o menu até o usuário escolher sair."""
    while True:
        mostrar_menu()
        try:
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "0":
                print("GeoLine encerrado.")
                return
            acoes = {
                "1": testar_vetores,
                "2": construir_reta_r2,
                "3": construir_reta_r3,
                "4": analisar_retas_r2,
                "5": analisar_retas_r3,
            }
            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida. Escolha uma opção de 0 a 5.")
                continue
            acao()
        except (TypeError, ValueError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")
        except EOFError:
            print("\nEntrada encerrada. GeoLine finalizado.")
            return


if __name__ == "__main__":
    main()
