from django.contrib.auth.backends import ModelBackend
import re
from .models import User
def get_user_by_account(account):
    try:
        if re.match(r'1[3-9]\d{9}$',account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

#AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        #判断是后台还是前台传入的登录验证
        if request is None: # 后台用户走 后台验证逻辑
            admin_user = User.objects.get(username=username)
            if admin_user.check_password(password) and admin_user.is_superuser:
                return admin_user

        else:# 普通用户还走原来的业务逻辑
            user = get_user_by_account(username)
            if user and user.check_password(password):
                return user