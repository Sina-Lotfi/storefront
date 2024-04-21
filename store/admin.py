from typing import Any, List, Optional, Tuple
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import Product, Collection
from . import models


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('description', 'discount')
    list_editable = ('discount',)
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_count')
    list_per_page = 10

    def product_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + \
            urlencode({'collection__id': str(collection.id)})
        return format_html('<a href={}>{}</a>', url, collection.product_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(product_count=Count('product'))


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [
            ('<10', 'Low'),
            ('>10', 'OK')
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>10':
            return queryset.filter(inventory__gt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    actions = ['clear_inventory']
    list_display = ('title', 'unit_price', 'inventory_status', 'collection')
    list_editable = ('unit_price',)
    list_filter = ('collection', 'last_update', InventoryFilter)
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} was deleted successfully',
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership')
    list_editable = ('membership',)
    list_per_page = 10
    ordering = ('first_name', 'last_name')
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(models.Order)
class OrderClass(admin.ModelAdmin):
    list_display = ('payment_status', 'placed_at', 'customer')
