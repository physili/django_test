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


#创建市区视图
class SubAreasView(View):
    def get(self,request,pk): #路径传参
        #判断是否有缓存
        sub_dict = cache.get('sub_dict_%s'%pk)
        if not sub_dict:
        #没有缓存, 从数据库提取数据
            try:
                sub_set = Area.objects.filter(parent_id=pk)
                parent_sub = Area.objects.get(id=pk)
                sub_list = []
                for sub_sub in sub_set:
                    sub_list.append({'id':sub_sub.id, 'name':sub_sub.name})
                sub_dict = {'id':parent_sub.id, 'name':parent_sub.name, 'subs':sub_list}
        #设定缓存
                cache.set('sub_dict'+pk, sub_dict, 3600)
        #提取失败返回json数据
            except Exception as e:
                return http.JsonResponse({'code': 400,  'errmsg': '城市或区县数据错误'})
        #成功,返回json数据
        return http.JsonResponse({'code': 0,  'errmsg': 'OK',  'sub_data': sub_dict})