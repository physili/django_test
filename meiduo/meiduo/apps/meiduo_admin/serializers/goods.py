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
        extra_kwargs = {
            'sales':{'required':False},
            'comments':{'required':False},
            'category1':{'required':False},
            'category2':{'required':False},
            'category3':{'required':False},
        }



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id','name')

class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id','name')