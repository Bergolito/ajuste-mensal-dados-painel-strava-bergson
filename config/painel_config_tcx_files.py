import xml.etree.ElementTree as ET
import os
import pandas as pd
import datetime

class TCXParser:
    """
    Implementação personalizada do parser TCX para extrair coordenadas dos arquivos TCX
    """
    def __init__(self, tcx_file_path):
        self.tcx_file_path = tcx_file_path
        self.namespace = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
        self.root = None
        self.tracks = []
        self.parse()
    
    def parse(self):
        """Parse o arquivo TCX e extrai as informações"""
        try:
            tree = ET.parse(self.tcx_file_path)
            self.root = tree.getroot()
            
            # Extrair os trackpoints
            trackpoints = self.root.findall('.//ns:Trackpoint', self.namespace)
            
            # Agrupar trackpoints por track (geralmente apenas um track por arquivo)
            track_data = {'trackpoints': []}
            
            for tp in trackpoints:
                # Extrair timestamp
                time_elem = tp.find('./ns:Time', self.namespace)
                timestamp = time_elem.text if time_elem is not None else None
                
                # Extrair posição (lat/lon)
                position = tp.find('./ns:Position', self.namespace)
                latitude = None
                longitude = None
                
                if position is not None:
                    lat_elem = position.find('./ns:LatitudeDegrees', self.namespace)
                    lon_elem = position.find('./ns:LongitudeDegrees', self.namespace)
                    
                    if lat_elem is not None and lon_elem is not None:
                        latitude = float(lat_elem.text)
                        longitude = float(lon_elem.text)
                
                # Extrair altitude
                altitude_elem = tp.find('./ns:AltitudeMeters', self.namespace)
                if altitude_elem is not None and altitude_elem.text is not None:
                    try:
                        altitude = float(altitude_elem.text)
                    except Exception:
                        altitude = None
                else:
                    altitude = None
                
                # Criar objeto de ponto
                point = {
                    'time': timestamp,
                    'latitude': latitude,
                    'longitude': longitude,
                    'altitude': altitude
                }
                
                track_data['trackpoints'].append(point)
                
            # Adicionar track à lista de tracks
            self.tracks.append(TrackData(track_data))
                
        except Exception as e:
            raise Exception(f"Erro ao analisar o arquivo TCX: {str(e)}")

class TrackData:
    """Representa um track (percurso) em um arquivo TCX"""
    def __init__(self, track_data):
        self.trackpoints = [TrackPoint(tp) for tp in track_data['trackpoints']]

class TrackPoint:
    """Representa um ponto no percurso"""
    def __init__(self, point_data):
        self.time = point_data['time']
        self.latitude = point_data['latitude']
        self.longitude = point_data['longitude']
        self.altitude = point_data['altitude']

# ==================================
def recupera_coordenadas_arquivos_tcx():
    """
    Recupera todos os arquivos TCX da pasta activities-tcx, extrai as coordenadas
    de latitude e longitude e gera um arquivo CSV para cada arquivo TCX na pasta
    datasets/mapas.
    """
    import os
    import pandas as pd
    
    # Criar diretório de saída se não existir
    output_dir = "datasets/mapas"
    os.makedirs(output_dir, exist_ok=True)
    
    # Listar todos os arquivos TCX na pasta de entrada
    tcx_dir = "activities-tcx"
    tcx_files = [f for f in os.listdir(tcx_dir) if f.endswith('.tcx')]
    
    if not tcx_files:
        print("Nenhum arquivo TCX encontrado na pasta activities-tcx")
        return
    
    print(f"Processando {len(tcx_files)} arquivos TCX...")
    
    # Contador de arquivos processados
    count_success = 0
    count_errors = 0
    
    for tcx_file in tcx_files:
        try:
            # Caminho completo para o arquivo TCX
            tcx_path = os.path.join(tcx_dir, tcx_file)
            
            # Nome do arquivo sem extensão
            base_name = os.path.splitext(tcx_file)[0]
            
            # Caminho para o arquivo CSV de saída
            csv_path = os.path.join(output_dir, f"{base_name}.csv")
            
            # Parsear o arquivo TCX e extrair as coordenadas
            tcx = TCXParser(tcx_path)
            
            # Lista para armazenar as coordenadas
            coordinates = []
            
            # Extrair coordenadas de cada trackpoint
            for track in tcx.tracks:
                for trackpoint in track.trackpoints:
                    if trackpoint.latitude and trackpoint.longitude:
                        coordinates.append({
                            'timestamp': trackpoint.time,
                            'latitude': trackpoint.latitude,
                            'longitude': trackpoint.longitude,
                            'altitude': trackpoint.altitude if trackpoint.altitude else None
                        })
            
            # Verificar se existem coordenadas
            if not coordinates:
                print(f"Nenhuma coordenada encontrada no arquivo {tcx_file}")
                count_errors += 1
                continue
            
            # Criar DataFrame e salvar como CSV
            df = pd.DataFrame(coordinates)
            df.to_csv(csv_path, index=False)
            
            count_success += 1
            
            # Mostrar progresso a cada 10 arquivos
            if count_success % 10 == 0:
                print(f"Progresso: {count_success} arquivos processados")
            
        except Exception as e:
            print(f"Erro ao processar o arquivo {tcx_file}: {str(e)}")
            count_errors += 1
    
    print(f"\nProcessamento concluído!")
    print(f"Total de arquivos: {len(tcx_files)}")
    print(f"Processados com sucesso: {count_success}")
    print(f"Erros: {count_errors}")
    
    return count_success

def processar_arquivo_tcx_para_csv(input_dir, output_dir):
    """
    Função para processar arquivos TCX da pasta INPUT, extrair as principais informações
    e salvar os dados em arquivos CSV na pasta OUTPUT.
    
    Args:
        input_dir (str): Diretório onde estão os arquivos TCX (padrão='INPUT')
        output_dir (str): Diretório onde serão salvos os arquivos CSV (padrão='OUTPUT')
    
    Returns:
        int: Número de arquivos processados com sucesso
    """
    import os
    import pandas as pd
    import xml.etree.ElementTree as ET
    from pathlib import Path
    import re
    
    # Criar diretório de saída se não existir
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Namespace padrão usado nos arquivos TCX da Garmin/Strava
    NAMESPACES = {
        'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
        'ns2': 'http://www.garmin.com/xmlschemas/UserProfile/v2',
        'ns3': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2',
        'ns4': 'http://www.garmin.com/xmlschemas/ProfileExtension/v1',
        'ns5': 'http://www.garmin.com/xmlschemas/ActivityGoals/v1'
    }
    
    # Listar todos os arquivos TCX na pasta de entrada
    arquivos_tcx = [f for f in os.listdir(input_dir) if f.endswith('.tcx')]
    
    if not arquivos_tcx:
        print(f"Nenhum arquivo TCX encontrado na pasta {input_dir}")
        return 0
    
    print(f"Processando {len(arquivos_tcx)} arquivos TCX...")
    
    # Contador de arquivos processados
    count_success = 0
    count_errors = 0
    
    for tcx_file in arquivos_tcx:
        try:
            # Caminho completo para o arquivo TCX
            tcx_path = os.path.join(input_dir, tcx_file)
            
            # Nome do arquivo sem extensão
            base_name = os.path.splitext(tcx_file)[0]
            
            # Caminho para o arquivo CSV de saída
            csv_path = os.path.join(output_dir, f"{base_name}.csv")
            
            # Ler o conteúdo do arquivo e corrigir problemas com a declaração XML
            with open(tcx_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Remover espaços em branco e outros caracteres antes da declaração XML
            # ou antes da tag raiz se não houver declaração XML
            match_xml = re.search(r'<\?xml.*?\?>', conteudo)
            if match_xml:
                inicio = match_xml.start()
            else:
                # Se não encontrar declaração XML, procurar a primeira tag
                match_tag = re.search(r'<\w+', conteudo)
                if match_tag:
                    inicio = match_tag.start()
                else:
                    raise Exception(f"Não foi possível encontrar o início do XML no arquivo {tcx_file}")
            
            # Se houver conteúdo indesejado antes do início do XML, remover
            if inicio > 0:
                conteudo_ajustado = conteudo[inicio:]
                
                # Criar arquivo temporário com o conteúdo ajustado
                temp_path = tcx_path + ".temp"
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(conteudo_ajustado)
                
                # Usar o arquivo temporário para o parsing
                try:
                    tree = ET.parse(temp_path)
                    # Remover arquivo temporário após uso bem-sucedido
                    os.remove(temp_path)
                except Exception as e:
                    # Se ainda falhar, tentar outra abordagem
                    os.remove(temp_path)
                    raise Exception(f"Erro no parsing do XML após correção: {str(e)}")
            else:
                # Se o XML já começa no início do arquivo, parse normal
                tree = ET.parse(tcx_path)
            
            root = tree.getroot()
            
            # Lista para armazenar os dados de cada trackpoint
            trackpoints_data = []
            
            # Extrair informações básicas da atividade
            activity_element = root.find('.//ns:Activity', NAMESPACES)
            
            # Tipo de esporte (corrida, ciclismo, etc.)
            sport_type = activity_element.attrib.get('Sport', 'Unknown') if activity_element is not None else 'Unknown'
            
            # Data e ID da atividade
            activity_id = root.find('.//ns:Id', NAMESPACES)
            activity_id_text = activity_id.text if activity_id is not None else 'Unknown'
            
            # Encontrar todos os trackpoints
            trackpoints = root.findall('.//ns:Trackpoint', NAMESPACES)
            
            # Extrair dados de cada trackpoint
            for trackpoint in trackpoints:
                # Dados básicos
                point_data = {
                    'activity_id': activity_id_text,
                    'sport_type': sport_type
                }
                
                # Timestamp
                time_elem = trackpoint.find('./ns:Time', NAMESPACES)
                if time_elem is not None:
                    point_data['timestamp'] = time_elem.text
                
                # Posição (latitude/longitude)
                position = trackpoint.find('./ns:Position', NAMESPACES)
                if position is not None:
                    lat_elem = position.find('./ns:LatitudeDegrees', NAMESPACES)
                    lon_elem = position.find('./ns:LongitudeDegrees', NAMESPACES)
                    
                    if lat_elem is not None and lon_elem is not None:
                        point_data['latitude'] = float(lat_elem.text)
                        point_data['longitude'] = float(lon_elem.text)
                
                # Altitude
                altitude_elem = trackpoint.find('./ns:AltitudeMeters', NAMESPACES)
                if altitude_elem is not None:
                    point_data['altitude'] = float(altitude_elem.text)
                
                # Distância
                distance_elem = trackpoint.find('./ns:DistanceMeters', NAMESPACES)
                if distance_elem is not None:
                    point_data['distance'] = float(distance_elem.text)
                
                # Frequência cardíaca
                heart_rate = trackpoint.find('.//ns:HeartRateBpm/ns:Value', NAMESPACES)
                if heart_rate is not None:
                    point_data['heart_rate'] = int(heart_rate.text)
                
                # Cadência
                cadence = trackpoint.find('./ns:Cadence', NAMESPACES)
                if cadence is not None:
                    point_data['cadence'] = int(cadence.text)
                
                # Extensões (potência, etc.)
                extensions = trackpoint.find('.//ns3:TPX', NAMESPACES)
                if extensions is not None:
                    # Potência (Watts)
                    power = extensions.find('.//ns3:Watts', NAMESPACES)
                    if power is not None:
                        point_data['power'] = float(power.text)
                    
                    # Velocidade
                    speed = extensions.find('.//ns3:Speed', NAMESPACES)
                    if speed is not None:
                        point_data['speed'] = float(speed.text)
                
                # Adicionar ponto à lista se tiver pelo menos latitude e longitude
                if 'latitude' in point_data and 'longitude' in point_data:
                    trackpoints_data.append(point_data)
            
            # Verificar se existem trackpoints
            if not trackpoints_data:
                print(f"Nenhum ponto com coordenadas encontrado no arquivo {tcx_file}")
                count_errors += 1
                continue
            
            # Criar DataFrame e salvar como CSV
            df = pd.DataFrame(trackpoints_data)
            
            # Calcular campos derivados
            if len(df) > 0:
                # Adicionar colunas adicionais de análise
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    
                    # Calcular duração (segundos desde o início)
                    start_time = df['timestamp'].min()
                    df['duration_seconds'] = (df['timestamp'] - start_time).dt.total_seconds()
                
                # Calcular inclinação (gradiente) se tivermos altitude e distância
                if 'altitude' in df.columns and 'distance' in df.columns:
                    df['altitude_diff'] = df['altitude'].diff()
                    df['distance_diff'] = df['distance'].diff()
                    # Evitar divisão por zero
                    mask = df['distance_diff'] > 0
                    if mask.any():
                        df.loc[mask, 'gradient'] = (df.loc[mask, 'altitude_diff'] / df.loc[mask, 'distance_diff']) * 100
            
            # Salvar como CSV
            df.to_csv(csv_path, index=False)
            
            count_success += 1
            print(f"Arquivo processado com sucesso: {tcx_file} -> {csv_path}")
            print(f"  - {len(trackpoints_data)} pontos de coordenadas extraídos")
            
        except Exception as e:
            print(f"Erro ao processar o arquivo {tcx_file}: {str(e)}")
            count_errors += 1
    
    print(f"\nProcessamento concluído!")
    print(f"Total de arquivos: {len(arquivos_tcx)}")
    print(f"Processados com sucesso: {count_success}")
    print(f"Erros: {count_errors}")
    
    return count_success

# ==================================
if __name__ == "__main__":
  # Executa o código
  processar_arquivo_tcx_para_csv('processamento/atividades-tcx', 'processamento/arquivos-csv')  
# ==================================
