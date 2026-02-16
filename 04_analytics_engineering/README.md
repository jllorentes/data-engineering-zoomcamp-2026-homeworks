How to build the containers (create the environment), injest and test:
* Giving rights to execute the script:
```bash
chmod +x start.sh
```
* Execute teh script:
```bash
./start.sh
```

Results after running the script:
* The script will download the data and create the taxi_rides_ny.duckdb file in our local folder (thanks to the volume).
* It will configure dbt.
* Finally, it will leave us at a terminal that looks like this: root@<container_id>:/usr/app#.
* From there, we can run our normal dbt commands:
```bash
cd taxi_rides_ny
dbt run
dbt test
```
* Since we are using Containers (Podman) and volumes, any changes we make to our .sql templates in our local code editor will be immediately reflected inside the container.

* Access Duckdb UI:
```bash
docker-compose exec duckdb-cli duckdb /data/taxi_rides_ny.duckdb
```

# Homework 4

## Q1. 
```bash
dbt run --select int_trips_unioned --target prod
```

```bash
Running with dbt=1.11.5
22:32:47  Registered adapter: duckdb=1.10.0
22:32:48  Found 8 models, 2 seeds, 33 data tests, 2 sources, 618 macros
22:32:48  
22:32:48  Concurrency: 1 threads (target='prod')
22:32:48  
22:32:48  1 of 1 START sql table model prod.int_trips_unioned ............................ [RUN]
22:34:32  1 of 1 OK created sql table model prod.int_trips_unioned ....................... [OK in 103.74s]
22:34:32  
22:34:32  Finished running 1 table model in 0 hours 1 minutes and 44.14 seconds (104.14s).
22:34:32  
22:34:32  Completed successfully
22:34:32  
22:34:32  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=1
```

Answer: int_trips_unioned only

## Q2.

```bash
dbt test --select fct_trips --target prod
```

Answer: dbt will fail the test, returning a non-zero exit code

## Q3.

```bash
select count(1)
from taxi_rides_ny.prod.fct_monthly_zone_revenue
;
```
Answer: 12184

## Q4.

```bash
select pickup_zone
    , sum(revenue_monthly_total_amount) as sum_revenue_monthly_total_amount
from taxi_rides_ny.prod.fct_monthly_zone_revenue
where year(revenue_month) = 2020
    and service_type = 'Green'
group by pickup_zone
order by sum_revenue_monthly_total_amount desc
limit 1
;
```

Answer: 'East Harlem North'

## Q5.

```bash
select sum(total_amount)
from taxi_rides_ny.prod.fct_monthly_zone_revenue
where year(revenue_month) = 2019
    and month(revenue_month) = 10
    and service_type = 'Green'
;
```

Answer: 384624

## Q6.

```bash
select count(1)
from taxi_rides_ny.prod.stg_fhv_tripdata
;
```

Answer: 43244693

