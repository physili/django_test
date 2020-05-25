from rest_framework.generics import ListCreateAPIView
from meiduo_admin.serializers.user import UserSerializer
from meiduo_admin.utils import PageNum
from users.models import User
#展示用户和新增用户
class UserListView(ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNum
    # 根据用户的不同操作提供不同的查询集
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return User.objects.filter(username__contains=keyword)
        else:
            return User.objects.all()
