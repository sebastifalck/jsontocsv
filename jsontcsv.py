import json
import csv

# Leer archivo JSON desde disco
with open('proyectos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rows = []

for project in data.get('project', []):
    project_name = project.get('name')
    for ms in project.get('ms', []):
        config_str = ms.get('config', '{}')
        config = json.loads(config_str) if isinstance(config_str, str) else config_str

        row = {
            'project_name': project_name,
            'repositoryUrl': ms.get('repositoryUrl'),
            'buildConfigurationMode': ms.get('buildConfigurationMode'),
            'tokenOcp': ms.get('tokenOcp'),
            'appName': config.get('appName'),
            'country': config.get('country'),
            'ocpLabel': config.get('ocpLabel'),
            'project': config.get('project'),
            'baseImageVersion': config.get('baseImageVersion'),
            'secrets': ', '.join([s.get('secretName', '') for s in config.get('secrets', [])]),
            'secrets_enabled': ', '.join([str(s.get('secret', '')) for s in config.get('secrets', [])]),
            'configMaps': ', '.join([c.get('configMapName', '') for c in config.get('configMaps', [])]),
            'configMaps_enabled': ', '.join([str(c.get('configMap', '')) for c in config.get('configMaps', [])]),
            'volumes': ', '.join([v.get('mountPath', '') for v in config.get('volumes', [])]),
            'volumes_enabled': ', '.join([str(v.get('volume', '')) for v in config.get('volumes', [])]),
        }

        quotas = {
            'resQuotasdev': config.get('resQuotasdev'),
            'resQuotasmaster': config.get('resQuotasmaster'),
            'resQuotasqa': config.get('resQuotasqa')
        }

        if quotas['resQuotasdev'] and not quotas['resQuotasmaster'] and not quotas['resQuotasqa']:
            quotas['resQuotasmaster'] = quotas['resQuotasdev']
            quotas['resQuotasqa'] = quotas['resQuotasdev']

        for env, env_data in quotas.items():
            if env_data:
                quota_item = env_data[0] if isinstance(env_data, list) else env_data
                for key in ['cpuLimits', 'cpuRequest', 'memoryLimits', 'memoryRequest', 'replicas']:
                    row[f'{env}_{key}'] = quota_item.get(key)

        rows.append(row)

headers = sorted(set().union(*(r.keys() for r in rows)))

with open('microservices_config.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(\"CSV generado correctamente como 'microservices_config.csv'\")
