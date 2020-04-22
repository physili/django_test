
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),

]
