from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # SSO Endpoints
    path('sso/', views.sso_info, name='sso_info'),
    path('sso/login/', views.sso_login, name='sso_login'),
    path('sso/validate/', views.validate_token, name='validate_token'),
    path('sso/refresh/', views.refresh_token, name='refresh_token'),
    path('sso/me/', views.current_user, name='current_user'),
]
