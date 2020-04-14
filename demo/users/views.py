from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    print("hello world")
    return HttpResponse("index")

def haha(request):
    print('呵呵')
    return HttpResponse("haha")

def jump(requset):
    sub1 = HttpResponse('jump')
    return sub1