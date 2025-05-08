import json
import csv
import os

# Carpeta donde están todos los archivos JSON
carpeta = 'ruta/a/la/carpeta'  # <- Cambia esto por la ruta real

# Lista para filas del CSV
rows = []

# Iterar sobre todos los archivos .json en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.json'):
        ruta_completa = os.path.join(carpeta, archivo)
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for project in data.get('project', []):
                    project_name = project.get('name', '')
                    for db in project.get('db', []):
                        rows.append({
                            'project_name': project_name,
                            'repositoryUrl': db.get('repositoryUrl', ''),
                            'type': db.get('type', ''),
                            'source_file': archivo  # para saber de qué JSON vino
                        })
            except Exception as e:
                print(f"Error procesando {archivo}: {e}")

# Escribir archivo CSV consolidado
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['project_name', 'repositoryUrl', 'type', 'source_file']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)

print("CSV consolidado generado como 'output.csv'")
