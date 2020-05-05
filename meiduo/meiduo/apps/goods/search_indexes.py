from haystack import indexes
from .models import SKU

#SKU索引数据模型类
class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # 返回建立索引的模型类
    def get_model(self):
        return SKU

    # 返回要建立索引的数据查询集
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_launched=True)