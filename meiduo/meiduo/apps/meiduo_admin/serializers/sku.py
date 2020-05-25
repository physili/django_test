from rest_framework import serializers
from goods.models import SKU, GoodsCategory, Goods


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'

class SKUCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'