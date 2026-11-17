"""Classifica relações geométricas entre retas do R² e do R³."""

from math import isfinite
from numbers import Real

from backend.reta import Reta
from backend.vetor import Vetor


class Analisador:
    """Analisa paralelismo, coincidência, interseção e retas reversas."""

    TOLERANCIA = 1e-9

    @staticmethod
    def _validar_tolerancia(tolerancia):
        if isinstance(tolerancia, bool) or not isinstance(tolerancia, Real):
            raise TypeError("A tolerância deve ser um número real não negativo.")
        if not isfinite(tolerancia) or tolerancia < 0:
            raise ValueError("A tolerância deve ser finita e não negativa.")

    @staticmethod
    def _validar_retas(reta1, reta2):
        if not isinstance(reta1, Reta) or not isinstance(reta2, Reta):
            raise TypeError("Os argumentos devem ser objetos Reta ou classes derivadas.")
        if reta1.dimensao != reta2.dimensao:
            raise ValueError("As retas devem pertencer ao mesmo espaço.")

    @staticmethod
    def verificar_paralelismo(reta1, reta2, tolerancia=TOLERANCIA):
        """Retorna True se as retas têm vetores diretores proporcionais."""
        Analisador._validar_retas(reta1, reta2)
        Analisador._validar_tolerancia(tolerancia)
        return reta1.vetor_diretor.sao_proporcionais(reta2.vetor_diretor, tolerancia)

    @staticmethod
    def verificar_coincidencia(reta1, reta2, tolerancia=TOLERANCIA):
        """Retorna True se as retas são paralelas e compartilham todos os pontos."""
        Analisador._validar_retas(reta1, reta2)
        Analisador._validar_tolerancia(tolerancia)
        return (
            Analisador.verificar_paralelismo(reta1, reta2, tolerancia)
            and reta1.ponto_pertence(reta2.ponto_inicial, tolerancia)
        )

    @staticmethod
    def _obter_relacao(reta1, reta2, tolerancia=TOLERANCIA):
        Analisador._validar_retas(reta1, reta2)
        Analisador._validar_tolerancia(tolerancia)

        if Analisador.verificar_paralelismo(reta1, reta2, tolerancia):
            if Analisador.verificar_coincidencia(reta1, reta2, tolerancia):
                return "coincidentes"
            return "paralelas"

        if reta1.dimensao == 2:
            return "concorrentes"

        deslocamento = reta2.ponto_inicial.subtrair(reta1.ponto_inicial)
        normal = reta1.vetor_diretor.produto_vetorial(reta2.vetor_diretor)
        produto_misto = abs(deslocamento.produto_escalar(normal))
        limite = tolerancia * max(1.0, deslocamento.modulo() * normal.modulo())
        if produto_misto <= limite:
            return "concorrentes"
        return "reversas"

    @staticmethod
    def verificar_reversas(reta1, reta2, tolerancia=TOLERANCIA):
        """Retorna True somente para retas reversas do R³."""
        Analisador._validar_retas(reta1, reta2)
        if reta1.dimensao != 3:
            return False
        return Analisador._obter_relacao(reta1, reta2, tolerancia) == "reversas"

    @staticmethod
    def calcular_intersecao(reta1, reta2, tolerancia=TOLERANCIA):
        """Retorna o ponto de interseção único, ou None se não existir."""
        Analisador._validar_retas(reta1, reta2)
        Analisador._validar_tolerancia(tolerancia)
        if Analisador._obter_relacao(reta1, reta2, tolerancia) != "concorrentes":
            return None

        ponto1 = reta1.ponto_inicial
        ponto2 = reta2.ponto_inicial
        direcao1 = reta1.vetor_diretor
        direcao2 = reta2.vetor_diretor
        deslocamento = ponto2.subtrair(ponto1)

        if reta1.dimensao == 2:
            x1, y1 = direcao1.coordenadas
            x2, y2 = direcao2.coordenadas
            wx, wy = deslocamento.coordenadas
            determinante = x1 * y2 - y1 * x2
            parametro = (wx * y2 - wy * x2) / determinante
        else:
            normal = direcao1.produto_vetorial(direcao2)
            parametro = (
                deslocamento.produto_vetorial(direcao2).produto_escalar(normal)
                / normal.produto_escalar(normal)
            )

        return reta1.obter_ponto(parametro)

    @staticmethod
    def analisar(reta1, reta2, tolerancia=TOLERANCIA):
        """Retorna classificação, flags, ponto único de interseção e mensagem."""
        relacao = Analisador._obter_relacao(reta1, reta2, tolerancia)
        ponto = (
            Analisador.calcular_intersecao(reta1, reta2, tolerancia)
            if relacao == "concorrentes"
            else None
        )
        paralelas = relacao in {"paralelas", "coincidentes"}
        coincidentes = relacao == "coincidentes"
        reversas = relacao == "reversas"

        if relacao == "concorrentes":
            coordenadas = ", ".join(f"{valor:g}" for valor in ponto.coordenadas)
            mensagem = f"As retas se intersectam no ponto ({coordenadas})."
        elif coincidentes:
            mensagem = "As retas são coincidentes."
        elif paralelas:
            mensagem = "As retas são paralelas e distintas."
        else:
            mensagem = "As retas são reversas no R³."

        return {
            "relacao": relacao,
            "ponto_intersecao": ponto,
            "sao_paralelas": paralelas,
            "sao_coincidentes": coincidentes,
            "sao_reversas": reversas,
            "mensagem": mensagem,
        }

    @staticmethod
    def formatar_resultado(resultado):
        """Retorna a mensagem já calculada por analisar()."""
        return resultado["mensagem"]
