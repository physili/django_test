from django.shortcuts import render
from django.views import View
from areas.models import Area
from django import http
from django.core.cache import cache
# Create your views here.

#创建省视图
class ProvinceAreasView(View):
    def get(self,request):
        #先判断缓存是否有数据
        province_list = cache.get('province_list')
        if province_list is None:
            #查询省级数据
            try:
                province_set = Area.objects.filter(parent__isnull=True)
            #整理省级数据,转化成列表返回
                province_list = []
                for province_sub in province_set:
                    province_list.append({'id':province_sub.id, 'name':province_sub.name})
            except Exception as e:
                return http.JsonResponse({'code': 400, 'errmsg': '省份数据错误'})
            else:
                cache.set('province_list',province_list,3600)
        #返回数据
        return http.JsonResponse({'code': 0,  'errmsg': 'OK',  'province_list': province_list})