from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product


def say_hello(request):
    query_set = Product.objects.filter(Q(inventory__lt=10) | Q(
        unit_price__lt=20)).order_by('unit_price')[5:10]
    return render(request, 'hello.html', {'name': 'Xiao', 'products': query_set})
