from account.tests.mixins import TestAccountBase
from django.test import TestCase
from rest_framework import status

class APICoreTests(TestAccountBase, TestCase):

    def setUp(self):
        self.init_account_base()
        
        self.register_data = {
            "username": "nosoyadmin",
            "email": "noadminemail@example.com",
            "first_name": "pedro",
            "last_name": "pérzez",
            "is_superuser": False,
            "password": "1234admin1234",
            "password_confirmation": "1234admin1234",
        }
    
    # Register tests

    def test_register_simple_user(self):
        
        self.post(
            self.register_view, 
            data = self.register_data, 
            status_code = status.HTTP_201_CREATED,
            token = self.login_admin_and_get_token()
        )

    def test_register_already_username_email(self):

        self.post(
            self.register_view, 
            data = self.register_data, 
            status_code = status.HTTP_201_CREATED,
            token = self.login_admin_and_get_token()
        )

        self.post(
            self.register_view, 
            data = self.register_data, 
            status_code = status.HTTP_400_BAD_REQUEST,
            token = self.login_admin_and_get_token()
        )

    def test_register_invalid_username(self):

        register_data = self.register_data.copy()
        register_data.update({"username": "d%&pe1012"})

        self.post(
            self.register_view, 
            data = register_data, 
            status_code = status.HTTP_400_BAD_REQUEST,
            token = self.login_admin_and_get_token()
        )

    def test_register_invalid_email(self):

        register_data = self.register_data.copy()
        register_data.update({"email": "exampleexample.com"})

        self.post(
            self.register_view, 
            data = register_data, 
            status_code = status.HTTP_400_BAD_REQUEST,
            token = self.login_admin_and_get_token()
        )

    def test_register_invalid_password(self):

        register_data = self.register_data.copy()
        register_data.update({
            "password": "1234",
            "password_confirmation": "1234",
        })

        self.post(
            self.register_view, 
            data = register_data, 
            status_code = status.HTTP_400_BAD_REQUEST,
            token = self.login_admin_and_get_token()
        )

    def test_register_mismatch_password(self):

        register_data = self.register_data.copy()
        register_data.update({
            "password": "1234admin1234",
            "password_confirmation": "admin1234admin123",
        })

        self.post(
            self.register_view, 
            data = register_data, 
            status_code = status.HTTP_400_BAD_REQUEST,
            token = self.login_admin_and_get_token()
        )

    def test_register_wrong_field_input(self):

        large_first_name = "".join([str(i) for i in range(30)])
        large_last_name = "".join([str(i) for i in range(150)])
        large_username = "".join([str(i) for i in range(150)])

        register_data = {
            "username": large_username,
            "email": "example@example.com",
            "first_name": large_first_name,
            "last_name": large_last_name,
            "is_superuser": "casa",
            "password": 1230,
            "password_confirmation": "1234admin1234",
        }

        self.post(
            self.register_view, 
            data = register_data, 
            status_code = status.HTTP_400_BAD_REQUEST,
            token = self.login_admin_and_get_token()
        )

        self.post(
            self.register_view, 
            data = {}, 
            status_code = status.HTTP_400_BAD_REQUEST,
            token = self.login_admin_and_get_token()
        )

    # User - Profile tests

    # NOTE it is posible to update the profile from user detail, or it was
    # a bug
    def profile_user_test_generator(self, url, auth_type = 'token',
        data_generator_func = None):
        
        if auth_type == 'token':

            kwargs = {
                "token": self.login_admin_and_get_token(),
                "status_code": status.HTTP_200_OK
            }

        elif auth_type == 'invalid_token':

            kwargs = {
                "token": "asd910ujdasidnhakusdhya7",
                "status_code": status.HTTP_401_UNAUTHORIZED
            }

        else:

            kwargs = {
                "status_code": status.HTTP_401_UNAUTHORIZED
            }

        
        if data_generator_func:

            data = data_generator_func()
            kwargs.update({"data": data})

            self.put(
                url,
                **kwargs
            )

            # Just compare if it is posible update data
            if auth_type == 'token':
                self.compare_json_response_given_data(data)

            data = data_generator_func()
            kwargs.pop('data')

            for key, item in data.items():
                self.patch(
                    url,
                    data = {key : item},
                    **kwargs
                )

            if auth_type == 'token':
                self.compare_json_response_given_data(data)

        else:

            self.get(
                url,
                **kwargs
            )
                

    # User Detail tests
        
    def test_user_detail(self):

        self.profile_user_test_generator(
            self.user_url,
            auth_type = 'token'
        )

    def test_user_update_data(self):

        self.profile_user_test_generator(
            self.user_url,
            auth_type = 'token',
            data_generator_func = self.get_user_data
        )

    def test_user_detail_no_auth(self):

        self.profile_user_test_generator(
            self.user_url,
            auth_type = 'invalid_token'
        )

        self.profile_user_test_generator(
            self.user_url,
            auth_type = ''
        )

    def test_user_update_data_no_auth(self):

        self.profile_user_test_generator(
            self.user_url,
            auth_type = 'invalid_token',
            data_generator_func = self.get_user_data
        )

        self.profile_user_test_generator(
            self.user_url,
            auth_type = '',
            data_generator_func = self.get_user_data
        )

    def test_user_update_wrong_fields(self):

        token = self.login_admin_and_get_token()

        new_user_data = {
            "username": "causa%-||",
            "first_name": "012345678910111213141516 \
                1718192021222324252627282930aa",
        }

        self.patch(
            self.user_url,
            token = token,
            data = new_user_data,
            status_code = status.HTTP_400_BAD_REQUEST
        )

    def test_user_update_read_only_fields(self):

        token = self.login_admin_and_get_token()

        new_user_data = {
            "email": "update@example.com",
            "is_superuser": False,
        }

        for key, item in new_user_data.items():

            self.patch(
                self.user_url,
                data = {key: item},
                token = token,
                status_code = status.HTTP_200_OK
            )
            assert self.json_response[key] != new_user_data[key]

    # Test user profile

    def test_profile_detail(self):

        self.profile_user_test_generator(
            self.profile_url,
            auth_type = 'token'
        )

    def test_profile_update_data(self):

        self.profile_user_test_generator(
            self.profile_url,
            auth_type = 'token',
            data_generator_func = self.get_random_profile_data
        )

    def test_profile_detail_no_auth(self):

        self.profile_user_test_generator(
            self.profile_url,
            auth_type = 'invalid_token'
        )

        self.profile_user_test_generator(
            self.profile_url,
            auth_type = ''
        )

    def test_profile_update_data_no_auth(self):

        self.profile_user_test_generator(
            self.profile_url,
            auth_type = 'invalid_token',
            data_generator_func = self.get_random_profile_data
        )

        self.profile_user_test_generator(
            self.profile_url,
            auth_type = '',
            data_generator_func = self.get_random_profile_data
        )

    def test_profile_update_wrong_fields(self):

        token = self.login_admin_and_get_token()

        profile_data = {
            "tice": "1001819090 asda sd asd asd asd",
            "cellphone": "32222210 asd asd asd ",
            "age": -123,
            "date_of_birth": "A"
        }

        self.put(
            self.profile_url,
            token = token,
            data = profile_data,
            status_code = status.HTTP_400_BAD_REQUEST
        )

    # Test userlist

    def test_user_list(self):
        token = self.login_admin_and_get_token()

        self.get(
            self.user_list_url,
            token = token,
            status_code = status.HTTP_200_OK
        )

    def test_user_list_no_auth(self):

        self.get(
            self.user_list_url,
            token = "asdasf1234456dfs",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

        self.get(
            self.user_list_url,
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    def test_user_list_no_superuser(self):

        self.register_new_user(register_data = self.register_data)
        token = self.login_user_with_credentials_and_get_token(
            data = {
                "username": self.register_data["username"],
                "password": self.register_data["password"],
            }
        )

        self.get(
            self.user_list_url,
            token = token,
            status_code = status.HTTP_403_FORBIDDEN
        )