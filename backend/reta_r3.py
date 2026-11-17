"""Especialização de Reta para retas no espaço tridimensional."""

from math import acos, degrees

from backend.reta import Reta
from backend.vetor import Vetor


class RetaR3(Reta):
    """Reta do R³ definida por dois pontos distintos."""

    __slots__ = ()

    def __init__(self, ponto_inicial, ponto_final):
        if not isinstance(ponto_inicial, Vetor) or not isinstance(ponto_final, Vetor):
            raise TypeError("Os pontos devem ser objetos Vetor.")
        if ponto_inicial.dimensao != 3 or ponto_final.dimensao != 3:
            raise ValueError("RetaR3 exige dois pontos do R³.")

        vetor_diretor = ponto_final.subtrair(ponto_inicial)
        super().__init__(ponto_inicial, vetor_diretor)

    @classmethod
    def por_dois_pontos(cls, ponto_a, ponto_b):
        """Forma alternativa explícita para construir uma reta por dois pontos."""
        return cls(ponto_a, ponto_b)

    def equacao_simetrica(self):
        """Retorna a forma simétrica; coordenadas fixas viram igualdades."""
        simbolos = ("x", "y", "z")
        fracoes = []
        fixas = []

        for simbolo, coordenada, direcao in zip(
            simbolos,
            self.ponto_inicial.coordenadas,
            self.vetor_diretor.coordenadas,
        ):
            if direcao == 0:
                fixas.append(f"{simbolo} = {coordenada:g}")
            else:
                fracoes.append(f"({simbolo} - {coordenada:g}) / {direcao:g}")

        if len(fracoes) == 1:
            return ", ".join(fixas)

        equacao = " = ".join(fracoes)
        if fixas:
            return f"{equacao}, {', '.join(fixas)}" if equacao else ", ".join(fixas)
        return equacao

    @staticmethod
    def _validar_outra(outra):
        if not isinstance(outra, RetaR3):
            raise TypeError("O argumento deve ser um objeto RetaR3.")

    def distancia_ponto(self, ponto):
        """Calcula a distância de um ponto do R³ à reta."""
        if not isinstance(ponto, Vetor):
            raise TypeError("ponto deve ser um objeto Vetor.")
        if ponto.dimensao != 3:
            raise ValueError("O ponto deve ter dimensão 3.")

        deslocamento = ponto.subtrair(self.ponto_inicial)
        return deslocamento.produto_vetorial(self.vetor_diretor).modulo() / self.vetor_diretor.modulo()

    def eh_paralela(self, outra, tolerancia=1e-9):
        """Indica se as direções são proporcionais."""
        self._validar_outra(outra)
        return self.vetor_diretor.sao_proporcionais(outra.vetor_diretor, tolerancia)

    def eh_ortogonal(self, outra, tolerancia=1e-9):
        """Indica se os vetores diretores são ortogonais dentro da tolerância."""
        self._validar_outra(outra)
        produto = self.vetor_diretor.produto_escalar(outra.vetor_diretor)
        limite = tolerancia * self.vetor_diretor.modulo() * outra.vetor_diretor.modulo()
        return abs(produto) <= limite

    def angulo_com(self, outra):
        """Retorna o menor ângulo entre as retas, em graus, de 0° a 90°."""
        self._validar_outra(outra)
        u = self.vetor_diretor
        v = outra.vetor_diretor
        cosseno = abs(u.produto_escalar(v)) / (u.modulo() * v.modulo())
        return degrees(acos(min(1.0, cosseno)))

    def posicao_relativa(self, outra, tolerancia=1e-9):
        """Classifica a relação entre duas retas do R³."""
        self._validar_outra(outra)
        from backend.analisador import Analisador

        return Analisador._obter_relacao(self, outra, tolerancia)

    def distancia_reta(self, outra, tolerancia=1e-9):
        """Calcula a distância entre duas retas do R³."""
        self._validar_outra(outra)
        if self.eh_paralela(outra, tolerancia):
            return self.distancia_ponto(outra.ponto_inicial)

        deslocamento = outra.ponto_inicial.subtrair(self.ponto_inicial)
        normal = self.vetor_diretor.produto_vetorial(outra.vetor_diretor)
        return abs(deslocamento.produto_escalar(normal)) / normal.modulo()

    def ponto_intersecao(self, outra, tolerancia=1e-9):
        """Retorna o ponto comum único, ou None se as retas não se cruzarem."""
        self._validar_outra(outra)
        from backend.analisador import Analisador

        return Analisador.calcular_intersecao(self, outra, tolerancia)

    def __repr__(self):
        return f"RetaR3({self.ponto_inicial!r}, {self.vetor_diretor!r})"
