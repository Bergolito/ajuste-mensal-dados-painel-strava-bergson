#!/bin/bash
# Script de configuração automática do painel Strava
# Gera datasets e organiza arquivos conforme painel-strava-passo-a-passo-configuracao.md

set -e

# Passo 1: Extrair arquivos .gz da pasta arquivos-atividades-strava
cd arquivos-atividades-strava || exit 1
echo "Extraindo arquivos .gz em arquivos-atividades-strava..."
gunzip -v *.gz || true
cd ..

# Passo 2: Pré-processamento dos arquivos
if [ -f config/painel_config_preprocessamento.py ]; then
    echo "Executando painel_config_preprocessamento.py..."
    python3.10 config/painel_config_preprocessamento.py
fi

# Passo 3: Geração dos datasets
if [ -f config/painel_config_geracao_dados.py ]; then
    echo "Executando painel_config_geracao_dados.py..."
    python3.10 config/painel_config_geracao_dados.py
fi

# Passo 4: Copiar arquivos para processamento
if [ -d arquivos-atividades-strava ]; then
    echo "Copiando arquivos de arquivos-atividades-strava para processamento..."
    cp -r arquivos-atividades-strava/*.gpx processamento
    cp -r arquivos-atividades-strava/*.tcx processamento
fi

# Passo 5: Verificar arquivos de atividades
if [ -f config/painel_config_proc_atividades.py ]; then
    echo "Executando painel_config_proc_atividades.py..."
    python3.10 config/painel_config_proc_atividades.py
fi

# Passo 6: Processar arquivos TCX
if [ -f config/painel_config_tcx_files.py ]; then
    echo "Executando painel_config_tcx_files.py..."
    python3.10 config/painel_config_tcx_files.py
fi

# Passo 7: Processar arquivos GPX
if [ -f config/painel_config_gpx_files.py ]; then
    echo "Executando painel_config_gpx_files.py..."
    python3.10 config/painel_config_gpx_files.py
fi

echo "Processo finalizado."
