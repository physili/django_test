from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.group import GroupSerialzier, PermissionSerialzier
#获取用户组表列表数据, 保存,更新,删除分组表数据功能
class GroupModelViewSet(ModelViewSet):
    serializer_class = GroupSerialzier
    queryset = Group.objects.all()
    pagination_class = PageNum


#获取权限表数据
class PermissionAPIView(APIView):
    def get(self,request):
        perms = Permission.objects.all()
        serializer = PermissionSerialzier(perms, many=True)
        return Response(serializer.data)