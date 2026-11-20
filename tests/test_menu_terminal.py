import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from scripts import menu_terminal


class TestMenuTerminal(unittest.TestCase):
    def executar_com_entradas(self, funcao, entradas):
        saida = StringIO()
        with patch("builtins.input", side_effect=entradas), redirect_stdout(saida):
            funcao()
        return saida.getvalue()

    def test_operacoes_de_vetores(self):
        casos = (
            (["soma", "2", "1, 2", "3, 4"], "Soma: Vetor((4.0, 6.0))"),
            (["subtração", "2", "5, 4", "2, 1"], "Subtração: Vetor((3.0, 3.0))"),
            (["escalar", "2", "2, 3", "3"], "Vetor((6.0, 9.0))"),
            (["módulo", "2", "3, 4"], "Módulo: 5"),
            (["escalar-produto", "2", "1, 2", "3, 4"], "Produto escalar: 11"),
            (["vetorial", "3", "1, 0, 0", "0, 1, 0"], "Vetor((0.0, 0.0, 1.0))"),
            (["proporcionalidade", "2", "1, 2", "2, 4"], "São proporcionais? True"),
        )
        for entradas, esperado in casos:
            with self.subTest(operacao=entradas[0]):
                saida = self.executar_com_entradas(menu_terminal.testar_vetores, entradas)
                self.assertIn(esperado, saida)

    def test_produto_vetorial_no_r2_retorna_mensagem(self):
        saida = self.executar_com_entradas(
            menu_terminal.main,
            ["1", "vetorial", "2", "1, 0", "0, 1", "0"],
        )
        self.assertIn("apenas para vetores do R³", saida)
        self.assertIn("GeoLine encerrado.", saida)

    def test_construir_reta_r2(self):
        saida = self.executar_com_entradas(
            menu_terminal.construir_reta_r2, ["1, 2", "3, 4"]
        )
        self.assertIn("Ponto inicial: Vetor((1.0, 2.0))", saida)
        self.assertIn("Vetor diretor: Vetor((2.0, 2.0))", saida)
        self.assertIn("Equação reduzida:", saida)

    def test_construir_reta_r3(self):
        saida = self.executar_com_entradas(
            menu_terminal.construir_reta_r3, ["1, 2, 3", "4, 6, 8"]
        )
        self.assertIn("Vetor diretor: Vetor((3.0, 4.0, 5.0))", saida)
        self.assertIn("Equação simétrica:", saida)

    def test_analisar_retas_r2(self):
        saida = self.executar_com_entradas(
            menu_terminal.analisar_retas_r2,
            ["0, 0", "2, 0", "1, -1", "1, 1"],
        )
        self.assertIn("Relação: concorrentes", saida)
        self.assertIn("Ponto de interseção: Vetor((1.0, 0.0))", saida)
        self.assertIn("Concorrentes: True", saida)

    def test_analisar_retas_r3(self):
        saida = self.executar_com_entradas(
            menu_terminal.analisar_retas_r3,
            ["0, 0, 0", "1, 0, 0", "0, 1, 1", "0, 2, 1"],
        )
        self.assertIn("Relação: reversas", saida)
        self.assertIn("Reversas: True", saida)
        self.assertIn("Ponto de interseção: None", saida)

    def test_entradas_invalidas_e_retorno_ao_menu(self):
        saida = self.executar_com_entradas(
            menu_terminal.main,
            ["invalida", "1", "módulo", "2", "1, texto", "0"],
        )
        self.assertIn("Opção inválida", saida)
        self.assertIn("Digite somente números", saida)
        self.assertGreaterEqual(saida.count("MENU DE TESTES MATEMÁTICOS"), 3)
        self.assertIn("GeoLine encerrado.", saida)

    def test_dimensao_quantidade_pontos_iguais_e_escalar_invalidos(self):
        with self.assertRaisesRegex(ValueError, "dimensão deve ser 2 ou 3"):
            self.executar_com_entradas(menu_terminal.ler_vetor, ["4"])

        with self.assertRaisesRegex(ValueError, "exatamente 2 coordenadas"):
            self.executar_com_entradas(menu_terminal.ler_vetor, ["2", "1, 2, 3"])

        with self.assertRaises(ValueError):
            self.executar_com_entradas(
                menu_terminal.construir_reta_r2, ["1, 1", "1, 1"]
            )

        with self.assertRaisesRegex(ValueError, "número válido"):
            self.executar_com_entradas(
                menu_terminal.testar_vetores, ["escalar", "2", "1, 2", "x"]
            )

    def test_opcao_sair_e_eof(self):
        saida = self.executar_com_entradas(menu_terminal.main, ["0"])
        self.assertIn("GeoLine encerrado.", saida)

        saida = self.executar_com_entradas(menu_terminal.main, [EOFError()])
        self.assertIn("Entrada encerrada", saida)


if __name__ == "__main__":
    unittest.main()
