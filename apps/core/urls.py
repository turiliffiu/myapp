from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'core'

def home_redirect(request):
    """Redirect root to dashboard or login."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('core:login')

urlpatterns = [
    path('', home_redirect, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
]
