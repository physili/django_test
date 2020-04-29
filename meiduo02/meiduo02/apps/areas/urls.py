
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^areas/$', views.ProvinceAreasView.as_view()),
]
