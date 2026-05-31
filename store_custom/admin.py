from django.contrib import admin
from store.admin import ProductAdmin  # Take Original ProductAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.models import Product
from tags.models import TaggedItem


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)  # Unregister the original ProductAdmin
# Register the new CustomProductAdmin
admin.site.register(Product, CustomProductAdmin)
