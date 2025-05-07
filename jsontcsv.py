import json
import csv

# Leer archivo JSON desde disco
with open('proyectos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lista para almacenar filas del CSV
rows = []

# Procesar cada proyecto y microservicio
for project in data['project']:
    project_name = project['name']
    for ms in project['ms']:
        config = json.loads(ms['config'])  # Deserializar el string JSON de "config"
        row = {
            'project_name': project_name,
            'repositoryUrl': ms['repositoryUrl'],
            'buildConfigurationMode': ms['buildConfigurationMode'],
            'tokenOcp': ms['tokenOcp'],
            'appName': config.get('appName'),
            'country': config.get('country'),
            'ocpLabel': config.get('ocpLabel'),
            'project': config.get('project'),
            'baseImageVersion': config.get('baseImageVersion'),
            'secrets': ', '.join([s.get('secretName', '') for s in config.get('secrets', [])]),
            'configMaps': ', '.join([c.get('configMapName', '') for c in config.get('configMaps', [])]),
            'volumes': ', '.join([v.get('mountPath', '') for v in config.get('volumes', [])]),
        }

        # Lógica para normalizar los entornos
        quotas = {
            'resQuotasdev': config.get('resQuotasdev'),
            'resQuotasmaster': config.get('resQuotasmaster'),
            'resQuotasqa': config.get('resQuotasqa')
        }

        # Si solo tiene resQuotasdev, replicar para master y qa
        if quotas['resQuotasdev'] and not quotas['resQuotasmaster'] and not quotas['resQuotasqa']:
            quotas['resQuotasmaster'] = quotas['resQuotasdev']
            quotas['resQuotasqa'] = quotas['resQuotasdev']

        for env, env_data in quotas.items():
            if env_data:
                for key in ['cpuLimits', 'cpuRequest', 'memoryLimits', 'memoryRequest', 'replicas']:
                    row[f'{env}_{key}'] = env_data[0].get(key)

        rows.append(row)

# Obtener encabezados unificados
headers = sorted(set().union(*(r.keys() for r in rows)))

# Escribir archivo CSV
with open('microservices_config.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print("CSV generado correctamente como 'microservices_config.csv'")
