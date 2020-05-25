from datetime import date, timedelta

from goods.models import GoodsVisitCount
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

#用户总量统计
class UserTotalCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        now_date = date.today()
        print(now_date,type(now_date))
        count = User.objects.all().count()
        return Response({'count':count,'date':now_date})


#日活跃用户统计
class UserDailyActiveCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        now_date = date.today()
        count = User.objects.filter(last_login__gte=now_date).count()
        return Response({'count':count,'date':now_date})


#日下单用户量统计
class UserDailyOrderCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        now_date = date.today()
        count = User.objects.filter(orderinfo__create_time__gte=now_date).count()
        return Response({'count':count,'date':now_date})


#月增用户统计
class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        now_date = date.today()
        start_date = now_date - timedelta(days=30)
        date_list = []
        for i in range(1,31):
            index_date = start_date + timedelta(days=i)
            cur_date = start_date + timedelta(days=i+1)
            count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date).count()
            date_list.append({'count':count,'date':index_date})
        return Response(date_list)


#日增用户统计
class UserDayCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        now_date = date.today()# 获取当前日期
        count = User.objects.filter(date_joined__gte=now_date).count()
        return Response({'count': count,'date': now_date})


#日分类商品访问量
class CategoryVistCountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        now_date = date.today()
        cates = GoodsVisitCount.objects.filter(date=now_date)
        list = []
        for cate in cates:
            list.append({"category": cate.category.name,"count": cate.count})
        return Response(list)
