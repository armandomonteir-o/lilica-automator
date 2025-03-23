# Arquitetura do Lilica Automator

## Visão Geral

O Lilica Automator foi desenvolvido com uma arquitetura modular e extensível, focando em separação de responsabilidades e facilidade de manutenção.

## Diagrama de Arquitetura

```mermaid
graph TD
    subgraph Interface
        GUI[GUI - CustomTkinter]
        Controls[Controles de Usuário]
        Events[Eventos de Teclado]
    end

    subgraph Core
        Automation[Módulo de Automação]
        Coordinator[Coordenador de Processos]
        Logger[Sistema de Logs]
    end

    subgraph Utils
        Config[Configurações]
        Coordinates[Coordenadas]
        Version[Versionamento]
    end

    subgraph CI/CD
        GHA[GitHub Actions]
        Build[Build System]
        Release[Release Manager]
    end

    GUI --> Controls
    GUI --> Events
    Controls --> Automation
    Events --> Automation
    Automation --> Coordinator
    Coordinator --> Logger
    Coordinator --> Config
    Config --> Coordinates
    GHA --> Build
    Build --> Release

    classDef primary fill:#f9f,stroke:#333,stroke-width:2px
    classDef secondary fill:#bbf,stroke:#333,stroke-width:2px
    classDef utility fill:#dfd,stroke:#333,stroke-width:2px
    classDef cicd fill:#ffd,stroke:#333,stroke-width:2px

    class GUI,Controls,Events primary
    class Automation,Coordinator,Logger secondary
    class Config,Coordinates,Version utility
    class GHA,Build,Release cicd
```

## Componentes Principais

### Interface

- **GUI**: Interface gráfica moderna construída com CustomTkinter
- **Controles**: Gerenciamento de inputs do usuário
- **Eventos**: Captura de atalhos de teclado (CTRL/ALT)

### Core

- **Automação**: Lógica principal usando PyAutoGUI
- **Coordenador**: Gerencia o fluxo de processos
- **Logger**: Sistema de logs para monitoramento

### Utilitários

- **Configurações**: Gerenciamento de configurações
- **Coordenadas**: Armazenamento de posições
- **Versionamento**: Controle de versão

### CI/CD

- **GitHub Actions**: Automação de build e deploy
- **Build System**: Geração de executáveis
- **Release**: Gestão de releases

## Fluxo de Dados

1. Usuário interage com a interface
2. Eventos são capturados e processados
3. Módulo de automação executa ações
4. Sistema de logs registra operações
5. CI/CD gerencia builds e releases
