from requests import Request, Session

from .service import Service


class Bothub(Service):
    GLOBAL_CONFIG_FILE = '.bothub-service.yaml'

    @classmethod
    def api_request(cls, path, data=None):
        session = Session()
        request = Request(
            'POST' if data else 'GET',
            f'https://bothub.it/api/{path}/',
            data=data,
            headers={})
        prepped = request.prepare()
        return session.send(prepped)


    @classmethod
    def login(cls, username, password):
        response = cls.api_request(
            'login',
            {'username': username, 'password': password})
        response.raise_for_status()
        token = response.json().get('token')
        cls.update_global_config(user_token=token)
        return token
