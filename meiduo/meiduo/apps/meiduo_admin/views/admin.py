from django.contrib.auth.models import Group
from users.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.admin import UserSerialzier, GroupSerialzier
#获取管理员用户列表数据, 保存,更新,删除管理员数据
class UserModelViewSet(ModelViewSet):
    serializer_class = UserSerialzier
    queryset = User.objects.all()
    pagination_class = PageNum


#获取组表数据
class GroupAPIView(APIView):
    def get(self,request):
        groups = Group.objects.all()
        serializer = GroupSerialzier(groups, many=True)
        return Response(serializer.data)