from . import views
from django.urls import path
from pprint import pprint
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
pprint(router.urls)

urlpatterns = router.urls
