import xml.etree.ElementTree as ET
import os
import pandas as pd
import datetime

class GPXParser:
    """
    Parser simples para arquivos GPX, extrai coordenadas e informações básicas.
    """
    def __init__(self, gpx_file_path):
        self.gpx_file_path = gpx_file_path
        self.root = None
        self.tracks = []
        self.parse()
    
    def parse(self):
        try:
            tree = ET.parse(self.gpx_file_path)
            self.root = tree.getroot()
            ns = {'default': 'http://www.topografix.com/GPX/1/1'}
            trackpoints = self.root.findall('.//default:trkpt', ns)
            track_data = {'trackpoints': []}
            for tp in trackpoints:
                lat = tp.attrib.get('lat')
                lon = tp.attrib.get('lon')
                if lat is None or lon is None:
                    continue  # Pula pontos inválidos
                try:
                    latitude = float(lat)
                    longitude = float(lon)
                except Exception:
                    continue  # Pula se não for possível converter
                ele_elem = tp.find('./default:ele', ns)
                altitude = float(ele_elem.text) if ele_elem is not None else None
                time_elem = tp.find('./default:time', ns)
                timestamp = time_elem.text if time_elem is not None else None
                point = {
                    'time': timestamp,
                    'latitude': latitude,
                    'longitude': longitude,
                    'altitude': altitude
                }
                track_data['trackpoints'].append(point)
            self.tracks.append(TrackData(track_data))
        except Exception as e:
            raise Exception(f"Erro ao analisar o arquivo GPX: {str(e)}")

class TrackData:
    def __init__(self, track_data):
        self.trackpoints = [TrackPoint(tp) for tp in track_data['trackpoints']]

class TrackPoint:
    def __init__(self, point_data):
        self.time = point_data['time']
        self.latitude = point_data['latitude']
        self.longitude = point_data['longitude']
        self.altitude = point_data['altitude']

def recupera_coordenadas_arquivos_gpx():
    """
    Recupera todos os arquivos GPX da pasta atividades-gpx, extrai as coordenadas
    de latitude e longitude e gera um arquivo CSV para cada arquivo GPX na pasta
    datasets/mapas.
    """
    output_dir = "processamento/arquivos-csv"
    os.makedirs(output_dir, exist_ok=True)
    gpx_dir = "processamento/atividades-gpx"
    gpx_files = [f for f in os.listdir(gpx_dir) if f.endswith('.gpx')]
    if not gpx_files:
        print("Nenhum arquivo GPX encontrado na pasta atividades-gpx")
        return
    print(f"Processando {len(gpx_files)} arquivos GPX...")
    count_success = 0
    count_errors = 0
    for gpx_file in gpx_files:
        try:
            gpx_path = os.path.join(gpx_dir, gpx_file)
            base_name = os.path.splitext(gpx_file)[0]
            csv_path = os.path.join(output_dir, f"{base_name}.csv")
            gpx = GPXParser(gpx_path)
            # Extrair dados dos trackpoints
            data = [{
                'time': tp.time,
                'latitude': tp.latitude,
                'longitude': tp.longitude,
                'altitude': tp.altitude
            } for track in gpx.tracks for tp in track.trackpoints]
            df = pd.DataFrame(data)
            df.to_csv(csv_path, index=False)
            count_success += 1
        except Exception as e:
            print(f"Erro ao processar {gpx_file}: {e}")
            count_errors += 1
    print(f"Arquivos processados com sucesso: {count_success}")
    print(f"Arquivos com erro: {count_errors}")

if __name__ == '__main__':
    recupera_coordenadas_arquivos_gpx()
