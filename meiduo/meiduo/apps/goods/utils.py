#定义面包屑函数
def get_breadcrumb(category):
    breadcrumb  = {'cat1':'','cat2':'','cat3':''}
    if category.parent is None:
        breadcrumb['cat1'] = category.name
    elif category.parent.parent is None:
        breadcrumb['cat2'] = category.name
        breadcrumb['cat1'] = category.parent.name
    else:
        breadcrumb['cat3'] = category.name
        breadcrumb['cat2'] = category.parent.name
        breadcrumb['cat1'] = category.parent.parent.name
    return breadcrumb


# 将我们之前写的获取商品分类的代码,提取出来一部分, 封装成一个独立的函数:
from django import http
from collections import OrderedDict
from goods.models import GoodsCategory
from goods.models import GoodsChannel, SKU
from goods.models import  SKUImage, SKUSpecification
from goods.models import  GoodsSpecification, SpecificationOption

def get_goods_and_spec(sku_id):
    # ======== 获取该商品和该商品对应的规格选项id ========
    try:
        sku = SKU.objects.get(id=sku_id) # 根据 sku_id 获取该商品(sku)
        sku.images = SKUImage.objects.filter(sku=sku)# 获取该商品的图片
    except Exception as e:
        return http.JsonResponse({'code':400,  'errmsg':'获取数据失败'})

    # 获取该商品的所有规格: [颜色, 内存大小, ...]
    sku_specs =SKUSpecification.objects.filter(sku=sku).order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        sku_key.append(spec.option.id)

    # ======== 获取类别下所有商品对应的规格选项id ========
    goods = sku.goods  # 根据sku对象,获取对应的类别
    skus = SKU.objects.filter(goods=goods)# 获取该类别下面的所有商品
    dict = {}
    for temp_sku in skus:     # 获取每一个商品(temp_sku)的规格参数
        s_specs = SKUSpecification.objects.filter(sku=temp_sku).order_by('spec_id')
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        dict[tuple(key)] = temp_sku.id

    # ======== 在每个选项上绑定对应的sku_id值 ========
    specs = GoodsSpecification.objects.filter(goods=goods).order_by('id')
    for index, spec in enumerate(specs):
        key = sku_key[:]          # 复制当前sku的规格键
        spec_options = SpecificationOption.objects.filter(spec=spec) # 该规格的选项
        for option in spec_options:
            key[index] = option.id              # 在规格参数sku字典中查找符合当前规格的sku
            option.sku_id = dict.get(tuple(key))
        spec.spec_options = spec_options
    return goods, specs, sku

def get_categories():
    # ==========提取类别频道数据===========
    # 定义一个有序字典对象
    categories = OrderedDict()
    # 对goods channel进行排序, 按照所属组 再按照序号
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 遍历排序后的结果:得到所有的一级菜单
    for channel in channels:
        # 从频道中得到当前组的组id
        group_id = channel.group_id
        # 判断当前组id是否在有序字典中,若不在,添加进去
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}  # 商品频道每一行有一级菜单和二级菜单
        # 获取一级菜单的类别对象
        cat1 = channel.category
        # 给一级菜单补充内容
        categories[group_id]['channels'].append({'id': cat1.id, 'name': cat1.name, 'url': channel.url})
        # ......................二级菜单
        # 获取二级菜单的类别对象
        cat2s = GoodsCategory.objects.filter(parent=cat1)
        # 遍历所有二级类别对象
        for cat2 in cat2s:
            # 给每个二级类别对象动态添加一个'下级'属性
            cat2.sub_cats = []  # 商品频道的三级菜单
            # ......................三级菜单
            cat3s = GoodsCategory.objects.filter(parent=cat2)
            print(cat3s, type(cat3s))
            # 遍历所有三级类别对象
            for cat3 in cat3s:
                # 把三级类别对象加到二级的'下级'属性里
                cat2.sub_cats.append(cat3)
            # 把二级类别对象加到一级的'下级'属性里
            categories[group_id]['sub_cats'].append(cat2)
    return categories