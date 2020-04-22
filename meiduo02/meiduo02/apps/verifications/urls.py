
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$',views.ImageCodeView.as_view()),
]