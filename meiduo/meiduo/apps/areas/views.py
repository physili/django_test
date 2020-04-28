from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
from django.views import View
from areas.models import Area
from django import http

#创建省模型类
class ProvinceAreasView(View):
    def get(self,request):
        #没有传参
        #1.增加:判断是否有缓存
        province_list = cache.get('province_list')
        if not province_list:
            #查询省级数据
            try:
                #生成过滤对象
                province_model_list = Area.objects.filter(parent__isnull=True)
                #把对象转换成列表
                province_list = []
                for province_model in province_model_list:
                    province_list.append({'id':province_model.id,'name':province_model.name})
                cache.set('province_list',province_list,3600)
            except Exception as e:
                return http.JsonResponse({'code': 400, 'errmsg': '省份数据错误'})
        return http.JsonResponse({'code':0,'errmsg':'ok','province_list':province_list})


class SubAreasView(View):
    def get(self,request,pk):
        #判断是否有缓存
        sub_list = cache.get('sub_list_%s'%pk)
        if sub_list is None:
            try:
                #没有缓存, 模型类提取数据对象
                sub_model_list = Area.objects.filter(parent=pk)
                parent_model = Area.objects.get(id = pk)
                #把对象转换成列表
                sub_list=[]
                for sub_model in sub_model_list:
                    sub_list.append({'id':sub_model.id, 'name':sub_model.name})
                sub_dict = {'id': parent_model.id,  'name': parent_model.name, 'subs': sub_list}
                cache.set('sub_list_%s'%pk,sub_list,3600)
            except Exception as e:
                return http.JsonResponse({'code': 400,  'errmsg': '城市或区县数据错误'})
            return http.JsonResponse({'code': 0,  'errmsg': 'OK',  'sub_data': sub_dict})

