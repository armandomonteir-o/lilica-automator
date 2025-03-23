import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.automacao_ozia import AutomacaoOzia


class TestAutomacaoOzia(unittest.TestCase):
    """Testes para a classe core da automação."""

    def setUp(self):
        """Configuração inicial para cada teste."""
        self.automacao = AutomacaoOzia()

    def tearDown(self):
        """Limpeza após cada teste."""
        if hasattr(self, "automacao"):
            self.automacao.continuar_automacao.clear()

    def test_carregar_coordenadas(self):
        """Testa o carregamento de coordenadas."""
        # Teste com arquivo inexistente
        self.assertFalse(self.automacao.carregar_coordenadas())

        # Teste com coordenadas válidas
        self.automacao.coordenadas = {
            "ultimo_atendimento": {"x": 100, "y": 100},
            "botao_finalizar": {"x": 200, "y": 200},
        }
        self.assertTrue(self.automacao.salvar_coordenadas())
        self.assertTrue(self.automacao.carregar_coordenadas())

    def test_salvar_coordenadas(self):
        """Testa o salvamento de coordenadas."""
        self.automacao.coordenadas = {
            "ultimo_atendimento": {"x": 100, "y": 100},
            "botao_finalizar": {"x": 200, "y": 200},
        }
        self.assertTrue(self.automacao.salvar_coordenadas())

    @patch("pyautogui.click")
    def test_clicar_coordenada(self, mock_click):
        """Testa se o método clicar_coordenada chama pyautogui.click corretamente."""
        x, y = 100, 200
        self.automacao.clicar_coordenada(x, y)
        mock_click.assert_called_once_with(x=x, y=y)

    def test_validar_coordenadas(self):
        """Testa a validação de coordenadas."""
        # Teste com coordenadas válidas
        x, y = 100, 200
        self.assertTrue(self.automacao.validar_coordenadas(x, y))

        # Teste com coordenadas negativas
        x, y = -100, -200
        self.assertFalse(self.automacao.validar_coordenadas(x, y))


if __name__ == "__main__":
    unittest.main()
