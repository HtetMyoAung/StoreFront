from . import views
from django.urls import path

urlpatterns = [
    # created a path for product list, and passing it to the view function
    path('products', views.product_list, name='product_list'),
    # created a path for product details, adding an id parameter to the url, and passing it to the view function
    path('products/<int:id>', views.product_detail, name='product_detail'),
]
