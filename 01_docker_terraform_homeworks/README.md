## Question 1

bash
```
docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \
    --entrypoint=bash \
    python:3.13
```

bash
```
pip --version
```

Response: pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

## Question 2
Response: db:5432

## Question 3
Query:
select count(1)
from public.green_taxi_data
where lpep_pickup_datetime between '2025-11-01' and '2025-12-01'
	and trip_distance <= 1
;

Response: 8,007

## Question 4
Query:
with filtered_days as (
	select *
	from public.green_taxi_data
	where trip_distance < 100
), longest_dist as (
	select CAST(fd.lpep_dropoff_datetime AS DATE) as day_trip
		, MAX(fd.trip_distance) as distance
	from filtered_days fd
	group by CAST(fd.lpep_dropoff_datetime AS DATE)
)
select ld.day_trip
	, ld.distance
from longest_dist ld
order by ld.distance Desc
limit 2
;

Response: 2025-11-14, 88.03

## Question 5
Query:
with selected_day as (
	select gt.index
		, gt.total_amount
		, tz."Zone" as trip_zone
	from public.green_taxi_data gt
	join public.taxi_zones tz on gt."PULocationID" = tz."LocationID"
	where CAST(gt.lpep_pickup_datetime AS DATE) = '2025-11-18'
)
select trip_zone
	, SUM(total_amount) as total_zone
from selected_day
group by trip_zone
order by total_zone DESC
;

Response: East Harlem North, 9281.92

## Question 6

with filtered_data as (
	select gt.index
		, gt.trip_distance
		, dotz."Zone" as do_zone_name
	from public.green_taxi_data gt
	join public.taxi_zones putz on gt."PULocationID" = putz."LocationID"
	join public.taxi_zones dotz on gt."DOLocationID" = dotz."LocationID"
	where putz."Zone" = 'East Harlem North'
)
select do_zone_name
	, SUM(trip_distance) as max_trip
from filtered_data fd
group by do_zone_name
order by max_trip DESC
;

Response: Upper East Side North, 2887.52

Anyway, IMO the question is not clear enough, and the query should be:
select gt.trip_distance
	, dotz."Zone" as do_zone_name
from public.green_taxi_data gt
join public.taxi_zones putz on gt."PULocationID" = putz."LocationID"
join public.taxi_zones dotz on gt."DOLocationID" = dotz."LocationID"
where putz."Zone" = 'East Harlem North'
order by trip_distance desc
;

Response: 26.21, Coney Island