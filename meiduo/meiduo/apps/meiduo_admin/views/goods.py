from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from goods.models import Goods, Brand
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.goods import GoodsSerializer, BrandSerializer

#查询获取SPU表列表数据
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


#1、获取品牌信息
class BrandAPIView(APIView):
    def get(self,request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)