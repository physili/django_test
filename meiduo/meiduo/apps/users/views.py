from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from users.models import User

#用户名重复注册验证
class UsernameCountView(View):
    def get(self,request,username):
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400, 'errmsg':'访问服务器失败'})
        return JsonResponse({'code':200,'errmsg':'ok','count':count})

#手机号重复注册验证
class MobileCountView(View):
    def get(self,request,mobile):
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'查询出错'})
        return JsonResponse({'code':200,'errmsg':'ok','count':count})
