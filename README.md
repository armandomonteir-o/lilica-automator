# 🤖 Lilica Automator

> Automatização inteligente para serviços da Ozia, com interface gráfica amigável e suporte para Windows e Linux.

## 📋 Índice

- [🤖 Lilica Automator](#-lilica-automator)
  - [📋 Índice](#-índice)
  - [✨ Funcionalidades](#-funcionalidades)
  - [🚀 Instalação](#-instalação)
    - [Windows](#windows)
    - [Linux](#linux)
  - [🎮 Como Usar](#-como-usar)
  - [📁 Estrutura do Projeto](#-estrutura-do-projeto)
  - [🛠 Tecnologias](#-tecnologias)
  - [💻 Desenvolvimento](#-desenvolvimento)
    - [Configuração do Ambiente](#configuração-do-ambiente)
    - [Build Manual](#build-manual)
      - [Windows](#windows-1)
      - [Linux](#linux-1)
  - [🎓 Conceitos Aplicados](#-conceitos-aplicados)
    - [Python](#python)
    - [GitHub Actions](#github-actions)
  - [📚 Roadmap de Estudo](#-roadmap-de-estudo)
  - [📄 Licença](#-licença)
  - [👥 Contribuição](#-contribuição)

## ✨ Funcionalidades

- Interface gráfica moderna com CustomTkinter
- Automação de serviços com PyAutoGUI
- Controle de velocidade de scroll
- Atalhos de teclado para finalizar (CTRL) ou pular (ALT) serviços
- Disponível para Windows e Linux
- Logs detalhados das operações

## 🚀 Instalação

### Windows

1. Baixe o executável mais recente da [página de releases](https://github.com/armandomonteir-o/lilica-automator/releases)
2. Execute o arquivo `Automacao-Ozia-Windows.exe`

### Linux

1. Baixe o executável mais recente da [página de releases](https://github.com/armandomonteir-o/lilica-automator/releases)
2. Dê permissão de execução:
   ```bash
   chmod +x automacao_ozia_linux
   ```
3. Execute o arquivo:
   ```bash
   ./automacao_ozia_linux
   ```

## 🎮 Como Usar

1. Inicie o programa
2. Ajuste a velocidade de scroll (1-3)
3. Clique em "Iniciar Automação"
4. Use os atalhos:
   - CTRL: Finalizar serviço atual
   - ALT: Pular para próximo serviço

## 📁 Estrutura do Projeto

```
lilica-automator/
├── src/                      # Código fonte
│   ├── gui/                  # Interface gráfica
│   │   └── automacao_ozia_gui.py
│   ├── core/                 # Lógica principal
│   │   └── automacao_ozia.py
│   └── utils/               # Utilitários
│       └── coordenadas.json
├── scripts/                  # Scripts de inicialização
│   ├── setup_linux.sh
│   └── iniciar_windows.bat
├── docs/                     # Documentação
│   └── github-actions-roadmap.md
├── tests/                    # Testes (futuro)
├── .github/                  # Configurações GitHub
│   └── workflows/
│       └── build.yml
├── requirements.txt          # Dependências
└── README.md                # Documentação principal
```

## 🛠 Tecnologias

- Python 3.10
- CustomTkinter
- PyAutoGUI
- GitHub Actions
- PyInstaller

## 💻 Desenvolvimento

### Configuração do Ambiente

1. Clone o repositório:

   ```bash
   git clone https://github.com/armandomonteir-o/lilica-automator.git
   cd lilica-automator
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Build Manual

#### Windows

```bash
pyinstaller --noconfirm --onefile --windowed --name="Automacao Ozia" src/gui/automacao_ozia_gui.py --collect-all customtkinter
```

#### Linux

```bash
pyinstaller --noconfirm --onefile --windowed --name="automacao_ozia" src/gui/automacao_ozia_gui.py --collect-all customtkinter
```

## 🎓 Conceitos Aplicados

### Python

- Programação Orientada a Objetos
- GUI com CustomTkinter
- Automação com PyAutoGUI
- Logging e tratamento de erros
- Gerenciamento de dependências

### GitHub Actions

- CI/CD automatizado
- Build multiplataforma
- Gestão de artifacts e releases
- Segurança e tokens
- Workflows condicionais

## 📚 Roadmap de Estudo

Veja o [Roadmap Detalhado](docs/github-actions-roadmap.md) para um guia completo de aprendizado dos conceitos aplicados no projeto.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Contribuição

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre nosso código de conduta e o processo de submissão de pull requests.

![Cobertura de Testes](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/armandomonteir-o/GIST_ID/raw/coverage.json)
