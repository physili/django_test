from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json

# Create your views here.

#字符串传参
def string_qj(request):
    #重点request.GET
    a = request.GET.get('a')
    b = request.GET.get('b')
    alist = request.GET.getlist('a')

    print(a)
    print(b)
    print(alist)

    return HttpResponse("string_qj")

#路由传参
def url_qj(request,city,year):
    # 添加了断点 应该是走的。没有走 说明什么？
    # 有路由截胡了 去看路由
    print(city)
    print(year)
    return HttpResponse('url_ql')

#表单传参
def f_qj(request):
    # 重点request.POST
    a = request.POST.get('a')
    b = request.POST.get('b')
    c = request.POST.getlist('a')
    print(a)
    print(b)
    print(c)
    return HttpResponse('f_qj')

#json传参
def json_qj(request):
    # 重点①导模块，②request.body，③json.loads()
    json_str = request.body.decode()
    json_dict = json.loads(json_str)
    print(json_dict)
    return HttpResponse(json_str)

#请求头信息
def head(request):
    #在请求头里通过META获取请求头的内容长度
    a = request.META.get('CONTENT_LENGTH')
    #获取请求头内容
    b = request.META
    print(a)
    print(b)
    #获取发起请求的用户名（这里的结果是匿名）
    print(request.user)
    #获取路径
    print(request.path)
    #获取请求的方法
    print(request.method)
    c = HttpResponse('head')
    # 把键值对放进请求头里
    c['hello']='world'
    return c

def jsonfunc(request):
    my_dict={'a':'bb','c':123}
    return JsonResponse(my_dict)