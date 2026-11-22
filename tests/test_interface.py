import unittest
from unittest import mock

from backend.reta_r2 import RetaR2
from backend.reta_r3 import RetaR3
from backend.vetor import Vetor
from interface.janela import JanelaPrincipal, ttk


class CampoFalso:
    def __init__(self, texto):
        self.texto = texto

    def get(self):
        return self.texto


class VariavelFalsa:
    def __init__(self, valor):
        self.valor = valor

    def get(self):
        return self.valor

    def set(self, valor):
        self.valor = valor


class WidgetFalso:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.children = []
        self.destroyed = False
        if master is not None and hasattr(master, "children"):
            master.children.append(self)

    def grid(self, **kwargs):
        pass

    def pack(self, **kwargs):
        pass

    def columnconfigure(self, *args, **kwargs):
        pass

    def winfo_children(self):
        return list(self.children)

    def winfo_exists(self):
        return not self.destroyed

    def winfo_y(self):
        return 420

    def destroy(self):
        self.destroyed = True
        if self.master is not None and hasattr(self.master, "children"):
            if self in self.master.children:
                self.master.children.remove(self)


class FiguraFalsa:
    def __init__(self):
        self.clear = mock.Mock()


class CanvasRolagemFalso:
    def __init__(self):
        self.y_movido = None
        self.unidades_roladas = []

    def update_idletasks(self):
        pass

    def bbox(self, _item):
        return (0, 0, 600, 900)

    def yview_moveto(self, valor):
        self.y_movido = valor

    def yview_scroll(self, unidades, _tipo):
        self.unidades_roladas.append(unidades)


class JanelaFalsa:
    def after_idle(self, callback):
        callback()


class CanvasMatplotlibFalso:
    def __init__(self, figura, master):
        self.figura = figura
        self.widget = WidgetFalso(master)

    def draw(self):
        pass

    def get_tk_widget(self):
        return self.widget


class BarraMatplotlibFalsa(WidgetFalso):
    def __init__(self, _canvas, master, **kwargs):
        super().__init__(master, **kwargs)

    def update(self):
        pass


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


class TestEstadoDaInterface(unittest.TestCase):
    def _criar_janela_sem_tk(self, dimensao=3, quantidade=2):
        janela = JanelaPrincipal.__new__(JanelaPrincipal)
        janela.root = JanelaFalsa()
        janela.FUNDO = "#F3F5F8"
        janela.TEXTO = "#243247"
        janela.dimensao_grafico = VariavelFalsa(dimensao)
        janela.quantidade_graficos = VariavelFalsa(quantidade)
        janela.grafico_container = WidgetFalso()
        janela.grafico_figura = None
        janela.grafico_canvas = None
        janela.grafico_toolbar = None
        janela._grafico_pagina = True
        janela.canvas_rolagem = CanvasRolagemFalso()
        janela.form_graficos = WidgetFalso()
        janela.campos = {}
        janela._construir_reta = mock.Mock()
        return janela

    def _reta(self, dimensao, ponto_final):
        if dimensao == 2:
            return RetaR2(Vetor([0, 0]), Vetor(ponto_final))
        return RetaR3(Vetor([0, 0, 0]), Vetor(ponto_final))

    def test_atualizacao_dos_quatro_tipos_de_grafico_e_limpeza(self):
        for dimensao in (2, 3):
            for quantidade in (1, 2):
                with self.subTest(dimensao=dimensao, quantidade=quantidade):
                    janela = self._criar_janela_sem_tk(dimensao, quantidade)
                    retas = [self._reta(dimensao, [1] * dimensao)
                             for _ in range(quantidade)]
                    janela._construir_reta.side_effect = retas
                    with (
                        mock.patch("interface.janela.tk.Label",
                                   side_effect=lambda master, **kw: WidgetFalso(master, **kw)),
                        mock.patch("matplotlib.backends.backend_tkagg.FigureCanvasTkAgg",
                                   CanvasMatplotlibFalso),
                        mock.patch("matplotlib.backends.backend_tkagg.NavigationToolbar2Tk",
                                   BarraMatplotlibFalsa),
                    ):
                        janela.exibir_grafico()

                    self.assertEqual(len(janela.grafico_container.winfo_children()), 2)
                    self.assertIsNotNone(janela.grafico_figura)
                    eixo = janela.grafico_figura.axes[0]
                    self.assertEqual(len(eixo.get_legend().get_texts()), quantidade)
                    esperado_linhas = quantidade if dimensao == 3 else quantidade + 2
                    self.assertEqual(len(eixo.lines), esperado_linhas)
                    self.assertIsNotNone(janela.canvas_rolagem.y_movido)

                    figura_antiga = janela.grafico_figura
                    janela.quantidade_graficos.set(1 if quantidade == 2 else 2)
                    janela._construir_reta.side_effect = None
                    janela._construir_reta.return_value = self._reta(
                        dimensao, [2] * dimensao
                    )
                    with (
                        mock.patch("interface.janela.tk.Label",
                                   side_effect=lambda master, **kw: WidgetFalso(master, **kw)),
                        mock.patch("matplotlib.backends.backend_tkagg.FigureCanvasTkAgg",
                                   CanvasMatplotlibFalso),
                        mock.patch("matplotlib.backends.backend_tkagg.NavigationToolbar2Tk",
                                   BarraMatplotlibFalsa),
                    ):
                        janela.exibir_grafico()
                    self.assertEqual(figura_antiga.axes, [])
                    self.assertEqual(len(janela.grafico_container.winfo_children()), 2)

    def test_opcao_invalida_remove_figura_antiga(self):
        janela = self._criar_janela_sem_tk()
        janela.grafico_figura = FiguraFalsa()
        antigo = WidgetFalso(janela.grafico_container)
        janela._construir_reta.side_effect = ValueError("coordenada inválida")
        with (
            mock.patch("interface.janela.tk.Label",
                       side_effect=lambda master, **kw: WidgetFalso(master, **kw)),
            mock.patch("interface.janela.messagebox.showerror") as mostrar_erro,
        ):
            janela.exibir_grafico()
        self.assertTrue(antigo.destroyed)
        self.assertIsNone(janela.grafico_figura)
        mostrar_erro.assert_called_once()

    def test_falha_no_canvas_remove_figura_parcial_e_antiga(self):
        janela = self._criar_janela_sem_tk(dimensao=3, quantidade=1)
        janela._construir_reta.return_value = self._reta(3, [1, 2, 3])

        class CanvasComFalha(CanvasMatplotlibFalso):
            def draw(self):
                raise RuntimeError("falha simulada ao desenhar")

        with (
            mock.patch("interface.janela.tk.Label",
                       side_effect=lambda master, **kw: WidgetFalso(master, **kw)),
            mock.patch("matplotlib.backends.backend_tkagg.FigureCanvasTkAgg",
                       CanvasComFalha),
            mock.patch("matplotlib.backends.backend_tkagg.NavigationToolbar2Tk",
                       BarraMatplotlibFalsa),
            mock.patch("interface.janela.messagebox.showerror") as mostrar_erro,
        ):
            janela.exibir_grafico()

        self.assertIsNone(janela.grafico_figura)
        self.assertIsNone(janela.grafico_canvas)
        self.assertEqual(len(janela.grafico_container.winfo_children()), 1)
        mostrar_erro.assert_called_once()

    def test_troca_de_opcoes_limpa_figura_e_reconstroi_campos(self):
        janela = self._criar_janela_sem_tk()
        janela.grafico_figura = FiguraFalsa()
        limpar_figura = janela.grafico_figura.clear
        WidgetFalso(janela.grafico_container)
        janela.criar_campos_entrada = mock.Mock(
            side_effect=lambda _pai, nome, _dimensao, _linha: janela.campos.update({nome: []})
        )
        with (
            mock.patch("interface.janela.tk.Label",
                       side_effect=lambda master, **kw: WidgetFalso(master, **kw)),
            mock.patch.object(ttk, "LabelFrame", side_effect=WidgetFalso),
            mock.patch.object(ttk, "Button", side_effect=WidgetFalso),
        ):
            janela._atualizar_form_graficos()
        self.assertTrue(limpar_figura.called)
        self.assertEqual(len(janela.campos), 4)

        janela.quantidade_graficos.set(1)
        janela.dimensao_grafico.set(2)
        with (
            mock.patch("interface.janela.tk.Label",
                       side_effect=lambda master, **kw: WidgetFalso(master, **kw)),
            mock.patch.object(ttk, "LabelFrame", side_effect=WidgetFalso),
            mock.patch.object(ttk, "Button", side_effect=WidgetFalso),
        ):
            janela._atualizar_form_graficos()
        self.assertEqual(len(janela.campos), 2)

    def test_rolagem_mouse_e_limpeza_de_resultado(self):
        janela = self._criar_janela_sem_tk()
        evento_roda = type("Evento", (), {"delta": -120, "num": None})()
        self.assertEqual(janela._rolar_com_mouse(evento_roda), "break")
        self.assertEqual(janela.canvas_rolagem.unidades_roladas, [1])
        evento_linux = type("Evento", (), {"delta": 0, "num": 4})()
        janela._rolar_com_mouse(evento_linux)
        self.assertEqual(janela.canvas_rolagem.unidades_roladas, [1, -1])

        resultado = mock.Mock()
        resultado.winfo_exists.return_value = True
        janela.resultado = resultado
        janela.exibir_resultados = mock.Mock()
        janela._limpar_resultados()
        janela.exibir_resultados.assert_called_once_with("")


class TestApresentacaoAnaliseR3(unittest.TestCase):
    def test_mostra_indicadores_disponiveis_no_backend(self):
        janela = JanelaPrincipal.__new__(JanelaPrincipal)
        janela.resultado = None
        janela.dimensao_analise = VariavelFalsa(3)
        janela.root = JanelaFalsa()
        janela.exibir_resultados = mock.Mock()
        janela._construir_reta = mock.Mock(side_effect=(
            RetaR3(Vetor([0, 0, 0]), Vetor([1, 0, 0])),
            RetaR3(Vetor([0, 0, 1]), Vetor([0, 1, 1])),
        ))
        with mock.patch("interface.janela.messagebox.showerror") as mostrar_erro:
            janela.analisar_retas()
        mostrar_erro.assert_not_called()
        resultado = janela.exibir_resultados.call_args.args[0]
        self.assertIn("Ortogonalidade: Sim", resultado)
        self.assertIn("Ângulo entre as retas: 90°", resultado)
        self.assertIn("Distância entre as retas: 1", resultado)
        self.assertIn("Produto escalar dos vetores diretores: 0", resultado)

    def test_erro_de_analise_apaga_resultado_anterior(self):
        janela = JanelaPrincipal.__new__(JanelaPrincipal)
        janela.resultado = mock.Mock()
        janela.resultado.winfo_exists.return_value = True
        janela.dimensao_analise = VariavelFalsa(3)
        janela.root = JanelaFalsa()
        janela._construir_reta = mock.Mock(side_effect=ValueError("pontos iguais"))
        with mock.patch("interface.janela.messagebox.showerror") as mostrar_erro:
            janela.analisar_retas()
        janela.resultado.delete.assert_called_once_with("1.0", "end")
        mostrar_erro.assert_called_once()

    def test_erro_de_construcao_apaga_resultado_anterior(self):
        janela = JanelaPrincipal.__new__(JanelaPrincipal)
        janela.resultado = mock.Mock()
        janela.resultado.winfo_exists.return_value = True
        janela.root = JanelaFalsa()
        janela._construir_reta = mock.Mock(side_effect=ValueError("pontos iguais"))
        with mock.patch("interface.janela.messagebox.showerror") as mostrar_erro:
            janela.calcular_reta(2)
        janela.resultado.delete.assert_called_once_with("1.0", "end")
        mostrar_erro.assert_called_once()


if __name__ == "__main__":
    unittest.main()
