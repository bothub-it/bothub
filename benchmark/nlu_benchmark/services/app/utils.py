import json
import io


def load_json_file(entity_file):
    # with open(entity_file) as json_file:
        # data = json.dumps(json_file.read())
        # data_dict = json.loads(data)
    data_dict = json.load(io.open(entity_file, 'r', encoding='utf-8-sig'))
    return data_dict


def percentage(part, whole):
    return 100 * float(part) / float(whole)