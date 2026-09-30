from rest_framework import serializers
from .models import Product


# The serializer converts Django model objects into API data and validates incoming API data.

class ProductSerializer(serializers.ModelSerializer):
# This automatically creates most of the serializer fields from the Product model.
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']
        # Therefore, the API returns:
        # ```json
        # {
        #     "id": 1,
        #     "name": "Notebook",
        #     "description": "A notebook with 100 pages.",
        #     "price": "120.00",
        #     "stock": 25
        # }
        # ```
        read_only_fields = ['id']
        # This means users do not need to submit an ID. Django automatically generates the ID.

    def validate_name(self, value): # checks the submitted product name.
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Product name cannot be empty."
            )

        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value