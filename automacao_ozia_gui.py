import customtkinter as ctk
import pyautogui
import json
import time
import os
import logging
from pathlib import Path
from threading import Thread, Event
from queue import Queue
import tkinter as tk

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("automacao_ozia.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


class AutomacaoOziaGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.title("Automação Ozia 🌸")
        self.geometry("600x800")

        # Cores
        self.rosa_claro = "#FFD1DC"  # Rosa bebê
        self.rosa_medio = "#FFB6C1"  # Rosa claro
        self.rosa_escuro = "#FF69B4"  # Rosa mais escuro

        # Configurar tema
        ctk.set_appearance_mode("light")
        self.configure(fg_color=self.rosa_claro)

        # Variáveis de controle
        self.coordenadas = {}
        self.arquivo_config = "coordenadas.json"
        self.continuar_automacao = Event()
        self.thread_automacao = None
        self.capturando_coordenadas = Event()
        self.log_queue = Queue()
        self.aguardando_tecla = Event()
        self.resposta_tecla = None

        # Valor do scroll (positivo para scroll para cima)
        self.valor_scroll = ctk.IntVar(value=1)  # Valor inicial extremamente suave

        # Bind para as teclas
        self.bind("<Key>", self.verificar_teclas)
        self.bind("<Alt_L>", self.tecla_alt)
        self.bind("<Control_L>", self.tecla_ctrl)

        self.criar_interface()
        self.carregar_coordenadas()

        # Iniciar thread de atualização do log
        self.after(100, self.atualizar_log)

    def verificar_teclas(self, event):
        if event.char == "q":
            self.parar_automacao()

    def tecla_alt(self, event):
        if self.aguardando_tecla.is_set():
            self.resposta_tecla = "não"
            self.aguardando_tecla.clear()

    def tecla_ctrl(self, event):
        if self.aguardando_tecla.is_set():
            self.resposta_tecla = "sim"
            self.aguardando_tecla.clear()

    def aguardar_tecla(self):
        # Criar janela de instruções
        janela_tecla = ctk.CTkToplevel(self)
        janela_tecla.title("Ação Necessária 🌸")
        janela_tecla.geometry("400x200")
        janela_tecla.configure(fg_color=self.rosa_claro)

        # Fazer janela ficar sempre em cima
        janela_tecla.attributes("-topmost", True)

        # Centralizar a janela
        janela_tecla.geometry(
            "+{}+{}".format(
                self.winfo_x() + (self.winfo_width() - 400) // 2,
                self.winfo_y() + (self.winfo_height() - 200) // 2,
            )
        )

        # Label com instruções
        label = ctk.CTkLabel(
            janela_tecla,
            text="Pressione:\n\nCTRL = Finalizar este atendimento\nALT = Ver próximo atendimento",
            font=("Helvetica", 14),
            text_color="black",
        )
        label.pack(pady=20)

        # Bind das teclas diretamente na janela do modal
        janela_tecla.bind("<Alt_L>", self.tecla_alt)
        janela_tecla.bind("<Control_L>", self.tecla_ctrl)

        # Forçar foco para a janela
        janela_tecla.focus_force()

        # Resetar e configurar variáveis de controle
        self.aguardando_tecla.set()
        self.resposta_tecla = None

        # Aguardar resposta
        while self.aguardando_tecla.is_set() and self.continuar_automacao.is_set():
            janela_tecla.update()
            time.sleep(0.1)

        # Fechar janela
        janela_tecla.destroy()
        return self.resposta_tecla

    def criar_interface(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color=self.rosa_medio)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        self.titulo = ctk.CTkLabel(
            self.main_frame,
            text="Automação Ozia",
            font=("Helvetica", 24, "bold"),
            text_color=self.rosa_escuro,
        )
        self.titulo.pack(pady=20)

        # Frame para controle de scroll
        self.scroll_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.scroll_frame.pack(pady=10)

        # Label para o slider
        self.scroll_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Velocidade do Scroll:",
            font=("Helvetica", 12),
            text_color="black",
        )
        self.scroll_label.pack()

        # Slider para controlar velocidade do scroll
        self.scroll_slider = ctk.CTkSlider(
            self.scroll_frame,
            from_=1,  # Scroll mínimo
            to=3,  # Scroll máximo
            number_of_steps=2,
            variable=self.valor_scroll,
            width=200,
            progress_color=self.rosa_escuro,
            button_color=self.rosa_escuro,
            button_hover_color="#FF1493",
        )
        self.scroll_slider.pack(pady=5)

        # Label para mostrar o valor atual
        self.valor_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Altura do scroll: 1 (Ajuste conforme necessário)",
            font=("Helvetica", 10),
            text_color="black",
        )
        self.valor_label.pack()

        # Atualizar label quando o valor mudar
        self.scroll_slider.configure(command=self.atualizar_valor_scroll)

        # Área de status
        self.status_text = ctk.CTkTextbox(
            self.main_frame,
            height=300,
            width=500,
            font=("Helvetica", 12),
            fg_color="white",
            text_color="black",
        )
        self.status_text.pack(pady=20, padx=20)
        self.adicionar_log("Bem-vinda ao Automatizador Ozia! 🌸\n")
        self.status_text.configure(state="disabled")

        # Frame para botões
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        # Botão Capturar Coordenadas
        self.btn_coordenadas = ctk.CTkButton(
            self.button_frame,
            text="Capturar Coordenadas",
            command=self.iniciar_captura_coordenadas,
            font=("Helvetica", 14),
            width=200,
            height=40,
            fg_color=self.rosa_escuro,
            hover_color="#FF1493",
        )
        self.btn_coordenadas.pack(pady=10)

        # Botão Resetar Coordenadas
        self.btn_resetar = ctk.CTkButton(
            self.button_frame,
            text="Resetar Coordenadas",
            command=self.resetar_coordenadas,
            font=("Helvetica", 14),
            width=200,
            height=40,
            fg_color=self.rosa_escuro,
            hover_color="#FF1493",
        )
        self.btn_resetar.pack(pady=10)

        # Botão Iniciar/Parar
        self.btn_iniciar = ctk.CTkButton(
            self.button_frame,
            text="Iniciar Automação",
            command=self.toggle_automacao,
            font=("Helvetica", 14),
            width=200,
            height=40,
            fg_color=self.rosa_escuro,
            hover_color="#FF1493",
        )
        self.btn_iniciar.pack(pady=10)

        # Instruções
        self.instrucoes = ctk.CTkLabel(
            self.main_frame,
            text="Para parar a automação:\n1. Clique em 'Parar Automação'\n2. Pressione 'q'\n3. OU mova o mouse para o canto superior esquerdo",
            font=("Helvetica", 12),
            justify="left",
            text_color="black",
        )
        self.instrucoes.pack(pady=20)

    def adicionar_log(self, mensagem):
        self.log_queue.put(mensagem)

    def atualizar_log(self):
        while not self.log_queue.empty():
            mensagem = self.log_queue.get()
            self.status_text.configure(state="normal")
            self.status_text.insert("end", f"{mensagem}\n")
            self.status_text.see("end")
            self.status_text.configure(state="disabled")
        self.after(100, self.atualizar_log)

    def carregar_coordenadas(self):
        if os.path.exists(self.arquivo_config):
            with open(self.arquivo_config, "r") as f:
                self.coordenadas = json.load(f)
                self.adicionar_log("✨ Coordenadas carregadas com sucesso!")
                return True
        return False

    def salvar_coordenadas(self):
        try:
            # Criar diretório se não existir
            Path(self.arquivo_config).parent.mkdir(parents=True, exist_ok=True)

            with open(self.arquivo_config, "w") as f:
                json.dump(self.coordenadas, f, indent=4)
                self.adicionar_log("✨ Coordenadas salvas com sucesso!")
                return True
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao salvar coordenadas: {str(e)}")
            return False

    def capturar_coordenadas(self):
        self.adicionar_log("\n=== Modo de Captura de Coordenadas ===")
        self.adicionar_log(
            "Você terá 5 segundos para posicionar o mouse em cada elemento."
        )

        elementos = [
            ("ultimo_atendimento", "último atendimento da lista"),
            ("botao_finalizar", "botão de finalizar (ícone de check)"),
            ("checkbox_mensagem", "checkbox de mensagem"),
            ("botao_confirmar", "botão verde de confirmar"),
        ]

        coordenadas_temp = {}

        for key, descricao in elementos:
            # Aguardar Enter antes de iniciar a captura
            self.adicionar_log(
                f"\nPosicione o mouse sobre o {descricao} e pressione Enter"
            )

            # Criar uma janela de diálogo para aguardar Enter
            dialog = ctk.CTkInputDialog(
                text=f"Posicione o mouse sobre o {descricao}\ne pressione Enter quando estiver pronto",
                title="Captura de Coordenadas",
            )
            resposta = dialog.get_input()

            # Se o usuário cancelou, interromper a captura
            if resposta is None:
                self.adicionar_log("❌ Captura cancelada pelo usuário")
                break

            self.adicionar_log("Capturando em:")
            for i in range(5, 0, -1):
                self.adicionar_log(f"{i}...")
                time.sleep(1)

            x, y = pyautogui.position()
            coordenadas_temp[key] = {"x": x, "y": y}
            self.adicionar_log(f"Coordenadas capturadas: ({x}, {y})")

            # Salvar cada coordenada individualmente
            self.coordenadas.update(coordenadas_temp)
            if not self.salvar_coordenadas():
                self.adicionar_log("❌ Erro ao salvar coordenadas. Tente novamente.")
                break

        if len(coordenadas_temp) == len(elementos):
            self.adicionar_log("\n✨ Todas as coordenadas foram capturadas e salvas!")
            self.adicionar_log(
                "ℹ️ Você pode resetar as coordenadas a qualquer momento usando o botão 'Resetar Coordenadas'"
            )
        else:
            self.adicionar_log("\n⚠️ Captura de coordenadas incompleta!")
            self.adicionar_log(
                "ℹ️ Por favor, capture todas as coordenadas antes de iniciar a automação"
            )

        self.btn_coordenadas.configure(state="normal")
        self.capturando_coordenadas.clear()

    def resetar_coordenadas(self):
        # Confirmar com o usuário
        dialog = ctk.CTkInputDialog(
            text="Tem certeza que deseja resetar todas as coordenadas?\nDigite 'sim' para confirmar:",
            title="Confirmar Reset",
        )
        resposta = dialog.get_input()

        if resposta and resposta.lower() == "sim":
            try:
                # Limpar coordenadas da memória
                self.coordenadas = {}

                # Remover arquivo de coordenadas se existir
                if os.path.exists(self.arquivo_config):
                    os.remove(self.arquivo_config)
                    self.adicionar_log("🗑️ Arquivo de coordenadas removido com sucesso!")

                self.adicionar_log("🗑️ Coordenadas resetadas com sucesso!")
                self.adicionar_log(
                    "ℹ️ Capture novas coordenadas antes de iniciar a automação."
                )
            except Exception as e:
                self.adicionar_log(f"❌ Erro ao resetar coordenadas: {str(e)}")
        else:
            self.adicionar_log("❌ Reset de coordenadas cancelado.")

    def iniciar_captura_coordenadas(self):
        if not self.capturando_coordenadas.is_set():
            self.btn_coordenadas.configure(state="disabled")
            self.capturando_coordenadas.set()
            Thread(target=self.capturar_coordenadas).start()

    def atualizar_valor_scroll(self, value):
        self.valor_label.configure(
            text=f"Altura do scroll: {int(value)} (Ajuste conforme necessário)"
        )

    def executar_automacao(self):
        while self.continuar_automacao.is_set():
            try:
                while True:
                    # 1. Clicar no último atendimento e aguardar tecla
                    self.adicionar_log("🖱️ Clicando no último atendimento...")
                    pyautogui.click(**self.coordenadas["ultimo_atendimento"])
                    time.sleep(0.2)  # Reduzido para 0.2

                    # Aguardar CTRL ou ALT
                    resposta = self.aguardar_tecla()

                    if resposta == "sim":
                        break  # Sai do loop de seleção e vai para a finalização
                    elif resposta == "não":
                        # Um único scroll suave para cima
                        self.adicionar_log("⬆️ Próximo atendimento...")
                        pyautogui.scroll(self.valor_scroll.get())
                        time.sleep(0.1)  # Reduzido para 0.1

                if not self.continuar_automacao.is_set():
                    break

                # Processo mais rápido após confirmação
                # 2. Clicar no botão de finalizar
                self.adicionar_log("✔️ Finalizando...")
                pyautogui.click(**self.coordenadas["botao_finalizar"])
                time.sleep(0.1)

                if not self.continuar_automacao.is_set():
                    break

                # 3. Desmarcar checkbox de mensagem
                pyautogui.click(**self.coordenadas["checkbox_mensagem"])
                time.sleep(0.1)

                if not self.continuar_automacao.is_set():
                    break

                # 4. Clicar no botão de confirmar
                pyautogui.click(**self.coordenadas["botao_confirmar"])
                time.sleep(0.1)

                self.adicionar_log("✨ Atendimento finalizado!")

                # Após finalizar, já prepara o próximo atendimento
                time.sleep(0.2)  # Pequena pausa para garantir que a página atualizou

                # Clica no último atendimento e faz scroll automaticamente
                self.adicionar_log("🔄 Preparando próximo atendimento...")
                pyautogui.click(**self.coordenadas["ultimo_atendimento"])
                time.sleep(0.1)
                pyautogui.scroll(self.valor_scroll.get())

            except Exception as e:
                self.adicionar_log(f"❌ Erro: {str(e)}")
                self.parar_automacao()
                break

    def iniciar_automacao(self):
        if not self.coordenadas:
            self.adicionar_log("❌ Por favor, capture as coordenadas primeiro!")
            return

        self.continuar_automacao.set()
        self.btn_iniciar.configure(text="Parar Automação")
        self.adicionar_log("\n🚀 Iniciando automação...")
        self.thread_automacao = Thread(target=self.executar_automacao)
        self.thread_automacao.start()

    def parar_automacao(self):
        self.continuar_automacao.clear()
        self.btn_iniciar.configure(text="Iniciar Automação")
        self.adicionar_log("🛑 Automação interrompida!")

    def toggle_automacao(self):
        if self.continuar_automacao.is_set():
            self.parar_automacao()
        else:
            self.iniciar_automacao()


if __name__ == "__main__":
    app = AutomacaoOziaGUI()
    app.mainloop()
