from requests import Request, Session

from .service import Service


class Bothub(Service):
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
        try:
            response.raise_for_status()
            return response.json().get('token')
        except Exception as e:
            raise Exception(' / '.join([
                f"{field}: {'; '.join(errors)}" for field, errors in
                response.json().items()
            ]))