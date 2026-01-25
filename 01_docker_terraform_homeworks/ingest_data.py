#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


def load_yellow_taxi_data_from_csv(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    """Download and ingest Yellow Taxi CSV data."""
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    print(f"Connecting to database {pg_db} on {pg_host}...")
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    print(f"Downloading CSV data from {url}...")
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )
    print("Ingestion completed successfully.")


def load_green_taxi_data_from_parquet(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table):
    """Download and ingest Green Taxi Parquet data."""
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet"
    
    print(f"Connecting to database {pg_db} on {pg_host}...")
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    print(f"Downloading Parquet file from {url}...")
    df = pd.read_parquet(url)
    
    print(f"Successfully downloaded {len(df)} rows.")
    
    # Parquet files are typically small enough to load at once, 
    # but we follow a similar pattern for table creation.
    print(f"Inserting data into table {target_table}...")
    df.head(0).to_sql(name=target_table, con=engine, if_exists='replace')
    df.to_sql(name=target_table, con=engine, if_exists='append')
    print("Ingestion completed successfully.")


def load_taxi_zones(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    """Download and ingest Taxi Zones data."""
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    
    print(f"Connecting to database {pg_db} on {pg_host}...")
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    print(f"Downloading Zones CSV from {url}...")
    df = pd.read_csv(url)
    
    print(f"Successfully downloaded {len(df)} rows.")
    
    print(f"Inserting data into table {target_table}...")
    df.to_sql(name=target_table, con=engine, if_exists='replace', index=False)
    print("Ingestion completed successfully.")


@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5433, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--target-yellow-table', default='yellow_taxi_data', help='Target table name')
@click.option('--target-green-table', default='green_taxi_data', help='Target table name')
@click.option('--target-zones-table', default='taxi_zones', help='Target zones table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
@click.option('--taxi-type', default='green', type=click.Choice(['yellow', 'green', 'zones']), help='Type of taxi data (yellow/green/zones)')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_yellow_table, target_green_table, target_zones_table, chunksize, taxi_type):
    """Ingest NYC taxi data into PostgreSQL database."""
    if taxi_type == 'yellow':
        load_yellow_taxi_data_from_csv(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_yellow_table, chunksize)
    elif taxi_type == 'green':
        load_green_taxi_data_from_parquet(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_green_table)
    elif taxi_type == 'zones':
        load_taxi_zones(pg_user, pg_pass, pg_host, pg_port, pg_db, target_zones_table)


if __name__ == '__main__':
    run()