import requests
import json

from app.settings import BOTHUB_APP_URL, BOTHUB_USER_TOKEN, BOTHUB_NLP_URL, BOTHUB_NLP_TOKEN

user_token_header = {'Authorization': BOTHUB_USER_TOKEN}
nlp_authorization_header = {'Authorization': BOTHUB_NLP_TOKEN}

def create_new_repository(args):
    data = {
            'description':'temp_',
            'is_private': True,
            'language':'pt_br',
            'name':'temp_validation_1337_0g38h7',
            'slug':'temp_1337_0g38h7',
            'categories':[1]}
    response = requests.post('{}/api/repository/new/'.format(BOTHUB_APP_URL),headers=user_token_header,data=data)
    response_json = json.loads(response.text)
    return [response_json["uuid"],response_json["slug"]]
    

def delete_repository(owner_nickname, repository_slug):
    params = {'owner__nickname': owner_nickname, 'slug': repository_slug}
    requests.delete('{0}/api/repository/{1}/{2}/'.format(BOTHUB_APP_URL, owner_nickname, repository_slug),headers=user_token_header,params=params)
    print('Saved output.csv')
    print('Removed')


def save_on_bothub(args, text, entities, intent):
    data = {'repository': args, 'text': text, 'entities': entities, 'intent': intent}
    requests.post('{0}/api/example/new/'.format(BOTHUB_APP_URL), headers=user_token_header, json=json.loads(json.dumps(data)))

    
def analyze_text(text, language, owner_nickname, repository_slug):
    data = {'text': text, 'language':language}
    response = requests.post('{0}/api/repository/{1}/{2}/analyze/'.format(BOTHUB_APP_URL, owner_nickname, repository_slug), headers=user_token_header, data=data)
    return json.loads(response.content)


def store_result(expression, bothub_result):
    detected_entities = '-'
    for entity in bothub_result['answer']['entities']:
        detected_entities += '{}-'.format(entity['entity'])
    if bothub_result['answer']['intent']['name'] == expression['intent']:
        return '{0},{1},{2},{3}%,OK,{4}'.format(expression['value'], expression['intent'], bothub_result['answer']['intent']['name'],int(float(bothub_result['answer']['intent']['confidence'])*100),detected_entities)        
    else:
        return '{0},{1},{2},{3}%,FAILURE,{4}'.format(expression['value'], expression['intent'], bothub_result['answer']['intent']['name'],int(float(bothub_result['answer']['intent']['confidence'])*100),detected_entities)


def train(owner_nickname, repository_slug):
    params = {'owner__nickname': owner_nickname, 'slug': repository_slug}
    requests.get('{0}/api/repository/{1}/{2}/train/'.format(BOTHUB_APP_URL,owner_nickname, repository_slug), params=params, headers=user_token_header)
    print("Bot trained")


def write_csv_file(data, csv_footer):
    csv_headers = "Phrases,Expected intents,Bothub predicts,Confidence,Result,Detected entities\n"
    with open('Bothub_output.csv', "w") as csv_file:
        csv_file.write(csv_headers)
        for line in data:
            csv_file.write(line)
            csv_file.write('\n')
        csv_file.write('\n' + csv_footer)


def get_intent_data(result):
    return result['answer']['intent']


def get_intent_name(result):
    return get_intent_data(result)['name']
