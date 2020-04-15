from django.conf.urls import re_path
from . import views

app_name = 'session'

urlpatterns = [
    re_path(r'^set_session/$', views.set_session),
    re_path(r'^get_session/$', views.get_session),

]
