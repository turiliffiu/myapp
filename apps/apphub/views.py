from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from .models import App, AppCategory


def app_list_view(request):
    """
    Homepage MyApp - Grid card app.
    Mostra solo app accessibili dall'utente.
    """
    # Filtra app attive
    all_apps = App.objects.filter(is_active=True).select_related('category', 'created_by')
    
    # Filtra per permessi utente
    if request.user.is_authenticated:
        accessible_apps = [app for app in all_apps if app.user_can_access(request.user)]
    else:
        # Solo app pubbliche per utenti non loggati
        accessible_apps = [app for app in all_apps if app.is_public]
    
    # Categorie con app
    categories = AppCategory.objects.prefetch_related('apps').all()
    
    context = {
        'apps': accessible_apps,
        'categories': categories,
        'total_apps': len(accessible_apps),
    }
    return render(request, 'apphub/app_list.html', context)


@require_http_methods(['GET', 'POST'])
def app_access_view(request, slug):
    """
    Accesso a un'app specifica.
    - Incrementa contatore
    - Redirect o render HTML
    """
    app = get_object_or_404(App, slug=slug, is_active=True)
    
    # Verifica permessi
    if not app.user_can_access(request.user):
        return render(request, 'apphub/app_forbidden.html', {'app': app}, status=403)
    
    # Incrementa contatore
    app.increment_click()
    
    # Gestione in base al tipo
    if app.app_type == 'html_page':
        # Render HTML content
        return render(request, 'apphub/app_html_viewer.html', {'app': app})
    
    elif app.app_type == 'iframe':
        # Render in iframe
        return render(request, 'apphub/app_iframe_viewer.html', {'app': app})
    
    elif app.app_type in ['internal_url', 'external_url']:
        # Redirect diretto
        return redirect(app.url)
    
    else:
        raise Http404("Tipo app non supportato")


def app_html_content(request, slug):
    """
    Serve il contenuto HTML raw dell'app.
    Usato per iframe o standalone.
    """
    app = get_object_or_404(App, slug=slug, is_active=True, app_type='html_page')
    
    # Verifica permessi
    if not app.user_can_access(request.user):
        return HttpResponse('<h1>Accesso Negato</h1>', status=403)
    
    # Serve HTML raw
    return HttpResponse(app.html_content, content_type='text/html')
