from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    email_active = models.BooleanField(default=False,verbose_name='邮箱是否激活')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    #创建类方法, 生成邮箱验证链接
    def generate_verify_email_url(self):
        #生成加密对象
        obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY,expires_in=3600*24)
        #设置加密数据
        dict = {'user_id':self.id, 'email':self.email}
        #对象.dumps(数据)生成加密token
        token = obj.dumps(dict).decode()
        #拼接加密邮箱验证链接
        verify_url = settings.EMAIL_VERIFY_URL + token
        return verify_url