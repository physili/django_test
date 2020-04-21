from django.http import HttpResponse
from django_redis import get_redis_connection

from django.shortcuts import render

# Create your views here.
from django.views import View

from meiduo.libs.captcha.captcha import captcha


class ImageCodeView(View):

    def get(self,requset,uuid):
        #1.调用captcha框架, 生成图片和对应的信息
        text, image = captcha.generate_captcha()
        #2.链接redis, 获取redis的链接对象
        redis_conn = get_redis_connection('verify_code')
        #3.调用链接对象, 把数据保存到redis
        redis_conn.setex('img_%s'%uuid,300,text)
        #4.返回图片
        return HttpResponse(image,content_type='image/jpg')