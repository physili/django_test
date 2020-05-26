from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from orders.models import OrderInfo
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.order import OrderInfoSerializer
from rest_framework.decorators import action

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

    #添加额外的方法: 更新订单表状态数据
    @action(methods=['put'], detail=True)
    def status(self,request, pk=None):
        order = self.get_object()
        status = request.data['status']
        if isinstance(status,int):
            try:
                order.status = status
                order.save()
                return Response({"order_id": order.order_id, "status": order.status})
            except Exception as e:
                return Response({'code':400,'errmsg':'保存数据出错'})
        else:
            return Response({'code':400,'errmsg':'status有误'})
