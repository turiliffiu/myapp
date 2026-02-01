from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from apps.core.models import UserProfile
from .serializers import UserSerializer
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    API gestione utenti - solo Admin.
    
    Endpoint:
        GET    /api/users/          → lista
        GET    /api/users/{id}/     → dettaglio
        PATCH  /api/users/{id}/     → modifica
        DELETE /api/users/{id}/     → elimina
        PATCH  /api/users/{id}/role/   → cambia ruolo
        PATCH  /api/users/{id}/active/ → attiva/disattiva
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.select_related('profile').order_by('-date_joined')

    @action(detail=True, methods=['patch'], url_path='role')
    def change_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get('role')

        if role not in ('admin', 'editor', 'viewer'):
            return Response({'error': 'Ruolo non valido'}, status=status.HTTP_400_BAD_REQUEST)

        # Previene rimozione ultimo admin
        if user.profile.role == 'admin' and role != 'admin':
            if UserProfile.objects.filter(role='admin').count() <= 1:
                return Response(
                    {'error': 'Impossibile: ultimo amministratore'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user.profile.role = role
        user.profile.save()
        return Response({'message': 'Ruolo aggiornato', 'role': role})

    @action(detail=True, methods=['patch'], url_path='active')
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        active = request.data.get('active')
        if active is None:
            return Response({'error': 'Campo "active" mancante'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = bool(active)
        user.save()
        return Response({'message': 'Stato aggiornato', 'is_active': user.is_active})
