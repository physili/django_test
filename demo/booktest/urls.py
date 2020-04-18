from django.conf.urls import re_path
from . import views

app_name = 'booktest'

urlpatterns = [
    re_path(r'^save/$',views.SaveDataView.as_view())
]
