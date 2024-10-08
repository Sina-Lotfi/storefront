from typing import Any, List, Tuple
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from . import models


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("description", "discount")
    list_editable = ("discount",)
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "product_count")
    list_per_page = 10

    def product_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html("<a href={}>{}</a>", url, collection.product_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(product_count=Count("products"))


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [("<10", "Low"), (">10", "OK")]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        elif self.value() == ">10":
            return queryset.filter(inventory__gt=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance: models.ProductImage):
        if instance.image.name != "":
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ""


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    inlines = [ProductImageInline]
    list_display = ("title", "unit_price", "inventory_status", "collection")
    list_editable = ("unit_price",)
    search_fields = ["title"]
    list_filter = ("collection", "last_update", InventoryFilter)
    list_per_page = 10

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{updated_count} was deleted successfully", messages.ERROR
        )

    class Media:
        css = {"all": ["store/styles.css"]}


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]
    list_display = ("first_name", "last_name", "membership")
    list_editable = ("membership",)
    list_per_page = 10
    list_select_related = ["user"]
    ordering = ("user__first_name", "user__last_name")
    search_fields = ["first_name__istartswith", "last_name__istartswith"]


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ["product"]
    max_num = 10
    min_num = 0
    extra = 0


@admin.register(models.Order)
class OrderClass(admin.ModelAdmin):
    search_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ("payment_status", "placed_at", "customer")


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]
