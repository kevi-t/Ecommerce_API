# customer/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models.models import Customer
import re


# Registration logic
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only (not returned)
    
    def validate_phone_number(self, value):
        # Remove any non-numeric characters (spaces, dashes, etc.)
        value = re.sub(r'\D', '', value)

        # Ensure phone number has exactly 10 digits
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must have exactly 10 digits (e.g., 0722123456).")

        # Convert to international format (Kenya: +254)
        if value.startswith("07"):
            formatted_number = "+254" + value[1:]  # Remove leading 0 and add +254
        else:
            raise serializers.ValidationError("Invalid phone number format. Must start with '07'.")
        return formatted_number
    
    def create(self, validated_data):
        validated_data['phone_number'] = self.validate_phone_number(validated_data['phone_number'])
        
        customer = Customer(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        customer.set_password(validated_data['password'])  
        customer.save()
        return customer

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value