import base64, pickle
import json
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection

from goods.models import SKU
from django.shortcuts import render

# Create your views here.


#创建购物车管理接口



class CartsView(View):
    #添加购物车
    def post(self,request):
        #1.提取参数 user_id sku_id count selected
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected',True)
        #2.验证参数(整体
        if not all([sku_id,count]):
            return JsonResponse({'code':400,'errmsg':'缺少参数'})
        #3.验证参数(单个
            #判断sku_id是否存在
        try:
            SKU.objects.get(id = sku_id)
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'商品不存在'})
            #判断count是否为数字
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '参数count有误'})
            #判断selected是否为布尔值
        if selected:
            if not isinstance(selected,bool):
                return JsonResponse({'code': 400, 'errmsg': '参数selected有误'})
            #判断用户是否登录
        if request.user.is_authenticated:
        #4.用户已登录, 使用redis的hash和set存储4个参数
        #5.链接redis
            redis_conn = get_redis_connection('carts')
        #6.使用管道
            pl = redis_conn.pipeline()
        #7.使用hincrby累加或新建count, 注意count必须是数字
            pl.hincrby('carts_%s'%request.user.id,sku_id,count)
            if selected:
                pl.sadd('selected_%s'%request.user.id,sku_id)
            pl.execute()
            return JsonResponse({'code': 0,   'errmsg': '添加购物车成功'})
        #8.用户未登录, 使用cookie存储3个参数
        else:
            cookie_cart = request.COOKIES.get('carts')
        #9.判断cookie是否存在, 存在则解密, 新增数据
            if cookie_cart:
                cart_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))
        #10.不存在则设置未空字典
            else:
                cart_dict = {}
            #11.判断sku_id是否在cookie里, 是则累加求和
            if sku_id in cart_dict:
                count = count + cart_dict[sku_id]['count']
            #12.构造新的cookie
            cart_dict[sku_id] = {'count':count,'selected':selected}
            #13.加密新cookie
            cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()
            #14.cookie加载返回
            response = JsonResponse({'code': 0,  'errmsg': '添加购物车成功'})
            response.set_cookie('carts',cart_data)
            return response


    #展示购物车
    def get(self,request):
        #1.判断是否用户登录
        if request.user.is_authenticated:
            # 2.是则调用redis的hash和set
            redis_conn = get_redis_connection('carts')
            hash_dict = redis_conn.hgetall('carts_%s'%request.user.id)
            set_selected = redis_conn.smembers('selected_%s'%request.user.id)
        #3.整合成cookie的key field value格式
            cart_dict = {}
            for sku_id,count in hash_dict.items():
                cart_dict[int(sku_id)] = {'count':int(count), 'selected':sku_id in set_selected}
        #4.
        #5.
        #6.否则调用返回的cookie
        else:
            cookie_cart = request.COOKIES.get('carts')
            if cookie_cart:
                # 7.解密cookie
                cart_dict = pickle.loads(base64.b64decode(cookie_cart.encode()))
            else:
                cart_dict = {}
        #9.遍历sku_id, 调取数据库的sku,
        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        #10.重新构造返回的数据
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id':sku.id,
                'name':sku.name,
                'count':cart_dict[sku.id]['count'],
                'selected':cart_dict[sku.id]['selected'],
                'default_image_url':sku.default_image_url,
                'price':sku.price,
                'amount':(sku.price * cart_dict[sku.id]['count']),
            })
        return JsonResponse({'code':0, 'errmsg':'ok',   'cart_skus':cart_skus})


    #修改购物车
    def put(self,request):
        #1.提取参数sku_id count selected
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected',True)
        #2.验证参数(整体 sku_id count)
        if not all([sku_id,count]):
            return JsonResponse({'code': 400,
                                 'errmsg': '必传参数为空'})
        #3.验证参数(单个sku_id是否在数据库, count是否是数字, select是否传参
        try:
            SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': 'sku_id参数有误'})
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'errmsg': 'count参数有误'})
        if selected:
            if not isinstance(selected,bool):
                return JsonResponse({'code': 400,
                                     'errmsg': 'selected参数有误'})
        #4.判断是否登录用户
        if request.user.is_authenticated:
            #5.是, 链接redis, 改hash表的count和selected_set的sku_id
            redis_conn = get_redis_connection('carts')
            user_id = request.user.id
            pl = redis_conn.pipeline()
            pl.hset('history_%s'%user_id, sku_id, count)
            if selected:
                pl.sadd('selected_%s'%user_id,sku_id)
            else:
                pl.srem('selected_%s'%user_id,sku_id)
            pl.execute()
            #6.返回json
            car_sku = {
                'id':sku_id,
                'count':count,
                'selected':selected
            }
            return JsonResponse({'code': 0,
                                 'errmsg': 'ok',
                                 'cart_sku':dict})

        else:
            #7.否, 提取cookie,解密, 覆盖count和selected
            cookie_cart = request.COOKIES.get('carts')
            if cookie_cart:
                cookie_dict = pickle.loads(base64.b64decode(cookie_cart))
            else:
                cookie_dict = {}
            cookie_dict[sku_id] = {
                'count':count,
                'selected':selected
            }
            cookie_data = base64.b64encode(pickle.dumps(cookie_dict)).decode()
            #8.返回json
            car_sku = {
                'id':sku_id,
                'count':count,
                'selected':selected
            }
            response = JsonResponse({'code': 0,
                                     'errmsg': 'ok',
                                     'cart_sku': car_sku})
            response.set_cookie('carts',cookie_data)
            return response
        #9.
        #10.

    #删除购物车
    def delete(self,request):
        pass
        #1.提取参数sku_id
        #2.验证sku_id是否存在数据库
        #3.判断是否登录
        #4.是, 链接redis, 改selected_set的sku_id
        #5.否, 链接cookie, 解密, 覆盖selected
        #6.
        #7.
        #8.
        #9.
        #10.













