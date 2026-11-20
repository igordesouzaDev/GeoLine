
from math import atan2, degrees, isfinite
from numbers import Real

from backend.reta import Reta
from backend.vetor import Vetor


def _formatar_numero(valor):
    """Mostra 2.0 como 2, mantendo frações como 0.5."""
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def _formatar_numerador(simbolo, ponto):
    """Formata (simbolo - ponto) com sinal limpo: x, (x - 1) ou (x + 2)."""
    if ponto == 0:
        return simbolo
    if ponto > 0:
        return f"({simbolo} - {_formatar_numero(ponto)})"
    return f"({simbolo} + {_formatar_numero(-ponto)})"


class RetaR3(Reta):
    """
    Representa uma reta no R³ e analisa suas relações geométricas
    com pontos e com outras retas. O construtor recebe dois pontos;
    use ``por_ponto_e_direcao`` quando a entrada for ponto + direção.

    A reta é definida por um ponto pertencente a ela (ponto inicial)
    e por um vetor diretor não nulo, ambos com três coordenadas.
    Seus pontos são dados por P(t) = P₀ + t·v, com t real.

    CRITÉRIOS DE CLASSIFICAÇÃO (posicao_relativa):

    - Coincidentes: os vetores diretores são proporcionais e o ponto
      inicial de uma das retas pertence à outra. As retas possuem
      infinitos pontos em comum.
    - Paralelas: os vetores diretores são proporcionais, mas as retas
      são distintas, sem pontos em comum.
    - Concorrentes: os vetores diretores não são proporcionais e as
      retas são coplanares, ou seja, o produto misto entre o vetor
      que liga os pontos iniciais e os dois vetores diretores é zero.
      As retas possuem um único ponto em comum.
    - Reversas: os vetores diretores não são proporcionais e as retas
      não são coplanares (produto misto diferente de zero). Não há
      ponto de interseção e a distância entre elas é positiva.

    PERTENCIMENTO DE PONTO:
    Um ponto pertence à reta quando o vetor que liga o ponto inicial
    ao ponto analisado é proporcional ao vetor diretor, considerando
    a tolerância (método herdado de Reta).

    DISTÂNCIAS:
    - Ponto à reta: |AP × v| / |v|, em que A é o ponto inicial, P é o
      ponto analisado e v é o vetor diretor.
    - Reta à reta: |w · (u × v)| / |u × v| para retas não paralelas,
      em que w liga os pontos iniciais e u, v são os vetores diretores.
      Para retas paralelas, é a distância de um ponto de uma à outra.

    ÂNGULO ENTRE RETAS:
    É o menor ângulo entre as direções das retas, de 0° a 90°,
    calculado por cos θ = |u · v| / (|u|·|v|). Retas ortogonais
    têm u · v = 0.

    EXEMPLOS:

    Ponto 1 = (0, 0, 0), direção 1 = (1, 0, 0)
    Ponto 2 = (0, 1, 0), direção 2 = (0, 1, 0)
    Resultado: retas concorrentes, interseção em (0, 0, 0).

    Ponto 1 = (0, 0, 0), direção 1 = (1, 0, 0)
    Ponto 2 = (0, 1, 1), direção 2 = (0, 1, 0)
    Resultado: retas reversas, a distância entre elas é 1.

    Ponto 1 = (0, 0, 0), direção 1 = (1, 1, 1)
    Ponto 2 = (1, 0, 0), direção 2 = (2, 2, 2)
    Resultado: retas paralelas, a distância entre elas é √(2/3) ≈ 0.8165.

    Ponto = (1, 2, 3), direção = (2, 0, 4)
    Equação simétrica: (x - 1)/2 = (z - 3)/4, y = 2
    (componentes nulas do vetor diretor viram igualdades separadas).

    As verificações geométricas usam tolerância numérica relativa de
    1e-9 por padrão, para lidar com aproximações de ponto flutuante.
    """
    __slots__ = ()

    def __init__(self, ponto_inicial, ponto_final):
        """Cria a reta por dois pontos distintos do R³, conforme o contrato."""
        if not isinstance(ponto_inicial, Vetor) or not isinstance(ponto_final, Vetor):
            raise TypeError("Os pontos devem ser objetos Vetor.")
        if ponto_inicial.dimensao != 3 or ponto_final.dimensao != 3:
            raise ValueError("RetaR3 exige dois pontos com dimensão 3.")
        vetor_diretor = ponto_final.subtrair(ponto_inicial)
        super().__init__(ponto_inicial, vetor_diretor)

    # ------------------------------------------------------------------
    # Construção alternativa
    # ------------------------------------------------------------------
    @classmethod
    def por_dois_pontos(cls, ponto_a, ponto_b):
        """Cria a reta que passa por dois pontos distintos do R³."""
        if not isinstance(ponto_a, Vetor) or not isinstance(ponto_b, Vetor):
            raise TypeError("Os pontos devem ser objetos Vetor.")
        if ponto_a.dimensao != ponto_b.dimensao:
            raise ValueError("Os pontos devem ter a mesma dimensão.")
        return cls(ponto_a, ponto_b)

    @classmethod
    def por_ponto_e_direcao(cls, ponto_inicial, vetor_diretor):
        """Cria a reta a partir de um ponto e um vetor diretor não nulo."""
        if not isinstance(ponto_inicial, Vetor) or not isinstance(vetor_diretor, Vetor):
            raise TypeError("O ponto e o vetor diretor devem ser objetos Vetor.")
        if ponto_inicial.dimensao != 3 or vetor_diretor.dimensao != 3:
            raise ValueError("RetaR3 exige ponto e vetor diretor com dimensão 3.")
        instancia = cls.__new__(cls)
        Reta.__init__(instancia, ponto_inicial, vetor_diretor)
        return instancia

    # ------------------------------------------------------------------
    # Validações internas
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_tolerancia(tolerancia):
        if isinstance(tolerancia, bool) or not isinstance(tolerancia, Real):
            raise TypeError("A tolerância deve ser um número real não negativo.")
        if not isfinite(tolerancia) or tolerancia < 0:
            raise ValueError("A tolerância deve ser finita e não negativa.")

    @staticmethod
    def _validar_reta(outra):
        if not isinstance(outra, RetaR3):
            raise TypeError("O argumento deve ser um objeto RetaR3.")

    # ------------------------------------------------------------------
    # Equações
    # ------------------------------------------------------------------
    def equacao_simetrica(self):
        """Retorna a equação simétrica; componentes nulas viram igualdades."""
        simbolos = ("x", "y", "z")
        fracoes = []
        fixas = []
        for simbolo, p, d in zip(
            simbolos, self.ponto_inicial.coordenadas, self.vetor_diretor.coordenadas
        ):
            if d == 0:
                fixas.append(f"{simbolo} = {_formatar_numero(p)}")
            else:
                numerador = _formatar_numerador(simbolo, p)
                fracoes.append(f"{numerador}/{_formatar_numero(d)}")
        partes = []
        if fracoes:
            partes.append(" = ".join(fracoes))
        partes.extend(fixas)
        return ", ".join(partes)

    # ------------------------------------------------------------------
    # Relações com pontos
    # ------------------------------------------------------------------
    def distancia_ponto(self, ponto):
        """Distância de um ponto do R³ à reta: |AP × v| / |v|."""
        if not isinstance(ponto, Vetor):
            raise TypeError("ponto deve ser um objeto Vetor.")
        if ponto.dimensao != 3:
            raise ValueError("O ponto deve ter dimensão 3.")
        deslocamento = ponto.subtrair(self.ponto_inicial)
        return (
            deslocamento.produto_vetorial(self.vetor_diretor).modulo()
            / self.vetor_diretor.modulo()
        )

    # ------------------------------------------------------------------
    # Relações entre retas
    # ------------------------------------------------------------------
    def eh_paralela(self, outra, tolerancia=1e-9):
        """Indica se os vetores diretores são paralelos (inclui coincidentes)."""
        self._validar_reta(outra)
        self._validar_tolerancia(tolerancia)
        produto_vetorial = self.vetor_diretor.produto_vetorial(outra.vetor_diretor)
        limite = tolerancia * self.vetor_diretor.modulo() * outra.vetor_diretor.modulo()
        return produto_vetorial.modulo() <= limite

    def eh_ortogonal(self, outra, tolerancia=1e-9):
        """Indica se os vetores diretores são ortogonais."""
        self._validar_reta(outra)
        self._validar_tolerancia(tolerancia)
        produto_escalar = self.vetor_diretor.produto_escalar(outra.vetor_diretor)
        limite = tolerancia * self.vetor_diretor.modulo() * outra.vetor_diretor.modulo()
        return abs(produto_escalar) <= limite

    def angulo_com(self, outra):
        """Menor ângulo (em graus, entre 0° e 90°) entre duas retas."""
        self._validar_reta(outra)
        produto_vetorial = self.vetor_diretor.produto_vetorial(outra.vetor_diretor)
        seno_relativo = produto_vetorial.modulo()
        produto_escalar = abs(self.vetor_diretor.produto_escalar(outra.vetor_diretor))
        return degrees(atan2(seno_relativo, produto_escalar))

    def posicao_relativa(self, outra, tolerancia=1e-9):
        """Retorna 'coincidentes', 'paralelas', 'concorrentes' ou 'reversas'."""
        self._validar_reta(outra)
        from backend.analisador import Analisador

        return Analisador._obter_relacao(self, outra, tolerancia)

    def distancia_reta(self, outra, tolerancia=1e-9):
        """Distância entre duas retas (0 se concorrentes ou coincidentes)."""
        self._validar_reta(outra)
        self._validar_tolerancia(tolerancia)
        if self.eh_paralela(outra, tolerancia):
            return self.distancia_ponto(outra.ponto_inicial)

        deslocamento = outra.ponto_inicial.subtrair(self.ponto_inicial)
        normal = self.vetor_diretor.produto_vetorial(outra.vetor_diretor)
        return abs(deslocamento.produto_escalar(normal)) / normal.modulo()

    def ponto_intersecao(self, outra, tolerancia=1e-9):
        """Retorna o ponto de interseção (Vetor) se as retas forem concorrentes.

        Retorna None quando não há um único ponto em comum
        (paralelas, coincidentes ou reversas).
        """
        self._validar_reta(outra)
        from backend.analisador import Analisador

        return Analisador.calcular_intersecao(self, outra, tolerancia)

    def __repr__(self):
        return f"RetaR3({self.ponto_inicial!r}, {self.obter_ponto(1)!r})"
