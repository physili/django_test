from django.contrib.auth.models import Group,Permission
from rest_framework import serializers

class GroupSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields="__all__"

class PermissionSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields="__all__"
