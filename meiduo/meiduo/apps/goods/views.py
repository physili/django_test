from datetime import date

from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage
from django.utils import timezone
from django.views import View
from goods.models import SKU,GoodsCategory,GoodsVisitCount
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


#商品列表热销排行接口
class HotGoodsView(View):
    def get(self,request,category_id):
        #根据销量倒序
        try:
            skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[0:2]
        except Exception as e:
            return JsonResponse({'code':400, 'errmsg':'获取商品出错'})
        #JsonResponse不能返回对象. 需要转化成字典或列表格式
        hot_skus = []
        for sku in skus:
            hot_skus.append({'id':sku.id,'default_image_url':sku.default_image_url, 'name':sku.name,'price':sku.price })
        return JsonResponse({'code':0,'errmsg':'OK','hot_skus':hot_skus})


#重写haystack的SearchView类的create_response方法
from haystack.views import SearchView
class MySearchView(SearchView):
    def create_response(self):
        page = self.request.GET.get('page')
        context = self.get_context()   # 获取搜索结果
        data_list = []
        for sku in context['page'].object_list:
            data_list.append({
                'id':sku.object.id,
                'name':sku.object.name,
                'price':sku.object.price,
                'default_image_url':sku.object.default_image_url,
                'searchkey':context.get('query'),
                'page_size':context['page'].paginator.num_pages,
                'count':context['page'].paginator.count
            })
        return JsonResponse(data_list, safe=False)


#统计分类商品访问量接口
class DetailVisitCountView(View):
    def post(self,request,category_id):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        now_date = timezone.localdate()
        print(now_date)
        now_date2 = date.today()
        print(now_date2)
        try:
            category_date_visit = category.goodsvisitcount_set.get(date=now_date)
        except Exception as e:
            category_date_visit = GoodsVisitCount()
        try:
            category_date_visit.category = category
            category_date_visit.count += 1
            category_date_visit.save()
        except Exception as e:
            return JsonResponse({'code':400,'errmsg':'服务器异常'})
        return JsonResponse({'code':0,'errmsg':'ok'})