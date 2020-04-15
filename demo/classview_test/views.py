from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.

class TestView(View):
    def get(self,request):
        print('get')
        return HttpResponse('get_TestView')
    def post(self,request):
        print('post')
        return HttpResponse('post_TestView')