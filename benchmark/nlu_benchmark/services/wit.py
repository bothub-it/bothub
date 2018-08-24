import string
import json

from requests import Request, Session

from .service import Service


class Wit(Service):
    GLOBAL_CONFIG_FILE = '.bothub-service.yaml'

    @classmethod
    def analyze(self,phrase,version,token):
        session = Session()
        params = {'q':phrase, 'v':version}
        headers = {'Authorization':token}
        request = Request('GET','https://api.wit.ai/message',params=params,headers=headers)
        prepped = request.prepare()
        return session.send(prepped)