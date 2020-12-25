from django.test.testcases import TestCase
from rest_framework import status
from dashboard.tests.mixins import TestCoreDashboardBase


class TestCoreDashboardTest(TestCoreDashboardBase, TestCase):

    def setUp(self):
        self.init_core_dashboard_base()

    def positive_sale_purchase_generator(self, get_url_func,
        action, data_func_generator, extra_data_kwargs = {}):
        
        token = self.login_user_with_credentials_and_get_token(
            data = {
                "username": self.employee1_data['username'],
                "password": self.employee1_data['password'],
            }
        )

        if action == 'update' or action == 'create':

            self.post(
                get_url_func(),
                data = data_func_generator(**extra_data_kwargs),
                token = token,
                status_code = status.HTTP_201_CREATED
            )

            # Post sale

            if action == 'update':

                new_data = data_func_generator(**extra_data_kwargs)

                self.put(
                    get_url_func(item_id = 1), 
                    data = new_data, 
                    token = token,
                    status_code = status.HTTP_200_OK
                )

                # update sale

                self.compare_json_response_given_data(data = new_data)

    
        elif action == 'get' or action == 'delete':

            # Post sale

            items_to_create = 3

            for _ in range(items_to_create):
                self.post(
                    get_url_func(), 
                    data = data_func_generator(**extra_data_kwargs),
                    token = token,
                    status_code = status.HTTP_201_CREATED
                )



            if 'delete':

                self.delete(
                    get_url_func(item_id = 2),
                    token = token,
                    status_code = status.HTTP_204_NO_CONTENT
                )

                items_to_create -= 1

            self.get(
                get_url_func(),
                token = token,
                status_code = status.HTTP_200_OK
            )
            
            self.assertEqual(self.json_response['count'], items_to_create)
    
    def negative_sale_purchase_generator(self, get_url_func,
        action, **kwargs):
        
        if action == 'create':

            req_kwargs = {}
            
            if kwargs['auth']:
                token = self.login_user_with_credentials_and_get_token(
                    data = {
                        "username": self.employee1_data['username'],
                        "password": self.employee1_data['password'],
                    }
                )
                status_code = status.HTTP_400_BAD_REQUEST
                req_kwargs.update({'token': token})
            else:
                status_code = status.HTTP_401_UNAUTHORIZED
            
            req_kwargs.update({'status_code': status_code})

            self.post(
                get_url_func(), 
                data = kwargs['invalid_data'], 
                **req_kwargs
            )
            
            self.post(
                get_url_func(), 
                data = {}, 
                **req_kwargs
            )

        else:

            token1 = self.login_user_with_credentials_and_get_token(
                data = {
                    "username": self.employee1_data['username'],
                    "password": self.employee1_data['password'],
                }
            )

            token2 = self.login_user_with_credentials_and_get_token(
                data = {
                    "username": self.employee2_data['username'],
                    "password": self.employee2_data['password'],
                }
            )

            extra_data_args = ()
            if 'parent_post_func' in kwargs:
                parent_post_func = kwargs['parent_post_func']
                parent_post_func(custom_token = token1)  
                parent_post_func(custom_token = token2)
                extra_data_args = (1, self.product_data['code'])

            data_func_generator = kwargs['data_func_generator']
            if 'extra_data_kwargs' not in kwargs:
                extra_data_kwargs = {}    
            else:
                extra_data_kwargs =  kwargs['extra_data_kwargs']

            self.post(
                get_url_func(), 
                data = data_func_generator(
                    *extra_data_args, **extra_data_kwargs
                ), 
                token = token1,
                status_code = status.HTTP_201_CREATED
            )

            if 'parent_post_func' in kwargs:
                extra_data_args = (2, self.product_data['code'])

            self.post(
                get_url_func(), 
                data = data_func_generator(
                    *extra_data_args, **extra_data_kwargs
                ), 
                token = token2,
                status_code = status.HTTP_201_CREATED
            )

            if action == 'get':

                self.get(
                    get_url_func(item_id = 1),
                    token = token2,
                    status_code = status.HTTP_403_FORBIDDEN
                )

                self.get(
                    get_url_func(),
                    token = token1,
                    status_code = status.HTTP_200_OK
                )

                self.assertEqual(self.json_response['count'], 1)
                
                admin_token = self.login_admin_and_get_token()

                self.get(
                    get_url_func(),
                    token = admin_token,
                    status_code = status.HTTP_200_OK
                )

                self.assertEqual(self.json_response['count'], 2)
            
            
            if action == 'update':

                self.put(
                    get_url_func(item_id = 1),
                    token = token2,
                    status_code = status.HTTP_403_FORBIDDEN
                )

            if action == 'delete':
                
                # BUG is forbidden
                self.delete(
                    get_url_func(item_id = 2),
                    token = token1,
                    status_code = status.HTTP_403_FORBIDDEN
                )


    def post_exit_for_sale(self, custom_token = None):

        if not custom_token:
            token = self.login_user_with_credentials_and_get_token(
                {
                    "username": self.employee1_data['username'],
                    "password": self.employee1_data['password'],
                }
            )
        else:
            token = custom_token

        self.post(
            self.get_exit_url(),
            data = {},
            token = token,
            status_code = status.HTTP_201_CREATED
        )

    def post_entry_for_purchase(self, custom_token = None):

        if not custom_token:
            token = self.login_user_with_credentials_and_get_token(
                {
                    "username": self.employee1_data['username'],
                    "password": self.employee1_data['password'],
                }
            )
        else:
            token = custom_token

        self.post(
            self.get_entry_url(),
            data = {'provider': self.provider_data['name']},
            token = token,
            status_code = status.HTTP_201_CREATED
        )

    # Basic Positive Exits and sales Tests 

    def test_create_exit(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_exit_url,
            action = 'create',
            data_func_generator = lambda: {},
        )

    def test_update_exit(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_exit_url,
            action = 'update',
            data_func_generator = lambda: {}
        )

    def test_get_exit(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_exit_url,
            action = 'get',
            data_func_generator = lambda: {}
        )

    def test_delete_exit(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_exit_url,
            action = 'delete',
            data_func_generator = lambda: {}
        )

    def test_create_sale(self):

        self.post_exit_for_sale()

        self.positive_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'create',
            data_func_generator = self.get_sale_valid_data,
            extra_data_kwargs = {
                "exit_id": 1,
                "product_code": self.product_data['code']
            }
        )

    # NOTE you coudl create another product
    def test_update_sale(self):

        self.post_exit_for_sale()

        self.positive_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'update',
            data_func_generator = self.get_sale_valid_data,
            extra_data_kwargs = {
                "exit_id": 1,
                "product_code": self.product_data['code']
            }
        )

    def test_get_sale(self):

        self.post_exit_for_sale()
    
        self.positive_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'get',
            data_func_generator = self.get_sale_valid_data,
            extra_data_kwargs = {
                "exit_id": 1,
                "product_code": self.product_data['code']
            }
        )

    def test_delete_sale(self):

        self.post_exit_for_sale()

        self.positive_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'delete',
            data_func_generator = self.get_sale_valid_data,
            extra_data_kwargs = {
                "exit_id": 1,
                "product_code": self.product_data['code']
            }
        )

    # Basic Positive Entries and purchases Tests 

    def test_create_entry(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'create',
            data_func_generator = self.get_entry_valid_data,
            extra_data_kwargs = {
                "provider_name": self.provider_data['name']
            }
        )


    def test_update_entry(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'update',
            data_func_generator = self.get_entry_valid_data,
            extra_data_kwargs = {
                "provider_name": self.provider_data['name']
            }
        )


    def test_get_entry(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'get',
            data_func_generator = self.get_entry_valid_data,
            extra_data_kwargs = {
                "provider_name": self.provider_data['name']
            }
        )


    def test_delete_entry(self):

        self.positive_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'delete',
            data_func_generator = self.get_entry_valid_data,
            extra_data_kwargs = {
                "provider_name": self.provider_data['name']
            }
        )

    def test_create_purchase(self):

        self.post_entry_for_purchase()

        self.positive_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'create',
            data_func_generator = self.get_purchase_valid_data,
            extra_data_kwargs = {
                "entry_id": 1,
                "product_code": self.product_data['code'],
            }
        )


    def test_update_purchase(self):

        self.post_entry_for_purchase()

        self.positive_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'update',
            data_func_generator = self.get_purchase_valid_data,
            extra_data_kwargs = {
                "entry_id": 1,
                "product_code": self.product_data['code'],
            }
        )


    def test_get_purchase(self):

        self.post_entry_for_purchase()

        self.positive_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'get',
            data_func_generator = self.get_purchase_valid_data,
            extra_data_kwargs = {
                "entry_id": 1,
                "product_code": self.product_data['code'],
            }
        )


    def test_delete_purchase(self):

        self.post_entry_for_purchase()

        self.positive_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'delete',
            data_func_generator = self.get_purchase_valid_data,
            extra_data_kwargs = {
                "entry_id": 1,
                "product_code": self.product_data['code'],
            }
        )
    

    # Negative Exits and sales Tests

    def test_create_negative_exit(self):
        pass

    def test_get_exit_bad_permission(self):
        
        self.negative_sale_purchase_generator(
            get_url_func = self.get_exit_url,
            action = 'get',
            data_func_generator = lambda: {},
        )

    def test_update_exit_bad_permission(self):
        
        self.negative_sale_purchase_generator(
            get_url_func = self.get_exit_url,
            action = 'update',
            data_func_generator = lambda: {},
        )

    def test_delete_exit_bad_permission(self):
        
        self.negative_sale_purchase_generator(
            get_url_func = self.get_exit_url,
            action = 'delete',
            data_func_generator = lambda: {},
        )

    def test_create_invalid_sale(self):
        
        invalid_data = self.get_sale_valid_data(
            exit_id = 5,
            product_code = '109238901',
            amount = -10
        )

        self.negative_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'create',
            invalid_data = invalid_data,
            auth = True
        )

        self.negative_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'create',
            invalid_data = invalid_data,
            auth = False
        )

    def test_get_sale_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'get',
            data_func_generator = self.get_sale_valid_data,
            parent_post_func = self.post_exit_for_sale
        )


    def test_update_sale_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'update',
            data_func_generator = self.get_sale_valid_data,
            parent_post_func = self.post_exit_for_sale
        )

    def test_delete_sale_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_sale_url,
            action = 'delete',
            data_func_generator = self.get_sale_valid_data,
            parent_post_func = self.post_exit_for_sale
        )

    # Negative entries and purchases tests

    def test_create_invalid_entry(self):

        invalid_data = self.get_entry_valid_data(
            provider_name = 'random'
        )

        self.negative_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'create',
            invalid_data = invalid_data,
            auth = True
        )

        self.negative_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'create',
            invalid_data = invalid_data,
            auth = False
        )

    def test_update_entry_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'update',
            data_func_generator = self.get_entry_valid_data,
            extra_data_kwargs = {
                "provider_name": self.provider_data['name'],
            }
        )


    def test_get_entry_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'get',
            data_func_generator = self.get_entry_valid_data,
            extra_data_kwargs = {
                "provider_name": self.provider_data['name'],
            }
        )


    def test_delete_entry_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_entry_url,
            action = 'delete',
            data_func_generator = self.get_entry_valid_data,
            extra_data_kwargs = {
                "provider_name": self.provider_data['name'],
            }
        )

    def test_create_invalid_purchase(self):
        
        invalid_data = self.get_purchase_valid_data(
            entry_id = 5,
            product_code = '103238901',
            amount = -123
        )

        self.negative_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'create',
            invalid_data = invalid_data,
            auth = True
        )

        self.negative_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'create',
            invalid_data = invalid_data,
            auth = False
        )

    def test_update_purchase_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'update',
            data_func_generator = self.get_purchase_valid_data,
            parent_post_func = self.post_entry_for_purchase
        )


    def test_get_purchase_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'get',
            data_func_generator = self.get_purchase_valid_data,
            parent_post_func = self.post_entry_for_purchase
        )

    def test_delete_purchase_bad_permission(self):

        self.negative_sale_purchase_generator(
            get_url_func = self.get_purchase_url,
            action = 'delete',
            data_func_generator = self.get_purchase_valid_data,
            parent_post_func = self.post_entry_for_purchase
        )