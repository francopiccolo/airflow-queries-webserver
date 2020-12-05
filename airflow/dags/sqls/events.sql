CREATE TABLE IF NOT EXISTS events (
    event               VARCHAR(10),
    time                TIMESTAMP,
    unique_visitor_id   VARCHAR(100),
    ha_user_id          VARCHAR(100),
    browser             VARCHAR(10),
    os                  VARCHAR(10),
    country_code        VARCHAR(10)
);

COPY events
FROM '/usr/local/airflow/dags/data/events/{{ execution_date }}.csv';



