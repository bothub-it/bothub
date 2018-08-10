import random
import string

from requests import Request, Session

from .service import Service


class Bothub(Service):
    GLOBAL_CONFIG_FILE = '.bothub-service.yaml'

    @classmethod
    def api_request(cls, path, data=None, headers={}, user_token=None,
                    replace_method=None):
        if user_token:
            headers.update({ 'Authorization': f'Token {user_token}' })
        session = Session()
        method = 'POST' if data else 'GET'
        if replace_method:
            method = replace_method
        request = Request(
            method,
            f'https://bothub.it/api/{path}/',
            data=data,
            headers=headers)
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

    @classmethod
    def repository_exists(cls, owner_nickname, repository_slug):
        response = Bothub.api_request(
            f'repository/{owner_nickname}/{repository_slug}')
        return response.status_code is 200

    @classmethod
    def get_categories(cls):
        response = cls.api_request('categories')
        response.raise_for_status()
        return response.json()

    def __init__(self, user_token=None, **kwargs):
        self.user_token = user_token
        self._user_info = None
        super().__init__(**kwargs)

    @property
    def user_info(self):
        if not self._user_info:
            self._user_info = self.get_user_info()
        return self._user_info

    def get_user_info(self):
        assert self.user_token
        response = Bothub.api_request(
            'my-profile',
            user_token=self.user_token)
        response.raise_for_status()
        return response.json()

    def create_repository(self, **data):
        assert self.user_token
        return Bothub.api_request(
            'repository/new',
            data=data,
            user_token=self.user_token)

    def create_temporary_repository(self, language):
        owner_nickname = self.user_info.get('nickname')
        repository_slug = None

        while True:
            repository_slug = ''.join([
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(16)
            ])
            if not Bothub.repository_exists(owner_nickname, repository_slug):
                break

        categories = Bothub.get_categories()

        return self.create_repository(**{
            'name': f'Temporary repository {repository_slug}',
            'slug': repository_slug,
            'language': language,
            'categories': map(lambda c: c.get('id'), categories[:1]),
            'description': 'This is a temporary repository to benchmark test.',
            'private': True,
        })

    def delete_repository(self, owner_nickname, repository_slug):
        return Bothub.api_request(
            f'repository/{owner_nickname}/{repository_slug}',
            replace_method='DELETE',
            user_token=self.user_token)

    def submit_example(self, repository_uuid, example, language=None):
        data = example
        data.update({'repository': repository_uuid})
        if language:
            data.update({'language': language})
        return Bothub.api_request(
            'example/new',
            data,
            user_token=self.user_token)

    def train(self, owner_nickname, slug):
        return Bothub.api_request(
            f'repository/{owner_nickname}/{slug}/train',
            user_token=self.user_token)

    def analyze(self, owner_nickname, slug, text, language):
        data = {
            'text': text,
            'language': language,
        }
        return Bothub.api_request(
            f'repository/{owner_nickname}/{slug}/analyze',
            data,
            user_token=self.user_token)
