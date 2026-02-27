import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    # Price range
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Year range
    min_year = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = django_filters.NumberFilter(field_name='year', lookup_expr='lte')

    # Brand filter (partial, case-insensitive)
    # brand=toyota  matches "Toyota", "TOYOTA", "toyota corolla brand" etc.
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='icontains')

    # Owner filter (exact username, case-insensitive)
    owner = django_filters.CharFilter(field_name='owner__username', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'owner', 'min_price', 'max_price', 'min_year', 'max_year']