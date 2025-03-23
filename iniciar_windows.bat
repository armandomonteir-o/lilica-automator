@echo off

REM Criar ambiente virtual se não existir
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
call venv\Scripts\activate

REM Instalar dependências
echo Instalando dependências...
pip install -r requirements.txt

echo.
echo Setup concluído! 
echo Para usar a automação:
echo 1. Abra o Chrome normalmente
echo 2. Execute "python automacao_ozia.py"
echo.
pause 