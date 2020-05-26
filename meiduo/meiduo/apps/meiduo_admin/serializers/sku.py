from rest_framework import serializers
from goods.models import SKU, GoodsCategory, Goods, SpecificationOption, GoodsSpecification, SKUSpecification
from django.db import transaction

class SKUSpecificationSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()
    class Meta:
        model = SKUSpecification
        fields = ('spec_id','option_id')

class SKUSerializer(serializers.ModelSerializer):
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    spu = serializers.StringRelatedField(required=False)
    category = serializers.StringRelatedField(required=False)
    #获取SKUSpecification的两个字段
    specs = SKUSpecificationSerializer(many=True)
    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        #获取规格信息,并从validated_data数据中, 删除规格信息数据
        specs_data = validated_data.pop('specs')
        #开启事务保存多表数据
        with transaction.atomic():
            #设置保存点
            savepoint = transaction.savepoint()
            #保存sku数据库信息
            sku = SKU.objects.create(**validated_data)
            #保存skuspecification的数据库信息
            for spec_data in specs_data:
                SKUSpecification.objects.create(sku=sku,**spec_data)
            #清除保存点
            transaction.savepoint_commit(savepoint)
            return sku



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