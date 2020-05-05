import os, time

from goods.utils import get_categories

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo.settings.dev')
import django
django.setup()

from collections import OrderedDict
from django.conf import settings
from django.template import loader

from contents.models import ContentCategory, Content
from goods.models import GoodsChannel, GoodsCategory  #导入商品频道和商品类别模型类

#定义一个函数, 生成静态化页面
def generate_static_index_html():
    #==========提取类别频道数据===========
    categories = get_categories()

    #==========提取首页广告数据===========
    #定义一个字典来存储广告内容部分
    contents = {}
    #从广告类别模型类中获取所有数据,存放到变量中:
    content_categories = ContentCategory.objects.all()
    #遍历每一个广告类别, 把对应的广告内容添加到contents字典里
    for cat in content_categories:
        #例如: 滚动广告里有xxx这三个广告内容
        contents[cat.key]=Content.objects.filter(category=cat,status=True).order_by('sequence')
    # 把类别频道数据和广告内容数据整合到一个新字典里
    context = {'categories': categories, 'contents': contents}

    #==========提取template模板=========
    #根据导入的loader获取'index.html'模板
    template = loader.get_template('index.html')
    #==========生成新的静态化页面给前端====
    # 将context渲染到模板中, 生成渲染过的模板
    html_text = template.render(context)
    #我们拼接新的index.html模板将要生成的所在地地址:
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR,'index.html')
    #以写的权限,将渲染过的模板重新生成,写入到文件中
    with open(file_path,'w',encoding='utf-8') as f:
        f.write(html_text)

if __name__ == '__main__':
    generate_static_index_html()