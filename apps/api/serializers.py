from rest_framework import serializers
from django.contrib.auth.models import User
from apps.core.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'role', 'bio', 'created_at', 'updated_at')
        read_only_fields = ('id', 'role', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    """Serializzatore per User - mai include la password."""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'profile')
        read_only_fields = ('id',)
