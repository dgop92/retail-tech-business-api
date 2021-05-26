from django.db import models
from django.db.models import Sum, F, DecimalField

from account.models import MyUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    name = models.CharField(max_length=80, unique = True)

    objects = models.Manager()

    class Meta:
        ordering = ('name', )

class Catalogue(models.Model):
    name = models.CharField(max_length=80, unique = True)

    objects = models.Manager()

    class Meta:
        ordering = ('name', )

class Product(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=80, unique=True)
    details = models.TextField(blank=True, default="Sin detalles")
    sale_price = models.DecimalField(max_digits=14, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2)

    brand = models.ForeignKey(
        Brand, 
        on_delete=models.PROTECT, 
        related_name='brands'
    )
    catalogue = models.ForeignKey(
        Catalogue, 
        on_delete=models.PROTECT, 
        related_name='catalogues'
    )

    stock = models.IntegerField()

    objects = models.Manager()

    class Meta:
        ordering = ('name', )

    def delete(self, *args, **kwargs):
        if self.stock > 0:
            raise Exception(
                _("In order to delete a product its stock must be zero")
            )
        else:
            super(Product, self).delete(*args, **kwargs)


class Provider(models.Model):

    name = models.CharField(max_length=80, unique = True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=80, unique=True, blank=True , null=True)

    objects = models.Manager()

    class Meta:
        ordering = ('name', )

    def save(self, *args, **kwargs):
        # if email is empty treated as None
        if not self.email:
            self.email = None

        super().save(*args, **kwargs)


class Client(models.Model):

    name = models.CharField(max_length=80)
    tice = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15, blank=True)


class Exit(models.Model):

    created_date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(MyUser, 
        null = True, 
        on_delete = models.SET_NULL,
        related_name='user_exits'
    )

    client = models.ForeignKey(Client, 
        null = True, 
        on_delete = models.SET_NULL,
        related_name='client_exits',
    )

    objects = models.Manager()

    class Meta:
        ordering = ('created_date', )

    def get_units_sold(self):
        return self.exit_sales.count()
    
    def total_amount_sold(self):
        return self.exit_sales.aggregate(
            total_sold=Sum(
                F('amount') * F('unit_price'), output_field=DecimalField()
            )
        )['total_sold'] or 0


class Entry(models.Model):

    created_date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(MyUser, 
        null = True, 
        on_delete = models.SET_NULL,
        related_name='user_entries'
    )
    provider = models.ForeignKey(Provider,
        null = True,
        on_delete = models.SET_NULL,
        related_name='provider_entries'
    )

    objects = models.Manager()

    class Meta:
        ordering = ('created_date', )

    def get_units_bought(self):
        return self.entry_purchases.count()
    
    def total_amount_spent(self):
        return self.entry_purchases.aggregate(
            total_spent=Sum(
                F('amount') * F('unit_price'), output_field=DecimalField()
            )
        )['total_spent'] or 0

class Purchase(models.Model):

    entry = models.ForeignKey(Entry,
        on_delete = models.PROTECT,
        related_name='entry_purchases'
    )

    product = models.ForeignKey(Product,
        on_delete = models.PROTECT,
        related_name='product_purchases'
    )

    amount = models.IntegerField()
        
    unit_price = models.DecimalField(max_digits=14, decimal_places=2)

    objects = models.Manager()

    # Increase the product stock according to the amount purchased
    def save(self, *args, **kwargs):
        curr_amount = Purchase.objects.get(pk = self.pk). \
            amount if self.pk else 0
        self.product.stock = self.product.stock - curr_amount + self.amount
        self.product.save()
        super(Purchase, self).save(*args, **kwargs)

    def get_amount_spent(self):
        return self.amount * self.unit_price

class Sale(models.Model):

    exit = models.ForeignKey(Exit,
        on_delete = models.PROTECT,
        related_name='exit_sales'
    )

    product = models.ForeignKey(Product,
        on_delete = models.PROTECT,
        related_name='product_sales'
    )
        
    unit_price = models.DecimalField(max_digits=14, decimal_places=2)

    amount = models.IntegerField()

    objects = models.Manager()

    # Decrease the product stock according to the amount sold
    def save(self, *args, **kwargs):
        curr_amount = Sale.objects.get(pk = self.pk).amount if self.pk else 0
        self.product.stock += curr_amount - self.amount
        self.product.save()
        super(Sale, self).save(*args, **kwargs) 

    def get_amount_sold(self):
        return self.amount * self.unit_price