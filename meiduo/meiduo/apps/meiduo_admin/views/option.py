from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from goods.models import SpecificationOption, GoodsSpecification
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.option import SpecificationOptionSerializer, GoodsSpecificationSerializer

#查询获取,保存,修改,删除规格选项
class SpecificationOptionModelViewSet(ModelViewSet):
    queryset = SpecificationOption.objects.all()
    serializer_class = SpecificationOptionSerializer
    pagination_class = PageNum

class GoodsSpecificationAPIView(APIView):
    def get(self, request):
        specs = GoodsSpecification.objects.all()
        serializer = GoodsSpecificationSerializer(specs, many=True)
        return Response(serializer.data)