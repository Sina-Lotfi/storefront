from django_filters.rest_framework import FilterSet
import django_filters
from .models import Product


class ProductFiltering(FilterSet):
    price_gt = django_filters.NumberFilter(
        field_name="unit_price", lookup_expr="gt", label="price_from"
    )
    price_lt = django_filters.NumberFilter(
        field_name="unit_price", lookup_expr="lt", label="price_to"
    )
    collection_id = django_filters.NumberFilter(
        field_name="collection_id", lookup_expr="exact"
    )
