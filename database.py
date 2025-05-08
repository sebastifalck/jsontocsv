import json
import csv

# Leer el archivo JSON
with open('Chile-DATABASE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lista para filas de CSV
rows = []

# Iterar sobre los proyectos y bases de datos
for project in data.get('project', []):
    project_name = project.get('name')
    for db in project.get('db', []):
        rows.append({
            'project_name': project_name,
            'repositoryUrl': db.get('repositoryUrl', ''),
            'type': db.get('type', '')
        })

# Escribir en archivo CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['project_name', 'repositoryUrl', 'type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)

print("CSV generado como 'output.csv'")
