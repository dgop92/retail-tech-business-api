from django.urls import reverse
from faker import Faker
import random
from dashboard import views


class BasicDashboardtUrlDataGetter:

    def init_basic_dashboard_url_data(self):

        self.faker = Faker()

        self.catalogues = [
            'Vehicles',
            'Technology',
            'Electrodomestics',
            'Toys',
            'Personal care',
            'Services',
            'Fashion'
        ]

    @staticmethod
    def get_brand_url(item_id = None):
        if item_id:
            return reverse(views.BrandDetail.name, args=[item_id])
        else:
            return reverse(views.BrandList.name)

    @staticmethod
    def get_catalogue_url(item_id = None):
        if item_id:
            return reverse(views.CatalogueDetail.name, args=[item_id])
        else:
            return reverse(views.CatalogueList.name)

    @staticmethod
    def get_product_url(item_id = None):
        if item_id:
            return reverse(views.ProductDetail.name, args=[item_id])
        else:
            return reverse(views.ProductList.name)

    @staticmethod
    def get_provider_url(item_id = None):
        if item_id:
            return reverse(views.ProviderDetail.name, args=[item_id])
        else:
            return reverse(views.ProviderList.name)


    def get_brand_valid_data(self):
        
        return {
            'name': self.faker.company()
        }

    def get_catalogue_valid_data(self):
        
        return {
            'name': random.choice(self.catalogues) 
                + str(random.randint(0, 999))
        }

    def get_product_valid_data(self, brand, catalogue):

        product_data = {
            'name': self.faker.domain_name(),
            'code': self.faker.credit_card_number(),
            'details': self.faker.text(),
            'sale_price': "{:.2f}".format(self.faker.pyfloat(
                right_digits = 2, 
                min_value = 1000, 
                max_value = 5000000)
            ),
            'purchase_price': "{:.2f}".format(self.faker.pyfloat(
                right_digits = 2, 
                min_value = 1000, 
                max_value = 5000000)
            ),
            'brand': brand,
            'catalogue': catalogue,
            'stock': 0
        }

        return product_data

    def get_provider_valid_data(self):

        provider_data = {
            'name': self.faker.domain_name(),
            'phone': "".join([str(random.randint(0,9)) for i in range(9)]),
            'email': self.faker.safe_email()
        }

        return provider_data

    def get_brand_invalid_data(self):

        return {
            'name': "".join(self.faker.words(nb = 30))
        }

    def get_catalogue_invalid_data(self):

        return {
            'name': "".join(self.faker.words(nb = 30))
        }

    def get_product_invalid_data(self):

        product_data = {
            'name': "".join(self.faker.words(nb = 30)),
            'code': "".join(str(i) for i in range(90)),
            'details': self.faker.text(),
            'sale_price': "{:.2f}".format(self.faker.pyfloat(
                right_digits = 2, 
                min_value = -1000, 
                max_value = 0)
            ),
            'purchase_price': "{:.2f}".format(self.faker.pyfloat(
                right_digits = 2, 
                min_value = -1000, 
                max_value = 0)
            ),
            'brand': self.faker.company(),
            'catalogue': random.choice(self.catalogues),
            'stock': -50
        }

        return product_data

    
    def get_provider_invalid_data(self):

        provider_data = {
            'name': "".join(self.faker.words(nb = 30)),
            'phone': "".join([str(random.randint(0,9)) for i in range(20)]),
            'email': "asduias no."
        }

        return provider_data


    
class CoreDashboardtUrlDataGetter:

    def init_core_dashboard_url_data(self):
        
        self.faker = Faker()
    
    @staticmethod
    def get_exit_url(item_id = None):
        if item_id:
            return reverse(views.ExitDetail.name, args=[item_id])
        else:
            return reverse(views.ExitList.name)

    @staticmethod
    def get_sale_url(item_id = None):
        if item_id:
            return reverse(views.SaleDetail.name, args=[item_id])
        else:
            return reverse(views.SaleList.name)

    @staticmethod
    def get_entry_url(item_id = None):
        if item_id:
            return reverse(views.EntryDetail.name, args=[item_id])
        else:
            return reverse(views.EntryList.name)
            
    @staticmethod
    def get_purchase_url(item_id = None):
        if item_id:
            return reverse(views.PurchaseDetail.name, args=[item_id])
        else:
            return reverse(views.PurchaseList.name)
    

    def get_sale_valid_data(self, exit_id, product_code, amount = None):

        if not amount:

            amount = self.faker.pyint(
                min_value = 10, 
                max_value = 100
            )

        sale_valid_data = {
            'exit': exit_id,
            'product': product_code,
            "unit_price": "50000.00",
            'amount': amount
        }

        return sale_valid_data

    def get_entry_valid_data(self, provider_name):
        provider_data =  {
            'provider': provider_name
        }
        return provider_data

    def get_purchase_valid_data(self, entry_id, product_code, amount = None):

        if not amount:

            amount = self.faker.pyint(
                min_value = 10, 
                max_value = 100
            )

        entry_valid_data = {
            'entry': entry_id,
            'product': product_code,            
            "unit_price": "32000.00",
            'amount': amount
        }

        return entry_valid_data