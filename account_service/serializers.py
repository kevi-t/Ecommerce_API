from django.contrib.auth import authenticate
from rest_framework import serializers

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