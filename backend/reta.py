"""Classe-base para retas no R² e no R³."""

from math import isfinite
from numbers import Real

from backend.formatacao import formatar_numero
from backend.vetor import Vetor


class Reta:
    """Representa uma reta por um ponto e um vetor diretor."""

    __slots__ = ("_ponto_inicial", "_vetor_diretor", "_dimensao")

    def __init__(self, ponto_inicial, vetor_diretor):
        if not isinstance(ponto_inicial, Vetor):
            raise TypeError("O ponto inicial deve ser um objeto Vetor.")
        if not isinstance(vetor_diretor, Vetor):
            raise TypeError("O vetor diretor deve ser um objeto Vetor.")
        if ponto_inicial.dimensao != vetor_diretor.dimensao:
            raise ValueError("O ponto inicial e o vetor diretor devem possuir a mesma dimensão.")
        if vetor_diretor.modulo() == 0:
            raise ValueError("O vetor diretor não pode ser nulo.")

        self._ponto_inicial = ponto_inicial
        self._vetor_diretor = vetor_diretor
        self._dimensao = ponto_inicial.dimensao

    @property
    def ponto_inicial(self):
        return self._ponto_inicial

    @property
    def vetor_diretor(self):
        return self._vetor_diretor

    @property
    def dimensao(self):
        return self._dimensao

    @staticmethod
    def _validar_t(t):
        if isinstance(t, bool) or not isinstance(t, Real):
            raise TypeError("O parâmetro t deve ser um número real.")
        if not isfinite(t):
            raise ValueError("O parâmetro t deve ser finito.")

    def obter_ponto(self, t):
        """Retorna P(t) = P₀ + t·v como um novo Vetor."""
        self._validar_t(t)
        return self.ponto_inicial.somar(self.vetor_diretor.multiplicar_escalar(t))

    def ponto_pertence(self, ponto, tolerancia=1e-9):
        """Indica se um Vetor pertence à reta, dentro da tolerância dada."""
        if not isinstance(ponto, Vetor):
            raise TypeError("O ponto deve ser um objeto Vetor.")
        if ponto.dimensao != self.dimensao:
            raise ValueError("O ponto deve possuir a mesma dimensão da reta.")
        if isinstance(tolerancia, bool) or not isinstance(tolerancia, Real):
            raise TypeError("A tolerância deve ser um número real.")
        if not isfinite(tolerancia) or tolerancia < 0:
            raise ValueError("A tolerância deve ser finita e não negativa.")

        deslocamento = ponto.subtrair(self.ponto_inicial)
        direcao = self.vetor_diretor.coordenadas
        diferenca = deslocamento.coordenadas
        # Como o vetor diretor não é nulo, pelo menos uma coordenada permite
        # determinar t. As demais devem concordar com esse mesmo parâmetro.
        indice = max(range(self.dimensao), key=lambda i: abs(direcao[i]))
        t = diferenca[indice] / direcao[indice]
        esperado = self.vetor_diretor.multiplicar_escalar(t)
        return all(
            abs(a - b) <= tolerancia * max(1.0, abs(a), abs(b))
            for a, b in zip(diferenca, esperado.coordenadas)
        )

    def equacao_vetorial(self):
        """Retorna a equação vetorial em forma textual."""
        simbolos = ("x", "y", "z")[:self.dimensao]
        variaveis = ", ".join(simbolos)
        ponto = ", ".join(formatar_numero(valor) for valor in self.ponto_inicial.coordenadas)
        direcao = ", ".join(formatar_numero(valor) for valor in self.vetor_diretor.coordenadas)
        return f"({variaveis}) = ({ponto}) + t({direcao})"

    def equacao_parametrica(self):
        """Retorna as equações paramétricas em linhas separadas."""
        simbolos = ("x", "y", "z")[:self.dimensao]
        equacoes = []
        for simbolo, coordenada, direcao in zip(
            simbolos, self.ponto_inicial.coordenadas, self.vetor_diretor.coordenadas
        ):
            if direcao < 0:
                operacao = f"- {formatar_numero(abs(direcao))}t"
            else:
                operacao = f"+ {formatar_numero(direcao)}t"
            equacoes.append(f"{simbolo} = {formatar_numero(coordenada)} {operacao}")
        return "\n".join(equacoes)

    def __repr__(self):
        return f"Reta({self.ponto_inicial!r}, {self.vetor_diretor!r})"
