import unittest

from backend.reta_r2 import RetaR2
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor
from visualizacao.graficos import Graficos


class TestGraficos(unittest.TestCase):
    def test_graficos_r2_reta_unica_e_duas(self):
        reta1 = RetaR2(Vetor([0, 0]), Vetor([1, 2]))
        reta2 = RetaR2(Vetor([1, 0]), Vetor([2, -1]))

        figura, eixo = Graficos.plotar_reta_r2(reta1)
        self.assertEqual(len(eixo.lines), 3)  # reta e eixos de referência
        self.assertEqual(len(eixo.collections), 2)
        figura.clear()

        figura, eixo = Graficos.plotar_duas_retas_r2(reta1, reta2)
        self.assertEqual(len(eixo.lines), 4)
        self.assertEqual(len(eixo.collections), 4)
        self.assertEqual(len(eixo.get_legend().get_texts()), 6)
        figura.clear()

    def test_graficos_r3_sao_linhas(self):
        reta1 = RetaR3(Vetor([0, 0, 0]), Vetor([1, 2, 3]))
        reta2 = RetaR3(Vetor([1, 0, 0]), Vetor([2, -1, 1]))

        figura, eixo = Graficos.plotar_reta_r3(reta1)
        self.assertEqual(len(eixo.lines), 1)
        self.assertEqual(len(eixo.collections), 2)
        figura.clear()

        figura, eixo = Graficos.plotar_duas_retas_r3(reta1, reta2)
        self.assertEqual(len(eixo.lines), 2)
        self.assertEqual(len(eixo.collections), 4)
        self.assertEqual(len(eixo.get_legend().get_texts()), 6)
        figura.clear()

    def test_graficos_validam_tipo_e_dimensao(self):
        reta2 = RetaR2(Vetor([0, 0]), Vetor([1, 1]))
        reta3 = RetaR3(Vetor([0, 0, 0]), Vetor([1, 1, 1]))
        with self.assertRaises(TypeError):
            Graficos.plotar_reta_r2("reta")
        with self.assertRaises(ValueError):
            Graficos.plotar_reta_r2(reta3)
        with self.assertRaises(ValueError):
            Graficos.plotar_duas_retas_r3(reta3, reta2)


if __name__ == "__main__":
    unittest.main()
