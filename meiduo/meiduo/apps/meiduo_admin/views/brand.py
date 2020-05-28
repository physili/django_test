from rest_framework.viewsets import ModelViewSet
from goods.models import Brand
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.brand import BrandSerializer

#查询获取,保存,修改,删除品牌
class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = PageNum
