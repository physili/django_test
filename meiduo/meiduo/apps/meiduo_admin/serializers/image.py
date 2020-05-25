from rest_framework import serializers
from goods.models import SKUImage, SKU

#序列化SKUImage
class ImageSerializer(serializers.ModelSerializer):
    sku = serializers.PrimaryKeyRelatedField(read_only=True)
    # sku = serializers.StringRelatedField(label='sku管理的模型__str__的内容')
    class Meta:
        model = SKUImage
        fields = ('sku','image','id')

#序列化SKU
class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('id','name')