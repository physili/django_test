
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^orders/settlement/$', views.OrderSettlementView.as_view()),
]
