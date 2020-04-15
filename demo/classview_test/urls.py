from django.conf.urls import re_path
from . import views

# 给子应用路由添加别名
app_name = 'cv'


urlpatterns = [
    #字符串传参路由
    re_path(r'^tv/$',views.TestView.as_view()),

]
