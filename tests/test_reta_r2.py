import unittest

from backend.reta import Reta
from backend.reta_r2 import RetaR2
from backend.vetor import Vetor


class TestRetaR2(unittest.TestCase):
    def setUp(self):
        self.reta = RetaR2(Vetor([1, 1]), Vetor([5, 3]))

    def test_construcao_e_heranca(self):
        self.assertIsInstance(self.reta, Reta)
        self.assertEqual(self.reta.vetor_diretor.coordenadas, (4, 2))
        self.assertEqual(self.reta.ponto_final.coordenadas, (5, 3))
        self.assertTrue(self.reta.ponto_pertence(Vetor([3, 2])))
        self.assertFalse(self.reta.ponto_pertence(Vetor([3, 3])))

    def test_equacoes(self):
        self.assertEqual(
            self.reta.equacao_vetorial(), "(x, y) = (1.0, 1.0) + t(4.0, 2.0)"
        )
        self.assertEqual(self.reta.equacao_parametrica(), "x = 1.0 + 4.0t\ny = 1.0 + 2.0t")
        self.assertEqual(
            self.reta.equacao_simetrica(), "(x - 1.0) / 4.0 = (y - 1.0) / 2.0"
        )
        self.assertEqual(self.reta.equacao_reduzida(), "y = 0.5x + 0.5")

    def test_retas_horizontais_e_verticais(self):
        horizontal = RetaR2(Vetor([1, 3]), Vetor([4, 3]))
        vertical = RetaR2(Vetor([2, 1]), Vetor([2, 5]))
        self.assertEqual(horizontal.equacao_simetrica(), "y = 3.0")
        self.assertEqual(horizontal.equacao_reduzida(), "y = 3.0")
        self.assertEqual(vertical.equacao_simetrica(), "x = 2.0")
        self.assertEqual(vertical.equacao_reduzida(), "x = 2.0")

    def test_entrada_invalida_e_pontos_iguais(self):
        with self.assertRaises(ValueError):
            RetaR2(Vetor([1, 2]), Vetor([1, 2]))
        with self.assertRaises(ValueError):
            RetaR2(Vetor([1, 2, 3]), Vetor([4, 5, 6]))

    def test_construtor_rejeita_sequencias_sem_vetor(self):
        with self.assertRaisesRegex(TypeError, "ponto inicial deve ser um objeto Vetor"):
            RetaR2([0, 0], Vetor([1, 1]))
        with self.assertRaisesRegex(TypeError, "ponto final deve ser um objeto Vetor"):
            RetaR2(Vetor([0, 0]), (1, 1))


if __name__ == "__main__":
    unittest.main()
