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

    # 重写create方法, 新增用户并加密
    def create(self, validated_data):
        #调用父类方法创建管理员用户
        admin = super().create(validated_data)
        #对新用户的密码加密
        password = validated_data['password']
        admin.set_password(password)
        admin.is_staff = True
        admin.save()
        return admin

    #重写update方法, 给用户改密码
    def update(self, instance, validated_data):
        # 调用父类实现数据更新
        super().update(instance,validated_data)
        password = validated_data['password']
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class GroupSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields="__all__"
