import requests
import json

from app.settings import BOTHUB_APP_URL, BOTHUB_USER_TOKEN, BOTHUB_NLP_URL, BOTHUB_NLP_TOKEN

user_token_header = {'Authorization': BOTHUB_USER_TOKEN}
nlp_authorization_header = {'Authorization': BOTHUB_NLP_TOKEN}

valid_predict = []
invalid_predict = []
phrases_count = 0
sum_bothub_hits = 0
sum_bothub_fails = 0

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
    response = requests.delete('{0}/api/repository/{1}/{2}/'.format(BOTHUB_APP_URL, owner_nickname, repository_slug),headers=user_token_header,params=params)
    print('Saved output.csv')
    print('Removed')


def save_on_bothub(args, text, entities, intent):
    data = {'repository': args, 'text': text, 'entities': entities, 'intent': intent}
    response = requests.post('{0}/api/example/new/'.format(BOTHUB_APP_URL), headers=user_token_header, json=json.loads(json.dumps(data)))
    # print(response)

    
def analyze_text(text, language, owner_nickname, repository_slug):
    data = {'text': text, 'language':language}
    response = requests.post('{0}/api/repository/{1}/{2}/analyze/'.format(BOTHUB_APP_URL, owner_nickname, repository_slug), headers=user_token_header, data=data)
    response_json = json.loads(response.content)
    return response_json


def store_result(expression, bothub_result):
    global phrases_count
    global sum_bothub_hits
    global sum_bothub_fails
    phrases_count += 1
    if bothub_result['answer']['intent']['name'] == expression['intent']:
        sum_bothub_hits += 1
        return '{0},{1},{2},{3}%,OK'.format(expression['value'], expression['intent'], bothub_result['answer']['intent']['name'],int(float(bothub_result['answer']['intent']['confidence'])*100))        
    else:
        sum_bothub_fails += 1
        return '{0},{1},{2},{3}%,FAILURE'.format(expression['value'], expression['intent'], bothub_result['answer']['intent']['name'],int(float(bothub_result['answer']['intent']['confidence'])*100))
    #valid_predict.extend(invalid_predict)
    #write_csv_file(valid_predict,'Analized phrases: {0}\nCorrect predictions: {1}\nWrong predictions: {2}'.format(phrases_count,sum_bothub_hits,sum_bothub_fails))


def train(owner_nickname, repository_slug):
    params = {'owner__nickname': owner_nickname, 'slug': repository_slug}
    requests.get('{0}/api/repository/{1}/{2}/train/'.format(BOTHUB_APP_URL,owner_nickname, repository_slug), params=params, headers=user_token_header)
    print("Bot trained")


def write_csv_file(data, csv_footer):
    csv_headers = "Phrases,Expected intents,Bothub predicts,Confidence,Result\n"
    with open('output1.csv', "w") as csv_file:
        csv_file.write(csv_headers)
        for line in data:
            csv_file.write(line)
            csv_file.write('\n')
        csv_file.write('\n' + csv_footer)


def get_intent_data(result):
    return result['answer']['intent']


def get_intent_name(result):
    return get_intent_data(result)['name']
