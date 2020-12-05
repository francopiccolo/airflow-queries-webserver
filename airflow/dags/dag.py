from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

from datetime import datetime, timedelta

import csv
import requests

default_args = {
            'owner': 'airflow',
            'start_date': datetime(2020, 10, 22),
            'end_date': datetime(2020, 10, 22, 23),
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        }

FIELD_NAMES = ['event', 'time', 'unique_visitor_id', 'ha_user_id', 'browser', 'os', 'country_code']

def process_event(event):
    clean_event = {}
    clean_event['event'] = event['event']
    for property in event['properties']:
        clean_event[property] = event['properties'][property]
    return clean_event

def download_events(**kwargs):
    # from airflow format 2020-10-22T00:00:00+00:00 '%Y-%m-%dT%H:%M:%S%z'
    # to json file format 2020-10-22 20:36:00.178590 '%Y-%m-%d %H:%M:%S.%f'
    execution_time = kwargs['execution_date']
    execution_time_str = datetime.strftime(execution_time, '%Y-%m-%d %H:%M:%S.%f')
    print('execution_time: ', execution_time_str)
    next_execution_time = kwargs['next_execution_date']
    next_execution_time_str = datetime.strftime(next_execution_time, '%Y-%m-%d %H:%M:%S.%f')
    print('next_execution_time: ', next_execution_time_str)

    params = {'time_from': execution_time_str,
              'time_to': next_execution_time_str}
    events = requests.get('http://flask:5000/events', params)
    print(events.json())

    with open('/usr/local/airflow/dags/data/events/{}.csv'.format(execution_time),
              'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        for event in events.json():
            clean_event = process_event(event)
            csv_writer.writerow(clean_event)

with DAG(dag_id='get_events',
         schedule_interval='@hourly',
         default_args=default_args,
         catchup=True) as dag:

    # download_events = PythonOperator(
    #         task_id='download_events',
    #         python_callable=download_events,
    #         provide_context=True
    # )

    save_events = PostgresOperator(
        task_id='save_events',
        postgres_conn_id='pg_dw',
        sql='sqls/events.sql'
    )