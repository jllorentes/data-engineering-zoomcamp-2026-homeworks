
Run the containers with podman
```bash
podman compose up
```

Results are calculated counting rows in the DB

```bash
select count(1)
from public.yellow_tripdata
where EXTRACT(YEAR FROM tpep_pickup_datetime) = 2020
;
```

```bash
select count(1)
from public.green_tripdata
where EXTRACT(YEAR FROM tpep_pickup_datetime) = 2020
;
```