from django.db import models

# Create your models here.
from meiduo.utils.BaseModel import BaseModel

class ContentCategory(BaseModel):                #广告类别表
    name = models.CharField(max_length=50, verbose_name='名称')     # 广告类别名称
    key = models.CharField(max_length=50, verbose_name='类别键名') # 广告的类别键名:
    class Meta:
        db_table = 'tb_content_category'
        verbose_name = '广告内容类别'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Content(BaseModel):                   #广告内容表
    category = models.ForeignKey(ContentCategory,  on_delete=models.PROTECT,  verbose_name='类别')# 外键,
    title = models.CharField(max_length=100,   verbose_name='标题')# 广告标题
    url = models.CharField(max_length=300, verbose_name='内容链接') # 广告被点击后跳转的 url
    image = models.ImageField(null=True,   blank=True, verbose_name='图片')# 广告图片地址保存字段:
    text = models.TextField(null=True,  blank=True,  verbose_name='内容') # 文字性广告保存在该字段:
    sequence = models.IntegerField(verbose_name='排序')# 广告内容排序:
    status = models.BooleanField(default=True, verbose_name='是否展示')# 广告是否展示的状态:
    class Meta:
        db_table = 'tb_content'
        verbose_name = '广告内容'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.category.name + ': ' + self.title