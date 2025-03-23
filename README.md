# Automação Ozia 🌸

Um aplicativo de automação com interface gráfica para otimizar o processo de finalização de atendimentos.

## Funcionalidades

- Interface gráfica amigável com tema rosa
- Captura de coordenadas para automatização
- Controle de velocidade de scroll ajustável
- Atalhos de teclado para operação rápida
- Logs detalhados das operações
- Disponível para Windows e Linux

## Como Usar

### Windows

1. Baixe o arquivo "Automacao Ozia.exe" da seção Releases
2. Execute o arquivo baixado
3. Clique em "Capturar Coordenadas" e siga as instruções
4. Ajuste a velocidade do scroll conforme necessário
5. Clique em "Iniciar Automação"

### Linux

1. Baixe o arquivo "automacao_ozia" da seção Releases
2. Abra o terminal na pasta onde baixou o arquivo
3. Dê permissão de execução: `chmod +x automacao_ozia`
4. Execute: `./automacao_ozia`
5. Siga as mesmas instruções da versão Windows

### Atalhos

- `CTRL`: Finalizar atendimento atual
- `ALT`: Ver próximo atendimento
- `Q`: Parar automação

## Download

Baixe a última versão do executável na seção [Releases](../../releases) do GitHub:

- Windows: Arquivo `.exe`
- Linux: Arquivo executável sem extensão

## Desenvolvimento

Para desenvolver ou modificar o aplicativo:

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute: `python automacao_ozia_gui.py`

## Build Manual

### Windows

```bash
pyinstaller --noconfirm --onefile --windowed --name="Automacao Ozia" automacao_ozia_gui.py --collect-all customtkinter
```

### Linux

```bash
# Instale as dependências do sistema
sudo apt-get install python3-tk python3-dev

# Crie o executável
pyinstaller --noconfirm --onefile --windowed --name="automacao_ozia" automacao_ozia_gui.py --collect-all customtkinter
```

## Notas

- O executável é criado automaticamente pelo GitHub Actions a cada push na branch main
- São geradas versões tanto para Windows quanto para Linux
- As coordenadas são salvas em `coordenadas.json`
- Logs são salvos em `automacao_ozia.log`
