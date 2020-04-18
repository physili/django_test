from django.db import models

class BookInfo(models.Model):
    b_title = models.CharField(max_length=20,verbose_name='标题')
    b_pub_date = models.DateTimeField(verbose_name='发布日期')
    b_read = models.IntegerField(default=0,verbose_name='阅读量')
    b_comment = models.IntegerField(default=0,verbose_name="评论量")
    is_delete = models.BooleanField(default=False,verbose_name="逻辑删除")

    class Meta:
        db_table = 'tb_books'
        verbose_name = '图书表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.b_title

class HeroInfo(models.Model):
    GENDER_CHOICES = ((0,'female'),(1,'male'))
    h_name = models.CharField(max_length=20, verbose_name='名称')
    h_gender = models.SmallIntegerField(choices=GENDER_CHOICES,default=0,verbose_name='性别')
    h_comment = models.CharField(max_length=200,null=True,verbose_name='描述信息')
    h_book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.h_name