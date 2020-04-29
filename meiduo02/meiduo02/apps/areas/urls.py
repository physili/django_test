
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^areas/$', views.ProvinceAreasView.as_view()),
    re_path(r'^areas/(?P<pk>[1-9]\d+)/$', views.SubAreasView.as_view()),
]
