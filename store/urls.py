from . import views
from django.urls import path

urlpatterns = [
    # created a path for product list, and passing it to the view function
    path('products', views.ProductList.as_view(), name='product_list'),
    # created a path for product details, adding an id parameter to the url, and passing it to the view function
    path('products/<int:id>', views.ProductDetail.as_view(), name='product_detail'),
    # created a path for collection list, and passing it to the view function
    path('collections', views.CollectionList.as_view(), name='collection_list'),
    # created a path for collection details, adding a pk parameter to the url, and passing it to the view function
    path('collections/<int:pk>', views.CollectionDetail.as_view(),
         name='collection_detail'),
]
