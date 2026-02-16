#!/bin/bash

# Detener el script si hay errores
set -e

# Nombre del archivo de base de datos
DB_FILE="taxi_rides_ny.duckdb"

echo "🚀 Iniciando entorno dbt + DuckDB con Podman..."

# 1. Levantar el contenedor en segundo plano (detached)
# Usamos docker-compose para orquestar (podman-compose si lo tienes aliasado)
docker compose up -d --build

echo "📦 Contenedor 'dbt-duckdb' levantado y corriendo."

# 2. Verificar si la base de datos ya existe
if [ -f "$DB_FILE" ]; then
    echo "✅ La base de datos '$DB_FILE' ya existe."
    echo "⏭️  Saltando la ingestión de datos."
else
    echo "⚠️  La base de datos '$DB_FILE' no se encontró."
    echo "⏳ Ejecutando script de ingestión de datos (esto puede tardar unos minutos)..."
    
    # Ejecutar el script de python DENTRO del contenedor
    docker compose exec dbt-duckdb python ingest_data.py
    
    echo "✅ Ingestión completada. Base de datos creada."
fi

# 3. Testear la conexión dbt
echo "🛠  Verificando conexión dbt..."

# Asumimos que el proyecto dbt está en la subcarpeta taxi_rides_ny
# --project-dir le dice a dbt dónde buscar el dbt_project.yml
docker compose exec dbt-duckdb dbt debug --project-dir taxi_rides_ny

echo "----------------------------------------------------------------"
echo "🎉 ¡Todo listo!"
echo ""
echo "💡 Comandos útiles:"
echo "   - Entrar al shell:   docker-compose exec dbt-duckdb /bin/bash"
echo "   - Correr modelos:    docker-compose exec dbt-duckdb dbt run --project-dir taxi_rides_ny"
echo "   - Abrir UI SQL:      docker-compose exec dbt-duckdb harlequin $DB_FILE"
echo ""
echo "Entrando a la terminal del contenedor..."
echo "Escribe 'exit' para salir."
echo "----------------------------------------------------------------"

# 4. Abrir shell interactiva
docker compose exec dbt-duckdb /bin/bash