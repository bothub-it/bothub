import requests
import json

from app.settings import BOTHUB_APP_URL, BOTHUB_USER_TOKEN, BOTHUB_NLP_URL, BOTHUB_NLP_TOKEN

user_token_header = {'Authorization': BOTHUB_USER_TOKEN}
nlp_authorization_header = {'Authorization': BOTHUB_NLP_TOKEN}


def save_on_bothub(args, text, intent):
    data = {'repository': args.repository, 'text': text, 'entities': [], 'intent': intent}
    response = requests.post('{0}/api/example/new/'.format(BOTHUB_APP_URL), headers=user_token_header, data=data)
    print('--> '+text+' {}'.format(response))


def analyze(text, language):
    data = {'text': text}
    response = requests.post(BOTHUB_NLP_URL, headers=nlp_authorization_header, data=data)
    response_json = json.loads(response.content)
    return response_json


def train(owner_nickname, repository_slug):
    params = {'owner__nickname': owner_nickname, 'slug': repository_slug}
    response = requests.get('{0}/api/repository/{1}/{2}/train/'.format(BOTHUB_APP_URL,owner_nickname, repository_slug), params=params, headers=user_token_header)
    print("Done")


def get_intent_data(result):
    return result['answer']['intent']


def get_intent_name(result):
    return get_intent_data(result)['name']
