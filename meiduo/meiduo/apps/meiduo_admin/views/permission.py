from django.contrib.auth.models import Permission
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.permission import PermissionSerialzier

class PermissionModelViewSet(ModelViewSet):
    serializer_class = PermissionSerialzier
    queryset = Permission.objects.all()
    pagination_class = PageNum