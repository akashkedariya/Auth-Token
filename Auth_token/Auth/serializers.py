from lib2to3.pgen2 import token
from django.forms import ValidationError
from rest_framework import serializers
from Auth.models import CustomUser
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator




class UserRegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password','city']
    #     extra_kwargs = {
    #         'password': {'write_only': True}
    #     }

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     password2 = attrs.get('password2')

    #     if password != password2:
    #         raise serializers.ValidationError("Passwords do not match.")
    #     return attrs

    # def create(self, validated_data):
    #     validated_data.pop('password2')
    #     user = CustomUser.objects.create_user(**validated_data)
    #     return user
