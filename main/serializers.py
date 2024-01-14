from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from main.models import CmsUser, Content

class ContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Content
		fields ='__all__'

class CmsUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CmsUser
        fields = ('id', 'email', 'full_name', 'phone','address', 'city', 'state', 'country', 'pincode', 'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError("Phone number must be a 10-digit numeric value.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        return value

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise ValidationError("Pincode must me 6 digit numeric value.")
        return value

    def create(self, validated_data):
        user = CmsUser.objects.create(
            # username=validated_data.get('email'),
            email=validated_data.get('email'),
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            country=validated_data.get('country'),
            pincode=validated_data['pincode'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


