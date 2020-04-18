from django.shortcuts import render
from datetime import date
from django.http import HttpResponse
from django.views import View
from .models import BookInfo,HeroInfo


class SaveDataView(View):
    def get(self,request):
        # # 使用对象.save()增加数据
        # book = BookInfo(
        #     b_title='西游记',
        #     b_pub_date=date(1991,1,1),
        #     b_read=100,
        #     b_comment=10,
        #     is_delete=False
        # )
        # book.save()
        # result = HttpResponse('save')

        # 使用模型类.objects.create()增加数据
        BookInfo.objects.create(
            b_title='寻秦记',
            b_pub_date=date(1992,1,1),
            b_read=1000,
            b_comment=300,
            is_delete=False
        )
        result = HttpResponse('creat')

        return result

    def post(self,request):
        # 基本查询get
        book = BookInfo.objects.get(id=2)
        print(book.b_title)
        result = HttpResponse('get')
        return result