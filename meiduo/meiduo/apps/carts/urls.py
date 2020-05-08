
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^carts/$', views.CartsView.as_view()),
    re_path(r'^carts/selection/$', views.CartSelectAllView.as_view()),
    re_path(r'^carts/simple/$', views.CartsSimpleView.as_view()),
]
