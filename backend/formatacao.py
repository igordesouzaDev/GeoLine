"""Funções compartilhadas para formatar valores numéricos do backend."""


def formatar_numero(valor):
    """Formata inteiros com ``.0`` e preserva a representação decimal.

    Para valores float não inteiros, ``str`` usa a representação curta que
    permite recuperar o mesmo float, evitando arredondamentos de exibição.
    Zeros com sinal negativo são normalizados para ``0.0``.
    """
    if isinstance(valor, float) and valor == 0:
        return "0.0"
    if isinstance(valor, int):
        return f"{valor}.0"
    if isinstance(valor, float) and valor.is_integer():
        return f"{valor:.0f}.0"
    return str(valor)


def formatar_numerador(simbolo, valor):
    """Formata a diferença entre uma variável e uma coordenada."""
    if valor == 0:
        return simbolo
    operador = "-" if valor > 0 else "+"
    return f"({simbolo} {operador} {formatar_numero(abs(valor))})"
