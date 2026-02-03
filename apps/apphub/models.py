from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class AppCategory(models.Model):
    """Categoria per organizzare le app (es: Produttività, Admin Tools)."""
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=10, default='📁', help_text='Emoji per icona categoria')
    order = models.IntegerField(default=0, help_text='Ordine visualizzazione (crescente)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria App'
        verbose_name_plural = 'Categorie App'
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.icon} {self.name}'


class App(models.Model):
    """Applicazione nel portale MyApp."""
    
    APP_TYPE_CHOICES = [
        ('internal_url', 'Link Interno'),
        ('external_url', 'Link Esterno'),
        ('html_page', 'Pagina HTML'),
        ('iframe', 'Iframe Embedded'),
    ]
    
    # Informazioni base
    name = models.CharField(max_length=200, verbose_name='Nome App')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Descrizione')
    icon = models.CharField(max_length=10, default='📱', help_text='Emoji per icona')
    
    # Colori gradiente (formato hex)
    color_from = models.CharField(
        max_length=7, 
        default='#667eea',
        help_text='Colore iniziale gradiente (es: #667eea)'
    )
    color_to = models.CharField(
        max_length=7, 
        default='#764ba2',
        help_text='Colore finale gradiente (es: #764ba2)'
    )
    
    # Tipo e URL
    app_type = models.CharField(
        max_length=20, 
        choices=APP_TYPE_CHOICES, 
        default='internal_url',
        verbose_name='Tipo App'
    )
    url = models.CharField(
        max_length=500, 
        blank=True,
        help_text='URL o path relativo (es: /apps/dashboard/ o https://example.com)'
    )
    html_content = models.TextField(
        blank=True,
        help_text='Contenuto HTML completo (per app_type=html_page)'
    )
    
    # Organizzazione
    category = models.ForeignKey(
        AppCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='apps'
    )
    order = models.IntegerField(default=0, help_text='Ordine visualizzazione')
    
    # Permessi e visibilità
    is_active = models.BooleanField(default=True, verbose_name='Attiva')
    is_public = models.BooleanField(
        default=False, 
        help_text='Visibile senza login'
    )
    requires_sso = models.BooleanField(
        default=True,
        help_text='Usa autenticazione MyApp (SSO)'
    )
    allowed_roles = models.CharField(
        max_length=200,
        default='admin,editor,viewer',
        help_text='Ruoli separati da virgola (admin,editor,viewer)'
    )
    
    # Statistiche
    click_count = models.IntegerField(default=0, verbose_name='Numero accessi')
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Applicazione'
        verbose_name_plural = 'Applicazioni'
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.icon} {self.name}'

    def save(self, *args, **kwargs):
        """Auto-genera slug se vuoto."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL per accedere all'app."""
        if self.app_type == 'html_page':
            return f'/apps/{self.slug}/'
        elif self.app_type == 'iframe':
            return f'/apps/{self.slug}/iframe/'
        else:
            return self.url

    def increment_click(self):
        """Incrementa contatore accessi."""
        self.click_count += 1
        self.save(update_fields=['click_count'])

    def user_can_access(self, user):
        """Verifica se l'utente può accedere a questa app."""
        if self.is_public:
            return True
        
        if not user.is_authenticated:
            return False
        
        # Admin vede sempre tutto
        if user.is_superuser:
            return True
        
        # Verifica ruolo
        user_role = getattr(user.profile, 'role', 'viewer')
        allowed = [r.strip() for r in self.allowed_roles.split(',')]
        return user_role in allowed
