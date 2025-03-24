import pyautogui
import json
import time
import os
import logging
from pynput import keyboard
from threading import Event

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("automacao_ozia.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True  # Mova o mouse para o canto superior esquerdo para parar
pyautogui.PAUSE = 0.5  # Pausa entre ações


class AutomacaoOzia:
    def carregar_coordenadas(self):
        """Carrega as coordenadas salvas do arquivo JSON"""
        if os.path.exists(self.arquivo_config):
            with open(self.arquivo_config, "r") as f:
                self.coordenadas = json.load(f)
                logger.info("Coordenadas carregadas com sucesso!")
                return True
        return False

    def __init__(self):
        self.coordenadas = {}
        self.arquivo_config = "coordenadas.json"
        self.continuar_automacao = Event()
        self.carregar_coordenadas()
        self.listener = None

    def clicar_coordenada(self, x, y):
        """Clica em uma coordenada específica."""
        if self.validar_coordenadas(x, y):
            pyautogui.click(x=x, y=y)
            return True
        return False

    def validar_coordenadas(self, x, y):
        """Valida se as coordenadas são válidas."""
        return (
            isinstance(x, (int, float))
            and isinstance(y, (int, float))
            and x >= 0
            and y >= 0
        )

    def salvar_coordenadas(self):
        """Salva as coordenadas no arquivo JSON"""
        try:
            with open(self.arquivo_config, "w") as f:
                json.dump(self.coordenadas, f, indent=4)
                logger.info("Coordenadas salvas com sucesso!")
                return True
        except Exception as e:
            logger.error(f"Erro ao salvar coordenadas: {str(e)}")
            return False

    def capturar_coordenadas(self):
        """Permite ao usuário capturar as coordenadas necessárias"""
        print("\n=== Modo de Captura de Coordenadas ===")
        print("Para cada elemento, você terá 5 segundos para posicionar o mouse.")
        print("Mantenha o mouse parado sobre o elemento quando a contagem terminar.")

        elementos = [
            ("ultimo_atendimento", "último atendimento da lista"),
            ("botao_finalizar", "botão de finalizar (ícone de check)"),
            ("checkbox_mensagem", "checkbox de mensagem"),
            ("botao_confirmar", "botão verde de confirmar"),
        ]

        for key, descricao in elementos:
            input(f"\nPosicione o mouse sobre o {descricao} e pressione Enter...")
            print("Capturando em:")
            for i in range(5, 0, -1):
                print(f"{i}...")
                time.sleep(1)

            x, y = pyautogui.position()
            self.coordenadas[key] = {"x": x, "y": y}
            print(f"Coordenadas capturadas: ({x}, {y})")

        self.salvar_coordenadas()
        print("\nTodas as coordenadas foram capturadas e salvas!")

    def esperar_verificando_q(self, segundos):
        """Espera o número de segundos especificado, verificando a tecla q"""
        for _ in range(segundos):
            if not self.continuar_automacao.is_set():
                return False
            time.sleep(1)
        return True

    def executar_automacao(self):
        """Executa a automação usando as coordenadas salvas"""
        try:
            # 1. Clicar no último atendimento (5 segundos de delay)
            if not self.continuar_automacao.is_set():
                return False
            logger.info("Clicando no último atendimento...")
            pyautogui.click(**self.coordenadas["ultimo_atendimento"])
            if not self.esperar_verificando_q(
                5
            ):  # 5 segundos para verificar o atendimento
                return False

            # 2. Clicar no botão de finalizar (2 segundos de delay)
            if not self.continuar_automacao.is_set():
                return False
            logger.info("Clicando no botão de finalizar...")
            pyautogui.click(**self.coordenadas["botao_finalizar"])
            if not self.esperar_verificando_q(2):  # Aumentado para 2 segundos
                return False

            # 3. Desmarcar checkbox de mensagem (2 segundos de delay)
            if not self.continuar_automacao.is_set():
                return False
            logger.info("Desmarcando checkbox de mensagem...")
            pyautogui.click(**self.coordenadas["checkbox_mensagem"])
            if not self.esperar_verificando_q(2):  # Aumentado para 2 segundos
                return False

            # 4. Clicar no botão de confirmar (2 segundos de delay)
            if not self.continuar_automacao.is_set():
                return False
            logger.info("Confirmando finalização...")
            pyautogui.click(**self.coordenadas["botao_confirmar"])
            if not self.esperar_verificando_q(2):  # Aumentado para 2 segundos
                return False

            logger.info("Atendimento finalizado com sucesso!")
            return True

        except Exception as e:
            logger.error(f"Erro durante a automação: {str(e)}")
            return False

    def on_press(self, key):
        """Callback para quando uma tecla é pressionada"""
        try:
            if key.char == "q":
                logger.info("Tecla 'q' pressionada. Finalizando automação...")
                self.continuar_automacao.clear()
                # Parar o listener
                return False
        except AttributeError:
            pass

    def iniciar_loop_automacao(self):
        """Inicia o loop principal da automação"""
        print("\n=== Automação Ozia ===")
        print("ATENÇÃO:")
        print(
            "1. Pressione 'q' ou mova o mouse para o canto superior esquerdo para PARAR"
        )
        print("2. Certifique-se de que o Ozia.app está aberto e você está logado")
        print("\nA automação vai executar automaticamente a cada 3 segundos.")
        print("Mantenha esta janela visível para poder ler os logs.")
        print("\nPressione 'q' a qualquer momento para parar IMEDIATAMENTE!")

        input("\nPressione Enter para começar...")

        # Inicia o listener de teclado em uma thread separada
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        while self.continuar_automacao.is_set():
            if self.executar_automacao():
                print("\nAtendimento finalizado! Aguardando 3 segundos...")
                if not self.esperar_verificando_q(3):
                    break
            else:
                if not self.continuar_automacao.is_set():
                    break
                print("\nOcorreu um erro durante a automação.")
                resposta = input("Deseja tentar novamente? (s/n): ")
                if resposta.lower() != "s":
                    break

        # Garante que o listener seja parado
        if self.listener:
            self.listener.stop()
        logger.info("Automação interrompida com sucesso!")


def main():
    automacao = AutomacaoOzia()

    if not automacao.carregar_coordenadas():
        print("\nNenhuma coordenada encontrada!")
        resposta = input("Deseja capturar as coordenadas agora? (s/n): ")
        if resposta.lower() == "s":
            automacao.capturar_coordenadas()
        else:
            print("Não é possível executar a automação sem as coordenadas.")
            return

    try:
        automacao.iniciar_loop_automacao()
    except KeyboardInterrupt:
        print("\nAutomação interrompida pelo usuário.")
    finally:
        print("\nAutomação finalizada!")


if __name__ == "__main__":
    main()
