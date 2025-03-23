#!/bin/bash

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Instalar dependências do sistema necessárias para o PyAutoGUI
echo "Instalando dependências do sistema..."
sudo apt-get update
sudo apt-get install -y python3-tk python3-dev

echo "Setup concluído!"
echo
echo "Para usar a automação:"
echo "1. Abra o Chrome normalmente e faça login no Ozia.app"
echo "2. Execute: python automacao_ozia.py"
echo "3. Na primeira vez, o script vai pedir para você posicionar o mouse em cada elemento"
echo "4. Nas próximas vezes, ele já vai usar as coordenadas salvas" 