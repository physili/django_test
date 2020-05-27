from rest_framework import serializers
from goods.models import Goods, Brand, GoodsCategory

class GoodsSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()
    class Meta:
        model = Goods
        fields = '__all__'



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id','name')

class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id','name')