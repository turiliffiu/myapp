from django.contrib import admin
from .models import App, AppCategory


@admin.register(AppCategory)
class AppCategoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'order', 'app_count')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order', 'name')

    def app_count(self, obj):
        """Conta app nella categoria."""
        return obj.apps.count()
    app_count.short_description = 'N° App'


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'app_type', 'is_active', 'category', 'click_count', 'order')
    list_filter = ('is_active', 'app_type', 'category', 'requires_sso')
    search_fields = ('name', 'description', 'slug')
    list_editable = ('is_active', 'order')
    readonly_fields = ('slug', 'click_count', 'created_at', 'updated_at', 'created_by')
    
    fieldsets = (
        ('Informazioni Base', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Aspetto Visivo', {
            'fields': ('color_from', 'color_to')
        }),
        ('Configurazione App', {
            'fields': ('app_type', 'url', 'html_content', 'category')
        }),
        ('Permessi e Visibilità', {
            'fields': ('is_active', 'is_public', 'requires_sso', 'allowed_roles', 'order')
        }),
        ('Statistiche', {
            'fields': ('click_count',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-imposta created_by."""
        if not change:  # Nuovo oggetto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
