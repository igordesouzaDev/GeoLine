import unittest

from backend.reta import Reta
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor


class TestRetaR3(unittest.TestCase):
    def setUp(self):
        self.reta = RetaR3(Vetor([1, 2, 3]), Vetor([4, 6, 8]))

    def test_construcao_heranca_e_pontos(self):
        self.assertIsInstance(self.reta, Reta)
        self.assertEqual(self.reta.vetor_diretor.coordenadas, (3, 4, 5))
        self.assertEqual(self.reta.obter_ponto(0).coordenadas, (1, 2, 3))
        self.assertEqual(self.reta.obter_ponto(1).coordenadas, (4, 6, 8))
        self.assertTrue(self.reta.ponto_pertence(Vetor([7, 10, 13])))
        self.assertFalse(self.reta.ponto_pertence(Vetor([7, 10, 14])))

    def test_equacoes_e_componentes_nulas(self):
        self.assertEqual(
            self.reta.equacao_vetorial(), "(x, y, z) = (1, 2, 3) + t(3, 4, 5)"
        )
        self.assertEqual(
            self.reta.equacao_parametrica(),
            "x = 1 + 3t\ny = 2 + 4t\nz = 3 + 5t",
        )

        eixo = RetaR3(Vetor([1, 2, 3]), Vetor([1, 3, 4]))
        self.assertEqual(
            eixo.equacao_simetrica(), "(y - 2) / 1 = (z - 3) / 1, x = 1"
        )

        com_uma_componente_nula = RetaR3(Vetor([1, 2, 3]), Vetor([2, 4, 3]))
        self.assertEqual(
            com_uma_componente_nula.equacao_simetrica(),
            "(x - 1) / 1 = (y - 2) / 2, z = 3",
        )

    def test_geometria_adicional_preservada(self):
        reta_x = RetaR3(Vetor([0, 0, 0]), Vetor([1, 0, 0]))
        reta_y = RetaR3(Vetor([0, 1, 0]), Vetor([0, 2, 0]))
        reversa = RetaR3(Vetor([0, 1, 1]), Vetor([0, 2, 1]))
        self.assertAlmostEqual(reta_x.distancia_ponto(Vetor([0, 1, 0])), 1.0)
        self.assertAlmostEqual(reta_x.angulo_com(reta_y), 90.0)
        self.assertEqual(reta_x.posicao_relativa(reta_y), "concorrentes")
        self.assertEqual(reta_x.posicao_relativa(reversa), "reversas")
        self.assertAlmostEqual(reta_x.distancia_reta(reversa), 1.0)

    def test_entradas_invalidas(self):
        with self.assertRaises(TypeError):
            RetaR3([0, 0, 0], Vetor([1, 1, 1]))
        with self.assertRaises(ValueError):
            RetaR3(Vetor([0, 0]), Vetor([1, 1]))
        with self.assertRaises(ValueError):
            RetaR3(Vetor([1, 2, 3]), Vetor([1, 2, 3]))


if __name__ == "__main__":
    unittest.main()
