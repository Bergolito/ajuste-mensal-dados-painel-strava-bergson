# Passo a passo da configuração

## Passos:

- Passo 1 - extrair todos os arquivos da pasta strava-acitivities:

    > cd strava-activities 

    > gunzip *.gz

- Passo 2 - executar o arquivo painel_strava_preprocessamento.py para preparar os arquivos para a geração dos datasets:

    > python3.10 painel_strava_preprocessamento.py

- Passo 3 - executar o arquivo painel_strava_geracao_dados.py para a geração dos datasets:

    > python3.10 painel_strava_geracao_dados.py

- Passo 4 - copiar os arquivos da pasta strava-activities para a pasta processamento:

    > cp -r strava-activities processamento

- Passo 5 - executar o script python painel_config_proc_atividades.py para verificar se os arquivos de atividades estão OK. Se estiverem OK, move-os para a pasta arquivos-ok. Se estiverem com problema, mova-os para a pasta arquivos-problema:

    > python3.10 painel_config_proc_atividades.py 

- Passo 6 - executar o script python painel_config_tcx_files.py:

    > python3.10 python painel_config_tcx_files.py

- Passo 7 - executar o script python painel_config_gpx_files.py:

    > python3.10 python painel_config_gpx_files.py


