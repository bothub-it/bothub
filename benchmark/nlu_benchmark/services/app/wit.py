import os

import requests

from app.utils import load_json_file


def get_expressions_data(source):
    files = os.listdir(source)
    for filename in files:
        file_item = os.path.join(source, filename)

        if filename == 'expressions.json':
            return load_json_file(file_item)
    return None


def get_intent_data(result, intent):
    entity = result['entities']
    if intent in entity:
        return entity[intent][0]


def get_intent_from_input(intent, file_item):
    entities_files = os.listdir(file_item)

    for entity_filename in entities_files:
        entity_file = os.path.join(file_item, entity_filename)
        data = load_json_file(entity_file)

        if intent in data['data']['name']:
            return data
    return None


def analyze(text, token):
    params = {'q': text}
    headers = {'Authorization': token}
    response = requests.get('https://api.wit.ai/message', params=params, headers=headers)
    return response.json()
