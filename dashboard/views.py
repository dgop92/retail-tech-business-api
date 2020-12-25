from account.custom_auth import BearerTokenAuthentication
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from dashboard.custom_filters import (EntryFilter, ExitFilter, ProductFilter,
                                      PurchaseFilter, SaleFilter)
from dashboard.custom_permissions import (IsCurrentUserOwnerOrAdmin,
                                          IsSuperUserOrReadOnly)

from .models import (Brand, Catalogue, Entry, Exit, Product, Provider,
                     Purchase, Sale)
from .serializers import (BrandSerializer, CatalogueSerializer,
                          EntrySerializer, ExitSerializer, ProductSerializer,
                          ProviderSerializer, PurchaseSerializer,
                          SaleSerializer)

DASHBOARD_AUTH_CLASSES = (BearerTokenAuthentication, )

class BrandList(generics.ListCreateAPIView):
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

class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    name = 'brand-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs) 
        except ProtectedError:
            return Response(
                status = status.HTTP_423_LOCKED, 
                data = {'detail': _("this brand is in use")}
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CatalogueList(generics.ListCreateAPIView):
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

class CatalogueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer
    name = 'catalogue-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs) 
        except ProtectedError:
            return Response(
                status = status.HTTP_423_LOCKED, 
                data = {'detail': _("this catalogue is in use")}
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductList(generics.ListCreateAPIView):
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

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    name = 'product-detail'
    
    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs) 
        except ProtectedError:
            return Response(
                status = status.HTTP_423_LOCKED, 
                data = {'detail': _("this product is in use")}
            )
        except Exception as e:
            return Response(status=status.HTTP_423_LOCKED, 
                data={'detail': str(e)})
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProviderList(generics.ListCreateAPIView):
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


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    name = 'provider-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUserOrReadOnly)


class ExitList(generics.ListCreateAPIView):
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

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class ExitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exit.objects.all()
    serializer_class = ExitSerializer
    name = 'exit-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs) 
        except ProtectedError:
            return Response(
                status = status.HTTP_423_LOCKED, 
                data = {'detail': _("this exit is in use")}
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class SaleList(generics.ListCreateAPIView):
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

class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    name = 'sale-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)


class EntryList(generics.ListCreateAPIView):
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

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    name = 'entry-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs) 
        except ProtectedError:
            return Response(
                status = status.HTTP_423_LOCKED, 
                data = {'detail': _("this entry is in use")}
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class PurchaseList(generics.ListCreateAPIView):
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

class PurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    name = 'purchase-detail'

    authentication_classes = DASHBOARD_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsCurrentUserOwnerOrAdmin)

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'brand-list': reverse(BrandList.name, request=request),
            'catalogue-list': reverse(CatalogueList.name, request=request),
            'product-list': reverse(ProductList.name, request=request),
            'provider-list': reverse(ProviderList.name, request=request),
            'exit-list': reverse(ExitList.name, request=request),
            'sale-list': reverse(SaleList.name, request=request),
            'entry-list': reverse(EntryList.name, request=request),
            'purchase-list': reverse(PurchaseList.name, request=request),
            })
