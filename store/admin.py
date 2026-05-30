from urllib.parse import urlencode

from django.contrib import admin
from django.urls import reverse
from . import models
from django.db.models import Count
from django.utils.html import format_html


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    ordering = ['title']
    list_per_page = 10
    # Query optimization
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'Collection_count']
    ordering = ['title']
    list_per_page = 10

    @admin.display(ordering='product_count')
    def Collection_count(self, collection):
        # Generate a link to the admin page that lists products filtered by this collection
        url = (reverse('admin:store_product_changelist') + '?' +
               urlencode({'collection__id': str(collection.id)}))
    # Return the HTML for the link, displaying the product count
        return format_html('<a href="{}">{}</a>', url, collection.product_set.count())


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    # Query optimization
    list_select_related = ['customer']


admin.site.register(models.OrderItem)
