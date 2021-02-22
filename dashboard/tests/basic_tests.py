from dashboard.tests.mixins import TestBasicDashboardBase
from django.test import TestCase
from rest_framework import status

class DashboardBasicTests(TestBasicDashboardBase, TestCase):

    def setUp(self):
        self.init_basic_dashboard_base()

    def positive_test_generator(self, get_url_func, data = {}, 
        old_data = None, delete = False, data_func_generator = None):

        token = self.login_admin_and_get_token()

        if data:

            if old_data:

                self.post(
                    get_url_func(), 
                    data = old_data, 
                    status_code = status.HTTP_201_CREATED,
                    token = token
                )

                self.put(
                    get_url_func(item_id = int(self.json_response['pk'])), 
                    data = data, 
                    status_code = status.HTTP_200_OK,
                    token = token
                )

                self.compare_json_response_given_data(data = data)
            else:

                self.post(
                    get_url_func(), 
                    data = data, 
                    status_code = status.HTTP_201_CREATED,
                    token = token
                )

                self.compare_json_response_given_data(data = data)

        else:

            items_to_create = 4

            #Note use extra kwargs in method
            if data_func_generator == self.get_product_valid_data:
                brand_data, catalogue_data = \
                    self.get_brand_catalogue_for_product()
                kwargs = {
                    "brand": brand_data['name'], 
                    "catalogue": catalogue_data['name']
                }
            else:
                kwargs = {}

            id_items = []

            for _ in range(items_to_create):
                self.post(
                    get_url_func(), 
                    data = data_func_generator(**kwargs), 
                    status_code = status.HTTP_201_CREATED,
                    token = token
                )

                id_items.append(int(self.json_response['pk']))

            if delete:
                for _id in id_items:

                    self.delete(
                        get_url_func(item_id = _id), 
                        status_code = status.HTTP_204_NO_CONTENT,
                        token = token
                    )

                self.get(
                    get_url_func(), 
                    status_code = status.HTTP_200_OK,
                    token = token
                )
                self.assertEqual(self.json_response['count'], 0)
            else:
                self.get(
                    get_url_func(), 
                    status_code = status.HTTP_200_OK,
                    token = token
                )
                self.assertEqual(self.json_response['count'], items_to_create)

     # Create Objects Tests

    def negative_test_generator(self, get_url_func, 
        valid_data, invalid_data = {}, duplicate_test = False):

        token = self.login_admin_and_get_token()

        if duplicate_test:

            status_code = status.HTTP_201_CREATED
            for _ in range(2):
                self.post(
                    get_url_func(), 
                    data = valid_data, 
                    status_code = status_code,
                    token = token
                )
                status_code = status.HTTP_400_BAD_REQUEST

        if invalid_data:

            self.post(
                get_url_func(), 
                data = invalid_data, 
                status_code = status.HTTP_400_BAD_REQUEST,
                token = token
            )

            self.post(
                get_url_func(), 
                data = {}, 
                status_code = status.HTTP_400_BAD_REQUEST,
                token = token
            )

            self.post(
                get_url_func(), 
                data = valid_data, 
                status_code = status.HTTP_201_CREATED,
                token = token
            )

            self.put(
                get_url_func(item_id = int(self.json_response['pk'])),
                data = invalid_data,
                status_code = status.HTTP_400_BAD_REQUEST,
                token = token
            )

    # Create Objects Tests

    def test_create_brand(self):

        self.positive_test_generator(
            self.get_brand_url,
            data = self.get_brand_valid_data(),
        )

    def test_create_catalogue(self):

        self.positive_test_generator(
            self.get_catalogue_url,
            data = self.get_catalogue_valid_data(),
        )

    def test_create_product(self):

        brand_data, catalogue_data = self.get_brand_catalogue_for_product()

        self.positive_test_generator(
            self.get_product_url,
            data = self.get_product_valid_data(
                brand_data['name'],
                catalogue_data['name']
            ),
        )


    def test_create_provider(self):

        self.positive_test_generator(
            self.get_provider_url,
            data = self.get_provider_valid_data(),
        )

    # Update Objects Tests

    def test_update_brand(self):

        old_data = self.get_brand_valid_data()
        new_data = self.get_brand_valid_data()

        self.positive_test_generator(
            self.get_brand_url,
            data = new_data,
            old_data = old_data,
        )

    def test_update_catalogue(self):

        old_data = self.get_catalogue_valid_data()
        new_data = self.get_catalogue_valid_data()

        self.positive_test_generator(
            self.get_catalogue_url,
            data = new_data,
            old_data = old_data,
        )

    def test_update_product(self):

        brand_data, catalogue_data = self.get_brand_catalogue_for_product()

        old_data = self.get_product_valid_data(
            brand_data['name'],
            catalogue_data['name']
        )
        new_data = self.get_product_valid_data(
            brand_data['name'],
            catalogue_data['name']
        )

        self.positive_test_generator(
            self.get_product_url,
            data = new_data,
            old_data = old_data,
        )

    def test_update_provider(self):

        old_data = self.get_provider_valid_data()
        new_data = self.get_provider_valid_data()

        self.positive_test_generator(
            self.get_provider_url,
            data = new_data,
            old_data = old_data,
        )

    def test_get_brands(self):

        self.positive_test_generator(
            self.get_brand_url,
            data_func_generator = self.get_brand_valid_data
        )

    def test_get_catalogues(self):

        self.positive_test_generator(
            self.get_catalogue_url,
            data_func_generator = self.get_catalogue_valid_data
        )

    def test_get_products(self):

        self.positive_test_generator(
            self.get_product_url,
            data_func_generator = self.get_product_valid_data
        )

    def test_get_providers(self):

        self.positive_test_generator(
            self.get_provider_url,
            data_func_generator = self.get_provider_valid_data
        )

    def test_delete_brand(self):

        self.positive_test_generator(
            self.get_brand_url,
            data_func_generator = self.get_brand_valid_data,
            delete = True
        )

    def test_delete_catalogue(self):

        self.positive_test_generator(
            self.get_catalogue_url,
            data_func_generator = self.get_catalogue_valid_data,
            delete = True
        )

    def test_delete_product(self):

        self.positive_test_generator(
            self.get_product_url,
            data_func_generator = self.get_product_valid_data,
            delete = True
        )

    def test_delete_provider(self):

        self.positive_test_generator(
            self.get_provider_url,
            data_func_generator = self.get_provider_valid_data,
            delete = True
        )

    # Negative cases, BUG: seralizaer improve some messages

    def test_invalid_brand_data(self):

        self.negative_test_generator(
            self.get_brand_url,
            self.get_brand_valid_data(),
            self.get_brand_invalid_data()
        )

    def test_invalid_catalogue_data(self):

        self.negative_test_generator(
            self.get_catalogue_url,
            self.get_brand_valid_data(),
            self.get_brand_invalid_data()
        )

    def test_invalid_product_data(self):

        brand_data, catalogue_data = self.get_brand_catalogue_for_product()
        
        self.negative_test_generator(
            self.get_product_url,
            self.get_product_valid_data(
                brand_data['name'],
                catalogue_data['name']
            ),
            self.get_product_invalid_data()
        )

    def test_invalid_provider_data(self):

        self.negative_test_generator(
            self.get_provider_url,
            self.get_provider_valid_data(),
            self.get_provider_invalid_data()
        )

    def test_protected_brand_catalogue(self):
        
        brand_data, catalogue_data = \
            self.get_brand_catalogue_for_product()

        token = self.login_admin_and_get_token()

        self.post(
            self.get_product_url(),
            data = self.get_product_valid_data(
                brand_data['name'],
                catalogue_data['name']
            ),
            status_code = status.HTTP_201_CREATED,
            token = token
        )

        self.delete(
            self.get_brand_url(item_id = int(brand_data['pk'])),
            status_code = status.HTTP_423_LOCKED,
            token = token
        )

        self.delete(
            self.get_catalogue_url(item_id = int(catalogue_data['pk'])),
            status_code = status.HTTP_423_LOCKED,
            token = token
        )

    def test_delete_product_with_stock(self):

        brand_data, catalogue_data = \
            self.get_brand_catalogue_for_product()

        product_data = self.get_product_valid_data(
            brand_data['name'],
            catalogue_data['name']
        )
        product_data.update({'stock': 120})

        token = self.login_admin_and_get_token()

        self.post(
            self.get_product_url(),
            data = product_data,
            status_code = status.HTTP_201_CREATED,
            token = token
        )

        self.delete(
            self.get_product_url(item_id = int(self.json_response['pk'])),
            status_code = status.HTTP_423_LOCKED,
            token = token
        )

    def test_product_unique_code(self):

        brand_data, catalogue_data = \
            self.get_brand_catalogue_for_product()
        
        self.negative_test_generator(
            self.get_product_url,
            valid_data = self.get_product_valid_data(
                brand_data['name'],
                catalogue_data['name']
            ), 
            duplicate_test = True
        )

    def test_provider_unique_email(self):

        self.negative_test_generator(
            self.get_provider_url,
            valid_data = self.get_provider_valid_data(),
            duplicate_test = True
        )
