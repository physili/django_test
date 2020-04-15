from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# 设置session
def set_session(request):
    #按照字典形式设置即可
    request.session['name'] = 'waterboss'
    request.session['psw'] = 123
    return HttpResponse('set_session')

# 获取session
def get_session(request):
    #按照字典形式获取即可
    a = request.session['name']
    b = request.session['psw']
    print(a)
    print(b)
    return HttpResponse('get_session')