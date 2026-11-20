"""Análise das relações geométricas entre retas do R² e do R³."""

from math import isfinite
from numbers import Real

from backend.reta import Reta


class Analisador:
    """Classifica e calcula interseções entre retas do mesmo espaço."""

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
        """Verifica se os vetores diretores são paralelos."""
        Analisador._validar_retas(reta1, reta2)
        Analisador._validar_tolerancia(tolerancia)

        if reta1.dimensao == 2:
            a1, b1 = reta1.vetor_diretor.coordenadas
            a2, b2 = reta2.vetor_diretor.coordenadas
            determinante = a1 * b2 - b1 * a2
            limite = tolerancia * reta1.vetor_diretor.modulo() * reta2.vetor_diretor.modulo()
            return abs(determinante) <= limite

        produto_vetorial = reta1.vetor_diretor.produto_vetorial(reta2.vetor_diretor)
        limite = tolerancia * reta1.vetor_diretor.modulo() * reta2.vetor_diretor.modulo()
        return produto_vetorial.modulo() <= limite

    @staticmethod
    def verificar_coincidencia(reta1, reta2, tolerancia=TOLERANCIA):
        """Verifica se as retas paralelas compartilham os mesmos pontos."""
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
        return "concorrentes" if produto_misto <= limite else "reversas"

    @staticmethod
    def verificar_reversas(reta1, reta2, tolerancia=TOLERANCIA):
        """Retorna True se as retas não paralelas do R³ não são coplanares."""
        Analisador._validar_retas(reta1, reta2)
        Analisador._validar_tolerancia(tolerancia)
        if reta1.dimensao != 3:
            return False
        return Analisador._obter_relacao(reta1, reta2, tolerancia) == "reversas"

    @staticmethod
    def calcular_intersecao(reta1, reta2, tolerancia=TOLERANCIA):
        """Calcula o ponto único de interseção, ou retorna None."""
        Analisador._validar_retas(reta1, reta2)
        Analisador._validar_tolerancia(tolerancia)
        if Analisador._obter_relacao(reta1, reta2, tolerancia) != "concorrentes":
            return None

        deslocamento = reta2.ponto_inicial.subtrair(reta1.ponto_inicial)
        direcao1 = reta1.vetor_diretor
        direcao2 = reta2.vetor_diretor

        if reta1.dimensao == 2:
            a1, b1 = direcao1.coordenadas
            a2, b2 = direcao2.coordenadas
            dx, dy = deslocamento.coordenadas
            determinante = a1 * b2 - b1 * a2
            parametro = (dx * b2 - dy * a2) / determinante
        else:
            normal = direcao1.produto_vetorial(direcao2)
            parametro = (
                deslocamento.produto_vetorial(direcao2).produto_escalar(normal)
                / normal.produto_escalar(normal)
            )

        return reta1.obter_ponto(parametro)

    @staticmethod
    def analisar(reta1, reta2, tolerancia=TOLERANCIA):
        """Retorna relação, ponto único de interseção, indicadores e mensagem."""
        relacao = Analisador._obter_relacao(reta1, reta2, tolerancia)
        ponto = (
            Analisador.calcular_intersecao(reta1, reta2, tolerancia)
            if relacao == "concorrentes"
            else None
        )
        sao_coincidentes = relacao == "coincidentes"
        sao_paralelas = relacao in {"paralelas", "coincidentes"}
        sao_reversas = relacao == "reversas"

        if ponto is not None:
            coordenadas = ", ".join(f"{valor:g}" for valor in ponto.coordenadas)
            mensagem = f"As retas se intersectam no ponto ({coordenadas})."
        elif sao_coincidentes:
            mensagem = "As retas são coincidentes."
        elif sao_paralelas:
            mensagem = "As retas são paralelas e distintas."
        else:
            mensagem = "As retas são reversas no R³."

        return {
            "relacao": relacao,
            "ponto_intersecao": ponto,
            "sao_paralelas": sao_paralelas,
            "sao_coincidentes": sao_coincidentes,
            "sao_reversas": sao_reversas,
            "mensagem": mensagem,
        }

    @staticmethod
    def formatar_resultado(resultado):
        """Formata o resumo de um dicionário retornado por analisar()."""
        return resultado["mensagem"]
