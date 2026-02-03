from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import jwt
from django.conf import settings

from .serializers import (
    UserSerializer,
    TokenValidationSerializer,
    SSOLoginSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def sso_info(request):
    """
    Info sulla SSO API - Endpoint pubblico che descrive le API disponibili.
    """
    return Response({
        'name': 'MyApp SSO API',
        'version': '1.0',
        'endpoints': {
            'login': '/api/sso/login/',
            'validate': '/api/sso/validate/',
            'refresh': '/api/sso/refresh/',
            'me': '/api/sso/me/'
        },
        'documentation': 'https://github.com/turiliffiu/myapp'
    })


@csrf_exempt  # <-- AGGIUNTO
@api_view(['POST'])
@permission_classes([AllowAny])
def sso_login(request):
    """
    Login SSO - Genera JWT tokens per l'utente autenticato.
    
    Request Body:
        {
            "username": "admin",
            "password": "password123"
        }
    
    Response:
        {
            "access": "jwt_access_token",
            "refresh": "jwt_refresh_token",
            "user": { ... user data ... }
        }
    """
    serializer = SSOLoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid request data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    # Autentica utente
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {'error': 'Account disabled'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Genera JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    })


@csrf_exempt  # <-- AGGIUNTO
@api_view(['POST'])
@permission_classes([AllowAny])
def validate_token(request):
    """
    Valida un JWT token e restituisce info utente se valido.
    
    Request Body:
        {
            "token": "jwt_token_here"
        }
    
    Response:
        {
            "valid": true,
            "user": { ... user data ... }
        }
    """
    serializer = TokenValidationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'valid': False, 'error': 'Token required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token = serializer.validated_data['token']
    
    try:
        # Decodifica JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        
        # Recupera utente
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        
        if not user.is_active:
            return Response({
                'valid': False,
                'error': 'Account disabled'
            })
        
        return Response({
            'valid': True,
            'user': UserSerializer(user).data
        })
        
    except jwt.ExpiredSignatureError:
        return Response({
            'valid': False,
            'error': 'Token expired'
        })
    except jwt.InvalidTokenError:
        return Response({
            'valid': False,
            'error': 'Invalid token'
        })
    except User.DoesNotExist:
        return Response({
            'valid': False,
            'error': 'User not found'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """
    Rigenera un nuovo access token usando il refresh token.
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Response:
        {
            "access": "new_jwt_access_token"
        }
    """
    try:
        refresh = RefreshToken(request.data.get('refresh'))
        return Response({
            'access': str(refresh.access_token)
        })
    except Exception as e:
        return Response(
            {'error': 'Invalid refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Restituisce informazioni sull'utente correntemente autenticato.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "id": 1,
            "username": "admin",
            ...
        }
    """
    return Response(UserSerializer(request.user).data)
