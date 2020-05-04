import os, time
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
    #定义一个有序字典对象
    categories = OrderedDict()
    #对goods channel进行排序, 按照所属组 再按照序号
    channels = GoodsChannel.objects.order_by('group_id','sequence')
    #遍历排序后的结果:得到所有的一级菜单
    for channel in channels:
        #从频道中得到当前组的组id
        group_id = channel.group_id
        #判断当前组id是否在有序字典中,若不在,添加进去
        if group_id not in categories:
            categories[group_id] = {'channels':[],'sub_cats':[]} #商品频道每一行有一级菜单和二级菜单
        #获取一级菜单的类别对象
        cat1 = channel.category
        #给一级菜单补充内容
        categories[group_id]['channels'].append({'id':cat1.id, 'name':cat1.name,'url':channel.url})
    #......................二级菜单
        #获取二级菜单的类别对象
        cat2s = GoodsCategory.objects.filter(parent=cat1)
        #遍历所有二级类别对象
        for cat2 in cat2s:
            #给每个二级类别对象动态添加一个'下级'属性
            cat2.sub_cats=[]  #商品频道的三级菜单
    #......................三级菜单
            cat3s = GoodsCategory.objects.filter(parent=cat2)
            print(cat3s,type(cat3s))
            # 遍历所有三级类别对象
            for cat3 in cat3s:
                #把三级类别对象加到二级的'下级'属性里
                cat2.sub_cats.append(cat3)
            #把二级类别对象加到一级的'下级'属性里
            categories[group_id]['sub_cats'].append(cat2)

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