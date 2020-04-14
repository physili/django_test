from django.conf.urls import re_path
from . import views

# 给子应用路由添加别名
app_name = 'qj'


urlpatterns = [
    #字符串传参路由
    re_path(r'^string/$',views.string_qj,name='sqj'),
    #路由传参，注意正则内容，传参的要加括号分组
    re_path(r'^url_qj/(.*)/(.*)/$',views.url_qj,name='uqj'),
    #表单传参路由
    re_path(r'^f_qj/$',views.f_qj,name='fqj'),
    #json传参路由
    re_path(r'^json_qj/$',views.json_qj,name='jqj'),
    #请求头部信息视图
    re_path(r'^head/$',views.head,name='head'),
    #JsonResponse自动转换字典格式返回响应体
    re_path(r'^jsonfunc/$',views.jsonfunc,name='jf'),
]
