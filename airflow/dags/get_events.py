from datetime import datetime

import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks import PostgresHook


default_args = {
            'owner': 'airflow',
            'start_date': datetime(2020, 10, 22),
            'end_date': datetime(2020, 10, 22, 23)
        }

FIELD_NAMES = ['event', 'time', 'unique_visitor_id', 'ha_user_id', 'browser', 'os', 'country_code']

def process_event(event):
    clean_event = {}
    clean_event['event'] = event['event']
    for property in event['properties']:
        clean_event[property] = event['properties'][property]
    return clean_event

def insert_events(**kwargs):
    # airflow format 2020-10-22T00:00:00+00:00 '%Y-%m-%dT%H:%M:%S%z'
    # json file format 2020-10-22 20:36:00.178590 '%Y-%m-%d %H:%M:%S.%f'
    execution_time = kwargs['execution_date']
    execution_time_str = datetime.strftime(execution_time, '%Y-%m-%d %H:%M:%S.%f')
    print('execution_time: ', execution_time_str)
    next_execution_time = kwargs['next_execution_date']
    next_execution_time_str = datetime.strftime(next_execution_time, '%Y-%m-%d %H:%M:%S.%f')
    print('next_execution_time: ', next_execution_time_str)

    params = {'time_from': execution_time_str,
              'time_to': next_execution_time_str}

    events = requests.get('http://nginx:80/events', params)
    print(events.json())

    pg_hook = PostgresHook(postgres_conn_id='pg_dw')
    query = """
        INSERT INTO events_stg (event, time, unique_visitor_id, ha_user_id, browser, os, country_code)
        VALUES ('{}', '{}', NULLIF('{}', 'None'), NULLIF('{}', 'None'), NULLIF('{}', 'None'), NULLIF('{}', 'None'), NULLIF('{}', 'None'))
    """
    for event in events.json():
        clean_event = process_event(event)
        pg_hook.run(query.format(clean_event['event'], clean_event['time'], clean_event['unique_visitor_id'], clean_event['ha_user_id'], clean_event['browser'], clean_event['os'], clean_event['country_code']))

with DAG(dag_id='get_events',
         schedule_interval='@hourly',
         default_args=default_args,
         catchup=True) as dag:

    insert_events = PythonOperator(
            task_id='insert_events',
            python_callable=insert_events,
            provide_context=True
    )

    clean_events = PostgresOperator(
        task_id='clean_events',
        postgres_conn_id='pg_dw',
        sql='sqls/clean_events.sql'
    )

    insert_events >> clean_events