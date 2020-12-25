from django_filters import (AllValuesFilter, DateTimeFilter, FilterSet,
                            NumberFilter)

from dashboard.models import Entry, Exit, Product, Purchase, Sale


class ProductFilter(FilterSet):

    brand = AllValuesFilter(
        field_name = 'brand__name',
    )

    catalogue = AllValuesFilter(
        field_name = 'catalogue__name',
    )

    class Meta:
        model = Product
        fields = (
            'brand',
            'catalogue',
        )

class EntryExitFilterBase(FilterSet):

    from_created_date = DateTimeFilter(
        field_name = 'created_date',
        lookup_expr = 'gte'
    )

    to_created_date = DateTimeFilter(
        field_name = 'created_date',
        lookup_expr = 'lte'
    )

    user = AllValuesFilter(
        field_name = 'user__username',
    )

class ExitFilter(EntryExitFilterBase):

    class Meta:
        model = Exit
        fields = (
            'from_created_date',
            'to_created_date',
            'user'
        )

class EntryFilter(EntryExitFilterBase):

    provider = AllValuesFilter(
        field_name = 'provider__name',
    )

    class Meta:
        model = Entry
        fields = (
            'from_created_date',
            'to_created_date',
            'user',
            'provider'
        )

class SalePurchaseFilter(FilterSet):

    max_amount = NumberFilter(
        field_name = 'amount',
        lookup_expr = 'lte'
    )

    min_amount = NumberFilter(
        field_name = 'amount',
        lookup_expr = 'gte'
    )

    product_code = AllValuesFilter(
        field_name = 'product__code',
    )


class SaleFilter(SalePurchaseFilter):

    class Meta:
        model = Sale
        fields = (
            'max_amount',
            'min_amount',
            'exit',
            'product_code',
        )

class PurchaseFilter(SalePurchaseFilter):

    class Meta:
        model = Purchase
        fields = (
            'max_amount',
            'min_amount',
            'entry',
            'product_code',
        )
