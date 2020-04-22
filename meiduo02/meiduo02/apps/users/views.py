from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from users.models import User2

# Create your views here.

class UsernameCountView(View):
    '''判断用户是否重复'''
    def get(self,request,username):
        '''判断用户名是否重复'''
    # 1.查询username在数据库中的个数
        try:
            count = User2.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'访问数据库失败'})
    # 2.返回结果json-->code&errmsg&count
        return JsonResponse({'code':200,'errmsg':'ok','count':'count'})