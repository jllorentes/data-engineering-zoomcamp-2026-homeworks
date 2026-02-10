# Data Engineering Zoomcamp 2026

## Homework 3

Preparation:
** Upload files in GCP Bucket:

```bash
uv venv
uv sync
```

```bash
uv run python load_yellow_taxi_data.py
```

** BigQuery setup

```bash
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-homeworks-486920.taxi_rides_ny.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://dezoomcamp_jl_hw3_2026/yellow_tripdata_2024-*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned` AS
SELECT * FROM `de-zoomcamp-homeworks-486920.taxi_rides_ny.external_yellow_tripdata`;

```

### Question 1
```bash
-- Q1. What is count of records for the 2024 Yellow Taxi Data?
select count(1)
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned`
;
```

Response: 20332093

### Question 2
```bash
-- Q2. 
--155.12 Mb
select count(distinct(PULocationID))
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned`
;
-- 0 Mb
select count(distinct(PULocationID))
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.external_yellow_tripdata`
;
```

### Question 3
```bash
--155.12 Mb
select PULocationID
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned`
;

-- 310.24 MB
select PULocationID
  , DOLocationID
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned`
;
```

### Question 4
```bash
-- Q4. How many records have a fare_amount of 0?
select count(1)
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned`
where fare_amount = 0
;
```

### Question 5
```bash
-- Q5
CREATE TABLE `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `de-zoomcamp-homeworks-486920.taxi_rides_ny.external_yellow_tripdata`;
```

### Question 6
```bash
-- Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
-- 310.24 MB
select distinct(VendorID)
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned`
where tpep_dropoff_datetime between '2024-03-01' AND '2024-03-15';

-- 26.84 MB
select distinct(VendorID)
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_optimized`
where tpep_dropoff_datetime between '2024-03-01' AND '2024-03-15';
```

### Question 7

GCP Bucket.
Creating an external table, we create a metadata pointer inside BigQuery that tells it how to read files directly from GCS.

### Question 8

False. Clustering is useful only when it matches our query patterns, not as a universal best practice.

### Question 9
```bash
-- Q9
SELECT count(*)  
from `de-zoomcamp-homeworks-486920.taxi_rides_ny.yellow_tripdata_non_partitioned`;
```

0 Mb. Because for a native materialized / physical table, BigQuery already stores:
* table metadata
* row count statistics
* storage statistics

So for this query BigQuery does NOT need to scan the data blocks. Instead it: 
* reads metadata
* uses internal statistics
* returns the count
