import random

from account import views
from account.urls import login_view_name, logout_view_name, user_view_name
from django.urls import reverse
from faker import Faker


class AccountUrlDataGetter:

    ADMIN_DATA = {
        "username": "admin_dp",
        "email": "admin_examaple@example.com",
        "first_name": "admin_name",
        "last_name": "admin_lastname",
        "is_superuser": True,
        "password": "admin1234admin",
        "password_confirmation": "admin1234admin",
    }

    def init_account_data_url(self):

        self.faker = Faker()

        self.register_view = reverse(views.RegisterView.name)

        self.login_url = reverse(login_view_name)
        self.logout_url = reverse(logout_view_name)
        self.user_url = reverse(user_view_name)

        self.profile_url = reverse(views.ProfileDetailView.name)
        self.user_list_url = reverse(views.UserList.name)

    def get_random_new_user_data(self):

        new_user_data = {
            "username": self.faker.user_name(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "email": self.faker.safe_email(),
            "password": "admin1234admin",
            "password_confirmation": "admin1234admin"
        }

        return new_user_data

    def get_user_data(self):

        user_data = {
            "username": self.faker.user_name(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name()
        }

        return user_data

    def get_random_profile_data(self):

        profile_data = {
            "tice": "".join([str(random.randint(0,9)) for i in range(10)]),
            "cellphone": "".join([str(random.randint(0,9)) for i in range(9)]),
            "age": random.randint(20, 70),
            "date_of_birth": str(self.faker.date_this_year()),
        }

        return profile_data
