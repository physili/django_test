from rest_framework import serializers
from goods.models import Goods

class GoodsSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()
    class Meta:
        model = Goods
        fields = '__all__'