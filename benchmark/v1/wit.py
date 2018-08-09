import os
import json
import requests

from app.utils import load_json_file
from app.settings import WIT_APP_URL, WIT_TOKEN, WIT_API_VERSION

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


def read_wit_and_push_bothub(expression):
    text = expression['text']
    wit_entities = expression['entities']
    filtered_entities = []
    intent = ''
    for entity in wit_entities:
        if entity['entity'] == 'intent':
            intent = entity['value'].strip('\"')
        else:
            new_entity = {}
            new_entity['entity'] = entity['entity']
            new_entity['start'] = entity['start']
            new_entity['end'] = entity['end']
            filtered_entities.append(new_entity)
    return [text, filtered_entities, intent]


def analyze(text):
    params = {'q':text, 'v':WIT_API_VERSION}
    headers = {'Authorization':WIT_TOKEN}
    response = requests.get(WIT_APP_URL, params=params, headers=headers)
    response_json = json.loads(response.content)
    return response_json

def store_wit_result(expression, wit_result):
    prediction_result = 'OK'
    detected_entities = '-'
    if 'intent' in wit_result['entities']:
        if wit_result['entities']['intent'][0]['value'] != expression['intent']:
            prediction_result = 'FAILURE'
            for key in wit_result['entities']:
                if key != 'intent':
                    detected_entities += '{}-'.format(key)
        return '{0},{1},{2},{3}%,{4},{5}'.format(expression['value'], expression['intent'], wit_result['entities']['intent'][0]['value'],int(float(wit_result['entities']['intent'][0]['confidence'])*100),prediction_result,detected_entities)
    else:
        prediction_result = 'FAILURE'
        return '{0},{1},,,{2},'.format(expression['value'], expression['intent'],prediction_result)


def write_csv_file_from_wit(data, csv_footer):
    csv_headers = "Phrases,Expected intents,wit predicts,Confidence,Result,Detected entities\n"
    with open('wit_output.csv', "w") as csv_file:
        csv_file.write(csv_headers)
        for line in data:
            csv_file.write(line)
            csv_file.write('\n')
        csv_file.write('\n' + csv_footer)