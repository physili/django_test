from rest_framework.viewsets import ModelViewSet
from goods.models import Goods
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.goods import GoodsSerializer

class GoodsModelViewSet(ModelViewSet):
    serializer_class = GoodsSerializer
    pagination_class = PageNum
    # 根据用户的不同操作提供不同的查询集
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return Goods.objects.filter(name__contains=keyword)
        else:
            return Goods.objects.all()
