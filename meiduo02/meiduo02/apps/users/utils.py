from django.contrib.auth.backends import ModelBackend
import re
from .models import User2

def get_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$',account):
            user = User2.objects.get(mobile=account)
        else:
            user = User2.objects.get(username=account)
    except User2.DoesNotExist:
        return None
    else:
        return user

class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
