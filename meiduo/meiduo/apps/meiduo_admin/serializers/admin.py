from django.contrib.auth.models import Group
from rest_framework import serializers

from users.models import User


class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','mobile','email','password','groups','user_permissions')
        extra_kwargs = {
            'id': {'required': False},
            'email':{'required':False},
            'password': {'max_length': 20, 'min_length': 8, 'write_only': True}
        }

    # # 重写create方法, 新增用户并加密
    # def create(self, validated_data):
    #     # 给password加密
    #     user = User.objects.create_user(**validated_data)
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save()
    #     return user


class GroupSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields="__all__"
