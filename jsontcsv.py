import os
import json
import csv

# Rutas de los archivos
json_file = 'Chile-MICROSERVICES.json'
token_file = 'token.json'

# Cargar tokens
with open(token_file, encoding='utf-8') as f:
    tokens = json.load(f)

# Combinatoria de secretos/configmaps/volumes
def combinatoria_id(secrets, configmap, volumes):
    return 1 + (4 if secrets else 0) + (2 if configmap else 0) + (1 if volumes else 0)

# Ambientes
ambientes = ['dev', 'qa', 'prod']

rows = []

with open(json_file, encoding='utf-8') as f:
    data = json.load(f)

for project in data.get('projects', []):
    project_name = project.get('name')
    for ms in project.get('ms', []):
        config = ms.get('config', {})
        app_name = config.get('appName')
        country = config.get('country')
        ocp_label = config.get('ocpLabel')
        base_image = config.get('baseImageVersion')
        repo_url = ms.get('repositoryUrl')
        token_key = ms.get('tokenOcp')
        token_value = tokens.get(token_key, '') if token_key else ''
        # Secretos/configmaps/volumes
        secrets = any(x.get('secret', True) for x in config.get('secrets', []))
        configmaps = any(x.get('configMap', True) for x in config.get('configMaps', []))
        volumes = any(x.get('volume', True) for x in config.get('volumes', []))
        combin_id = combinatoria_id(secrets, configmaps, volumes)
        # resQuotas por ambiente
        res_amb = {}
        for amb in ambientes:
            rq = config.get(f'resQuotas{amb}', None)
            if rq:
                res_amb[amb] = rq if isinstance(rq, dict) else rq[0]
        # Si hay resQuotas general, usar para todos
        if 'resQuotas' in config:
            for amb in ambientes:
                rq = config['resQuotas'][0] if isinstance(config['resQuotas'], list) else config['resQuotas']
                res_amb[amb] = rq
        # Si no hay resQuotas, poner None para todos
        if not res_amb:
            for amb in ambientes:
                res_amb[amb] = None
        # Fila por ambiente
        for amb in ambientes:
            rq = res_amb[amb]
            row = {
                'project_name': project_name,
                'appName': app_name,
                'country': country,
                'ocpLabel': ocp_label,
                'baseImageVersion': base_image,
                'repositoryUrl': repo_url,
                'token': token_value,
                'ambiente': amb,
                'secrets_enabled': secrets,
                'configmap_enabled': configmaps,
                'volumes_enabled': volumes,
                'combinatoria_id': combin_id,
            }
            if rq:
                row.update({
                    'cpuLimits': rq.get('cpuLimits'),
                    'cpuRequest': rq.get('cpuRequest'),
                    'memoryLimits': rq.get('memoryLimits'),
                    'memoryRequest': rq.get('memoryRequest'),
                    'replicas': rq.get('replicas'),
                })
            rows.append(row)

# Encabezados ordenados
headers = [
    'project_name', 'appName', 'country', 'ocpLabel', 'baseImageVersion', 'repositoryUrl',
    'token', 'ambiente', 'secrets_enabled', 'configmap_enabled', 'volumes_enabled',
    'combinatoria_id', 'cpuLimits', 'cpuRequest', 'memoryLimits', 'memoryRequest', 'replicas'
]

with open('microservices_config.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print("✅ CSV final generado como 'microservices_config.csv'")
