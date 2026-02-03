from rest_framework import serializers
from django.contrib.auth.models import User
from apps.core.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer per UserProfile."""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'role_display', 'bio', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer per User con profilo."""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'profile']
        read_only_fields = ['id', 'date_joined']


class TokenValidationSerializer(serializers.Serializer):
    """Serializer per validazione token."""
    token = serializers.CharField(required=True, help_text='JWT Access Token')


class SSOLoginSerializer(serializers.Serializer):
    """Serializer per login SSO."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
