import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import threading
import time
import pyautogui
from src.gui.automacao_ozia_gui import AutomacaoOziaGUI


class TestInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para todos os testes."""
        cls.root = tk.Tk()
        cls.interface = AutomacaoOziaGUI()

    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes."""
        cls.root.destroy()

    def setUp(self):
        """Configuração antes de cada teste.

        Sem ligar o sinalizador aqui: quem liga é o iniciar_automacao. E sem coordenadas o
        iniciar não faz nada, então os testes conferiam "parou" sem nunca ter começado.
        As coordenadas são falsas e o laço de cliques é trocado por um que só espera o sinal
        de parar: o que se testa é o liga e desliga, sem clicar na tela de ninguém.
        """
        self.interface.coordenadas = {
            "ultimo_atendimento": {"x": 1, "y": 1},
            "botao_finalizar": {"x": 1, "y": 1},
            "checkbox_mensagem": {"x": 1, "y": 1},
            "botao_confirmar": {"x": 1, "y": 1},
        }
        self.interface.executar_automacao = self._laco_que_espera_parar

    def _laco_que_espera_parar(self):
        while self.interface.continuar_automacao.is_set():
            time.sleep(0.05)

    def assert_comecou(self):
        self.assertTrue(self.interface.continuar_automacao.is_set())
        self.assertTrue(self.interface.thread_automacao.is_alive())

    def tearDown(self):
        """Limpeza após cada teste."""
        self.interface.continuar_automacao.clear()
        if (
            hasattr(self.interface, "thread_automacao")
            and self.interface.thread_automacao
        ):
            self.interface.thread_automacao.join(timeout=1)
            self.interface.thread_automacao = None
        del self.interface.executar_automacao  # volta o laço de verdade

    @patch("pyautogui.click")
    def test_parar_automacao(self, mock_click):
        """Testa se a automação para corretamente."""
        # Inicia a automação em uma thread
        self.interface.iniciar_automacao()
        time.sleep(0.5)  # Pequena pausa para a thread iniciar
        self.assert_comecou()

        # Para a automação
        self.interface.parar_automacao()
        time.sleep(0.5)  # Pequena pausa para a thread parar

        # Verifica se a automação foi parada
        self.assertFalse(self.interface.continuar_automacao.is_set())

    def test_failsafe_para_automacao(self):
        """Testa se o failsafe do PyAutoGUI para a automação."""
        # Simula o failsafe do PyAutoGUI
        self.interface.iniciar_automacao()
        time.sleep(0.5)  # Pequena pausa para a thread iniciar
        self.assert_comecou()

        # Simula o failsafe
        pyautogui.FAILSAFE = True
        try:
            pyautogui.moveTo(-1, -1)  # Isso deve disparar o failsafe
        except pyautogui.FailSafeException:
            self.interface.parar_automacao()

        time.sleep(0.5)  # Pequena pausa para a thread parar
        self.assertFalse(self.interface.continuar_automacao.is_set())

    def test_thread_cleanup(self):
        """Testa se as threads são limpas corretamente ao fechar."""
        # Inicia a automação
        self.interface.iniciar_automacao()
        time.sleep(0.5)  # Pequena pausa para a thread iniciar
        self.assert_comecou()

        # Para a automação e limpa
        self.interface.parar_automacao()
        time.sleep(0.5)  # Pequena pausa para a thread parar

        # Verifica se a thread foi finalizada
        if self.interface.thread_automacao:
            self.interface.thread_automacao.join(timeout=1)
            self.assertFalse(self.interface.thread_automacao.is_alive())


if __name__ == "__main__":
    unittest.main()
