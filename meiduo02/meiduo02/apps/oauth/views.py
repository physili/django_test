from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django import http
from django.views import View
from oauth.models import OAuthQQUser
import logging,json,re
logger = logging.getLogger('django')
from django.contrib.auth import login
from django_redis import get_redis_connection
from users.models import User2


#第一个接口,返回qq登录网址
class QQURLView(View):
    def get(self, request):
        next = request.GET.get('next')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        login_url = oauth.get_qq_url()
        return http.JsonResponse({'code': 0,  'errmsg': 'OK',  'login_url':login_url})


#第二个接口, 把code转化成openid, 并判断数据库是否有值
#用session保存openid值
class QQUserView(View):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return http.JsonResponse({'code': 400, 'errmsg': '缺少code参数'})
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '获取openid出错'})

        try:
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except Exception as e:
            # 采用session形式保存openid
            # 创建request.session['键'] = 值
            # 取值value = request.session.get('键',默认值)
            # 设置时长request.session.set_expiry(value)
            request.session['openid'] = openid
            request.session.set_expiry(600)
            return http.JsonResponse({'code': 300, 'errmsg': 'ok'})

        else:
            user = oauth_qq.user
            login(request, user)
            response = http.JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
            return response


    #第三个接口, 用户绑定openid
    def post(self,request):
        #1.接受请求,提取参数(mobile, password, sms_code, session)
        dict = json.loads(request.body.decode())
        mobile = dict.get('mobile')
        password = dict.get('password')
        sms_code_client = dict.get('sms_code')

        #2.验证参数(整体)
        if not all([mobile,password,sms_code_client]):
            return http.JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #3.验证参数(单个)
        if not re.match(r'^1[3-9]\d{9}$', mobile):  # 判断手机号是否合法
            return http.JsonResponse({'code': 400, 'errmsg': '请输入正确的手机号码'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):  # 判断密码是否合格
            return http.JsonResponse({'code': 400, 'errmsg': '请输入8-20位的密码'})
        #4.比较验证码
        redis_conn_sms = get_redis_connection('verify_code')
        sms_code_server = redis_conn_sms.get('sms_%s' % mobile)
        if sms_code_server is None:  # 判断获取出来的有没有:
            return http.JsonResponse({'code': 400, 'errmsg': '验证码失效'})
        if sms_code_client != sms_code_server.decode():  # 如果有, 则进行判断:
            return http.JsonResponse({'code': 400, 'errmsg': '输入的验证码有误'})
        #5.提取sessionid取出openid, value = request.session.get('键',默认值)
        openid = request.session.get('openid',None)
        if openid is None:
            return http.JsonResponse({'code': 400, 'errmsg': '缺少openid'})

        #6.保存用户信息
        try:
            user = User2.objects.get(mobile=mobile)
        except Exception as e:
            user = User2.objects.create_user(username=mobile,password=password,mobile=mobile)
        else:
            if not user.check_password(password):
                return http.JsonResponse({'code':400, 'errmsg':'输入的密码不正确'})
        #6.2绑定openid
        try:
            OAuthQQUser.objects.create(openid=openid,user=user)
        except Exception as e:
            return http.JsonResponse({'code':400, 'errmsg':'往数据库添加数据出错'})
        #7.保持状态
        login(request,user)
        #8.返回cookie信息
        response = http.JsonResponse({'code':0, 'errmsg':'ok'})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        #9.返回json数据
        return response