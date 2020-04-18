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
