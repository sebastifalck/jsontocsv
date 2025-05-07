import json
import csv

# Cargar el archivo JSON
with open("proyectos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Definir columnas del CSV
fieldnames = [
    "project_name",
    "app_name",
    "country",
    "ocp_label",
    "project_folder",
    "base_image_version",
    "repository_url",
    "token_ocp",
    "build_configuration_mode",

    "secrets",
    "config_maps",
    "volumes",

    # Recursos MASTER
    "cpu_limits_master", "cpu_request_master",
    "memory_limits_master", "memory_request_master", "replicas_master",

    # Recursos DEV
    "cpu_limits_dev", "cpu_request_dev",
    "memory_limits_dev", "memory_request_dev", "replicas_dev",

    # Recursos QA
    "cpu_limits_qa", "cpu_request_qa",
    "memory_limits_qa", "memory_request_qa", "replicas_qa"
]

# Escribir el archivo CSV
with open("microservicios_convertido.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for project in data.get("project", []):
        project_name = project.get("name", "")

        for ms in project.get("ms", []):
            # Decodificar config si es un string JSON embebido
            config_raw = ms.get("config", "{}")
            config = json.loads(config_raw) if isinstance(config_raw, str) else config

            # Usar resQuotasdev como fallback para master y qa si no existen
            dev = config.get("resQuotasdev", {})
            master = config.get("resQuotasmaster", dev)
            qa = config.get("resQuotasqa", dev)

            secrets = ";".join([s.get("secretName") for s in config.get("secrets", []) if s.get("secret")])
            config_maps = ";".join([cm.get("configMapName") for cm in config.get("configMaps", []) if cm.get("configMap")])
            volumes = ";".join([v.get("mountPath") for v in config.get("volumes", []) if v.get("volume")])

            writer.writerow({
                "project_name": project_name,
                "app_name": config.get("appName", ""),
                "country": config.get("country", ""),
                "ocp_label": config.get("ocpLabel", ""),
                "project_folder": config.get("project", ""),
                "base_image_version": config.get("baseImageVersion", ""),
                "repository_url": ms.get("repositoryUrl", ""),
                "token_ocp": ms.get("tokenOcp", ""),
                "build_configuration_mode": ms.get("buildConfigurationMode", ""),

                "secrets": secrets,
                "config_maps": config_maps,
                "volumes": volumes,

                # MASTER
                "cpu_limits_master": master.get("cpuLimits", ""),
                "cpu_request_master": master.get("cpuRequest", ""),
                "memory_limits_master": master.get("memoryLimits", ""),
                "memory_request_master": master.get("memoryRequest", ""),
                "replicas_master": master.get("replicas", ""),

                # DEV
                "cpu_limits_dev": dev.get("cpuLimits", ""),
                "cpu_request_dev": dev.get("cpuRequest", ""),
                "memory_limits_dev": dev.get("memoryLimits", ""),
                "memory_request_dev": dev.get("memoryRequest", ""),
                "replicas_dev": dev.get("replicas", ""),

                # QA
                "cpu_limits_qa": qa.get("cpuLimits", ""),
                "cpu_request_qa": qa.get("cpuRequest", ""),
                "memory_limits_qa": qa.get("memoryLimits", ""),
                "memory_request_qa": qa.get("memoryRequest", ""),
                "replicas_qa": qa.get("replicas", "")
            })
