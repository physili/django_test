from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings
from meiduo.utils.BaseModel import BaseModel

# Create your models here.
#创建用户模型类
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False,verbose_name='邮箱是否激活')
    default_address = models.ForeignKey('Address',related_name='users',null=True,blank=True,on_delete=models.SET_NULL,verbose_name='默认地址')

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

    #创建类方法, 检验邮箱验证链接
    @staticmethod
    def check_verify_email_url(token):
        # 生成解密对象
        obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY,expires_in=3600*24)
        try:
            #解密
            dict = obj.loads(token)
        except Exception as e:
            return None
        else:
            #获取解密内容
            user_id = dict.get('user_id')
            email = dict.get('email')
        try:
            #获取内容相符的对象
            user = User.objects.get(id=user_id,email=email)
        except Exception as e:
            return None
        else:
            #返回数据库对象
            return user


#创建用户地址模型类
class Address(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses',verbose_name='用户')
    province = models.ForeignKey('areas.Area',on_delete=models.PROTECT,related_name='province_addresses',verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses',verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',verbose_name='区')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']