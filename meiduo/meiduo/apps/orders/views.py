from django.shortcuts import render


# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse
from goods.models import SKU
from users.models import Address
from meiduo.utils.views import LoginVerifyMixin

#结算订单
class OrderSettlementView(LoginVerifyMixin,View): #用户登录了, 才能进来
    #提供订单结算页面
    def get(self,request):
        user = request.user
        #提取Address数据库数据
        try:
            addresses = Address.objects.filter(user_id=user.id, is_deleted=False)
        except Exception as e:
            #若提取不了,说明还没有设置地址信息而已,不需要返回return
            addresses = None
        #构建address返回信息
        address_list = []
        for address in addresses:
            address_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })

        #从Redis购物车中查询出被勾选的商品信息sku_id与count
        redis_conn = get_redis_connection('carts')
        hash_dict = redis_conn.hgetall('carts_%s'%user.id)
        set_select = redis_conn.smembers('selected_%s'%user.id)
        dict = {}
        for sku_id in set_select:
            dict[int(sku_id)]=int(hash_dict.get(sku_id))

        #查询商品信息
        sku_list = []
        skus = SKU.objects.filter(id__in=dict.keys())
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image_url,
                'count': dict[sku.id],
                'price': sku.price
            })

        #整理最后的返回内容
        context = {'addresses': address_list,'skus': sku_list,'freight': 10.00,}
        return JsonResponse({'code':0,'errmsg':'ok','context':context})