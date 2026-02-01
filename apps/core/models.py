from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Profilo esteso dell'utente con ruolo e permessi di business.
    Viene creato AUTOMATICAMENTE tramite signal quando si crea un User.
    """
    ROLE_CHOICES = [
        ('admin',  'Amministratore'),
        ('editor', 'Editor'),
        ('viewer', 'Visualizzatore'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profilo Utente'
        verbose_name_plural = 'Profili Utente'

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_editor(self):
        return self.role == 'editor'

    def can_create(self):
        """Admin e Editor possono creare entità."""
        return self.role in ('admin', 'editor')

    def can_edit(self, obj=None):
        """
        Admin: può modificare qualsiasi oggetto.
        Editor: solo gli oggetti di cui è owner.
        """
        if self.role == 'admin':
            return True
        if self.role == 'editor' and obj:
            return getattr(obj, 'owner_id', None) == self.user.id
        return False

    def can_delete(self, obj=None):
        """Stessa logica di can_edit."""
        if self.role == 'admin':
            return True
        if self.role == 'editor' and obj:
            return getattr(obj, 'owner_id', None) == self.user.id
        return False
