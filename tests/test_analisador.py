import unittest

from backend.analisador import Analisador
from backend.reta import Reta
from backend.vetor import Vetor


def criar_reta(ponto, direcao):
    return Reta(Vetor(ponto), Vetor(direcao))


class TestAnalisador(unittest.TestCase):
    def test_retas_intersectantes_r2(self):
        reta1 = criar_reta((0, 0), (1, 1))
        reta2 = criar_reta((0, 2), (1, -1))
        resultado = Analisador.analisar(reta1, reta2)

        self.assertEqual(resultado["relacao"], "concorrentes")
        self.assertEqual(resultado["ponto_intersecao"].coordenadas, (1.0, 1.0))
        self.assertFalse(resultado["sao_paralelas"])
        self.assertFalse(resultado["sao_coincidentes"])
        self.assertFalse(resultado["sao_reversas"])
        self.assertEqual(resultado["mensagem"], "As retas se intersectam no ponto (1, 1).")

    def test_paralelas_e_coincidentes_r2(self):
        reta = criar_reta((0, 0), (1, 0))
        paralela = criar_reta((0, 2), (1, 0))
        coincidente = criar_reta((3, 0), (-2, 0))

        self.assertTrue(Analisador.verificar_paralelismo(reta, paralela))
        self.assertFalse(Analisador.verificar_coincidencia(reta, paralela))
        self.assertEqual(Analisador.analisar(reta, paralela)["relacao"], "paralelas")
        self.assertTrue(Analisador.verificar_coincidencia(reta, coincidente))
        self.assertIsNone(Analisador.calcular_intersecao(reta, coincidente))

    def test_reversas_e_intersecao_r3(self):
        eixo_x = criar_reta((0, 0, 0), (1, 0, 0))
        reta_secante = criar_reta((1, -1, 0), (0, 1, 0))
        reta_reversa = criar_reta((0, 1, 1), (0, 1, 0))

        intersecao = Analisador.calcular_intersecao(eixo_x, reta_secante)
        self.assertEqual(intersecao.coordenadas, (1.0, 0.0, 0.0))
        self.assertTrue(Analisador.verificar_reversas(eixo_x, reta_reversa))
        self.assertEqual(Analisador.analisar(eixo_x, reta_reversa)["relacao"], "reversas")
        self.assertIsNone(Analisador.calcular_intersecao(eixo_x, reta_reversa))

    def test_validacoes(self):
        reta2 = criar_reta((0, 0), (1, 0))
        reta3 = criar_reta((0, 0, 0), (1, 0, 0))
        with self.assertRaises(TypeError):
            Analisador.analisar("reta", reta2)
        with self.assertRaises(ValueError):
            Analisador.analisar(reta2, reta3)
        with self.assertRaises(ValueError):
            Analisador.analisar(reta2, reta2, -1)


if __name__ == "__main__":
    unittest.main()
