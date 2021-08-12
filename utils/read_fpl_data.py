import os
import json

filepath = 'data/fpl-bootstrap-static.json'

def read_json_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def get_match_deadlines(data: dict = None) -> list:
    match_deadlines = [(match['name'], match['deadline_time_epoch']) for match in data['events']]
    return match_deadlines

print('here')
