from rest_framework import serializers
from goods.models import SpecificationOption, GoodsSpecification

class SpecificationOptionSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField()
    spec_id = serializers.IntegerField()
    class Meta:
        model = SpecificationOption
        fields = '__all__'


class GoodsSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsSpecification
        fields = ('id','name')