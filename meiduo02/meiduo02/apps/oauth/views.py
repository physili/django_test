from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django import http
from django.views import View
from oauth.models import OAuthQQUser
import logging
logger = logging.getLogger('django')
from django.contrib.auth import login


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