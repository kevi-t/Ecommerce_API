from django.contrib.auth import authenticate
from rest_framework import serializers
from customer.models import Customer
from customer.utils import normalize_kenyan_phone_number


class CustomerSerializer(serializers.ModelSerializer):
    """General customer representation for API responses."""

    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone_number"]
        read_only_fields = ["id", "email"]


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Customer with this email already exists."
            )
        return value

    def validate_phone_number(self, value):
        value = normalize_kenyan_phone_number(value)
        if Customer.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "Customer with this phone number already exists."
            )
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        return value

    def create(self, validated_data):
        return Customer.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )


class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        data["user"] = user
        return data


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "phone_number"]

    def validate_phone_number(self, value):
        value = normalize_kenyan_phone_number(value)
        queryset = Customer.objects.filter(phone_number=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Customer with this phone number already exists."
            )

        return value