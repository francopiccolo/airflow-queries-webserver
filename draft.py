import csv

import requests

FIELD_NAMES = ['event', 'time', 'unique_visitor_id', 'ha_user_id', 'browser', 'os', 'country_code']

def process_event(event):
    clean_event = {}
    clean_event['event'] = event['event']
    for property in event['properties']:
        clean_event[property] = event['properties'][property]
    return clean_event

def download_events(**kwargs):
    execution_time = kwargs['execution_date']
    next_execution_time = kwargs['next_execution_date']

    params = {'time_from': execution_time,
              'time_to': next_execution_time}
    events = requests.get('http://localhost:5000/events', params)
    print(min([event['properties']['time'] for event in events.json()]))
    print(max([event['properties']['time'] for event in events.json()]))


download_events(execution_date='2020-01-01 00:00:00',
                next_execution_date='2020-12-31 00:00:00')