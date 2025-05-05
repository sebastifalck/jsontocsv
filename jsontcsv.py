import json
import csv

# Archivo JSON de entrada
input_json = 'archivo.json'

# Archivo CSV de salida
output_csv = 'archivo.csv'

# Cargar datos del archivo JSON
with open(input_json, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Asumiendo que el JSON es una lista de diccionarios
if isinstance(data, list) and len(data) > 0:
    keys = data[0].keys()

    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Archivo CSV '{output_csv}' creado exitosamente.")
else:
    print("El JSON debe ser una lista de diccionarios.")
