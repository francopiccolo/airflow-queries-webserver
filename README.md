# airflow-queries-webserver


1. Place file `events_20201022.json` under `flask` directory.
2. Run `docker-compose up`   

Then in the Airflow UI:    
1. Create `pg_dw` connection with `conn_type` `Postgres`, `Login`, `Schema` and `password` equal to `airflow`, `Host` `pg_dw` and `Port` `5432`
2. Enable and trigger `ddl` dag.
3. Enable and let finish `get_events` dag.
4. Check results in AdHoc queries running: `SELECT * FROM events;`