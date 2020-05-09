
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^orders/settlement/$', views.OrderSettlementView.as_view()),
    re_path(r'^orders/commit/$', views.OrderCommitView.as_view()),
]
