import os
import plac
import yaml
import requests

from ..services.bothub import Bothub


@plac.annotations(
    data_file_path=plac.Annotation(),
    bothub_user_token=plac.Annotation(kind='option'))
def run(data_file_path, bothub_user_token=None):
    if not os.path.isfile(data_file_path):
        return print(f'{data_file_path} not exists')

    data_file = open(data_file_path, 'r')
    data = yaml.load(data_file)

    bothub_global_config = Bothub.get_current_global_config()

    bothub_user_token = bothub_user_token or bothub_global_config.get('user_token')
    assert bothub_user_token

    bothub = Bothub(user_token=bothub_user_token)
    create_repository_response = bothub.create_temporary_repository(
        data.get('language'))
    try:
        create_repository_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return print('Temporary repository not created :(\n' +
                     str(create_repository_response.content))
    temporary_repository = create_repository_response.json()
    delete_repository_response = bothub.delete_repository(
        temporary_repository.get('owner__nickname'),
        temporary_repository.get('slug'))
    delete_repository_response.raise_for_status()
