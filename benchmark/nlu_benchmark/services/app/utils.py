import json


def load_json_file(entity_file):
    with open(entity_file) as json_file:
        data = json.load(json_file)
    return data


def percentage(part, whole):
    return 100 * float(part) / float(whole)
