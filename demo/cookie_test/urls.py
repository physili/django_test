from django.conf.urls import re_path
from . import views

app_name = 'cookie'

urlpatterns = [
    re_path(r'^setcookie/$', views.set_cookie),
    re_path(r'^getcookie/$', views.get_cookie),

]
