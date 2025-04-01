# customer/serializers.py
from rest_framework import serializers
from customer.models.models import Customer
import re


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']  
    
    
    def validate_phone_number(self, value):
        # Remove any non-numeric characters (in case of user input errors)
        value = re.sub(r'\D', '', value)

        # Ensure the phone number has exactly 10 digits
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must have exactly 10 digits (e.g., 0722123456).")

        # Convert to international format (Kenyan numbers start with 07)
        if value.startswith("07"):
            formatted_number = "+254" + value[1:]  # Remove leading 0 and add +254
        elif value.startswith("254"):
            formatted_number = "+" + value  # Ensure +254 format
        elif value.startswith("+254"):
            formatted_number = value  # Already correct
        else:
            raise serializers.ValidationError("Invalid phone number format.")

        return formatted_number