from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from logistic.permissions import IsOwnerOrReadOnly


class AdvertisementViewSet(ModelViewSet):

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]


    def get_queryset(self):
        qs = super().get_queryset()
        creator = self.request.query_params.get('creator', None)
        if creator is not None:
            qs = qs.filter(creator=creator)
        else:
            qs = super().get_queryset()
        return qs

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]
        return []
