from django.conf.urls import re_path
from . import views

app_name = 'user'

urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^haha/$', views.haha, name='haha'),
    re_path(r'^jump/$', views.jump, name='jump'),

]
