import unittest
from unittest.mock import patch
import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.automacao_ozia import AutomacaoOzia


class TestAutomacaoOzia(unittest.TestCase):
    """Testes para a classe AutomacaoOzia."""

    def setUp(self):
        """Configuração inicial para cada teste."""
        self.automacao = AutomacaoOzia()

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
