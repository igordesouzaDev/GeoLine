import unittest

from backend.formatacao import formatar_numero
from backend.reta import Reta
from backend.reta_r2 import RetaR2
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor


class TestFormatacaoNumerica(unittest.TestCase):
    def test_formatar_inteiros_decimais_negativos_e_zero(self):
        casos = (
            (2, "2.0"),
            (2.0, "2.0"),
            (0.125, "0.125"),
            (-3, "-3.0"),
            (-2.75, "-2.75"),
            (0.0, "0.0"),
            (-0.0, "0.0"),
        )
        for valor, esperado in casos:
            with self.subTest(valor=valor):
                self.assertEqual(formatar_numero(valor), esperado)

    def test_equacoes_de_reta_r2_e_r3_usam_formatacao_compartilhada(self):
        inicio_r2 = Vetor([2.0, -0.0])
        fim_r2 = Vetor([-1.0, 0.25])
        reta_r2 = RetaR2(inicio_r2, fim_r2)
        reta_base_r2 = Reta(inicio_r2, fim_r2.subtrair(inicio_r2))

        self.assertEqual(reta_r2.equacao_vetorial(), reta_base_r2.equacao_vetorial())
        self.assertEqual(reta_r2.equacao_parametrica(), reta_base_r2.equacao_parametrica())
        reta_com_coordenada_negativa = RetaR2(Vetor([-2.0, -3.0]), Vetor([1.0, 1.0]))
        self.assertEqual(
            reta_r2.equacao_parametrica(), "x = 2.0 - 3.0t\ny = 0.0 + 0.25t"
        )
        self.assertEqual(
            reta_com_coordenada_negativa.equacao_simetrica(),
            "(x + 2.0) / 3.0 = (y + 3.0) / 4.0",
        )
        self.assertEqual(
            reta_com_coordenada_negativa.equacao_simetrica(form=0),
            "(x + 2.0) / (3.0) = (y + 3.0) / (4.0)",
        )

        inicio_r3 = Vetor([2.0, -0.0, 1.5])
        fim_r3 = Vetor([-1.0, 0.25, 1.0])
        reta_r3 = RetaR3(inicio_r3, fim_r3)
        reta_base_r3 = Reta(inicio_r3, fim_r3.subtrair(inicio_r3))

        self.assertEqual(reta_r3.equacao_vetorial(), reta_base_r3.equacao_vetorial())
        self.assertEqual(reta_r3.equacao_parametrica(), reta_base_r3.equacao_parametrica())
        self.assertEqual(
            reta_r3.equacao_simetrica(),
            "(x - 2.0)/-3.0 = y/0.25 = (z - 1.5)/-0.5",
        )


class TestConstrutoresConsistentes(unittest.TestCase):
    def test_ambos_aceitam_pontos_vetor(self):
        self.assertIsInstance(RetaR2(Vetor([0, 0]), Vetor([1, 1])), RetaR2)
        self.assertIsInstance(RetaR3(Vetor([0, 0, 0]), Vetor([1, 1, 1])), RetaR3)

    def test_ambos_rejeitam_listas_tuplas_e_tipos_incorretos(self):
        argumentos_invalidos = (
            ([0, 0], Vetor([1, 1])),
            (Vetor([0, 0]), (1, 1)),
        )
        for construtor, casos in (
            (RetaR2, argumentos_invalidos),
            (RetaR3, (([0, 0, 0], Vetor([1, 1, 1])), (Vetor([0, 0, 0]), (1, 1, 1)))),
        ):
            for argumentos in casos:
                with self.subTest(construtor=construtor.__name__, argumentos=argumentos):
                    with self.assertRaises(TypeError):
                        construtor(*argumentos)

    def test_dimensoes_incompativeis_e_dimensao_indevida(self):
        with self.assertRaisesRegex(ValueError, "Os pontos devem possuir a mesma dimensão"):
            RetaR2(Vetor([0, 0]), Vetor([0, 0, 0]))
        with self.assertRaisesRegex(ValueError, "Os pontos devem possuir a mesma dimensão"):
            RetaR3(Vetor([0, 0]), Vetor([0, 0, 0]))
        with self.assertRaisesRegex(ValueError, "RetaR2.*dimensão 2"):
            RetaR2(Vetor([0, 0, 0]), Vetor([1, 1, 1]))
        with self.assertRaisesRegex(ValueError, "RetaR3.*dimensão 3"):
            RetaR3(Vetor([0, 0]), Vetor([1, 1]))

    def test_pontos_iguais_sao_rejeitados_com_mensagem_coerente(self):
        pontos_iguais = (
            (RetaR2, Vetor([1, 2]), Vetor([1, 2])),
            (RetaR3, Vetor([1, 2, 3]), Vetor([1, 2, 3])),
        )
        for construtor, inicio, fim in pontos_iguais:
            with self.subTest(construtor=construtor.__name__):
                with self.assertRaisesRegex(ValueError, "vetor diretor não pode ser nulo"):
                    construtor(inicio, fim)


class TestProdutoEscalarTipado(unittest.TestCase):
    def test_retorna_float_com_coordenadas_inteiras_e_decimais(self):
        resultados = (
            Vetor([1, 2]).produto_escalar(Vetor([3, 4])),
            Vetor([1.5, 2.0]).produto_escalar(Vetor([3.0, 4.0])),
        )
        self.assertEqual(resultados, (11.0, 12.5))
        self.assertTrue(all(type(resultado) is float for resultado in resultados))

    def test_preserva_validacao_de_tipo_e_dimensao(self):
        with self.assertRaisesRegex(ValueError, "vetores devem possuir a mesma dimensão"):
            Vetor([1, 2]).produto_escalar(Vetor([1, 2, 3]))
        with self.assertRaisesRegex(TypeError, "outro vetor deve ser um objeto Vetor"):
            Vetor([1, 2]).produto_escalar([1, 2])


class TestMensagensDeValidacao(unittest.TestCase):
    def test_tipo_de_pontos_consistente_nas_retas_especificas(self):
        for construtor, ponto_final in (
            (RetaR2, Vetor([1, 1])),
            (RetaR3, Vetor([1, 1, 1])),
        ):
            with self.subTest(construtor=construtor.__name__):
                with self.assertRaisesRegex(TypeError, "ponto inicial deve ser um objeto Vetor"):
                    construtor([0, 0], ponto_final)

    def test_mensagem_de_dimensao_do_ponto_e_operacao_vetorial(self):
        reta = Reta(Vetor([0, 0]), Vetor([1, 0]))
        with self.assertRaisesRegex(ValueError, "ponto deve possuir a mesma dimensão da reta"):
            reta.ponto_pertence(Vetor([0, 0, 0]))
        with self.assertRaisesRegex(ValueError, "vetores devem possuir a mesma dimensão"):
            Vetor([1, 2]).somar(Vetor([1, 2, 3]))

    def test_tipo_e_valor_invalido_de_escalar_usam_excecoes_corretas(self):
        with self.assertRaisesRegex(TypeError, "escalar deve ser um número real"):
            Vetor([1, 2]).multiplicar_escalar("2")
        with self.assertRaisesRegex(ValueError, "escalar deve ser finito"):
            Vetor([1, 2]).multiplicar_escalar(float("inf"))


if __name__ == "__main__":
    unittest.main()
