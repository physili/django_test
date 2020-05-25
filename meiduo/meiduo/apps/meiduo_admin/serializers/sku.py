from rest_framework import serializers
from goods.models import SKU, GoodsCategory, Goods, SpecificationOption, GoodsSpecification


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

class GoodsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = ('id','value')

class GoodsSpecSerializer(serializers.ModelSerializer):
    options = GoodsOptionSerializer(many=True)
    # spu: str
    spu = serializers.StringRelatedField()
    # spu_id: id
    spu_id = serializers.IntegerField()
    class Meta:
        model = GoodsSpecification
        fields = '__all__'