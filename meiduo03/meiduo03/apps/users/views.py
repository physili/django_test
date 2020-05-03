from django import http
from django.shortcuts import render
from django.views import View
from users.models import User

#验证用户名是否重复接口  #传入一个用户名的参数
class UsernameCountView(View):
    def get(self,request,username):
        try:
            #获取count数据
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return http.JsonResponse({'code': 400, 'errmsg': '访问服务器失败'})
        #返回count数据, 由前端根据count值判断是否警告
        return http.JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})
