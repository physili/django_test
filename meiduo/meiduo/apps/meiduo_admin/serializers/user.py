from rest_framework import serializers
from users.models import User
# from users.utils import UserManager
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','mobile','email','password')
        #设置字段的属性
        extra_kwargs = {
            'username':{'max_length':20,'min_length':5},
            'password':{'max_length':20,'min_length':8,'write_only':True}
        }

    # 重写create方法, 新增用户并加密
    def create(self, validated_data):
        #给password加密
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user