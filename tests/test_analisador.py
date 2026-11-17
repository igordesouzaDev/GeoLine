import unittest

from backend.analisador import Analisador
from backend.reta_r2 import RetaR2
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor


class TestAnalisador(unittest.TestCase):
    def test_retas_intersectantes_no_r2(self):
        reta1 = RetaR2(Vetor([0, 0]), Vetor([1, 1]))
        reta2 = RetaR2(Vetor([0, 2]), Vetor([1, 1]))
        resultado = Analisador.analisar(reta1, reta2)
        self.assertEqual(resultado["relacao"], "concorrentes")
        self.assertTrue(resultado["ponto_intersecao"].coordenadas == (1.0, 1.0))
        self.assertFalse(resultado["sao_paralelas"])
        self.assertIn("(1, 1)", resultado["mensagem"])

    def test_paralelas_e_coincidentes_no_r2(self):
        reta1 = RetaR2(Vetor([0, 0]), Vetor([1, 0]))
        paralela = RetaR2(Vetor([0, 2]), Vetor([1, 2]))
        coincidente = RetaR2(Vetor([2, 0]), Vetor([4, 0]))

        self.assertTrue(Analisador.verificar_paralelismo(reta1, paralela))
        self.assertFalse(Analisador.verificar_coincidencia(reta1, paralela))
        self.assertEqual(Analisador.analisar(reta1, paralela)["relacao"], "paralelas")
        self.assertTrue(Analisador.verificar_coincidencia(reta1, coincidente))
        self.assertIsNone(Analisador.calcular_intersecao(reta1, coincidente))

    def test_intersecao_e_reversas_no_r3(self):
        eixo_x = RetaR3(Vetor([0, 0, 0]), Vetor([1, 0, 0]))
        cruzada = RetaR3(Vetor([1, -1, 0]), Vetor([1, 0, 0]))
        reversa = RetaR3(Vetor([0, 1, 1]), Vetor([0, 2, 1]))

        resultado = Analisador.analisar(eixo_x, cruzada)
        self.assertEqual(resultado["relacao"], "concorrentes")
        self.assertEqual(resultado["ponto_intersecao"].coordenadas, (1.0, 0.0, 0.0))
        self.assertTrue(Analisador.verificar_reversas(eixo_x, reversa))
        self.assertEqual(Analisador.analisar(eixo_x, reversa)["relacao"], "reversas")
        self.assertIsNone(Analisador.calcular_intersecao(eixo_x, reversa))

    def test_retorno_e_validacoes(self):
        reta2 = RetaR2(Vetor([0, 0]), Vetor([1, 0]))
        reta3 = RetaR3(Vetor([0, 0, 0]), Vetor([1, 0, 0]))
        resultado = Analisador.analisar(reta2, RetaR2(Vetor([0, 1]), Vetor([1, 1])))

        self.assertEqual(
            set(resultado),
            {
                "relacao", "ponto_intersecao", "sao_paralelas",
                "sao_coincidentes", "sao_reversas", "mensagem",
            },
        )
        self.assertFalse(Analisador.verificar_reversas(reta2, reta2))
        with self.assertRaises(ValueError):
            Analisador.analisar(reta2, reta3)
        with self.assertRaises(TypeError):
            Analisador.analisar("reta", reta2)


if __name__ == "__main__":
    unittest.main()
