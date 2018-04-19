from django.urls import re_path, path, include
from .views import AccountLoginView, AccountLogoutView
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
    re_path(r'^login/$', AccountLoginView.as_view(), name='login'),
    re_path(r'^logout/$', AccountLogoutView.as_view(), name='logout')
]