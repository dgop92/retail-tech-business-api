from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^brands/$',
        views.BrandList.as_view(),
        name=views.BrandList.name
    ),
    url(r'^brands/(?P<pk>[0-9]+)$',
        views.BrandDetail.as_view(),
        name=views.BrandDetail.name
    ),
    
    url(r'^catalogues/$',
        views.CatalogueList.as_view(),
        name=views.CatalogueList.name
    ),
    url(r'^catalogues/(?P<pk>[0-9]+)$',
        views.CatalogueDetail.as_view(),
        name=views.CatalogueDetail.name
    ),

    url(r'^products/$',
        views.ProductList.as_view(),
        name=views.ProductList.name
    ),
    url(r'^products/(?P<pk>[0-9]+)$',
        views.ProductDetail.as_view(),
        name=views.ProductDetail.name
    ),

    url(r'^providers/$',
        views.ProviderList.as_view(),
        name=views.ProviderList.name
    ),
    url(r'^providers/(?P<pk>[0-9]+)$',
        views.ProviderDetail.as_view(),
        name=views.ProviderDetail.name
    ),

    url(r'^exits/$',
        views.ExitList.as_view(),
        name=views.ExitList.name
    ),
    url(r'^exits/(?P<pk>[0-9]+)$',
        views.ExitDetail.as_view(),
        name=views.ExitDetail.name
    ),

    url(r'^entries/$',
        views.EntryList.as_view(),
        name=views.EntryList.name
    ),
    url(r'^entries/(?P<pk>[0-9]+)$',
        views.EntryDetail.as_view(),
        name=views.EntryDetail.name
    ),

    url(r'^sales/$',
        views.SaleList.as_view(),
        name=views.SaleList.name
    ),
    url(r'^sales/(?P<pk>[0-9]+)$',
        views.SaleDetail.as_view(),
        name=views.SaleDetail.name
    ),

    url(r'^purchases/$',
        views.PurchaseList.as_view(),
        name=views.PurchaseList.name
    ),
    url(r'^purchases/(?P<pk>[0-9]+)$',
        views.PurchaseDetail.as_view(),
        name=views.PurchaseDetail.name
    ),

    url(r'^clients/$',
        views.ClientList.as_view(),
        name=views.ClientList.name
    ),
    url(r'^clients/(?P<pk>[0-9]+)$',
        views.ClientDetail.as_view(),
        name=views.ClientDetail.name
    ),

    url(r'^$',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name),
]
