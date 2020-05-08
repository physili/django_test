from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django import http
from django.views import View

from carts.utils import merge_cart_cookie_to_redis
from oauth.models import OAuthQQUser
import logging
from django.db import DatabaseError
from users.models import User

logger = logging.getLogger('django')
from django.contrib.auth import login
from oauth.utils import encrypt_openid,check_access_token
import json
import re
from django_redis import get_redis_connection

# Create your views here.
#第一个接口:返回qq登录网址(包含内容有:client_id,redirect_uri,state)
class QQURLView(View):
    def get(self,request):
        #先接受请求,提取参数
        next = request.GET.get('next')
        #生成一个QQlogintool工具对象, 用于调取其他函数
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        #对象.方法(),获取qq登录网址(并附带其他信息),具体可查看该工具的源码
        login_url = oauth.get_qq_url()
        return http.JsonResponse({'code': 0,  'errmsg': 'OK',  'login_url':login_url})

#第二个接口,把code转化成openid, 并保存用户信息
class QQUserView(View):
    def get(self,request):
        #1.接受请求,提取参数
        code = request.GET.get('code')
        #2.检验参数:判断参数是否存在
        if not code:
            return http.JsonResponse({'code': 400, 'errmsg': '缺少code参数'})
        #3.创建qqlogintool工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            #4.对象.get_access_token()获取access_token值
            access_token = oauth.get_access_token(code)
            #5.对象.get_open_id()获取openid值
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '获取openid出错'})

        try:
            #6.查看数据库是否存有对应的openid值
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            #没有
            #11.把openid封装加密成token值
            access_token = encrypt_openid(openid)
            #12.把值返回到前端
            return http.JsonResponse({'code':300, 'errmsg':'ok', 'access_token':access_token})

        else:
            #有
            #7.获取记录对象. oauth_qq.user的user是该数据库的外键字段
            user = oauth_qq.user
            #8.实现状态保持
            login(request,user)
            response = http.JsonResponse({'code':0,'errmsg':'ok'})
            #9.通过cookie实现用户名显示
            response.set_cookie('username',user.username,max_age=3600*24)

            # 增加合并购物车功能
            response = merge_cart_cookie_to_redis(request, response)

            #10返回响应
            return response

    #第三个接口, 解密openid, 并保存用户信息
    def post(self,request):
        #1.接受请求, 提取参数(mobile,password,sms_code,access_token)
        dict = json.loads(request.body.decode())
        mobile = dict.get('mobile')
        password = dict.get('password')
        sms_code_client = dict.get('sms_code')
        access_token = dict.get('access_token')
        #2.检验参数, 整体检验
        if not all([mobile,password,sms_code_client]):
            return http.JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.单独检验(mobile,password
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return http.JsonResponse({'code':400, 'errmsg':'请输入正确的手机号码'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return http.JsonResponse({'code':400, 'errmsg':'请输入8-20位的密码'})
        #4.单个检验:sms_code
        #4.2创建redis链接对象
        redis_conn = get_redis_connection('verify_code')
        #4.3提取redis值
        try:
            sms_code_server = redis_conn.get('sms_%s' % mobile)
        except Exception as e:
            return http.JsonResponse({'code':400, 'errmsg':'数据库访问失败'})
        if sms_code_server is None:
            return http.JsonResponse({'code': 400, 'errmsg': '验证码失效'})
        if sms_code_client != sms_code_server.decode():
            return http.JsonResponse({'code':400,'errmsg':'输入的验证码有误'})
        #5.单个检验:access_token
        #5.2自定义一个检验函数-->在oauth/utils.py中
        openid = check_access_token(access_token)
        #5.3判断解密后的openid是否存在
        if openid is None:
            return http.JsonResponse({'code':400, 'errmsg':'缺少openid'})

        #6.从User表中获取一个该手机号对应的用户
        try:
            user = User.objects.get(mobile=mobile)
        #7.如果该客户不存在,给User增加一个新记录
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile,password=password,mobile=mobile)
        #8.如果存在,比较密码是否一致
        else:
            if not user.check_password(password):
                return http.JsonResponse({'code':400, 'errmsg':'输入的密码不正确'})
        #9.把openid和user保存到QQ表
        try:
            OAuthQQUser.objects.create(openid=openid,user=user)
        except DatabaseError:
            return http.JsonResponse({'code':400, 'errmsg':'往数据库添加数据出错'})
        #10.保持状态
        login(request,user)
        response = http.JsonResponse({'code':0, 'errmsg':'ok'})
        #11.设置cookie:username
        response.set_cookie('username',user.username,max_age=3600*24)

        # 增加合并购物车功能
        response = merge_cart_cookie_to_redis(request, response)

        #12.返回json
        return response