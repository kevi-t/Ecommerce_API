from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'item', 'amount', 'time']
        extra_kwargs = {
            'time': {'read_only': True},  # Automatically set the time, don't accept it from user input
        }

    def create(self, validated_data):
        # Custom logic before creating the Order, if needed
        order = Order(
            customer=validated_data['customer'],
            item=validated_data['item'],
            amount=validated_data['amount']
        )
        order.save()
        return order

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_item(self, value):
        if not value:
            raise serializers.ValidationError("Item cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Item name must be at least 3 characters long.")
        return value