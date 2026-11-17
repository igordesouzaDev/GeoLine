import unittest

from backend.reta import Reta
from backend.reta_r2 import RetaR2
from backend.vetor import Vetor


class TestRetaR2(unittest.TestCase):
    def setUp(self):
        self.reta = RetaR2(Vetor([1, 1]), Vetor([5, 3]))

    def test_construcao_heranca_e_pontos(self):
        self.assertIsInstance(self.reta, Reta)
        self.assertEqual(self.reta.vetor_diretor.coordenadas, (4, 2))
        self.assertEqual(self.reta.obter_ponto(0).coordenadas, (1, 1))
        self.assertEqual(self.reta.obter_ponto(1).coordenadas, (5, 3))
        self.assertTrue(self.reta.ponto_pertence(Vetor([3, 2])))
        self.assertFalse(self.reta.ponto_pertence(Vetor([3, 3])))

    def test_equacoes(self):
        self.assertEqual(
            self.reta.equacao_vetorial(), "(x, y) = (1, 1) + t(4, 2)"
        )
        self.assertEqual(self.reta.equacao_parametrica(), "x = 1 + 4t\ny = 1 + 2t")
        self.assertEqual(
            self.reta.equacao_simetrica(), "(x - 1) / 4 = (y - 1) / 2"
        )
        self.assertEqual(self.reta.equacao_reduzida(), "y = 0.5x + 0.5")

    def test_retas_horizontais_e_verticais(self):
        horizontal = RetaR2(Vetor([1, 3]), Vetor([4, 3]))
        vertical = RetaR2(Vetor([2, 1]), Vetor([2, 5]))
        self.assertEqual(horizontal.equacao_simetrica(), "y = 3")
        self.assertEqual(horizontal.equacao_reduzida(), "y = 3")
        self.assertEqual(vertical.equacao_simetrica(), "x = 2")
        with self.assertRaises(ValueError):
            vertical.equacao_reduzida()

    def test_entradas_invalidas(self):
        with self.assertRaises(TypeError):
            RetaR2((0, 0), Vetor([1, 1]))
        with self.assertRaises(ValueError):
            RetaR2(Vetor([0, 0, 0]), Vetor([1, 1, 1]))
        with self.assertRaises(ValueError):
            RetaR2(Vetor([1, 2]), Vetor([1, 2]))


if __name__ == "__main__":
    unittest.main()
