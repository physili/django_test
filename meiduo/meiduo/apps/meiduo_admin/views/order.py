from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import OrderInfo, OrderGoods
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.order import OrderInfoSerializer,OrderGoodsSerializer

class OrderModelViewSet(ModelViewSet):
    serializer_class = OrderInfoSerializer
    pagination_class = PageNum

    # 根据用户的不同操作提供不同的查询集
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return OrderInfo.objects.filter(user__contains=keyword)
        else:
            return OrderInfo.objects.all()