import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import json

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.automacao_ozia import AutomacaoOzia


class TestAutomacaoOzia(unittest.TestCase):
    """Testes para a classe core da automação."""

    def setUp(self):
        """Configuração inicial para cada teste."""
        self.automacao = AutomacaoOzia()
        # Garante que o arquivo de coordenadas não existe
        if os.path.exists(self.automacao.arquivo_config):
            os.remove(self.automacao.arquivo_config)

    def tearDown(self):
        """Limpeza após cada teste."""
        # Remove o arquivo de coordenadas se existir
        if os.path.exists(self.automacao.arquivo_config):
            os.remove(self.automacao.arquivo_config)

    def test_carregar_coordenadas(self):
        """Testa o carregamento de coordenadas."""
        # Teste com arquivo inexistente
        self.assertFalse(self.automacao.carregar_coordenadas())

        # Teste com arquivo existente
        coordenadas = {
            "ultimo_atendimento": {"x": 100, "y": 100},
            "botao_finalizar": {"x": 200, "y": 200},
        }
        with open(self.automacao.arquivo_config, "w") as f:
            json.dump(coordenadas, f)

        self.assertTrue(self.automacao.carregar_coordenadas())
        self.assertEqual(self.automacao.coordenadas, coordenadas)

    def test_salvar_coordenadas(self):
        """Testa o salvamento de coordenadas."""
        coordenadas = {
            "ultimo_atendimento": {"x": 100, "y": 100},
            "botao_finalizar": {"x": 200, "y": 200},
        }
        self.automacao.coordenadas = coordenadas

        self.assertTrue(self.automacao.salvar_coordenadas())
        self.assertTrue(os.path.exists(self.automacao.arquivo_config))

        with open(self.automacao.arquivo_config, "r") as f:
            coordenadas_salvas = json.load(f)
        self.assertEqual(coordenadas_salvas, coordenadas)

    @patch("pyautogui.click")
    def test_clicar_coordenada(self, mock_click):
        """Testa se o método clicar_coordenada chama pyautogui.click corretamente."""
        x, y = 100, 200
        self.automacao.clicar_coordenada(x, y)
        mock_click.assert_called_once_with(x=x, y=y)

    def test_validar_coordenadas(self):
        """Testa a validação de coordenadas."""
        # Coordenadas válidas
        self.assertTrue(self.automacao.validar_coordenadas(100, 100))
        self.assertTrue(self.automacao.validar_coordenadas(0, 0))
        self.assertTrue(self.automacao.validar_coordenadas(1.5, 2.5))

        # Coordenadas inválidas
        self.assertFalse(self.automacao.validar_coordenadas(-1, 100))
        self.assertFalse(self.automacao.validar_coordenadas(100, -1))
        self.assertFalse(self.automacao.validar_coordenadas("a", 100))
        self.assertFalse(self.automacao.validar_coordenadas(100, "b"))


if __name__ == "__main__":
    unittest.main()
