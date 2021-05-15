from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import (Brand, Catalogue, Client, Entry, Exit, Product, Provider,
                     Purchase, Sale)


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Brand
        fields = (
            'pk',
            'name'
        )
    
class CatalogueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Catalogue
        fields = (
            'pk',
            'name'
        )

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    brand = serializers.SlugRelatedField(queryset=Brand.objects.all(),
		slug_field='name', required=True, error_messages = {
            'does_not_exist': _("Brand with name {value} doesn't exit"),
        }
    )
    catalogue = serializers.SlugRelatedField(queryset=Catalogue.objects.all(),
		slug_field='name', required=True, error_messages = {
            'does_not_exist': _("Catalogue with name {value} doesn't exit"),
        }
    )
    
    code = serializers.CharField(max_length=80 , validators=[
        UniqueValidator(
            queryset=Product.objects.all(),
            message = _("Product code is unique")
        )],
    )

    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'code',
            'details',
            'sale_price',
            'purchase_price',
            'brand',
            'catalogue',
            'stock')

    def validate_sale_price(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                _("Price must be a positive number")
            )
        return data

    def validate_purchase_price(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                _("Price must be a positive number")
            )
        return data

    def validate_stock(self, data):
        if data < 0:
            raise serializers.ValidationError(
                _("Product stock can't be negative")
            )
        return data

class ProviderSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField(max_length=80 ,validators=[
        UniqueValidator(
            queryset=Provider.objects.all(),
            message = _('provider with this email already exists.')
        ),
        EmailValidator()
        ],
        allow_blank = True
    )

    class Meta:
        model = Provider
        fields = (
            'pk',
            'name',
            'phone',
            'email')

class SaleSerializer(serializers.ModelSerializer):

    product = serializers.SlugRelatedField(queryset=Product.objects.all(),
		slug_field='code', required=True, error_messages = {
            'does_not_exist': _("Product with code {value} doesn't exit"),
        }
    )

    sold = serializers.ReadOnlyField(
        source='get_amount_sold'
    )

    exit = serializers.SlugRelatedField(queryset=Exit.objects.all(),
		slug_field='pk', required=True, error_messages = {
            'does_not_exist': _("Exit with id {value} doesn't exit"),
        }
    )

    class Meta:
        model = Sale
        fields = (
            'pk',
            'exit',
            'product',
            'amount',
            'unit_price',
            'sold',
        )

    def validate_amount(self, amount):
        if amount < 0:
            raise serializers.ValidationError(
                _("Amount must be a positive number")
            )
        return amount

    def validate(self, data):

        curr_amount = self.instance.amount if self.instance else 0
        
        if self.instance:
            curr_product = self.instance.product
        else:
            curr_product = data['product']
        
        amount = data['amount']

        curr_stock = curr_product.stock
        
        if curr_amount + curr_stock - amount < 0:
            raise serializers.ValidationError(
                _("There is not enough stock for this product")
            )

        return data

class PurchaseSerializer(serializers.ModelSerializer):

    product = serializers.SlugRelatedField(queryset=Product.objects.all(),
		slug_field='code', required=True, error_messages = {
            'does_not_exist': _("Product with code {value} doesn't exit"),
        }
    )

    spent = serializers.ReadOnlyField(
        source='get_amount_spent'
    )

    entry = serializers.SlugRelatedField(queryset=Entry.objects.all(),
		slug_field='pk', required=True, error_messages = {
            'does_not_exist': _("Entry with id {value} doesn't exit"),
        }
    )

    class Meta:
        model = Purchase
        fields = (
            'pk',
            'entry',
            'product',
            'amount',            
            'unit_price',
            'spent',
        )

    def validate_amount(self, amount):
        if amount < 0:
            raise serializers.ValidationError(
                _("Amount must be a positive number")
            )
        return amount


class ExitSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    exit_sales = SaleSerializer(many=True, read_only=True)

    units_sold = serializers.ReadOnlyField(
        source='get_units_sold'
    )

    total_sold = serializers.ReadOnlyField(
        source='total_amount_sold'
    )

    client = serializers.SlugRelatedField(queryset=Client.objects.all(),
		slug_field='tice', required=False, error_messages = {
            'does_not_exist': _("Client with name {value} doesn't exit"),
        }
    )

    class Meta:
        model = Exit
        fields = (
            'pk',
            'created_date',
            'user',
            'client',
            'units_sold',
            'total_sold',
            'exit_sales'
        )    
        read_only_fields = ('created_date', 'user')


class EntrySerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    provider = serializers.SlugRelatedField(queryset=Provider.objects.all(),
		slug_field='name', required=True, error_messages = {
            'does_not_exist': _("Provider with name {value} doesn't exit"),
        }
    )
    entry_purchases = PurchaseSerializer(many=True, read_only=True)

    units_bought = serializers.ReadOnlyField(
        source='get_units_bought'
    )

    total_spent = serializers.ReadOnlyField(
        source='total_amount_spent'
    )

    class Meta:
        model = Entry
        fields = (
            'pk',
            'created_date',
            'user',
            'provider',
            'units_bought',
            'total_spent',
            'entry_purchases'
        )    
        read_only_fields = ('created_date', 'user')
        
class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = (
            'pk',
            'name',
            'phone',
            'tice',
        )