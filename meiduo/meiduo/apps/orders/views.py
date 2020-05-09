import json
from decimal import Decimal

from django.db import transaction
from django.shortcuts import render

from django.utils import timezone
# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse
from goods.models import SKU
from orders.models import OrderInfo, OrderGoods
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


#提交订单
class OrderCommitView(View):
    def post(self,request):
        #1.提取参数address_id, pay_method
        dict = json.loads(request.body.decode())
        address_id = dict.get('address_id')
        pay_method = dict.get('pay_method')
        #2.验证参数(整体
        if not all([address_id,pay_method]):
            return JsonResponse({'code':400,
                                 'errmsg':"缺少必传参数"})
        #3.验证参数(单个: address_id是否存在并生成address对象,
        try:
            address = Address.objects.get(id=address_id)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': "address_id有误"})
        #4.验证参数(单个: pay_method是否存在
        if pay_method not in [1,2]:
            return JsonResponse({'code': 400,
                                 'errmsg': "pay_method有误"})
        #5.从redis的hash表里提取count
        user = request.user
        redis_conn = get_redis_connection('carts')
        hash_dict = redis_conn.hgetall('carts_%s'%user.id)
        #6.从redis的set表里提取选中的sku_id
        set_sku_ids = redis_conn.smembers('selected_%s' % user.id)
        carts_dict = {}
        for sku_id in set_sku_ids:
            carts_dict[int(sku_id)] = int(hash_dict.get(sku_id))
        #7.生成order_id
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d'%user.id)
        #用with transaction创建事务
        with transaction.atomic():
            #设置savepoint
            save_id = transaction.savepoint()
            #8.往orderInfo里写入数据
            #9.新建order记录:order_id,address_id,pay_method,user,total_count,total_amount,freight,status)
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=request.user,
                address=address,
                total_count=0,
                total_amount=Decimal('0.00'),
                freight=Decimal('10.00'),
                pay_method=pay_method,
                status=1 if pay_method == 2 else 2
            )
            #10.往ordergoods里写入数据
            #11.遍历sku_id,创建记录:sku_id....
            sku_ids = carts_dict.keys()
            for sku_id in sku_ids:
                #开启乐观锁
                while True:
                    sku = SKU.objects.get(id=sku_id)
                    #乐观锁--读取原始库存
                    origin_stock = sku.stock
                    origin_sales = sku.sales
                    #判断sku库存
                    sku_count = carts_dict[sku_id]
                    if sku_count > sku.stock:
                        #事务回滚:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'code':400,
                                             'errmsg':'库存不足'})
                    #12.修改SKU表的数据
                    new_stock = origin_stock - sku_count
                    new_sales = origin_sales + sku_count
                    result = SKU.objects.filter(id=sku_id,stock=origin_stock).update(stock=new_stock,sales=new_sales)
                    if result == 0:
                        #证明资源又被占用, 重新循环, 下面代码不执行
                        continue
                    #13.修改GOODs表的数据
                    sku.goods.sales += sku_count
                    sku.goods.save()
                    #保存订单商品信息
                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=sku_count,
                        price=sku.price
                    )
                    #修改orderInfo表里的总价和总数量
                    order.total_count += sku_count
                    order.total_amount += (sku_count*sku.price)
                    #下单成功或者失败就跳出循环
                    break
            #修改所有sku总的总价
            order.total_amount += order.freight
            order.save()
        #清除购物车中的已结算的商品
        redis_conn.hdel('carts_%s'%user.id, *set_sku_ids)
        redis_conn.srem('selected_%s'%user.id, *set_sku_ids)
        #14.返回json
        return JsonResponse({'code':0,
                             'errmsg':'ok',
                             'order_id':order_id})