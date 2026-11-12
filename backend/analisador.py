
class AnalisadorRetas:
    """
    Analisa a relação entre duas retas no R².
    As retas são representadas por ponto e vetor diretor.
    """
    @staticmethod
    def vetores_proporcionais(v1, v2):
        
        tolerancia = 1e-9

        if len(v1) != len(v2):
            raise ValueError("Os vetores devem ter a mesma dimensão.")

        if all(abs(c) < tolerancia for c in v1):
            raise ValueError("O primeiro vetor não pode ser nulo.")

        if all(abs(c) < tolerancia for c in v2):
            raise ValueError("O segundo vetor não pode ser nulo.")

        indice = next(
            i for i in range(len(v2))
            if abs(v2[i]) >= tolerancia
        )

        proporcao = v1[indice] / v2[indice]

        return all(
            abs(v1[i] - proporcao * v2[i]) < tolerancia
            for i in range(len(v1))
        )

    @staticmethod
    def analisar_paralelismo_r3(ponto1, direcao1, ponto2, direcao2):
        tolerancia = 1e-9

        if len(ponto1) != 3 or len(ponto2) != 3:
            raise ValueError("Os pontos devem pertencer ao R³.")

        if len(direcao1) != 3 or len(direcao2) != 3:
            raise ValueError("Os vetores diretores devem pertencer ao R³.")

        if all(abs(c) < tolerancia for c in direcao1):
            raise ValueError("O primeiro vetor diretor não pode ser nulo.")

        if all(abs(c) < tolerancia for c in direcao2):
            raise ValueError("O segundo vetor diretor não pode ser nulo.")

        proporcionais = AnalisadorRetas.vetores_proporcionais(
            direcao1, direcao2
        )

        if not proporcionais:
            return "Não paralelas"

        diferenca = (
            ponto2[0] - ponto1[0],
            ponto2[1] - ponto1[1],
            ponto2[2] - ponto1[2]
        )

        produto_vetorial = (
            diferenca[1] * direcao1[2] - diferenca[2] * direcao1[1],
            diferenca[2] * direcao1[0] - diferenca[0] * direcao1[2],
            diferenca[0] * direcao1[1] - diferenca[1] * direcao1[0]
        )

        if all(abs(c) < tolerancia for c in produto_vetorial):
            return "Coincidentes"

        return "Paralelas"

    @staticmethod
    def calcular_intersecao_r3(ponto1, direcao1, ponto2, direcao2):
        tolerancia = 1e-9

        if len(ponto1) != 3 or len(ponto2) != 3:
            raise ValueError("Os pontos devem pertencer ao R³.")

        if len(direcao1) != 3 or len(direcao2) != 3:
            raise ValueError("Os vetores diretores devem pertencer ao R³.")

        if all(abs(c) < tolerancia for c in direcao1):
            raise ValueError("O primeiro vetor diretor não pode ser nulo.")

        if all(abs(c) < tolerancia for c in direcao2):
            raise ValueError("O segundo vetor diretor não pode ser nulo.")

        diferenca = (
            ponto2[0] - ponto1[0],
            ponto2[1] - ponto1[1],
            ponto2[2] - ponto1[2]
        )

        # Produto vetorial dos vetores diretores
        cruzado = (
            direcao1[1] * direcao2[2] - direcao1[2] * direcao2[1],
            direcao1[2] * direcao2[0] - direcao1[0] * direcao2[2],
            direcao1[0] * direcao2[1] - direcao1[1] * direcao2[0]
        )

        # Determina se as retas são paralelas
        if all(abs(c) < tolerancia for c in cruzado):
            classificacao = AnalisadorRetas.analisar_paralelismo_r3(
                ponto1, direcao1, ponto2, direcao2
            )

            return {
                "classificacao": classificacao,
                "intersecao": None
            }

        # Produto misto para verificar se as retas são coplanares
        produto_misto = (
            diferenca[0] * cruzado[0]
            + diferenca[1] * cruzado[1]
            + diferenca[2] * cruzado[2]
        )

        if abs(produto_misto) >= tolerancia:
            return {
                "classificacao": "Reversas",
                "intersecao": None
            }

        # Calcula o parâmetro da primeira reta
        numerador = (
            diferenca[1] * direcao2[2] - diferenca[2] * direcao2[1],
            diferenca[2] * direcao2[0] - diferenca[0] * direcao2[2],
            diferenca[0] * direcao2[1] - diferenca[1] * direcao2[0]
        )

        t = (
            numerador[0] * cruzado[0]
            + numerador[1] * cruzado[1]
            + numerador[2] * cruzado[2]
        ) / (
            cruzado[0] ** 2
            + cruzado[1] ** 2
            + cruzado[2] ** 2
        )

        intersecao = (
            ponto1[0] + t * direcao1[0],
            ponto1[1] + t * direcao1[1],
            ponto1[2] + t * direcao1[2]
        )

        return {
            "classificacao": "Intersectantes",
            "intersecao": intersecao
        }
    
    @staticmethod
    def determinante(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    @staticmethod
    def analisar(ponto1, direcao1, ponto2, direcao2):
        tolerancia = 1e-9

        if all(abs(c) < tolerancia for c in direcao1):
            raise ValueError("O primeiro vetor diretor não pode ser nulo.")

        if all(abs(c) < tolerancia for c in direcao2):
            raise ValueError("O segundo vetor diretor não pode ser nulo.")

        diferenca = (
            ponto2[0] - ponto1[0],
            ponto2[1] - ponto1[1]
        )

        det = AnalisadorRetas.determinante(
            direcao1, direcao2
        )

        norma1 = (direcao1[0] ** 2 + direcao1[1] ** 2) ** 0.5
        norma2 = (direcao2[0] ** 2 + direcao2[1] ** 2) ** 0.5

        if abs(det) <= tolerancia * norma1 * norma2:

            det_pontos = AnalisadorRetas.determinante(
                diferenca, direcao1
            )

            norma_diferenca = (
                diferenca[0] ** 2 + diferenca[1] ** 2
            ) ** 0.5

            if abs(det_pontos) <= tolerancia * norma_diferenca * norma1:
                return {
                    "classificacao": "Coincidentes",
                    "intersecao": None
                }

            return {
                "classificacao": "Paralelas",
                "intersecao": None
            }

        t = AnalisadorRetas.determinante(
            diferenca, direcao2
        ) / det

        x = ponto1[0] + t * direcao1[0]
        y = ponto1[1] + t * direcao1[1]

        return {
            "classificacao": "Intersectantes",
            "intersecao": (x, y)
        }

    
    @staticmethod
    def ponto_pertence_reta(ponto, ponto_reta, direcao):
        tolerancia = 1e-9

        if all(abs(c) < tolerancia for c in direcao):
            raise ValueError("O vetor diretor não pode ser nulo.")

        diferenca = (
            ponto[0] - ponto_reta[0],
            ponto[1] - ponto_reta[1]
        )

        determinante = AnalisadorRetas.determinante(
            diferenca, direcao
        )

        return abs(determinante) < tolerancia

    @staticmethod
    def formatar_resultado(resultado):
        classificacao = resultado["classificacao"]
        intersecao = resultado["intersecao"]

        if classificacao == "Intersectantes":
            coordenadas = ", ".join(
                f"{valor:.4f}".rstrip("0").rstrip(".")
                for valor in intersecao
            )

            return f"As retas são intersectantes. Ponto de interseção: ({coordenadas})."

        if classificacao == "Paralelas":
            return "As retas são paralelas e não possuem ponto de interseção."

        if classificacao == "Coincidentes":
            return "As retas são coincidentes e possuem infinitos pontos em comum."

        if classificacao == "Reversas":
            return "As retas são reversas: não são paralelas e não se intersectam."

        return f"Classificação das retas: {classificacao}."