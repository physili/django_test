from django.shortcuts import render

# Create your views here.
from django.views import View
from django import http
from django_redis import get_redis_connection
from meiduo02.libs.captcha.captcha import captcha

class ImageCodeView(View):
    def get(self,request,uuid):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s'%uuid,300,text)
        return http.HttpResponse(image,content_type='image/jpg')