from datetime import datetime

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator


default_args = {
            'owner': 'airflow',
            'start_date': datetime(2020, 10, 22)
        }

with DAG(dag_id='ddl',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    create_events = PostgresOperator(
        task_id='create_events',
        postgres_conn_id='pg_dw',
        sql='sqls/events.sql'
    )

    create_countries = PostgresOperator(
        task_id='create_countries',
        postgres_conn_id='pg_dw',
        sql='sqls/countries.sql'
    )