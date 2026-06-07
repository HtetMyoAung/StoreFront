from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .serializers import CollectionSerializer, ProductSerializer
from .models import Collection, Product
from django.db.models import Count


class ProductList(ListCreateAPIView):
    # get method to retrieve all products, and post method to create a new product
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # get_queryset method to return the queryset of products
    def get_queryset(self):
        return Product.objects.select_related('collection').all()

    # serializer_class method to return the serializer class for the products
    def get_serializer_class(self):
        return ProductSerializer

    # get_serializer_context method to return the context for the serializer, which includes the request object
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(APIView):
    # get method to retrieve a product by id, put method to update a product, and delete method to delete a product
    def get(self, request, id):
        # get the product with the given id, and return a 404 error if it doesn't exist
        product = get_object_or_404(Product, pk=id)
        # serialize the product and return it in the response
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        # update the product with the data from the request
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        # validate the data and raise an exception if it's invalid
        serializer.is_valid(raise_exception=True)
        # save the updated product to the database
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({"error": "Cannot delete product with existing orders"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer


class CollectionDetail(APIView):
    def get(self, request, pk):
        # get the collection with the given pk, annotate it with the count of products in the collection, and return a 404 error if it doesn't exist
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, pk):
        # update the collection with the data from the request
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        # validate the data and raise an exception if it's invalid
        serializer = CollectionSerializer(
            collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({"error": "Cannot delete collection with existing products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
