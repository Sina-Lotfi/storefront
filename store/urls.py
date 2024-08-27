from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.COllectionViewSet)
router.register("carts", views.CartViewSet)
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")
product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewset, "product-reviews")
product_router.register("images", views.ProductImageViewSet, basename="product-images")
cart_item_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_item_router.register("items", views.CartItemViewSet, basename="cart-items")
# URLConf
urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(product_router.urls)),
    path(r"", include(cart_item_router.urls)),
]
