from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client     # 先导入我们安装的 fdfs_client.client 客户端
from django.conf import settings       # 导入 settings 文件
class FastDFSStorage(Storage):
    def exists(self, name):                       # 判断文件名称是否冲突
        return False                         # fdfs 中的文件名是由哈希算法生成的, 所以不会冲突
    def save(self, name, content, max_length=None):     #重写上传文件的函数
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)       # 创建客户端对象:
        result = client.upload_by_buffer(content.read())       # 调用上传函数, 进行上传, 返回一个字典
        if result.get('Status') != 'Upload successed.':                 # 判断是否上传成功:
            raise Exception('上传文件到FDFS系统失败')
        file_id = result.get('Remote file_id')# 上传成功: 返回 file_id:
        return file_id     # 这个位置返回以后, django 自动会给我们保存到表字段里.
    def url(self, name):                   # 返回可访问到文件的完整的url地址
        return settings.FDFS_URL + name