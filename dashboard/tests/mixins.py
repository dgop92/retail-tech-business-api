from account.tests.mixins import TestAccountBase
from dashboard.tests.data_generator import (BasicDashboardtUrlDataGetter,
                                            CoreDashboardtUrlDataGetter)
from rest_framework import status


class TestBasicDashboardBase(TestAccountBase, 
                             BasicDashboardtUrlDataGetter):

    def init_basic_dashboard_base(self):
        self.init_basic_dashboard_url_data()
        self.init_account_base()


    def get_brand_catalogue_for_product(self):

        token = self.login_admin_and_get_token()

        brand_data = self.get_brand_valid_data()
        self.post(
            self.get_brand_url(), 
            data = brand_data, 
            status_code = status.HTTP_201_CREATED,
            token = token
        )
        brand_data = self.json_response

        catalogue_data = self.get_brand_valid_data()

        self.post(
            self.get_catalogue_url(),
            data = catalogue_data,
            status_code = status.HTTP_201_CREATED,
            token = token
        )
        catalogue_data = self.json_response

        return brand_data, catalogue_data



class TestCoreDashboardBase(TestBasicDashboardBase,
                            CoreDashboardtUrlDataGetter):
    
    def init_core_dashboard_base(self):
        self.init_core_dashboard_url_data()
        self.init_basic_dashboard_base()
        
        self.employee1_data = self.get_random_new_user_data()
        self.employee2_data = self.get_random_new_user_data()
        self.register_new_user(register_data = self.employee1_data)
        self.register_new_user(register_data = self.employee2_data)

        brand_data = self.get_brand_valid_data()
        catalogue_data = self.get_brand_valid_data()
        self.product_data = self.get_product_valid_data(
            brand_data['name'],
            catalogue_data['name']
        )
        self.PRODUCT_STOCK = 1000
        self.product_data.update({'stock': self.PRODUCT_STOCK})
        self.provider_data = self.get_provider_valid_data()

        datas = [
            brand_data,
            catalogue_data,
            self.product_data,
            self.provider_data
        ]

        urls = [
            self.get_brand_url(), 
            self.get_catalogue_url(),
            self.get_product_url(),
            self.get_provider_url()
        ]

        token = self.login_admin_and_get_token()

        for url, data in zip(urls, datas):
            self.post(
                url, 
                data = data,
                status_code = status.HTTP_201_CREATED,
                token = token
            )

        print("Global objects created")

    