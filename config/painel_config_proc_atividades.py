import os
import shutil
from glob import glob

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_tcx_ok(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return '<TrainingCenterDatabase' in content and len(content) > 100
    except Exception:
        return False

def is_gpx_ok(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return '<gpx' in content and len(content) > 100
    except Exception:
        return False

def main():
    pasta_proc = 'processamento'
    pasta_tcx = 'processamento/atividades-tcx'
    pasta_gpx = 'processamento/atividades-gpx'
    arquivos_csv = 'processamento/arquivos-csv'
    pasta_problema_tcx = 'processamento/atividades-tcx/arquivos-problema'
    pasta_problema_gpx = 'processamento/atividades-gpx/arquivos-problema'

    ensure_dir(arquivos_csv)
    ensure_dir(pasta_tcx)
    ensure_dir(pasta_gpx)
    ensure_dir(pasta_problema_tcx)
    ensure_dir(pasta_problema_gpx)

    log_tcx_ok = 'processamento/log_arquivos_tcx_ok.txt'
    log_gpx_ok = 'processamento/log_arquivos_gpx_ok.txt'
    log_tcx_prob = 'processamento/log_arquivos_tcx_problema.txt'
    log_gpx_prob = 'processamento/log_arquivos_gpx_problema.txt'

    arquivos = glob(os.path.join(pasta_proc, '*'))
    with open(log_tcx_ok, 'a', encoding='utf-8') as flog_tcx_ok, open(log_gpx_ok, 'a', encoding='utf-8') as flog_gpx_ok, open(log_tcx_prob, 'a', encoding='utf-8') as flog_tcx_prob, open(log_gpx_prob, 'a', encoding='utf-8') as flog_gpx_prob:
        for filepath in arquivos:
            filename = os.path.basename(filepath)
            if filename.lower().endswith('.tcx'):
                if is_tcx_ok(filepath):
                    destino = os.path.join(pasta_tcx, filename)
                    shutil.move(filepath, destino)
                    flog_tcx_ok.write(f'TCX OK: {filename}\n')
                else:
                    destino = os.path.join(pasta_problema_tcx, filename)
                    shutil.move(filepath, destino)
                    flog_tcx_prob.write(f'TCX PROBLEMA: {filename}\n')
            elif filename.lower().endswith('.gpx'):
                if is_gpx_ok(filepath):
                    destino = os.path.join(pasta_gpx, filename)
                    shutil.move(filepath, destino)
                    flog_gpx_ok.write(f'GPX OK: {filename}\n')
                else:
                    destino = os.path.join(pasta_problema_gpx, filename)
                    shutil.move(filepath, destino)
                    flog_gpx_prob.write(f'GPX PROBLEMA: {filename}\n')

if __name__ == '__main__':
    main()
