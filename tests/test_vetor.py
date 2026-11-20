import unittest

from backend.vetor import Vetor


class TestVetor(unittest.TestCase):
    def test_construcao_e_dimensao(self):
        self.assertEqual(Vetor([2, 3]).coordenadas, (2, 3))
        self.assertEqual(Vetor([1, 2, 3]).dimensao, 3)

    def test_soma_subtracao_e_escalar(self):
        vetor = Vetor([2, 3])
        outro = Vetor([1, 4])
        self.assertEqual(vetor.somar(outro).coordenadas, (3, 7))
        self.assertEqual(vetor.subtrair(outro).coordenadas, (1, -1))
        self.assertEqual(vetor.multiplicar_escalar(2).coordenadas, (4, 6))

    def test_modulo_e_produtos(self):
        self.assertEqual(Vetor([3, 4]).modulo(), 5.0)
        self.assertEqual(Vetor([1, 2, 3]).produto_escalar(Vetor([4, 5, 6])), 32)
        self.assertEqual(
            Vetor([1, 2, 3]).produto_vetorial(Vetor([4, 5, 6])).coordenadas,
            (-3, 6, -3),
        )

    def test_proporcionalidade(self):
        self.assertTrue(Vetor([1, 2]).sao_proporcionais(Vetor([2, 4])))
        self.assertFalse(Vetor([1, 2]).sao_proporcionais(Vetor([2, 5])))

    def test_validacoes(self):
        with self.assertRaises(ValueError):
            Vetor([])
        with self.assertRaises(ValueError):
            Vetor([1])
        with self.assertRaises(ValueError):
            Vetor([1, 2, 3, 4])
        with self.assertRaises(TypeError):
            Vetor([1, "2"])
        with self.assertRaises(ValueError):
            vetor = Vetor([1, 2])
            vetor.somar(Vetor([1, 2, 3]))
        with self.assertRaises(ValueError):
            Vetor([1, 2]).produto_vetorial(Vetor([3, 4]))


if __name__ == "__main__":
    unittest.main()
