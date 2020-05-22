"""meiduo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_jwt.views import obtain_jwt_token #obtain_jwt_token 就是　验证用户名和密码，没有问题，会返回Ｔｏｋｅｎ
from django.conf.urls import re_path

from .views import statistical

urlpatterns = [
    re_path(r'^authorizations/$',obtain_jwt_token),# ObtainJSONWebToken.as_view()
    re_path(r'^statistical/total_count/$',statistical.UserTotalCountView.as_view()),
]