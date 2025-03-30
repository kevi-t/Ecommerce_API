# customer/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Customer


# Registration logic
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only (not returned)

    def create(self, validated_data):
        # Hash the password before saving
        customer = Customer(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        customer.set_password(validated_data['password'])  # Hash password here
        customer.save()
        return customer

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        # Add more custom password validations if needed (e.g., checking for special characters, etc.)
        return value


# Login logic
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        data['user'] = user
        return data