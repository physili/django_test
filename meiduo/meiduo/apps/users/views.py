from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from users.models import User
from django_redis import get_redis_connection
import json
import re
from django.contrib.auth import login, authenticate, logout


#用户名重复注册验证
class UsernameCountView(View):
    def get(self,request,username):
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code':400, 'errmsg':'访问服务器失败'})
        return JsonResponse({'code':200,'errmsg':'ok','count':count})

#手机号重复注册验证
class MobileCountView(View):
    def get(self,request,mobile):
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'查询出错'})
        return JsonResponse({'code':200,'errmsg':'ok','count':count})

class RegisterView(View):
    def post(self,request):
        # 1.接受数据
        dict = json.loads(request.body.decode())
        # 2.提取参数
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        sms_code_client = dict.get('sms_code')
        # 3.检验参数(整体)
        if not all([username,password,password2,mobile,allow,sms_code_client]):
            return JsonResponse({'code':400,'errmsg':'传入参数缺少'})
        # 4.检验参数(单个)
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误'})
        if not re.match(r'^[a-zA-Z0-9]{8,20}$',password):
            return JsonResponse({'code': 400,  'errmsg': 'password格式有误'})
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对'})
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return JsonResponse({'code': 400,'errmsg': 'mobile格式有误'})
        if allow==False:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误'})

        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s'%mobile)
        if sms_code_server is None:
            return JsonResponse({'code': 400,'errmsg': '短信验证码过期'})
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '验证码有误'})
        # 5.保存用户
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保存到数据库出错'})
        # 6.状态保持
        login(request,user)
        # 登录后显示用户名
        # 通过cookie携带用户信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username',user.username,max_age=3600*24*12)
        # 7.返回响应
        return response

class LoginView(View):
    def post(self,request):
        #1.接受请求,提取参数
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        #2.检验参数(整体检验)
        if not all([username,password,remembered]):
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.登录认证authenticate
        user = authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({'code': 400,'errmsg': '用户名或者密码错误'})
        #4.保持状态login
        login(request,user)
        #5.判断是否需要记住登录
        if remembered == True:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.set_cookie('username',user.username,max_age=3600*24*12)

        #6.返回响应
        return response


#退出登录接口
class LogoutView(View):
    def delete(self,request):
        '''实现退出登录逻辑'''
        #清理session
        logout(request)

        #创建response对象, 删除cookie信息
        response = JsonResponse({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')
        return response
