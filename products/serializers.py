import datetime
from rest_framework import serializers
from .models import Product

CURRENT_YEAR = datetime.date.today().year


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = [
            'id', 'owner', 'name', 'category',
            'brand', 'price', 'description',
            'year', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value

    def validate_brand(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Brand must be at least 2 characters long.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        if value > 999_999_999:
            raise serializers.ValidationError("Price entered is unrealistically high.")
        return value

    def validate_year(self, value):
        if value is not None:
            if value < 1990:
                raise serializers.ValidationError("Year cannot be earlier than 1990.")
            if value > CURRENT_YEAR + 1:
                raise serializers.ValidationError(
                    f"Year cannot be in the future. Maximum allowed: {CURRENT_YEAR + 1}."
                )
        return value

    def validate(self, data):
        category = data.get('category')
        year = data.get('year')
        # Cars must always have a year — spare parts don't need one
        if category == 'car' and year is None:
            raise serializers.ValidationError({
                'year': 'Year is required for car listings.'
            })
        return data