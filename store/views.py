from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Collection, OrderItem, Product, Review, Cart, CartItem
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer


class ProductViewSet(ModelViewSet):
    #  used to define the queryset of products that will be used for retrieving and manipulating product data.
    queryset = Product.objects.all()
    #  used for validating and deserializing input, and for serializing output.
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_updated']

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({"error": "Cannot delete product with existing orders"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({"error": "Cannot delete collection with existing products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Filter reviews by the product_id passed in the URL (product_pk)
        return self.queryset.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        # Pass the product_id from the URL to the serializer context so that it can be used in the create method.
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  GenericViewSet,
                  DestroyModelMixin,
                  RetrieveModelMixin,):
    #  used to define the queryset of carts that will be used for retrieving and manipulating cart data.
    queryset = Cart.objects.prefetch_related('items__product').all()
    #  used for validating and deserializing input, and for serializing output.
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
