from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class CurrentUserSerializer(DjoserUserSerializer):

    # call customer relate_name from store_customer

    customer_id = serializers.IntegerField(
        source='customer.id', read_only=True)
    membership = serializers.CharField(
        source='customer.membership', read_only=True)

    class Meta(DjoserUserSerializer.Meta):

        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'customer_id', 'membership']
