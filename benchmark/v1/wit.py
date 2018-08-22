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
    known_entities = '-'
    wit_entities_count = 0
    known_entities_count = 0
    matched_entities = 0
    entity_result = ''
    entities_percentage = 0
    for known_entity in expression['entities']:
        known_entities_count += 1
        known_entities += '{0}("{1}")-'.format(known_entity['entity'],known_entity['value'])
    
    for key in wit_result['entities']:
        if key != 'intent':
            wit_entities_count += 1
            detected_entities += '{0}("{1}")-'.format(key,(wit_result['entities']).get(key)[0]['value'])
            for entity in expression['entities']:
                if key == entity['entity']:
                    matched_entities += 1
    if wit_entities_count == known_entities_count == matched_entities:
        entity_result = 'OK'
        entities_percentage = 100
    elif wit_entities_count != known_entities_count and matched_entities > 0:
        entities_percentage = (wit_entities_count/known_entities_count)*100
        entity_result = 'PARCIAL'
    else:
        entities_percentage = 0
        entity_result = 'FAILURE'
    
    if 'intent' in wit_result['entities']:
        if wit_result['entities']['intent'][0]['value'] != expression['intent']:
            prediction_result = 'FAILURE'                         
        return '{0},{1},{2},{3}%,{4},{5},{6},{7}%'.format(expression['text'], expression['intent'], wit_result['entities']['intent'][0]['value'],int(float(wit_result['entities']['intent'][0]['confidence'])*100),prediction_result,detected_entities,known_entities,entity_result,entities_percentage)
    else:
        prediction_result = 'FAILURE'
        return '{0},{1},,,{2},,{3},{4},{5}%'.format(expression['text'], expression['intent'],prediction_result,known_entities, entity_result,entities_percentage)


def write_csv_file_from_wit(data, csv_footer):
    csv_headers = "Phrases,Expected intents,wit predicts,Confidence accuracy,Result,Detected entities,Known entities,Result by Entity, Entity accuracy\n"
    with open('wit_output.csv', "w") as csv_file:
        csv_file.write(csv_headers)
        for line in data:
            csv_file.write(line)
            csv_file.write('\n')
        csv_file.write('\n' + csv_footer)