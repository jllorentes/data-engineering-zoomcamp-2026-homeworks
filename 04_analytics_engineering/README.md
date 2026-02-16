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
