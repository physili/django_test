from rest_framework import serializers
from orders.models import OrderInfo, OrderGoods
from goods.models import SKU
from django.db import transaction

class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'

class OrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'



class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('order_id','create_time')


