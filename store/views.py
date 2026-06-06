from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CollectionSerializer, ProductSerializer
from .models import Collection, Product
from django.db.models import Count


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        # get all products from the database, serialize them, and return them in the response
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # create a new product
        serializer = ProductSerializer(data=request.data)
        # validate the data and raise an exception if it's invalid
        serializer.is_valid(raise_exception=True)
        # save the new product to the database
        serializer.save()
        print(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
# created a view function for product details, which takes an id parameter
def product_detail(request, id):
    # get the product with the given id, and return a 404 error if it doesn't exist
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        # serialize the product and return it in the response
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # update the product with the data from the request
        serializer = ProductSerializer(product, data=request.data)
        # validate the data and raise an exception if it's invalid
        serializer.is_valid(raise_exception=True)
        # save the updated product to the database
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({"error": "Cannot delete product with existing orders"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(
            collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({"error": "Cannot delete collection with existing products"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
