from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage
from django.views import View
from goods.models import SKU,GoodsCategory
from django.http import JsonResponse
from goods.utils import get_breadcrumb


# Create your views here.

#商品列表页接口
class ListView(View):
    def get(self,request,category_id):#路径传参和查询字符串传参
        #提取查询字符串参数
        page_num = request.GET.get('page')
        page_size = request.GET.get('page_size')
        sort = request.GET.get('ordering')
        #获取三级菜单类别对象
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse

        #查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        #通过三级类别对象获取对应的sku商品对象查询集
        try:
            skus = SKU.objects.filter(category=category, is_launched=True).order_by(sort)
        except SKU.DoesNotExist:
            return JsonResponse
        #调用django自带的Paginator类生成 页对象
        # print(skus, type(skus))
        paginator = Paginator(skus,page_size)
        #通过对象.page(page_num)获取对应页的商品对象查询集
        try:
            page_skus = paginator.page(page_num)
        except EmptyPage:
            return JsonResponse
        #通过对象.num_pages获取总页数
        total_page = paginator.num_pages
        #把商品对象查询集转化成列表格式返回
        list=[]
        for sku in page_skus:
            list.append({ 'id':sku.id, 'default_image_url':sku.default_image_url, 'name':sku.name, 'price':sku.price })
            # list.append(sku)
        # print(list)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'breadcrumb': breadcrumb, 'list': list, 'count': total_page})