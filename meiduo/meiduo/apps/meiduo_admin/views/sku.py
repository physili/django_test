from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from goods.models import SKU, GoodsCategory, Goods, GoodsSpecification
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.sku import SKUSerializer, SKUCategoriesSerializer, GoodsSimpleSerializer, GoodsSpecSerializer

#1.获取sku数据
class SKUModelViewSet(ModelViewSet):
    serializer_class = SKUSerializer
    pagination_class = PageNum
    # 根据用户的不同操作提供不同的查询集
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return SKU.objects.filter(name__contains=keyword)
        else:
            return SKU.objects.all()


#获取category的三级分类信息
class SKUCategoriesView(ListAPIView):
    serializer_class = SKUCategoriesSerializer
    #goodscategory = None 指:下一级对象是空的
    #获取自关联的最后一级
    queryset = GoodsCategory.objects.filter(goodscategory=None)


#获取SPU表名称数据
class GoodsSimpleView(ListAPIView):
    serializer_class = GoodsSimpleSerializer
    queryset = Goods.objects.all()


#获取SPU商品规格信息
class GoodsSpecView(ListAPIView):
    serializer_class = GoodsSpecSerializer
    #查询集是用户指定的某一spu_id, 所以重写queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return GoodsSpecification.objects.filter(spu_id=pk)
#获取SPU商品规格信息, 方式二
# class GoodsSpecAPIView(APIView):
#     def get(self,request,pk):
#         gs = GoodsSpecification.objects.filter(spu_id=pk)
#         serializer = GoodsSpecSerializer(gs,many=True)
#         return Response(serializer.data)