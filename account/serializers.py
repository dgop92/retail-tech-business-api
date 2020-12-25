from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from account.models import MyUser

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            'tice',
            'cellphone',
            'age',
            'date_of_birth'
        )

    def validate_age(self, age):
        if age <= 0:
            raise serializers.ValidationError(
                _("Age must be a positive number")
            )
        return age

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only = True)

    class Meta:
        model = MyUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_superuser',
            'profile'
        )
        read_only_fields = ('email', 'is_superuser',)


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    
    class Meta:
        model = MyUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_confirmation',
            'is_superuser'
        )
    
    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError(_("Passwords didn't match"))

        password_validation.validate_password(passwd)

        return data

    def create(self, validated_data):

        user = MyUser.objects.create_user(**validated_data)
        Profile.objects.create(user = user)

        return user

