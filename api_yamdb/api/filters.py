from django_filters import rest_framework as flt
from reviews.models import Title


class TitleFilter(flt.FilterSet):
    name = flt.CharFilter(field_name='name', lookup_expr='icontains')
    year = flt.NumberFilter(field_name='year')
    category = flt.CharFilter(field_name='category__slug')
    genre = flt.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
