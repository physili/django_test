from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User2(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True,verbose_name='手机号')
    email_active = models.BooleanField(default=False,verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users2'
        verbose_name = '用户2'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
