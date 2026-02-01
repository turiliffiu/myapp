from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.TabularInline):
    """Mostra il profilo inline nella pagina admin dell'utente."""
    model = UserProfile
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


# Deregistra admin predefinito di Django per User
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin personalizzato per User con ProfileInline."""
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'is_active', 'date_joined')
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username',)
