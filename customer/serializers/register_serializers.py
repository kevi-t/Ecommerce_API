# customer/serializers.py
from rest_framework import serializers
from ..models.models import Customer
import re


# Registration logic
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}  
    
    def validate_email(self, value):
        # Check if the email already exists in the database
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("Customer with this email already exists.")
        return value
    
    def validate_phone_number(self, value):
        # Remove any non-numeric characters (spaces, dashes, etc.)
        num_value = re.sub(r'\D', '', value)

        if len(num_value) != 10:
            raise serializers.ValidationError("Phone number must have exactly 10 digits")
        
        formatted_number = "+254" + num_value[1:]
        
        if Customer.objects.filter(phone_number=formatted_number).exists():
            raise serializers.ValidationError("Customer with this phone number already exists.")
        
        return formatted_number
    
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