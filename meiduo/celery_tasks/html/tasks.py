import os
from goods.models import SKU
from django.conf import settings
from django.template import loader
from celery_tasks.main import celery_app
from goods.utils import get_categories, get_goods_and_spec

@celery_app.task(name='generate_static_sku_detail_html')
def generate_static_sku_detail_html(sku_id):
    dict = get_categories()
    goods, specs, sku = get_goods_and_spec(sku_id)
    context = { 'categories': dict, 'goods': goods, 'specs': specs, 'sku': sku }    # 渲染模板，生成静态html文件

    template = loader.get_template('detail.html')          # 加载 loader 的 get_template 函数, 获取对应的 detail 模板
    html_text = template.render(context)               # 拿到模板, 将上面添加好的数据渲染进去.
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'goods/'+str(sku_id)+'.html')
    with open(file_path, 'w') as f:
        f.write(html_text)