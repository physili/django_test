from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# 创建cookie
def set_cookie(request):
    # 先创建对象
    cc = HttpResponse('set_cookie')
    # 用对象调取set_cookie方法
    cc.set_cookie('name','water',max_age=3600)
    return cc

# 获取cookie
def get_cookie(request):
    # 直接用request调取COOKIES
    result = request.COOKIES['name']
    print(result)
    return HttpResponse('get_cookie')