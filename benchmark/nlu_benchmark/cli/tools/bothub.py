import plac

from getpass import getpass

from nlu_benchmark.services.bothub import Bothub


@plac.annotations(
    username=plac.Annotation(kind='option'),
    password=plac.Annotation(kind='option'))
def get_token(username=None, password=None):
    if not username:
        username = input('username: ')
    if not password:
        password = getpass('password: ')
    user_token = Bothub.login(username, password)
    print(f'Your user token is: {user_token}')
