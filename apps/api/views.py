from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    TokenValidationSerializer,
    SSOLoginSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def sso_login(request):
    """
    Login SSO - Genera JWT tokens.
    
    POST /api/sso/login/
    Body: {"username": "admin", "password": "xxx"}
    
    Returns: {
        "access": "token...",
        "refresh": "token...",
        "user": {...}
    }
    """
    serializer = SSOLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Credenziali non valide'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {'error': 'Account disabilitato'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Genera JWT tokens
    refresh = RefreshToken.for_user(user)
    
    # Serializza user info
    user_data = UserSerializer(user).data
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': user_data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def validate_token(request):
    """
    Valida un JWT token e restituisce info utente.
    
    POST /api/sso/validate/
    Body: {"token": "xxx"}
    
    Returns: {
        "valid": true,
        "user": {...}
    }
    """
    serializer = TokenValidationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    token_string = serializer.validated_data['token']
    
    try:
        # Decodifica token
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken(token_string)
        
        # Ottieni user
        user_id = token['user_id']
        user = User.objects.get(id=user_id)
        
        if not user.is_active:
            return Response(
                {'valid': False, 'error': 'Account disabilitato'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Serializza user
        user_data = UserSerializer(user).data
        
        return Response({
            'valid': True,
            'user': user_data
        })
        
    except (InvalidToken, TokenError) as e:
        return Response(
            {'valid': False, 'error': str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )
    except User.DoesNotExist:
        return Response(
            {'valid': False, 'error': 'Utente non trovato'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """
    Refresh JWT token.
    
    POST /api/sso/refresh/
    Headers: Authorization: Bearer <access_token>
    Body: {"refresh": "refresh_token"}
    
    Returns: {"access": "new_token"}
    """
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response(
            {'error': 'Refresh token richiesto'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token)
        })
    except (InvalidToken, TokenError) as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Ottieni info utente corrente autenticato.
    
    GET /api/sso/me/
    Headers: Authorization: Bearer <token>
    
    Returns: user data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def sso_info(request):
    """
    Informazioni su API SSO disponibili.
    
    GET /api/sso/
    """
    return Response({
        'name': 'MyApp SSO API',
        'version': '1.0',
        'endpoints': {
            'login': '/api/sso/login/',
            'validate': '/api/sso/validate/',
            'refresh': '/api/sso/refresh/',
            'me': '/api/sso/me/',
        },
        'documentation': 'https://github.com/turiliffiu/myapp'
    })
