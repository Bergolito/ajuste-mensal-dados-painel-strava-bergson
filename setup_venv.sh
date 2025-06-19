#!/bin/bash

# Verifica se o Python 3.10 está instalado
if ! command -v python3.10 &> /dev/null; then
    echo "Python 3.10 não está instalado. Por favor, instale-o antes de continuar."
    echo "Você pode instalá-lo com: sudo apt-get install python3.10 python3.10-venv"
    exit 1
fi

# Cria o ambiente virtual com Python 3.10
echo "Criando ambiente virtual com Python 3.10..."
python3.10 -m venv venv

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualiza pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instala as dependências necessárias
echo "Instalando dependências..."
pip install pandas matplotlib seaborn jupyter numpy autopep8 pylint

# Cria arquivo de requisitos
pip freeze > requirements.txt

echo "Ambiente virtual configurado com sucesso!"
echo "Para ativar o ambiente, execute: source venv/bin/activate"
echo "Para configurar o VSCode para usar este ambiente, selecione o interpretador em:"
echo "View > Command Palette > Python: Select Interpreter > ./venv/bin/python"
