
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^qq/authorization/$', views.QQURLView.as_view()),
    re_path(r'^oauth_callback/$', views.QQUserView.as_view()),

]
