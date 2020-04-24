from django.shortcuts import render

# Create your views here.
from django.views import View
from django import http
from django_redis import get_redis_connection
import logging
logger = logging.getLogger('django')
from celery_tasks.sms.tasks import ccp_send_sms_code
from meiduo02.libs.captcha.captcha import captcha
import random

class ImageCodeView(View):
    def get(self,request,uuid):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s'%uuid,300,text)
        return http.HttpResponse(image,content_type='image/jpg')

class SMSCodeView(View):
    def get(self,request,mobile):
        # 0.检验短信标志是否存在, 避免短信轰炸
        # 需要先链接数据库, 提取短信标志, 才能判断
        redis_conn = get_redis_connection('verify_code')
        send_flag = redis_conn.get('send_flag_%s'%mobile)
        if send_flag:
            return http.JsonResponse({'code':400,'errmsg':'短信发送过于频繁'})
        # 1.获取参数
        uuid = request.GET.get('image_code_id')
        image_code_client = request.GET.get('image_code')
        # 2.验证参数(整体验证, 单个验证)
        if not all([uuid,image_code_client]):
            return http.JsonResponse({'code':400,'errmsg':'参数有误'})
        # 图形验证码检验(提取,删除,对比)
        # 提取
        image_code_server = redis_conn.get('img_%s'%uuid)
        if image_code_server is None:
            return http.JsonResponse({'code':400,'errmsg':'图形码失效'})
        # 删除
        try:
            redis_conn.delete('img_%s'%uuid)
        except Exception as e:
            logger.error(e)
        # 对比
        if image_code_client.lower() != image_code_server.decode().lower():
            return http.JsonResponse({'code':400,'errmsg':'图形码验证失败'})
        # 3.生成短信验证码
        sms_code = '%d'%random.randint(100000,999999)
        logger.info(sms_code)
        # 4.保存短信验证码
        # 用管道pipeline
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, 300, sms_code)
        pl.setex('send_flag_%s'%mobile,60,1)
        pl.execute()
        # 5.发送短信验证码
        #采用异步方案
        ccp_send_sms_code.delay(mobile,sms_code)
        # 6.返回响应结果
        return http.JsonResponse({'code':200,'errmsg':'ok'})