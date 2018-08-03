import plac
import yaml
import json
import requests

from . import logger
from ..services.bothub import Bothub


@plac.annotations(
    data_file_path=plac.Annotation(),
    data_file_type=plac.Annotation(kind='option', choices=['yaml', 'json']),
    bothub_user_token=plac.Annotation(kind='option'))
def run(data_file_path, data_file_type='yaml', bothub_user_token=None):
    try:
        data_file = open(data_file_path, 'r')
    except Exception as e:
        logger.error(f'Can\'t open the data file "{data_file_path}"')
        raise e

    try:
        if data_file_type == 'yaml':
            data = yaml.load(data_file)
        elif data_file_type == 'json':
            data = json.load(data_file)
    except Exception as e:
        raise e

    logger.debug(f'data loaded to run benchmark {data}')

    bothub_global_config = Bothub.get_current_global_config()

    bothub_user_token = bothub_user_token or bothub_global_config.get('user_token')
    assert bothub_user_token
    logger.debug(f'using {bothub_user_token} bothub user token')

    logger.info('Starting Bothub benchmark...')
    bothub = Bothub(user_token=bothub_user_token)

    create_repository_response = bothub.create_temporary_repository(
        data.get('language'))

    try:
        create_repository_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error('Bothub temporary repository not created')
        logger.debug(create_repository_response.text)
        raise e

    temporary_repository = create_repository_response.json()
    logger.info(f'Bothub temporary repository created "{temporary_repository.get("name")}"')

    delete_repository_response = bothub.delete_repository(
        temporary_repository.get('owner__nickname'),
        temporary_repository.get('slug'))

    try:
        delete_repository_response.raise_for_status()
    except Exception as e:
        logger.warning('Bothub temporary repository not deleted, manually delete')
        logger.debug(delete_repository_response.text)

    logger.info(f'Bothub temporary repository deleted')
