from rest_framework import serializers
from goods.models import GoodsSpecification

class GoodsSpecificationSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = GoodsSpecification
        fields = '__all__'
