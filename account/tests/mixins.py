import json

from account.models import Profile
from account.tests.data_generator import AccountUrlDataGetter
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


class TestsMixin:
    
    def init(self):

        self.client = APIClient()
        self.json_response = {}
        self.print_output = True

    def send_request(self, request_method, *args, **kwargs):
        request_func = getattr(self.client, request_method)
        status_code = None

        if 'content_type' not in kwargs and request_method != 'get':
            kwargs['content_type'] = 'application/json'

        if 'data' in kwargs and request_method != 'get' and \
            kwargs['content_type'] == 'application/json':
            
            data = kwargs.get('data', '')
            kwargs['data'] = json.dumps(data)

        if 'status_code' in kwargs:
            status_code = kwargs.pop('status_code')

        if 'token' in kwargs:
            kwargs['HTTP_AUTHORIZATION'] = \
                'Bearer %s' % kwargs.pop('token')

        self.response = request_func(*args, **kwargs)

        is_json = bool(
            'content-type' in self.response._headers and
            [x for x in self.response._headers['content-type'] if 'json' in x]
        )

        if is_json and self.response.content:
            self.json_response = self.response.json()
            if self.print_output:
                print(json.dumps(
                    self.json_response, indent=4, ensure_ascii=False
                ))

        if status_code:
            assert self.response.status_code == status_code

        return self.response

    def post(self, *args, **kwargs):
        return self.send_request('post', *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.send_request('get', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.send_request('put', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.send_request('patch', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.send_request('delete', *args, **kwargs)
    
    def compare_json_response_given_data(self, data: dict, 
        oppositive = False):

        for data_key in data.keys():
            if oppositive:
                assert self.json_response[data_key] != data[data_key]
            else:
                assert self.json_response[data_key] == data[data_key]



class TestAccountBase(TestsMixin, AccountUrlDataGetter):

    def init_account_base(self):
        self.init()
        self.init_account_data_url()

        User = get_user_model();
        user = User.objects.create_superuser(
            self.ADMIN_DATA["username"], 
            self.ADMIN_DATA["email"], 
            self.ADMIN_DATA["password"]
        )
        Profile.objects.create(user = user)

    def login_admin_and_get_token(self):

        payload = {
            "username": self.ADMIN_DATA['username'],
            "password": self.ADMIN_DATA['password']
        }

        self.post(self.login_url, data = payload)

        return self.json_response['key']

    def login_user_with_credentials_and_get_token(self, data):

        self.post(self.login_url, data = data)
        return self.json_response['key']
    

    def register_new_user(self, register_data):

        self.post(
            self.register_view, 
            data = register_data, 
            status_code = status.HTTP_201_CREATED,
            token = self.login_admin_and_get_token()
        )
