from django.contrib.auth.models import Permission, ContentType
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.permission import PermissionSerialzier, ContentTypeSerialzier
#获取权限数据, 保存权限数据, 更新权限数据, 删除权限数据
class PermissionModelViewSet(ModelViewSet):
    serializer_class = PermissionSerialzier
    queryset = Permission.objects.all()
    pagination_class = PageNum

#获取权限类型列表数据
class ContentTypeAPIView(APIView):
    def get(self,request):
        contents = ContentType.objects.all()
        serializer = ContentTypeSerialzier(contents, many=True)
        return Response(serializer.data)