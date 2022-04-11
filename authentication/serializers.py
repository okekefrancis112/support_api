from .models import User
from rest_framework import serializers,status
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password


class UserCreationSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(max_length=40,allow_blank=True)
    first_name=serializers.CharField(max_length=40,allow_blank=True)
    last_name=serializers.CharField(max_length=40,allow_blank=True)
    email=serializers.EmailField(max_length=80,allow_blank=False)
    password=serializers.CharField(allow_blank=False,write_only=True)


    class Meta:
        model=User
        fields=['id', 'email', 'user_name', 'first_name', 'last_name', 'password']

    def validate(self,attrs):
        email=User.objects.filter(user_name=attrs.get('email')).exists()
        if email:
            raise ValidationError(detail="User with email exists",code=status.HTTP_403_FORBIDDEN)

        user_name=User.objects.filter(user_name=attrs.get('user_name')).exists()
        if user_name:
            raise ValidationError(detail="User with user_name exists",code=status.HTTP_403_FORBIDDEN)

        return super().validate(attrs)


    def create(self,validated_data):
        new_user=User(**validated_data)

        new_user.password=make_password(validated_data.get('password'))

        new_user.save()

        return new_user