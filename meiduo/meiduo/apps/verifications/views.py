import captcha as captcha
from django.shortcuts import render

# Create your views here.
from django.views import View


class ImageCodeView(View):

    def get(self,requset,uuid):
        #1.调用captcha框架, 生成图片和对应的信息
        captcha.generate_captcha()
        #2.链接redis, 获取redis的链接对象
        #3.调用链接对象, 把数据保存到redis