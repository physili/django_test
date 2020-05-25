from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from goods.models import SKU, GoodsCategory
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.sku import SKUSerializer, SKUCategoriesSerializer

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