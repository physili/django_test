import pickle, base64

from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request,response):
    #1.获取cookie中购物车的数据
    cookie_cart = request.COOKIES.get('carts')
    if not cookie_cart:
        return response
    cookie_dict = pickle.loads(base64.b64decode(cookie_cart))
    #2.新建三个空的容器,一个装sku和count,一个装select_True_sku, 一个装select_False_sku
    new_dict = {}
    new_add = []
    new_rem = []
    #3.同步cookie中的购物车数据
    for sku_id,item_dict in cookie_dict.items():
        new_dict[sku_id] = item_dict['count']
        if item_dict['selected']:
            new_add.append(sku_id)
        else:
            new_rem.append(sku_id)
    #4.链接redis
    redis_conn = get_redis_connection('carts')
    pl = redis_conn.pipeline()
    #5.将new_dict写入到hash表中
    pl.hmset('carts_%s'%request.user.id, new_dict)
    #6.判断add=[]中是否有值, 有的话: 往set中增加数据
    if new_add:
        pl.sadd('selected_%s' % request.user.id, *new_add)
    #7.判断remove=[]中是否有值, 有的话: 从set中删除数据
    if new_rem:
        pl.srem('selected_%s' % request.user.id, *new_rem)
    #8.执行管道
    pl.execute()
    #9.清除购物车cookie
    response.delete_cookie('carts')
    return response
