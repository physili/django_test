from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from goods.models import Brand
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.brand import BrandSerializer
from fdfs_client.client import Fdfs_client


#查询获取,保存,修改,删除品牌
class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = PageNum

    # 保存图片数据
    # 重写拓展类的保存业务逻辑
    def create(self, request, *args, **kwargs):
        # 创建FASTDFS链接对象
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        # 获取前端传递的image文件
        image = request.FILES.get('logo')
        # 上传图片到fastDFS
        image_data = client.upload_by_buffer(image.read())
        if image_data['Status'] != 'Upload successed.':
            return Response(status=403)
        image_url = image_data['Remote file_id']
        name = request.data.get('name')
        first_letter = request.data.get('first_letter')
        brand = Brand.objects.create(name=name, first_letter=first_letter, logo=image_url)
        # img.image返回的是数据库保存的storage的地址,
        # img.image.url是调用imagefile的files的url属性, url属性会调用storage的url方法
        return Response(
            {
                'id': brand.id,
                'name': brand.name,
                'image': brand.logo.url,
                'first_letter': brand.first_letter
            },
            status=201
        )

    # 更新图片, put请求
    # 重写拓展类的更新业务逻辑
    def update(self, request, *args, **kwargs):
        # 获取pk对应的对象
        brand = self.get_object()
        # 创建FASTDFS链接对象
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        # 获取前端传递的image文件
        image = request.FILES.get('logo')
        # 上传图片到fastDFS
        image_data = client.upload_by_buffer(image.read())
        if image_data['Status'] != 'Upload successed.':
            return Response(status=403)
        image_url = image_data['Remote file_id']
        brand.logo = image_url
        brand.name = request.data.get('name')
        brand.first_letter = request.data.get('first_letter')
        brand.save()
        return Response(
            {
                'id': brand.id,
                'name': brand.name,
                'image': brand.logo.url,
                'first_letter': brand.first_letter
            },
            status=201
        )
