from . import views
from django.urls import path
from pprint import pprint
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

# Nested router for reviews under products
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

urlpatterns = router.urls + products_router.urls
