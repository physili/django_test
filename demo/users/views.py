from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


def index(request):
    print("hello world")
    return HttpResponse("index")

def haha(request):
    print('呵呵')
    jump_url = reverse('user:jump')

    return redirect(jump_url)

def jump(requset):

    sub1 = HttpResponse('jump')
    return sub1