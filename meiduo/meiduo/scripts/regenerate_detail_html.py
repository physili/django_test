#!/home/ubuntu/.virtualenvs/meiduo_water/bin/python3.6

import sys
sys.path.insert(0, '../')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo.settings.dev')

import django
django.setup()

from goods.models import SKU
from celery_tasks.html.tasks import generate_static_sku_detail_html

if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        # print(sku.id)
        generate_static_sku_detail_html(sku.id)
    # generate_static_sku_detail_html(1)