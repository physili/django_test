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
from rest_framework.routers import DefaultRouter
from .views import statistical,user, image, sku

urlpatterns = [
    re_path(r'^authorizations/$',obtain_jwt_token),# ObtainJSONWebToken.as_view()
    re_path(r'^statistical/total_count/$',statistical.UserTotalCountView.as_view()),
    re_path(r'^statistical/day_active/$',statistical.UserDailyActiveCountView.as_view()),
    re_path(r'^statistical/day_orders/$',statistical.UserDailyOrderCountView.as_view()),
    re_path(r'^statistical/month_increment/$',statistical.UserMonthCountView.as_view()),
    re_path(r'^statistical/day_increment/$',statistical.UserDayCountView.as_view()),
    re_path(r'^statistical/goods_day_views/$',statistical.CategoryVistCountView.as_view()),
    re_path(r'^users/$',user.UserListView.as_view()),
    re_path(r'^skus/simple/$', image.SKUView.as_view()),
    re_path(r'^skus/categories/$', sku.SKUCategoriesView.as_view()),
    re_path(r'^goods/simple/$', sku.GoodsSimpleView.as_view()),
    re_path(r'^goods/(?P<pk>\d+)/specs/$', sku.GoodsSpecView.as_view()),
]

router = DefaultRouter()
router.register(r'skus/images', image.ImageView, basename='image')
router.register(r'skus', sku.SKUModelViewSet, basename='skus')

urlpatterns += router.urls