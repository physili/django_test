#导入itsdangerous前,需安装pip install itsdangerous
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings

#定义一个加密方法
def encrypt_openid(openid):
    #把openid加密成access_token
    #先创建对象
    obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    #对象.dumps()加密
    access_token = obj.dumps({'openid':openid}).decode()
    return access_token
