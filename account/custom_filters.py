from django_filters import NumberFilter, DateTimeFilter, FilterSet
from account.models import MyUser

class MyUsersFilter(FilterSet):

    from_birth_date = DateTimeFilter(
        field_name = 'profile__date_of_birth',
        lookup_expr = 'gte'
    )

    to_birth_date = DateTimeFilter(
        field_name = 'profile__date_of_birth',
        lookup_expr = 'lte'
    )

    max_age = NumberFilter(
        field_name = 'profile__age',
        lookup_expr = 'lte'
    )

    min_age = NumberFilter(
        field_name = 'profile__age',
        lookup_expr = 'gte'
    )

    class Meta:
        model = MyUser
        fields = (
            'from_birth_date',
            'to_birth_date',
            'max_age',
            'min_age',
            'is_superuser'
        )