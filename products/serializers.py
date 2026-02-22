from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = [
            'id',
            'owner',
            'name',
            'category',
            'brand',
            'price',
            'description',
            'year',
            'created_at',
            'updated_at',
        ]