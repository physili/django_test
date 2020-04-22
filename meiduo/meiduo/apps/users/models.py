from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class BookInfo(models.Model):
    b_title=models.CharField(max_length=20,verbose_name='书名')

    class Meta:
        db_table = 'tb_bookinfo'
        verbose_name = '图书信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.b_title