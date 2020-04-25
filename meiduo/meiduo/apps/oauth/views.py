from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django import http
from django.views import View
from oauth.models import OAuthQQUser
import logging
logger = logging.getLogger('django')
from django.contrib.auth import login
from oauth.utils import encrypt_openid


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
            #10返回响应
            return response