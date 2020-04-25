from django.contrib.auth import login,authenticate,logout

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
import logging

from meiduo02.utils.views import LoginVerifyMixin

logger = logging.getLogger('django')
from users.models import User2
import re
import json

# Create your views here.
#用户名重复验证接口
class UsernameCountView(View):
    '''判断用户是否重复'''
    def get(self,request,username):
        '''判断用户名是否重复'''
    # 1.查询username在数据库中的个数
        try:
            count = User2.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'访问数据库失败'})
    # 2.返回结果json-->code&errmsg&count
        return JsonResponse({'code':200,'errmsg':'ok','count':'count'})

#手机号重复验证接口
class MobileCountView(View):
    '''判断手机号是否重复'''
    def get(self,request,mobile):
        '''判断手机号是否重复'''
        try:
            count = User2.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'访问数据库失败'})
        return JsonResponse({'code':200,'errmsg':'ok','count':'count'})

#注册接口
class RegisterView(View):
    def post(self,request):
        #1.接受请求, 提取参数(username,password,psd2,mobile,sms_code,allow)
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        sms_code_client = dict.get('sms_code')
        #2.验证参数(整体验证)
        if not all([username,password,password2,mobile,allow,sms_code_client]):
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.单个验证参数
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误'})
        if not re.match(r'^[a-zA-Z0-9]{8,20}$',password):
            return JsonResponse({'code': 400,  'errmsg': 'password格式有误'})
        if password2 != password:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对'})
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return JsonResponse({'code': 400,'errmsg': 'mobile格式有误'})
        if allow == False:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误'})
        #3.1验证短信码
        #3.1.1提取短信验证码
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s'%mobile)
        #3.1.2判断是否过期无效
        if sms_code_server is None:
            return JsonResponse({'code': 400,'errmsg': '短信验证码过期'})
        #3.1.3判断sms_code是否正确
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '验证码有误'})
        #4.保存数据到MySQL(try),用模型类
        try:
            user = User2.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保存到数据库出错'})
        #5.状态保存, 生成session返回,用login
        login(request,user)
        #用cookie携带用户user的信息返回, 展示用户名信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username',user.username,max_age=3600*24*12)
        #6.返回响应
        return response

#登录接口
class LoginView(View):
    def post(self,request):
        #1.接受请求,提取参数(username,password,remembered)
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        #2.验证参数(整体)
        if not all([username,password,remembered]):
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.验证username和password用authenticate
        #3.2判断user是否存在
        user = authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'验证失败'})
        #4.保持状态
        login(request,user)
        #5.判断是否remembered
        if remembered == True:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        #6.cookie携带用户名信息,显示信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=3600*24*12)
        #7.响应返回
        return response


#登录退出接口
class LogoutView(View):
    def delete(self,request):
        logout(request)

        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')
        return response


#用户信息中心
class UserInfoView(LoginVerifyMixin,View):
    def get(self,request):
        pass