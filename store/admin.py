from django.contrib import admin, messages
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
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
    search_fields = ['title']
    autocomplete_fields = ['collection']
    # automatically populate the slug field based on the title field
    prepopulated_fields = {'slug': ['title']}

    # add a custom action to clear inventory for selected products in the admin interface
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    ordering = ['title']
    # filter by collection and inventory status
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

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f'{updated_count} products were successfully updated.',
            messages.ERROR
        )


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
    search_fields = ['title__istartswith']
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


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    # add a search bar to the order admin page that allows searching by the customer's first name, last name, and email
    autocomplete_fields = ['customer']
    # add an inline to the order admin page that allows editing the order items directly on the order page
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    # Query optimization
    list_select_related = ['customer']
