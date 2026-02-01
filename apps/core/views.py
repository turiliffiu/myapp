from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from .forms import LoginForm, RegisterForm, ProfileForm


@require_http_methods(['GET', 'POST'])
@ratelimit(key='ip', rate='5/15m', block=True)
def login_view(request):
    """Login con rate limiting anti-brute force."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Benvenuto, {user.username}!')
            return redirect(request.GET.get('next', 'core:dashboard'))
        messages.error(request, 'Username o password non validi.')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
@ratelimit(key='ip', rate='3/h', block=True)
def register_view(request):
    """Registrazione con rate limiting."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account creato con successo!')
            return redirect('core:dashboard')
        messages.error(request, 'Correggi gli errori indicati nel form.')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Sei stato disconnesso.')
    return redirect('core:login')


@login_required
def dashboard_view(request):
    """Dashboard principale."""
    return render(request, 'core/dashboard.html', {
        'profile': request.user.profile,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def profile_view(request):
    """Profilo: visualizzazione e modifica."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('core:profile')
        messages.error(request, 'Correggi gli errori nel form.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/profile.html', {'form': form, 'profile': profile})
