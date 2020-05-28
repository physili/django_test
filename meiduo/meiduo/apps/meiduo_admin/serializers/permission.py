from django.contrib.auth.models import Permission, ContentType
from rest_framework import serializers

class PermissionSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields="__all__"

class ContentTypeSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('id','name')