import json

from flask import Flask, request

app = Flask(__name__)

@app.route('/events', methods=['GET'])
def query():
    event_type = request.args.get('event_type')
    time_from = request.args.get('time_from')
    time_to = request.args.get('time_to')

    with open('events_20201022.json', 'r') as f:
        events = json.load(f)

    if event_type:
        events = [
            event for event in events
            if event['event'] == event_type
        ]

    if time_from:
        events = [
            event for event in events
            if event['properties']['time'] >= time_from
        ]

    if time_to:
        events = [
            event for event in events
            if event['properties']['time'] < time_to
        ]

    return json.dumps(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0')