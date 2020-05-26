from rest_framework import serializers
from orders.models import OrderInfo, OrderGoods
from goods.models import SKU

class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'

class OrderGoodsSerializer(serializers.ModelSerializer):
    sku = SKUSerializer()
    class Meta:
        model = OrderGoods
        fields = '__all__'



class OrderInfoSerializer(serializers.ModelSerializer):
    skus = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'
        extra_kwargs = {
            'user':{'required': False},
            'address':{'required': False},
            'total_count':{'required': False},
            'total_amount':{'required': False},
            'freight':{'required': False},
            'pay_method':{'required': False},
        }

