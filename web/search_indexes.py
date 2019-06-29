import datetime
from haystack import indexes
from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """
    文章搜索索引
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    subject = indexes.CharField(model_attr='subject')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_deleted=False)
