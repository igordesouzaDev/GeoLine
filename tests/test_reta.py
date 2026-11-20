import unittest

from backend.reta import Reta
from backend.vetor import Vetor


class TestReta(unittest.TestCase):
    def test_construcao_e_obter_pontos(self):
        reta = Reta(Vetor([2, 3]), Vetor([4, 2]))
        self.assertEqual(reta.dimensao, 2)
        self.assertEqual(reta.obter_ponto(0).coordenadas, (2, 3))
        self.assertEqual(reta.obter_ponto(2).coordenadas, (10, 7))
        self.assertEqual(reta.obter_ponto(-1).coordenadas, (-2, 1))

    def test_equacoes_e_pertencimento(self):
        reta = Reta(Vetor([1, 2, 3]), Vetor([3, 4, 5]))
        self.assertEqual(
            reta.equacao_vetorial(), "(x, y, z) = (1, 2, 3) + t(3, 4, 5)"
        )
        self.assertEqual(
            reta.equacao_parametrica(),
            "x = 1 + 3t\ny = 2 + 4t\nz = 3 + 5t",
        )
        self.assertTrue(reta.ponto_pertence(Vetor([4, 6, 8])))
        self.assertFalse(reta.ponto_pertence(Vetor([4, 6, 9])))

    def test_validacoes(self):
        with self.assertRaises(TypeError):
            Reta([1, 2], Vetor([1, 1]))
        with self.assertRaises(ValueError):
            Reta(Vetor([1, 2]), Vetor([1, 2, 3]))
        with self.assertRaises(ValueError):
            Reta(Vetor([1, 2]), Vetor([0, 0]))
        with self.assertRaises(TypeError):
            Reta(Vetor([1, 2]), Vetor([1, 1])).obter_ponto("1")


if __name__ == "__main__":
    unittest.main()
