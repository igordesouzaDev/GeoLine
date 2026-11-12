"""Operações básicas com vetores do R² e do R³."""

from math import isclose, isfinite, sqrt
from numbers import Real


class Vetor:
    """Vetor de duas ou três coordenadas reais."""

    __slots__ = ("_coordenadas", "_dimensao")

    def __init__(self, coordenadas):
        try:
            valores = tuple(coordenadas)
        except TypeError as exc:
            raise TypeError("As coordenadas devem ser um iterável de números reais.") from exc

        if len(valores) not in (2, 3):
            raise ValueError("Um vetor deve ter exatamente 2 ou 3 coordenadas.")

        for valor in valores:
            if isinstance(valor, bool) or not isinstance(valor, Real):
                raise TypeError("Cada coordenada deve ser um número real.")
            if not isfinite(valor):
                raise ValueError("As coordenadas devem ser finitas.")

        self._coordenadas = valores
        self._dimensao = len(valores)

    @property
    def coordenadas(self):
        return self._coordenadas

    @property
    def dimensao(self):
        return self._dimensao

    def _validar_outro(self, outro):
        if not isinstance(outro, Vetor):
            raise TypeError("A operação exige outro objeto Vetor.")
        if self.dimensao != outro.dimensao:
            raise ValueError("Os vetores devem ter a mesma dimensão.")

    @staticmethod
    def _validar_escalar(valor):
        if isinstance(valor, bool) or not isinstance(valor, Real):
            raise TypeError("O escalar deve ser um número real.")
        if not isfinite(valor):
            raise ValueError("O escalar deve ser finito.")

    def somar(self, outro):
        self._validar_outro(outro)
        return Vetor(a + b for a, b in zip(self.coordenadas, outro.coordenadas))

    def subtrair(self, outro):
        self._validar_outro(outro)
        return Vetor(a - b for a, b in zip(self.coordenadas, outro.coordenadas))

    def multiplicar_escalar(self, valor):
        self._validar_escalar(valor)
        return Vetor(coordenada * valor for coordenada in self.coordenadas)

    def modulo(self):
        return sqrt(sum(coordenada * coordenada for coordenada in self.coordenadas))

    def produto_escalar(self, outro):
        self._validar_outro(outro)
        return sum(a * b for a, b in zip(self.coordenadas, outro.coordenadas))

    def produto_vetorial(self, outro):
        self._validar_outro(outro)
        if self.dimensao != 3:
            raise ValueError("O produto vetorial é definido aqui apenas para vetores do R³.")
        x1, y1, z1 = self.coordenadas
        x2, y2, z2 = outro.coordenadas
        return Vetor((y1 * z2 - z1 * y2,
                      z1 * x2 - x1 * z2,
                      x1 * y2 - y1 * x2))

    def sao_proporcionais(self, outro, tolerancia=1e-9):
        self._validar_outro(outro)
        if isinstance(tolerancia, bool) or not isinstance(tolerancia, Real):
            raise TypeError("A tolerância deve ser um número real não negativo.")
        if not isfinite(tolerancia) or tolerancia < 0:
            raise ValueError("A tolerância deve ser finita e não negativa.")

        # Dois vetores nulos são proporcionais; apenas um vetor nulo não é.
        nulo_self = all(isclose(c, 0.0, rel_tol=0.0, abs_tol=tolerancia) for c in self.coordenadas)
        nulo_outro = all(isclose(c, 0.0, rel_tol=0.0, abs_tol=tolerancia) for c in outro.coordenadas)
        if nulo_self or nulo_outro:
            return nulo_self and nulo_outro

        # Compara produtos cruzados, sem dividir por coordenadas próximas de zero.
        for i in range(self.dimensao):
            for j in range(i + 1, self.dimensao):
                if not isclose(self.coordenadas[i] * outro.coordenadas[j],
                               self.coordenadas[j] * outro.coordenadas[i],
                               rel_tol=tolerancia, abs_tol=tolerancia):
                    return False
        return True

    def __repr__(self):
        return f"Vetor({self.coordenadas!r})"
