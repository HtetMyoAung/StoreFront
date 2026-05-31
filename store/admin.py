from urllib.parse import urlencode
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    ordering = ['title']
    # Add a filter sidebar to filter products by inventory status
    list_filter = ['collection', InventoryFilter]
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
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    # search bar fields, case-insensitive, starts with
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'Collection_count']
    list_per_page = 10
    ordering = ['title']

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
