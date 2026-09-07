from rest_framework import serializers
from orders.models import Orders


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ["customer", "item", "amount", "time"]
        extra_kwargs = {
            "customer": {"read_only": True},
            "time": {"read_only": True},
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_item(self, value):
        if not value:
            raise serializers.ValidationError("Item cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError(
                "Item name must be at least 3 characters long."
            )
        return value