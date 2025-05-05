import json
import csv

# Archivos
input_file = 'Colombia-MICROSERVICES.json'
output_file = 'output_microservices_full.csv'

# Cargar JSON
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Columnas del CSV según el JSON proporcionado
fieldnames = [
    'projectName', 'repositoryUrl', 'buildConfigurationMode', 'tokenOcp',
    'appName', 'country', 'ocpLabel', 'projectInternal', 'baseImageVersion',
    'secret', 'secretName',
    'configMap', 'configMapName',
    'volume', 'mountPath',
    'environment', 'cpuLimits', 'cpuRequest', 'memoryLimits', 'memoryRequest', 'replicas'
]

rows = []

# Procesar proyectos
for project in data.get('project', []):
    project_name = project.get('name', '')
    for ms in project.get('ms', []):
        # Validar config
        config_raw = ms.get('config', {})
        config = config_raw if isinstance(config_raw, dict) else {}

        # Extraer secretos
        secret_data = config.get('secrets', [{}])[0] if config.get('secrets') else {}
        secret = secret_data.get('secret', '')
        secret_name = secret_data.get('secretName', '')

        # ConfigMaps
        config_map_data = config.get('configMaps', [{}])[0] if config.get('configMaps') else {}
        config_map = config_map_data.get('configMap', '')
        config_map_name = config_map_data.get('configMapName', '')

        # Volúmenes
        volume_data = config.get('volumes', [{}])[0] if config.get('volumes') else {}
        volume = volume_data.get('volume', '')
        mount_path = volume_data.get('mountPath', '')

        # Comunes
        row_common = {
            'projectName': project_name,
            'repositoryUrl': ms.get('repositoryUrl', ''),
            'buildConfigurationMode': ms.get('buildConfigurationMode', ''),
            'tokenOcp': ms.get('tokenOcp', ''),
            'appName': config.get('appName', ''),
            'country': config.get('country', ''),
            'ocpLabel': config.get('ocpLabel', ''),
            'projectInternal': config.get('project', ''),
            'baseImageVersion': config.get('baseImageVersion', ''),
            'secret': secret,
            'secretName': secret_name,
            'configMap': config_map,
            'configMapName': config_map_name,
            'volume': volume,
            'mountPath': mount_path
        }

        # Cuotas por entorno
        quotas = {
            'dev': config.get('resQuotasdev', {}),
            'qa': config.get('resQuotasqa', config.get('resQuotasdev', {})),
            'master': config.get('resQuotasmaster', config.get('resQuotasdev', {}))
        }

        for env, q in quotas.items():
            q = q if isinstance(q, dict) else {}  # Protección contra errores
            row = row_common.copy()
            row['environment'] = env
            row['cpuLimits'] = q.get('cpuLimits', '')
            row['cpuRequest'] = q.get('cpuRequest', '')
            row['memoryLimits'] = q.get('memoryLimits', '')
            row['memoryRequest'] = q.get('memoryRequest', '')
            row['replicas'] = q.get('replicas', '')
            rows.append(row)

# Escribir CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ CSV generado correctamente: {output_file}")
