import unittest
from unittest.mock import MagicMock, patch
import threading
import time
import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gui.automacao_ozia_gui import AutomacaoOziaGUI


class TestAutomacaoOziaGUI(unittest.TestCase):
    """Testes para a interface gráfica da automação."""

    def setUp(self):
        """Configuração inicial para cada teste."""
        self.app = AutomacaoOziaGUI()

    def tearDown(self):
        """Limpeza após cada teste."""
        if hasattr(self, "app"):
            self.app.quit()

    @patch("pyautogui.click")
    def test_parar_automacao(self, mock_click):
        """Testa se a automação para corretamente."""
        # Configura o mock
        mock_click.side_effect = lambda **kwargs: time.sleep(0.1)

        # Inicia a automação
        self.app.coordenadas = {
            "ultimo_atendimento": {"x": 100, "y": 100},
            "botao_finalizar": {"x": 200, "y": 200},
            "checkbox_mensagem": {"x": 300, "y": 300},
            "botao_confirmar": {"x": 400, "y": 400},
        }

        # Inicia a automação em uma thread
        self.app.iniciar_automacao()

        # Aguarda um pouco para a automação iniciar
        time.sleep(0.5)

        # Para a automação
        self.app.parar_automacao()

        # Aguarda um pouco para garantir que a thread parou
        time.sleep(0.5)

        # Verifica se a thread parou
        self.assertFalse(self.app.continuar_automacao.is_set())

        # Verifica se não há mais chamadas ao click após parar
        call_count = mock_click.call_count
        time.sleep(0.5)
        self.assertEqual(call_count, mock_click.call_count)

    @patch("pyautogui.click")
    def test_failsafe_para_automacao(self, mock_click):
        """Testa se a automação para quando o failsafe é acionado."""
        # Configura o mock para simular o failsafe
        mock_click.side_effect = pyautogui.FailSafeException()

        # Inicia a automação
        self.app.coordenadas = {"ultimo_atendimento": {"x": 100, "y": 100}}

        # Inicia a automação
        self.app.iniciar_automacao()

        # Aguarda um pouco
        time.sleep(0.5)

        # Verifica se a automação parou
        self.assertFalse(self.app.continuar_automacao.is_set())
        self.assertEqual(self.app.btn_iniciar["text"], "Iniciar Automação")

    def test_thread_cleanup(self):
        """Testa se as threads são limpas corretamente ao fechar."""
        # Inicia a automação
        self.app.coordenadas = {"ultimo_atendimento": {"x": 100, "y": 100}}

        self.app.iniciar_automacao()

        # Aguarda um pouco
        time.sleep(0.5)

        # Fecha a aplicação
        self.app.quit()

        # Verifica se a thread foi finalizada
        if self.app.thread_automacao:
            self.app.thread_automacao.join(timeout=1)
            self.assertFalse(self.app.thread_automacao.is_alive())


if __name__ == "__main__":
    unittest.main()
