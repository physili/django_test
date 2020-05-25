from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from goods.models import SKUImage, SKU
from meiduo_admin.utils import PageNum
from meiduo_admin.serializers.image import ImageSerializer, SKUSerializer
from fdfs_client.client import Fdfs_client

#获取图片列表, 获取修改图片的详情信息RetrieveModelMixin实现
class ImageView(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = SKUImage.objects.all()
    pagination_class = PageNum

    # 保存图片数据
    #重写拓展类的保存业务逻辑
    def create(self, request, *args, **kwargs):
        #创建FASTDFS链接对象
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        #获取前端传递的image文件
        image = request.FILES.get('image')
        #上传图片到fastDFS
        image_data = client.upload_by_buffer(image.read())
        if image_data['Status'] != 'Upload successed.':
            return Response(status=403)
        image_url = image_data['Remote file_id']
        sku_id = request.data.get('sku')
        img = SKUImage.objects.create(sku_id=sku_id, image=image_url)
        #img.image返回的是数据库保存的storage的地址,
        #img.image.url是调用imagefile的files的url属性, url属性会调用storage的url方法
        return Response(
            {'id':img.id, 'sku':sku_id, 'image':img.image.url},
            status=201
        )


    #更新图片, put请求
    # 重写拓展类的更新业务逻辑
    def update(self, request, *args, **kwargs):
        #获取pk对应的对象
        img = self.get_object()
        # 创建FASTDFS链接对象
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        # 获取前端传递的image文件
        image = request.FILES.get('image')
        # 上传图片到fastDFS
        image_data = client.upload_by_buffer(image.read())
        if image_data['Status'] != 'Upload successed.':
            return Response(status=403)
        image_url = image_data['Remote file_id']
        img.image = image_url
        img.save()
        sku_id = request.data.get('sku')
        # img.image返回的是数据库保存的storage的地址,
        # img.image.url是调用imagefile的files的url属性, url属性会调用storage的url方法
        return Response(
            {'id': img.id, 'sku': sku_id, 'image': img.image.url},
            status=201
        )


#获取图片关联的sku的id
class SKUView(APIView):
    def get(self,request):
        skus = SKU.objects.all()
        serializer = SKUSerializer(skus,many=True)
        return Response(serializer.data)

