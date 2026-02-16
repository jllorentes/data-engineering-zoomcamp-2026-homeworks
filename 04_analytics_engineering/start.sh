#!/bin/bash

# Detener el script si hay errores
set -e

echo "🚀 Iniciando entorno dbt + DuckDB con Podman..."

# 1. Levantar el contenedor en segundo plano (detached)
# Usamos docker-compose, que podman suele alias o tener podman-compose
docker-compose up -d --build

echo "📦 Contenedor levantado."
echo "⏳ Ejecutando script de ingestión de datos (esto puede tardar unos minutos)..."

# 2. Ejecutar el script de python DENTRO del contenedor
docker-compose exec dbt-duckdb python ingest_data.py

echo "✅ Ingestión completada. Base de datos 'taxi_rides_ny.duckdb' creada."

# 3. Testear la conexión dbt
echo "r🛠 Verificando conexión dbt..."

# Asumimos que el proyecto dbt está en la subcarpeta taxi_rides_ny
# --project-dir le dice a dbt dónde buscar el dbt_project.yml
docker-compose exec dbt-duckdb dbt debug --project-dir taxi_rides_ny

echo "🎉 ¡Todo listo!"
echo "Entrando a la terminal del contenedor para que puedas ejecutar 'dbt run', 'dbt test', etc."
echo "Escribe 'exit' para salir."
echo "----------------------------------------------------------------"

# 4. Abrir shell interactiva
docker-compose exec dbt-duckdb /bin/bash