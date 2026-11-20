"""Testes unitários de RetaR3 (compatível com unittest e pytest).

Execute na raiz do projeto:
    python -m unittest tests.test_reta_r3 -v
    pytest tests/test_reta_r3.py
"""
import sys
import unittest
from pathlib import Path

# Permite rodar este arquivo direto (F5 no VS Code): coloca a raiz do projeto no path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.reta_r3 import RetaR3  # noqa: E402
from backend.vetor import Vetor


def V(*coords):
    """Cria um Vetor. Ajuste aqui se o construtor de Vetor tiver outra assinatura."""
    try:
        return Vetor(*coords)
    except TypeError:
        return Vetor(list(coords))


def R(ponto, direcao):
    return RetaR3.por_ponto_e_direcao(ponto, direcao)


def coords(vetor):
    return tuple(vetor.coordenadas)


class TestEquacoes(unittest.TestCase):
    def test_sem_componentes_nulas(self):
        r = R(V(1, 2, 3), V(2, 3, 4))
        self.assertEqual(r.equacao_simetrica(), "(x - 1.0)/2.0 = (y - 2.0)/3.0 = (z - 3.0)/4.0")
        self.assertIsInstance(r.equacao_vetorial(), str)
        self.assertIsInstance(r.equacao_parametrica(), str)

    def test_uma_componente_nula(self):
        r = R(V(1, 2, 3), V(2, 0, 4))
        self.assertEqual(r.equacao_simetrica(), "(x - 1.0)/2.0 = (z - 3.0)/4.0, y = 2.0")

    def test_duas_componentes_nulas(self):
        r = R(V(1, 2, 3), V(0, 0, 5))
        self.assertEqual(r.equacao_simetrica(), "(z - 3.0)/5.0, x = 1.0, y = 2.0")

    def test_duas_componentes_nulas_outros_eixos(self):
        self.assertEqual(
            R(V(1, 2, 3), V(4, 0, 0)).equacao_simetrica(), "(x - 1.0)/4.0, y = 2.0, z = 3.0"
        )
        self.assertEqual(
            R(V(1, 2, 3), V(0, 4, 0)).equacao_simetrica(), "(y - 2.0)/4.0, x = 1.0, z = 3.0"
        )

    def test_sinal_negativo_no_ponto_inicial(self):
        r = R(V(1, -2, 3), V(2, 3, 4))
        self.assertEqual(r.equacao_simetrica(), "(x - 1.0)/2.0 = (y + 2.0)/3.0 = (z - 3.0)/4.0")
        self.assertNotIn("- -", r.equacao_simetrica())

    def test_ponto_inicial_com_zero(self):
        r = R(V(0, 0, 0), V(1, 2, 3))
        self.assertEqual(r.equacao_simetrica(), "x/1.0 = y/2.0 = z/3.0")

    def test_componente_negativa_no_vetor_diretor(self):
        r = R(V(1, 2, 3), V(-2, 3, 4))
        self.assertEqual(r.equacao_simetrica(), "(x - 1.0)/-2.0 = (y - 2.0)/3.0 = (z - 3.0)/4.0")

    def test_construtor_por_dois_pontos_do_contrato(self):
        r = RetaR3(V(1, 2, 3), V(3, 2, 7))
        self.assertEqual(coords(r.ponto_inicial), (1, 2, 3))
        self.assertEqual(coords(r.vetor_diretor), (2, 0, 4))
        self.assertEqual(repr(r), "RetaR3(Vetor((1, 2, 3)), Vetor((3, 2, 7)))")

    def test_por_dois_pontos(self):
        r = RetaR3.por_dois_pontos(V(1, 2, 3), V(3, 2, 7))
        self.assertEqual(coords(r.vetor_diretor), (2, 0, 4))
        self.assertEqual(coords(r.ponto_inicial), (1, 2, 3))


class TestPertencimento(unittest.TestCase):
    def setUp(self):
        self.r = R(V(1, 2, 3), V(2, 3, 4))

    def test_pertence_t_zero(self):
        self.assertTrue(self.r.ponto_pertence(V(1, 2, 3)))

    def test_pertence_t_positivo(self):
        self.assertTrue(self.r.ponto_pertence(V(3, 5, 7)))  # t = 1

    def test_pertence_t_negativo(self):
        self.assertTrue(self.r.ponto_pertence(V(-1, -1, -1)))  # t = -1

    def test_pertence_t_fracionario(self):
        self.assertTrue(self.r.ponto_pertence(V(2, 3.5, 5)))  # t = 0.5

    def test_nao_pertence(self):
        self.assertFalse(self.r.ponto_pertence(V(3, 5, 8)))

    def test_diferenca_dentro_da_tolerancia(self):
        self.assertTrue(self.r.ponto_pertence(V(3 + 1e-12, 5, 7)))

    def test_diferenca_fora_da_tolerancia(self):
        self.assertFalse(self.r.ponto_pertence(V(3 + 1e-3, 5, 7)))

    def test_pertencimento_com_componente_nula(self):
        r = R(V(1, 2, 3), V(2, 0, 4))
        self.assertTrue(r.ponto_pertence(V(3, 2, 7)))
        self.assertFalse(r.ponto_pertence(V(3, 2.5, 7)))


class TestRelacoesGeometricas(unittest.TestCase):
    def test_coincidentes(self):
        r1 = R(V(0, 0, 0), V(1, 2, 3))
        r2 = R(V(2, 4, 6), V(-2, -4, -6))
        self.assertEqual(r1.posicao_relativa(r2), "coincidentes")
        self.assertTrue(r1.eh_paralela(r2))
        self.assertAlmostEqual(r1.distancia_reta(r2), 0.0)

    def test_paralelas_distintas(self):
        r1 = R(V(0, 0, 0), V(0, 0, 1))
        r2 = R(V(3, 4, 0), V(0, 0, 2))
        self.assertEqual(r1.posicao_relativa(r2), "paralelas")
        self.assertTrue(r1.eh_paralela(r2))
        self.assertAlmostEqual(r1.distancia_reta(r2), 5.0)
        self.assertIsNone(r1.ponto_intersecao(r2))

    def test_concorrentes(self):
        r1 = R(V(0, 0, 0), V(1, 1, 0))
        r2 = R(V(2, 0, 0), V(-1, 1, 0))
        self.assertEqual(r1.posicao_relativa(r2), "concorrentes")
        self.assertAlmostEqual(r1.distancia_reta(r2), 0.0)
        self.assertEqual(
            tuple(round(c, 9) for c in coords(r1.ponto_intersecao(r2))), (1, 1, 0)
        )

    def test_concorrentes_no_espaco(self):
        r1 = R(V(1, 2, 3), V(1, 0, 1))
        r2 = R(V(2, 0, 4), V(0, 1, 0))  # ambas passam por (2, 2, 4)
        self.assertEqual(r1.posicao_relativa(r2), "concorrentes")
        self.assertEqual(
            tuple(round(c, 9) for c in coords(r1.ponto_intersecao(r2))), (2, 2, 4)
        )

    def test_reversas(self):
        r1 = R(V(0, 0, 0), V(1, 0, 0))
        r2 = R(V(0, 0, 1), V(0, 1, 0))
        self.assertEqual(r1.posicao_relativa(r2), "reversas")
        self.assertIsNone(r1.ponto_intersecao(r2))
        self.assertAlmostEqual(r1.distancia_reta(r2), 1.0)

    def test_ortogonais(self):
        r1 = R(V(0, 0, 0), V(1, 0, 0))
        r2 = R(V(0, 0, 1), V(0, 1, 0))
        self.assertTrue(r1.eh_ortogonal(r2))
        self.assertEqual(r1.angulo_com(r2), 90.0)

    def test_nao_ortogonais(self):
        r1 = R(V(0, 0, 0), V(1, 0, 0))
        r2 = R(V(0, 0, 0), V(1, 1, 0))
        self.assertFalse(r1.eh_ortogonal(r2))
        self.assertAlmostEqual(r1.angulo_com(r2), 45.0)

    def test_angulo_entre_paralelas_eh_zero(self):
        r1 = R(V(0, 0, 0), V(1, 2, 3))
        r2 = R(V(5, 5, 5), V(-2, -4, -6))
        self.assertEqual(r1.angulo_com(r2), 0.0)

    def test_distancia_ponto(self):
        r = R(V(0, 0, 0), V(0, 0, 1))
        self.assertAlmostEqual(r.distancia_ponto(V(3, 4, 7)), 5.0)
        self.assertAlmostEqual(r.distancia_ponto(V(0, 0, 9)), 0.0)


class TestEntradasInvalidas(unittest.TestCase):
    def test_dimensao_2(self):
        with self.assertRaises(ValueError):
            R(V(1, 2), V(1, 1))

    def test_dimensao_4(self):
        with self.assertRaises(ValueError):
            R(V(1, 2, 3, 4), V(1, 1, 1, 1))

    def test_vetor_diretor_nulo(self):
        with self.assertRaises(ValueError):
            R(V(1, 2, 3), V(0, 0, 0))

    def test_por_dois_pontos_identicos(self):
        with self.assertRaises(ValueError):
            RetaR3.por_dois_pontos(V(1, 2, 3), V(1, 2, 3))
        with self.assertRaises(ValueError):
            RetaR3(V(1, 2, 3), V(1, 2, 3))

    def test_por_dois_pontos_tipo_errado(self):
        with self.assertRaises(TypeError):
            RetaR3.por_dois_pontos((1, 2, 3), (4, 5, 6))

    def test_por_dois_pontos_dimensoes_diferentes(self):
        with self.assertRaises(ValueError):
            RetaR3.por_dois_pontos(V(1, 2, 3), V(1, 2))

    def test_tipos_errados_no_construtor(self):
        with self.assertRaises(TypeError):
            RetaR3([1, 2, 3], [1, 1, 1])
        with self.assertRaises(TypeError):
            RetaR3((1, 2, 3), (1, 1, 1))

    def test_outra_reta_de_tipo_errado(self):
        r = R(V(0, 0, 0), V(1, 0, 0))
        for metodo in (r.posicao_relativa, r.eh_paralela, r.eh_ortogonal,
                       r.angulo_com, r.distancia_reta, r.ponto_intersecao):
            with self.assertRaises(TypeError):
                metodo("não é reta")

    def test_ponto_invalido_em_distancia_ponto(self):
        r = R(V(0, 0, 0), V(1, 0, 0))
        with self.assertRaises(TypeError):
            r.distancia_ponto((1, 2, 3))
        with self.assertRaises(ValueError):
            r.distancia_ponto(V(1, 2))

    def test_tolerancia_invalida(self):
        r1 = R(V(0, 0, 0), V(1, 0, 0))
        r2 = R(V(0, 0, 1), V(0, 1, 0))
        for tol in (True, "1e-9", None):
            with self.assertRaises(TypeError):
                r1.posicao_relativa(r2, tol)
        for tol in (-1e-9, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                r1.posicao_relativa(r2, tol)
            with self.assertRaises(ValueError):
                r1.eh_paralela(r2, tol)
            with self.assertRaises(ValueError):
                r1.eh_ortogonal(r2, tol)


if __name__ == "__main__":
    unittest.main()
