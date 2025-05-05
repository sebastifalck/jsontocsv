import json
import csv

# Archivos
input_file = 'Colombia-MICROSERVICES.json'
output_file = 'output_microservices_full.csv'

# Cargar JSON
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Definir columnas del CSV
fieldnames = [
    'projectName', 'repositoryUrl', 'buildConfigurationMode', 'tokenOcp',
    'appName', 'country', 'ocplabel', 'baseImageVersion',
    'projectInternal', 'configMapName', 'volumePath',
    'environment', 'cpuLimits', 'cpuRequest', 'memoryLimits', 'memoryRequest', 'replicas'
]

rows = []

# Procesar cada proyecto
for project in data.get('project', []):
    project_name = project.get('name', '')
    for ms in project.get('ms', []):
        config = ms.get('config', {})

        # General fields
        row_common = {
            'projectName': project_name,
            'repositoryUrl': ms.get('repositoryUrl', ''),
            'buildConfigurationMode': ms.get('buildConfigurationMode', ''),
            'tokenOcp': ms.get('tokenOcp', ''),
            'appName': config.get('appName', ''),
            'country': config.get('country', ''),
            'ocplabel': config.get('ocplabel', ''),
            'baseImageVersion': config.get('baseImageVersion', ''),
            'projectInternal': config.get('project', ''),
            'configMapName': ''
        }

        # ConfigMap (extrae el primer configMapName si existe)
        config_map_list = config.get('configMaps', [])
        if config_map_list and isinstance(config_map_list[0], dict):
            row_common['configMapName'] = config_map_list[0].get('configMapName', '')

        # Volumes (extrae el primer path si existe)
        volume_list = config.get('volumes', [])
        if volume_list and isinstance(volume_list[0], dict):
            row_common['volumePath'] = volume_list[0].get('Path', '')

        # Obtener cuotas
        quotas = {
            'dev': config.get('resQuotasdev', {}),
            'qa': config.get('resQuotasqa', config.get('resQuotasdev', {})),
            'master': config.get('resQuotasmaster', config.get('resQuotasdev', {}))
        }

        for env, quota in quotas.items():
            row = row_common.copy()
            row['environment'] = env
            row['cpuLimits'] = quota.get('cpuLimits', '')
            row['cpuRequest'] = quota.get('cpuRequest', '')
            row['memoryLimits'] = quota.get('memoryLimits', '')
            row['memoryRequest'] = quota.get('memoryRequest', '')
            row['replicas'] = quota.get('replicas', '')
            rows.append(row)

# Escribir CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV generado con éxito: {output_file}")
