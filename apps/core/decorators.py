from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


def role_required(*roles):
    """
    Decoratore che verifica se l'utente ha uno dei ruoli specificati.
    
    Uso:
        @role_required('admin')
        def my_view(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.profile.role not in roles:
                messages.error(request, 'Non hai i permessi necessari per questa azione.')
                return redirect('core:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
