from rest_framework.viewsets import ModelViewSet
from goods.models import GoodsSpecification
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.spec import GoodsSpecificationSerializer

#查询获取,保存,修改,删除商品类别的规格列表数据
class GoodsSpecificationModelViewSet(ModelViewSet):
    queryset = GoodsSpecification.objects.all()
    serializer_class = GoodsSpecificationSerializer
    pagination_class = PageNum
