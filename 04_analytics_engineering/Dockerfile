FROM python:3.10-slim

WORKDIR /usr/app

# Git installation (needed for dbt packages) + system dependencies for duckdb
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# dbt-duckdb, duckdb, requests (Injest script) and pandas, pyarrow (to manage dataframes & parquet)
# dbt-duckdb installs dbt-core
RUN pip install --no-cache-dir dbt-duckdb duckdb requests pandas pyarrow

# Env variable (profiles.yml)
ENV DBT_PROFILES_DIR=/usr/app

# Keep the container running
CMD ["tail", "-f", "/dev/null"]