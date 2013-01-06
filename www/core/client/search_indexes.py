import datetime
from haystack import indexes
from core.client.models import Room

class RoomIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    category = indexes.CharField(model_attr='category', faceted=True)

    def get_model(self):
        return Room

    def index_queryset(self):
        return self.get_model().objects.filter(is_private=False)
