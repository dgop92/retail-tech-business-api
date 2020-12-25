"""simple_retail_business_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import rest_auth.views as rest_auth_views
from account.urls import (login_view_name, logout_view_name,
                          password_change_name, user_view_name)
from account.views import ACCOUNT_AUTH_CLASSES
from django.conf.urls import include, url
from django.urls import include

urlpatterns = [
    url(r'^dashboard/', include('dashboard.urls')),

    url(r'^auth/login/$', 
        rest_auth_views.LoginView.as_view(), 
        name = login_view_name
    ),

    url(r'^auth/logout/$', 
        rest_auth_views.LogoutView.as_view(
            authentication_classes = ACCOUNT_AUTH_CLASSES
        ), 
        name = logout_view_name
    ),
    
    url(r'^auth/user/$', 
        rest_auth_views.UserDetailsView.as_view(
            authentication_classes = ACCOUNT_AUTH_CLASSES
        ), 
        name = user_view_name
    ),

    url(r'^auth/password/change/$', 
        rest_auth_views.PasswordChangeView.as_view(
            authentication_classes = ACCOUNT_AUTH_CLASSES
        ), 
        name = password_change_name),

    url(r'^auth/password_reset/', 
        include(
            'django_rest_passwordreset.urls', 
            namespace = 'password_reset'
        )
    ),
    
    url(r'^account/', include('account.urls'))
]
