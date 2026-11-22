import unittest
from matplotlib.backends.backend_agg import FigureCanvasAgg

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
        self.assertEqual(len(eixo.get_legend().get_texts()), 2)
        self.assertEqual(len(eixo.texts), 4)
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
        self.assertEqual(len(eixo.get_legend().get_texts()), 2)
        self.assertEqual(len(eixo.texts), 4)
        FigureCanvasAgg(figura).draw()
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

    def test_intervalo_contem_t_zero_e_t_um_em_r2_e_r3(self):
        retas = (
            RetaR2(Vetor([-3, 2]), Vetor([-2.999, 1.998])),
            RetaR2(Vetor([0, 0]), Vetor([1000, -2000])),
            RetaR3(Vetor([-4, 2, -1]), Vetor([-3.999, 1.998, -0.997])),
            RetaR3(Vetor([0, 0, 0]), Vetor([1000, -2000, 3000])),
        )
        for reta in retas:
            with self.subTest(reta=reta):
                self.assertGreaterEqual(Graficos._intervalo(reta), 1.0)

    def test_segmento_2d_desenhado_alcanca_o_ponto_final(self):
        reta = RetaR2(Vetor([0, 0]), Vetor([1000, -2000]))
        figura, eixo = Graficos.plotar_reta_r2(reta)
        xs, ys = eixo.lines[0].get_data()
        for ponto in (reta.ponto_inicial.coordenadas, reta.ponto_final.coordenadas):
            self.assertTrue(
                min(xs) <= ponto[0] <= max(xs)
                and min(ys) <= ponto[1] <= max(ys)
            )
        figura.clear()

    def test_segmento_3d_com_direcao_grande_alcanca_os_dois_pontos(self):
        reta = RetaR3(Vetor([-5, 3, -2]), Vetor([1000, -2000, 3000]))
        figura, eixo = Graficos.plotar_reta_r3(reta)
        xs, ys, zs = eixo.lines[0].get_data_3d()
        ponto = reta.ponto_inicial.coordenadas
        direcao = reta.vetor_diretor.coordenadas
        indices = [i for i, valor in enumerate(direcao) if valor != 0]
        parametros = [
            (coordenada - ponto[indice]) / direcao[indice]
            for indice, coordenadas in zip(indices, (xs, ys, zs))
            for coordenada in coordenadas
        ]
        self.assertLessEqual(min(parametros), 0.0)
        self.assertGreaterEqual(max(parametros), 1.0)
        figura.clear()


if __name__ == "__main__":
    unittest.main()
