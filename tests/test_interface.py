import unittest

from interface.janela import JanelaPrincipal


class CampoFalso:
    def __init__(self, texto):
        self.texto = texto

    def get(self):
        return self.texto


class TestValidacaoInterface(unittest.TestCase):
    def test_le_coordenadas_com_ponto_ou_virgula_decimal(self):
        vetor = JanelaPrincipal._coordenadas(
            [CampoFalso("1,5"), CampoFalso("-2")], "ponto de teste"
        )
        self.assertEqual(vetor.coordenadas, (1.5, -2.0))

    def test_rejeita_campo_vazio_e_texto(self):
        with self.assertRaisesRegex(ValueError, "Preencha todas"):
            JanelaPrincipal._coordenadas([CampoFalso(""), CampoFalso("2")], "ponto")
        with self.assertRaisesRegex(ValueError, "deve ser numérica"):
            JanelaPrincipal._coordenadas([CampoFalso("x"), CampoFalso("2")], "ponto")

    def test_rejeita_valor_nao_finito_via_vetor(self):
        with self.assertRaisesRegex(ValueError, "finitas"):
            JanelaPrincipal._coordenadas([CampoFalso("nan"), CampoFalso("2")], "ponto")


if __name__ == "__main__":
    unittest.main()
