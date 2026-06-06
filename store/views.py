from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product


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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
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


@api_view()
def collection_detail(request, pk):
    return HttpResponse('ok')
