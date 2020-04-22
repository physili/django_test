from django import http
from django_redis import get_redis_connection
import random
from django.shortcuts import render
from meiduo.libs.yuntongxun.sms import CCP
# Create your views here.
from django.views import View
import logging
logger = logging.getLogger('django')
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
        return http.HttpResponse(image,content_type='image/jpg')


class SMSCodeView(View):
    '''短信验证码'''
    def get(self,request,mobile):
        # 1.接受参数:图形验证码,uuid,电话号码
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2.整体校验参数
        if not all([image_code_client,uuid]):
            return http.JsonResponse({'code':400,'errmsg':'缺少比传参数'})
        # 3.创建链接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 4.提取图形验证码
        image_code_server = redis_conn.get('img_%s'%uuid)
        if image_code_server is None:
            return http.JsonResponse({'code':400,'errmsg':'图形验证码失效'})
        # 5.删除redis的图形验证码,避免恶意测试图形验证码
        try:
            redis_conn.delete('img_%s'%uuid)
        except Exception as e:
            logger.error(e)
        # 6.对比图形验证码
        image_code_server = image_code_server.decode()
        if image_code_client.lower()!=image_code_server.lower():
            return http.JsonResponse({'code':400,'errmsg':'输入图形验证码有误'})
        # 7.生成短信验证码:生成6位数验证码
        sms_code = '%06d'%random.randint(0,999999)
        logger.info(sms_code)
        # 8.保存短信验证码
        redis_conn.setex('sms_%s'%mobile, 300, sms_code)
        # 9.发送短信验证码
        CCP().send_template_sms(mobile,[sms_code,5],1)
        # 10.响应结果
        return http.JsonResponse({'code':0,'errmsg':'发送短信成功'})