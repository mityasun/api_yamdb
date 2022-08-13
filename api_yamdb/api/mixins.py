from rest_framework import mixins, viewsets


class ListCreateGenericViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass
