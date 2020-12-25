from django.conf.urls import url
from account import views

login_view_name = 'login-view'
logout_view_name = 'logout-view'
user_view_name = 'user-view'
password_change_name = 'password-change'
password_reset_name = 'password-reset-view'
password_reset_confirm_name = 'password-reset-confirm-view'

urlpatterns = [

    url(r'^users/$',
        views.UserList.as_view(),
        name=views.UserList.name
    ),

    url(r'^register/$',
        views.RegisterView.as_view(),
        name=views.RegisterView.name
    ),

    url(r'^profile/$',
        views.ProfileDetailView.as_view(),
        name=views.ProfileDetailView.name
    ),

    url(r'^$',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name
    ),
]