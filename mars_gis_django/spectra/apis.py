import django_filters
from rest_framework import viewsets, filters, routers

from .models import Collection
from .serializers import CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

router = routers.DefaultRouter()
router.register('collection',CollectionViewSet)
