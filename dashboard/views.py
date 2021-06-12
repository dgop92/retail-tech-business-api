from account.custom_auth import BearerTokenAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from dashboard.custom_filters import (EntryFilter, ExitFilter, ProductFilter,
                                      PurchaseFilter, SaleFilter)
from dashboard.custom_permissions import (IsCurrentUserOwnerOrAdmin,
                                          IsSuperUserOrReadOnly)

from .models import (Brand, Catalogue, Client, Entry, Exit, Product, Provider,
                     Purchase, Sale)
from .serializers import (BrandSerializer, CatalogueSerializer, ClientSerializer,
                          EntrySerializer, ExitSerializer, ProductSerializer,
                          ProviderSerializer, PurchaseSerializer,
                          SaleSerializer)

DASHBOARD_AUTH_CLASSES = (BearerTokenAuthentication, )

class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    name = 'brand-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    search_fields = (
        '$name',
        )
    ordering_fields = (
        'name',
        )

class BrandDetail(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    name = 'brand-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)


class CatalogueList(generics.ListAPIView):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer
    name = 'catalogue-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    search_fields = (
        '$name',
        )
    ordering_fields = (
        'name',
        )

class CatalogueDetail(generics.RetrieveAPIView):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer
    name = 'catalogue-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    name = 'product-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)
    
    search_fields = (
        '$name',
        '$code',
    )
    filter_class = ProductFilter
    ordering_fields = (
        'name',
        'stock',
        'purchase_price',
        'sale_price',
    )

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    name = 'product-detail'
    
    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)


class ProviderList(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    name = 'provider-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    search_fields = (
        '$name',
    )
    ordering_fields = (
        'name',
    )


class ProviderDetail(generics.RetrieveAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    name = 'provider-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)


class ExitList(generics.ListAPIView):
    serializer_class = ExitSerializer
    name = 'exit-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, )

    filter_class = ExitFilter

    ordering_fields = (
        'created_date',
    )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Exit.objects.all()
        return Exit.objects.filter(user = self.request.user)

class ExitDetail(generics.RetrieveAPIView):
    queryset = Exit.objects.all()
    serializer_class = ExitSerializer
    name = 'exit-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)


class SaleList(generics.ListAPIView):
    serializer_class = SaleSerializer
    name = 'sale-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, )

    search_fields = (
        '$product__code',
    )
    filter_class = SaleFilter
    ordering_fields = (
        'amount',
    )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Sale.objects.all()
        return Sale.objects.filter(exit__user = self.request.user)

class SaleDetail(generics.RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    name = 'sale-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)


class EntryList(generics.ListAPIView):
    serializer_class = EntrySerializer
    name = 'entry-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated,)

    filter_class = EntryFilter

    ordering_fields = (
        'created_date',
    )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Entry.objects.all()
        return Entry.objects.filter(user = self.request.user)

class EntryDetail(generics.RetrieveAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    name = 'entry-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)

    
class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    name = 'purchase-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, )

    search_fields = (
        '$product__code',
    )
    filter_class = PurchaseFilter
    ordering_fields = (
        'amount',
    )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Purchase.objects.all()
        return Purchase.objects.filter(entry__user = self.request.user)

class PurchaseDetail(generics.RetrieveAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    name = 'purchase-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)


class ClientList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    name = 'client-list'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    search_fields = (
        '$name',
        '$tice'
    )
    ordering_fields = (
        'name',
    )

class ClientDetail(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    name = 'client-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)
