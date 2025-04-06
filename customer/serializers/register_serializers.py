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
        extra_kwargs = {'password': {'write_only': True}}  
    
    def validate_phone_number(self, value):
        # Remove any non-numeric characters (spaces, dashes, etc.)
        num_value = re.sub(r'\D', '', value)

        if len(num_value) != 10:
            raise serializers.ValidationError("Phone number must have exactly 10 digits")
        return "+254" + num_value[1:]
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def create(self, validated_data):        
        customer = Customer(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        customer.set_password(validated_data['password'])  
        customer.save()
        return customer