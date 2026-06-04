from rest_framework import serializers
from decimal import Decimal


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='get_price_with_tax')

    def get_price_with_tax(self, product):
        return product.unit_price * Decimal('1.1')
